from __future__ import annotations
import traceback
import logging
import os
import sys
import socket
import mimetypes
import re as rgx
import json as jsn
import random as rnd
import time
from functools import wraps
from typing import Any, Dict, List, Set, Tuple, Optional, Callable, Union
from typing_extensions import Literal

import gevent as gvt
import bottle as btl
try:
    import bottle_websocket as wbs
except ImportError:
    import bottle.ext.websocket as wbs
import pyparsing as pp
import importlib_resources
from pathlib import Path

from eel.types import OptionsDictT, WebSocketT
import eel.browsers as brw

# Configure module-level logger
logger = logging.getLogger('eel')
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Security logger
_security_logger = logging.getLogger('reel.security')
if not _security_logger.handlers:
    _sec_handler = logging.StreamHandler()
    _sec_formatter = logging.Formatter('[%(asctime)s] %(levelname)s [Reel Security] %(message)s')
    _sec_handler.setFormatter(_sec_formatter)
    _security_logger.addHandler(_sec_handler)
    _security_logger.setLevel(logging.INFO)

if os.environ.get('REEL_LOG_FILE'):
    try:
        _file_handler = logging.FileHandler(os.environ['REEL_LOG_FILE'])
        _file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s [Reel Security] %(message)s'))
        _security_logger.addHandler(_file_handler)
    except Exception as e:
        logger.warning(f"Could not create log file: {e}")

mimetypes.add_type('application/javascript', '.js')

# Load eel.js
_eel_js_reference = importlib_resources.files('eel') / 'eel.js'
with importlib_resources.as_file(_eel_js_reference) as _eel_js_path:
    _eel_js: str = _eel_js_path.read_text(encoding='utf-8')

# PyParsing grammar
EXPOSED_JS_FUNCTIONS: pp.ZeroOrMore = pp.ZeroOrMore(
    pp.Suppress(
        pp.SkipTo(pp.Literal('eel.expose('))
        + pp.Literal('eel.expose(')
        + pp.Optional(
            pp.Or([pp.nestedExpr(), pp.Word(pp.printables, excludeChars=',')]) + pp.Literal(',')
        )
    )
    + pp.Suppress(pp.Regex(r'["\']?'))
    + pp.Word(pp.printables, excludeChars='"\')')
    + pp.Suppress(pp.Regex(r'["\']?\s*\\)')),
)

