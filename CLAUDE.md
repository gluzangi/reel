# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Reel** (Revived Eel) is a Python library for creating simple Electron-like offline HTML/JS GUI apps with full access to Python capabilities. It provides bi-directional communication between Python and JavaScript via WebSockets.

**IMPORTANT**: This is a revival of the original Eel project, which was unmaintained. Reel is actively maintained with focus on security hardening, modern Python patterns, and AI/LLM integration.

> **Note:** The package name remains `eel` for backwards compatibility with the original Eel ecosystem.

## Core Architecture

### Communication Model
- **WebSocket-based**: Eel creates a local Bottle web server with WebSocket support for real-time Python-JavaScript communication
- **Bidirectional exposure**: Functions in Python can be exposed to JavaScript using `@eel.expose`, and vice versa using `eel.expose()` in JS
- **Greenlets**: Built on Gevent for asynchronous event handling. Use `eel.sleep()` and `eel.spawn()` instead of standard `time.sleep()` and threading

### Key Components

**eel/__init__.py**: Core module containing:
- `init()`: Initializes Eel, scans web folder for exposed JS functions using pyparsing grammar
- `start()`: Starts the Bottle server and opens browser window in specified mode
- `expose()`: Decorator for exposing Python functions to JavaScript
- WebSocket handling via `_websocket()` and message processing via `_process_message()`
- Call/return mechanism for synchronous and asynchronous function invocation

**eel/browsers.py**: Browser management:
- Detects and launches browsers (Chrome, Edge, Electron, MSIE)
- Builds URLs from start pages and options
- Browser-specific modules: `chrome.py`, `edge.py`, `electron.py`, `msIE.py`

**eel/eel.js**: Client-side JavaScript library served at `/eel.js`:
- Exposes `eel` object for calling Python functions from JavaScript
- Manages WebSocket connection and message passing
- Dynamically injected with `_py_functions` list during serving

### File Structure
```
eel/                    # Main package
  __init__.py          # Core Eel functionality
  browsers.py          # Browser detection and launching
  chrome.py, edge.py   # Browser-specific implementations
  eel.js               # Client-side JavaScript library
  types.py             # Type definitions
examples/              # Example applications demonstrating features
tests/
  unit/               # Unit tests
  integration/        # Integration tests (use Selenium)
```

## Development Commands

### Installation
```bash
# Install for development
pip install -r requirements.txt        # Core dependencies
pip install -r requirements-test.txt   # Testing dependencies
pip install -r requirements-meta.txt   # Tox for multi-version testing

# Install Eel in development mode
pip install -e .

# Install with Jinja2 template support
pip install -e .[jinja2]
```

### Testing
```bash
# Run tests with pytest
pytest

# Run tests for specific Python version
tox -e py37

# Run all tests across all supported Python versions
tox

# Run type checking
tox -e typecheck

# Or manually
mypy --strict eel
```

**Note**: Integration tests require Chrome and ChromeDriver installed. Check compatible versions.

### Building Distributables
```bash
# Build distributable with PyInstaller
python -m eel <main_script.py> <web_folder>

# Example
python -m eel examples/01\ -\ hello_world/hello.py examples/01\ -\ hello_world/web

# With exclusions and single file
python -m eel hello.py web --exclude numpy --exclude cryptography --onefile --noconsole
```

### Running Examples
```bash
# Run any example
python examples/01\ -\ hello_world/hello.py
python examples/04\ -\ file_access/file_access.py
```

## Key Technical Details

### Function Exposure Pattern
**Python side:**
```python
@eel.expose
def my_function(arg1, arg2):
    return result
```

**JavaScript side:**
```javascript
eel.expose(my_function, 'my_function');
function my_function(arg) { ... }

// Call Python from JS
eel.my_function(arg1, arg2)();  // Double parentheses for return value
```

### Gevent Integration
- Eel uses Gevent's greenlet-based concurrency
- Avoid `time.sleep()` - use `eel.sleep()` instead
- Avoid standard threading - use `eel.spawn()` for concurrent tasks
- Monkey patching (if needed) must be done BEFORE importing eel

### Browser Modes
- `'chrome'`: Chrome in app mode (default)
- `'edge'`: Microsoft Edge
- `'electron'`: Electron wrapper
- `'custom'`: Custom command via `cmdline_args`
- `None` or `False`: No browser window (headless server)

### Return Value Mechanisms
1. **Callbacks**: Pass callback function as second parentheses `eel.func()(callback)`
2. **Synchronous**: Use double parentheses and await `await eel.func()()` (JS) or `result = eel.func()()` (Python)
3. **Timeout**: Default JS result timeout is 10000ms, configurable via `eel.init(js_result_timeout=...)`

### Route Registration
Eel registers 4 Bottle routes:
- `/eel.js`: Serves the eel.js library
- `/`: Root, serves default_path
- `/<path:path>`: Static files from web folder
- `/eel`: WebSocket endpoint

Custom Bottle apps can use `eel.register_eel_routes(app)` for middleware integration.

## Important Conventions

### Security Considerations
- No authentication/authorization built-in - add via Bottle middleware if needed
- WebSocket communication is unencrypted by default
- Exposed functions have full Python access - validate all inputs
- Be cautious exposing file system operations to client

### PyInstaller Integration
- Use `python -m eel` command rather than direct PyInstaller
- The `__main__.py` module handles proper bundling of eel.js and web assets
- Check `sys.frozen` to detect PyInstaller environment (handled in `_get_real_path()`)

### Type Checking
- Project uses strict mypy type checking (`mypy --strict`)
- Type hints from `typing` and `typing_extensions` modules
- Custom types defined in `eel/types.py`

## Testing Notes
- Unit tests in `tests/unit/` test Eel core functionality
- Integration tests in `tests/integration/` use Selenium to test browser interaction
- `tests/conftest.py` contains pytest fixtures and configuration
- Test timeout configured to 30 seconds in tox.ini

## Supported Python Versions
Python 3.7 through 3.13 (see tox.ini and setup.py)