class EelApplication:
    """
    Main Eel application class encapsulating state and functionality.
    """

    def __init__(self):
        self._websockets: List[Tuple[Any, WebSocketT]] = []
        self._call_return_values: Dict[Any, Any] = {}
        self._call_return_callbacks: Dict[float, Tuple[Callable[..., Any], Optional[Callable[..., Any]]]] = {}
        self._call_number: int = 0
        self._exposed_functions: Dict[str, Callable[..., Any]] = {}
        self._js_functions: List[str] = []
        self._mock_queue: List[Dict[str, Any]] = []
        self._mock_queue_done: Set[Any] = set()
        self._shutdown: Optional[gvt.Greenlet] = None
        self._root_path: str = ""
        self._js_result_timeout: int = 10000
        self._max_message_size: int = int(os.environ.get('EEL_MAX_MESSAGE_SIZE', 1024 * 1024))
        self._rate_limit_storage: Dict[str, Dict[str, List[float]]] = {}
        self._start_args: OptionsDictT = {}
        
        # Initialize default routes
        self._bottle_routes = {
            "/eel.js": (self._eel, dict()),
            "/": (self._root, dict()),
            "/<path:path>": (self._static, dict()),
            "/eel": (self._websocket, dict(apply=[wbs.websocket]))
        }

    def expose(self, name_or_function: Optional[Union[str, Callable[..., Any]]] = None) -> Callable[..., Any]:
        """Decorator to expose Python callables via Eel's JavaScript API."""
        if name_or_function is None:
            return self.expose

        if isinstance(name_or_function, str):
            name = name_or_function
            def decorator(function: Callable[..., Any]) -> Any:
                self._expose(name, function)
                return function
            return decorator
        else:
            function = name_or_function
            self._expose(function.__name__, function)
            return function

    def _expose(self, name: str, function: Callable[..., Any]) -> None:
        if name in self._exposed_functions:
            raise ValueError(f'Already exposed function with name "{name}"')
        self._exposed_functions[name] = function

    def rate_limit(self, max_calls: int = 60, time_window: int = 60) -> Callable[..., Any]:
        """Decorator to rate limit exposed functions."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                client_id = str(id(args)) if args else 'default'
                func_name = func.__name__
                current_time = time.time()

                if func_name not in self._rate_limit_storage:
                    self._rate_limit_storage[func_name] = {}
                
                if client_id not in self._rate_limit_storage[func_name]:
                    self._rate_limit_storage[func_name][client_id] = []

                # Clean up old timestamps
                self._rate_limit_storage[func_name][client_id] = [
                    ts for ts in self._rate_limit_storage[func_name][client_id]
                    if current_time - ts < time_window
                ]

                if len(self._rate_limit_storage[func_name][client_id]) >= max_calls:
                    _security_logger.warning(
                        f"Rate limit exceeded for '{func_name}': {max_calls}/{time_window}s (client: {client_id[:8]})"
                    )
                    raise Exception(f"Rate limit exceeded: {max_calls} calls per {time_window} seconds")

                self._rate_limit_storage[func_name][client_id].append(current_time)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def init(self, path: str, allowed_extensions: List[str] = ['.js', '.html', '.txt', '.htm', '.xhtml', '.vue'],
             js_result_timeout: int = 10000) -> None:
        """Initialize Eel."""
        self._root_path = self._get_real_path(path)
        self._js_result_timeout = js_result_timeout

        js_functions = set()
        for root, _, files in os.walk(self._root_path):
            for name in files:
                if not any(name.endswith(ext) for ext in allowed_extensions):
                    continue

                try:
                    with open(os.path.join(root, name), encoding='utf-8') as file:
                        contents = file.read()
                        matches = EXPOSED_JS_FUNCTIONS.parseString(contents).asList()
                        for expose_call in matches:
                            if rgx.findall(r'[\(=]', expose_call):
                                logger.warning(f"Invalid eel.expose() call: {expose_call}")
                                continue
                            js_functions.add(expose_call)
                except UnicodeDecodeError:
                    pass
                except Exception as e:
                    logger.error(f"Error parsing file {name}: {e}")

        self._js_functions = list(js_functions)
        for js_function in self._js_functions:
            self._mock_js_function(js_function)

    def start(self, *start_urls: str, mode: str = 'chrome', host: str = 'localhost',
              port: int = 8000, block: bool = True, jinja_templates: str = None,
              cmdline_args: List[str] = ['--disable-http-cache'], size: Tuple[int, int] = None,
              position: Tuple[int, int] = None, geometry: Dict[str, Tuple[int, int]] = {},
              close_callback: Callable = None, app_mode: bool = True,
              all_interfaces: bool = False, disable_cache: bool = True,
              default_path: str = 'index.html', app: btl.Bottle = None,
              shutdown_delay: float = 1.0, suppress_error: bool = False) -> None:
        """Start the Eel app."""
        
        if app is None:
            app = btl.default_app()

        self._start_args.update({
            'mode': mode, 'host': host, 'port': port, 'block': block,
            'jinja_templates': jinja_templates, 'cmdline_args': cmdline_args,
            'size': size, 'position': position, 'geometry': geometry,
            'close_callback': close_callback, 'app_mode': app_mode,
            'all_interfaces': all_interfaces, 'disable_cache': disable_cache,
            'default_path': default_path, 'app': app,
            'shutdown_delay': shutdown_delay, 'suppress_error': suppress_error,
        })

        if self._start_args['port'] == 0:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', 0))
            self._start_args['port'] = sock.getsockname()[1]
            sock.close()

        if self._start_args['jinja_templates'] is not None:
            from jinja2 import Environment, FileSystemLoader, select_autoescape
            templates_path = os.path.join(self._root_path, self._start_args['jinja_templates'])
            self._start_args['jinja_env'] = Environment(
                loader=FileSystemLoader(templates_path),
                autoescape=select_autoescape(['html', 'xml'])
            )

        self.show(*start_urls)

        def run_lambda() -> None:
            HOST = '0.0.0.0' if self._start_args['all_interfaces'] else self._start_args['host']
            
            app_instance = self._start_args['app']
            if isinstance(app_instance, btl.Bottle):
                self.register_eel_routes(app_instance)
            else:
                self.register_eel_routes(btl.default_app())

            btl.run(
                host=HOST,
                port=self._start_args['port'],
                server=wbs.GeventWebSocketServer,
                quiet=True,
                app=app_instance
            )

        if self._start_args['block']:
            run_lambda()
        else:
            self.spawn(run_lambda)

    def show(self, *start_urls: str) -> None:
        """Show the specified URL(s) in the browser."""
        brw.open(list(start_urls), self._start_args)

    def sleep(self, seconds: Union[int, float]) -> None:
        """Non-blocking sleep."""
        gvt.sleep(seconds)

    def spawn(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> gvt.Greenlet:
        """Spawn a new Greenlet."""
        return gvt.spawn(function, *args, **kwargs)

    def register_eel_routes(self, app: btl.Bottle) -> None:
        """Register Eel routes with a Bottle app."""
        for route_path, route_params in self._bottle_routes.items():
            route_func, route_kwargs = route_params
            app.route(path=route_path, callback=route_func, **route_kwargs)

    # Internal methods

    def _eel(self) -> str:
        start_geometry = {'default': {'size': self._start_args['size'],
                                      'position': self._start_args['position']},
                          'pages':   self._start_args['geometry']}

        page = _eel_js.replace('/** _py_functions **/',
                               '_py_functions: %s,' % list(self._exposed_functions.keys()))
        page = page.replace('/** _start_geometry **/',
                            '_start_geometry: %s,' % self._safe_json(start_geometry))
        btl.response.content_type = 'application/javascript'
        self._set_response_headers(btl.response)
        return page

    def _root(self) -> btl.Response:
        return self._static(self._start_args['default_path'])

    def _static(self, path: str) -> btl.Response:
        try:
            root = Path(self._root_path).resolve()
            requested = (Path(self._root_path) / path).resolve()
            if not str(requested).startswith(str(root)):
                _security_logger.warning(f"Path traversal attempt blocked: {path}")
                return btl.HTTPError(403, "Forbidden: Path traversal detected")
        except (ValueError, OSError) as e:
            _security_logger.warning(f"Invalid path request: {path} - {e}")
            return btl.HTTPError(400, "Bad Request: Invalid path")

        response = None
        if 'jinja_env' in self._start_args and 'jinja_templates' in self._start_args:
            template_prefix = self._start_args['jinja_templates'] + '/'
            if path.startswith(template_prefix):
                n = len(template_prefix)
                template = self._start_args['jinja_env'].get_template(path[n:])
                response = btl.HTTPResponse(template.render())

        if response is None:
            response = btl.static_file(path, root=self._root_path)

        self._set_response_headers(response)
        return response

    def _websocket(self, ws: WebSocketT) -> None:
        origin = btl.request.environ.get('HTTP_ORIGIN', '')
        allowed_origins = os.environ.get('EEL_ALLOWED_ORIGINS', 'http://localhost:8000').split(',')
        localhost_patterns = ['http://localhost:', 'http://127.0.0.1:', 'http://0.0.0.0:']
        is_localhost = any(origin.startswith(pattern) for pattern in localhost_patterns)

        if origin and not is_localhost and origin not in allowed_origins:
            _security_logger.warning(f"Rejected WebSocket connection from unauthorized origin: {origin}")
            ws.close()
            return

        if origin:
            _security_logger.info(f"WebSocket connection established from origin: {origin}")

        for js_function in self._js_functions:
            self._import_js_function(js_function)

        page = btl.request.query.page
        if page not in self._mock_queue_done:
            for call in self._mock_queue:
                self._repeated_send(ws, self._safe_json(call))
            self._mock_queue_done.add(page)

        self._websockets += [(page, ws)]

        while True:
            msg = ws.receive()
            if msg is not None:
                msg_size = len(msg.encode('utf-8')) if isinstance(msg, str) else len(msg)
                if msg_size > self._max_message_size:
                    _security_logger.warning(f"Rejected oversized WebSocket message: {msg_size} bytes")
                    ws.close()
                    self._websockets.remove((page, ws))
                    break

                try:
                    message = jsn.loads(msg)
                    self.spawn(self._process_message, message, ws)
                except jsn.JSONDecodeError:
                    logger.warning("Invalid JSON received")
            else:
                self._websockets.remove((page, ws))
                break

        self._websocket_close(page)

    def _safe_json(self, obj: Any) -> str:
        return jsn.dumps(obj, default=lambda o: None)

    def _repeated_send(self, ws: WebSocketT, msg: str) -> None:
        for _ in range(100):
            try:
                ws.send(msg)
                break
            except Exception:
                self.sleep(0.001)

    def _process_message(self, message: Dict[str, Any], ws: WebSocketT) -> None:
        if 'call' in message:
            error_info = {}
            try:
                if message['name'] in self._exposed_functions:
                    return_val = self._exposed_functions[message['name']](*message['args'])
                    status = 'ok'
                else:
                    return_val = None
                    status = 'error'
                    error_info['errorText'] = f"Function {message['name']} not found"
            except Exception as e:
                err_traceback = traceback.format_exc()
                logger.error(f"Error calling {message['name']}: {e}", exc_info=True)
                return_val = None
                status = 'error'
                if os.environ.get('EEL_DEBUG'):
                    error_info['errorText'] = repr(e)
                    error_info['errorTraceback'] = err_traceback
                else:
                    error_info['errorText'] = 'An error occurred while processing your request'
                    _security_logger.error(f"Function error: {message.get('name')} - {e}")

            self._repeated_send(ws, self._safe_json({
                'return': message['call'],
                'status': status,
                'value': return_val,
                'error': error_info,
            }))
        elif 'return' in message:
            call_id = message['return']
            if call_id in self._call_return_callbacks:
                callback, error_callback = self._call_return_callbacks.pop(call_id)
                if message['status'] == 'ok':
                    callback(message['value'])
                elif message['status'] == 'error' and error_callback is not None:
                    error_callback(message['error'], message.get('stack'))
            elif call_id in self._call_return_values:
                # Value was already set, or we're just storing it
                pass
            else:
                self._call_return_values[call_id] = message['value']
        else:
            logger.warning(f'Invalid message received: {message}')

    def _get_real_path(self, path: str) -> str:
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, path) # type: ignore
        else:
            return os.path.abspath(path)

    def _mock_js_function(self, f: str) -> None:
        def make_mock_wrapper(function_name: str) -> Callable:
            return lambda *args: self._mock_call(function_name, args)
        
        # Inject into instance
        setattr(self, f, make_mock_wrapper(f))

    def _import_js_function(self, f: str) -> None:
        def make_js_wrapper(function_name: str) -> Callable:
            return lambda *args: self._js_call(function_name, args)
        
        # Inject into instance
        setattr(self, f, make_js_wrapper(f))

    def _call_object(self, name: str, args: Any) -> Dict[str, Any]:
        self._call_number += 1
        call_id = self._call_number + rnd.random()
        return {'call': call_id, 'name': name, 'args': args}

    def _mock_call(self, name: str, args: Any) -> Callable:
        call_object = self._call_object(name, args)
        self._mock_queue += [call_object]
        return self._call_return(call_object)

    def _js_call(self, name: str, args: Any) -> Callable:
        call_object = self._call_object(name, args)
        for _, ws in self._websockets:
            self._repeated_send(ws, self._safe_json(call_object))
        return self._call_return(call_object)

    def _call_return(self, call: Dict[str, Any]) -> Callable:
        call_id = call['call']
        def return_func(callback: Callable = None, error_callback: Callable = None) -> Any:
            if callback is not None:
                self._call_return_callbacks[call_id] = (callback, error_callback)
            else:
                for _ in range(self._js_result_timeout):
                    if call_id in self._call_return_values:
                        return self._call_return_values.pop(call_id)
                    self.sleep(0.001)
        return return_func

    def _detect_shutdown(self) -> None:
        if len(self._websockets) == 0:
            sys.exit()

    def _websocket_close(self, page: str) -> None:
        close_callback = self._start_args.get('close_callback')
        if close_callback is not None:
            if not callable(close_callback):
                raise TypeError("'close_callback' must be callable or None")
            sockets = [p for _, p in self._websockets]
            close_callback(page, sockets)
        else:
            if isinstance(self._shutdown, gvt.Greenlet):
                self._shutdown.kill()
            self._shutdown = gvt.spawn_later(self._start_args['shutdown_delay'], self._detect_shutdown)

    def _set_response_headers(self, response: btl.Response) -> None:
        response.set_header('X-Content-Type-Options', 'nosniff')
        response.set_header('X-Frame-Options', 'DENY')
        response.set_header('X-XSS-Protection', '1; mode=block')
        default_csp = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'"
        response.set_header('Content-Security-Policy', default_csp)
        if self._start_args['disable_cache']:
            response.set_header('Cache-Control', 'no-store')

# Default Instance
_default_app = EelApplication()

# Module-level Proxies
def init(*args, **kwargs): return _default_app.init(*args, **kwargs)
def start(*args, **kwargs): return _default_app.start(*args, **kwargs)
def expose(name_or_function=None): return _default_app.expose(name_or_function)
def rate_limit(*args, **kwargs): return _default_app.rate_limit(*args, **kwargs)
def sleep(seconds): return _default_app.sleep(seconds)
def spawn(function, *args, **kwargs): return _default_app.spawn(function, *args, **kwargs)
def show(*args, **kwargs): return _default_app.show(*args, **kwargs)
def register_eel_routes(app): return _default_app.register_eel_routes(app)

# Support for eel.my_js_function() on the default app
def __getattr__(name: str) -> Any:
    return getattr(_default_app, name)