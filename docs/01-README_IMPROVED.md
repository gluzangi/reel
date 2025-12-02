<div align="center">

# Eel

### Build Beautiful Desktop Apps with Python and Web Technologies

[![PyPI version](https://img.shields.io/pypi/v/Eel?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/Eel/)
[![Downloads](https://img.shields.io/pypi/dm/Eel?style=for-the-badge&logo=pypi&logoColor=white)](https://pypistats.org/packages/eel)
[![Python](https://img.shields.io/pypi/pyversions/Eel?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/Eel/)
[![License](https://img.shields.io/pypi/l/Eel.svg?style=for-the-badge)](https://pypi.org/project/Eel/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/3nqXPFX)

</div>

---

> **Project Status Notice**
>
> This project is currently **unmaintained**. While it remains functional and widely used, it has not received regular updates in several years. The maintainer team is not actively developing new features.
>
> **However**, the codebase is stable, well-tested, and suitable for:
> - Internal tools and utilities
> - Proof-of-concept applications
> - Learning Python-JavaScript integration
> - Rapid prototyping of desktop apps
>
> Use with appropriate consideration for security hardening and maintenance. Community contributions and forks are welcome!

---

## What is Eel?

**Eel** is a lightweight Python library that makes it dead-simple to create **Electron-style desktop applications** using HTML, CSS, and JavaScript for the frontend, while leveraging the full power of Python for the backend.

### The Core Idea

```python
import eel

eel.init('web')  # Point to your web files

@eel.expose      # Expose Python functions to JavaScript
def my_python_function(data):
    # Full Python power: ML, data processing, file I/O, etc.
    return processed_data

eel.start('index.html')  # Launch your app
```

```javascript
// In your JavaScript - call Python directly!
async function handleClick() {
    let result = await eel.my_python_function(userData)();
    console.log(result);
}
```

That's it. No complex build processes, no IPC protocols to learn, no Chromium bundling headaches.

---

## Why Choose Eel?

| Feature | Eel | Electron | CEF Python | PyQt/Tkinter |
|---------|-----|----------|------------|--------------|
| **Size** | Tiny (~50KB) | Large (~150MB) | Large (~200MB) | Medium |
| **Learning Curve** | Minimal | Moderate | Steep | Steep |
| **Web Technologies** | Full HTML/CSS/JS | Full HTML/CSS/JS | Full HTML/CSS/JS | Limited |
| **Python Integration** | Native & Simple | Via IPC | Complex | Native but old UI |
| **Modern Frontend** | React, Vue, Svelte | React, Vue, Svelte | React, Vue, Svelte | No |
| **Use Case** | Internal tools, utilities | Production apps | Production apps | Traditional desktop |

**Perfect for:**
- Data science dashboards using Plotly, D3.js, or Chart.js with NumPy/Pandas backend
- System administration tools with beautiful web UIs
- Quick prototypes that need both Python libraries and modern UI
- Internal business applications
- Educational projects teaching full-stack concepts

**Not ideal for:**
- Large-scale commercial software requiring app store distribution
- Apps needing offline Chrome bundling (though possible with Electron mode)
- Projects requiring maximum security hardening out-of-the-box

---

## Quick Start

### Installation

```bash
pip install eel
```

For HTML templating support (Jinja2):

```bash
pip install eel[jinja2]
```

### Your First Eel App

Create this file structure:

```
my_app/
├── app.py
└── web/
    ├── index.html
    ├── style.css
    └── script.js
```

**app.py:**

```python
import eel
import random

# Initialize Eel with the folder containing web files
eel.init('web')

@eel.expose
def get_random_number():
    """This Python function can be called from JavaScript"""
    return random.randint(1, 100)

@eel.expose
def process_data(data):
    """Example: Do heavy Python processing"""
    # Use NumPy, Pandas, TensorFlow, anything Python!
    result = sum(data) / len(data)
    return f"Average: {result}"

# Start the app
eel.start('index.html', size=(800, 600))
```

**web/index.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Eel App</title>
    <link rel="stylesheet" href="style.css">
    <script type="text/javascript" src="/eel.js"></script>
</head>
<body>
    <h1>My Awesome Eel App</h1>
    <button onclick="getRandom()">Get Random Number</button>
    <p id="result"></p>

    <script>
        async function getRandom() {
            // Call Python function from JavaScript!
            let number = await eel.get_random_number()();
            document.getElementById('result').innerText =
                `Random number: ${number}`;
        }

        // Expose JavaScript function to Python
        eel.expose(displayMessage);
        function displayMessage(msg) {
            alert(msg);
        }
    </script>
</body>
</html>
```

**Run it:**

```bash
python app.py
```

A Chrome app window opens with your UI, and Python and JavaScript can talk seamlessly!

---

## Key Features

### 1. Bidirectional Communication

**Python → JavaScript:**

```python
eel.displayMessage("Hello from Python!")  # Call JS function
```

**JavaScript → Python:**

```javascript
let result = await eel.get_random_number()();  // Call Python function
```

### 2. Multiple Return Patterns

**Callbacks (JavaScript):**

```javascript
eel.my_python_func(arg1, arg2)(function(result) {
    console.log(result);
});
```

**Async/Await (Modern JavaScript):**

```javascript
async function doWork() {
    let result = await eel.my_python_func(arg1, arg2)();
    console.log(result);
}
```

**Synchronous (Python):**

```python
# Wait for JavaScript to return a value
result = eel.my_js_function()(param1, param2)
```

### 3. Browser Flexibility

```python
# Chrome app mode (default, no browser chrome)
eel.start('main.html', mode='chrome')

# Microsoft Edge
eel.start('main.html', mode='edge')

# Electron wrapper
eel.start('main.html', mode='electron')

# System default browser
eel.start('main.html', mode=None)

# Headless (no UI, just web server)
eel.start('main.html', mode=False)
```

### 4. PyInstaller Support

Build standalone executables:

```bash
# Quick build
python -m eel app.py web

# Production build (single file, no console)
python -m eel app.py web --onefile --noconsole

# Exclude unnecessary packages to reduce size
python -m eel app.py web --exclude matplotlib --exclude pandas --onefile
```

Creates a distributable `.exe` (Windows) or binary (macOS/Linux) with your app embedded!

### 5. Works with Modern Frameworks

Eel plays nicely with:
- **React** - See `examples/07 - CreateReactApp`
- **Vue.js**
- **Svelte**
- **Bootstrap, Tailwind, Material-UI** - Any CSS framework
- **D3.js, Three.js, Plotly** - Visualization libraries

---

## Real-World Use Cases

### 1. Data Science Dashboard

```python
import eel
import pandas as pd
import numpy as np

eel.init('web')

@eel.expose
def analyze_csv(filepath):
    df = pd.read_csv(filepath)
    return {
        'rows': len(df),
        'columns': list(df.columns),
        'summary': df.describe().to_dict()
    }

eel.start('dashboard.html')
```

Use Plotly.js or D3.js in your HTML to visualize the results!

### 2. System Administration Tool

```python
import eel
import psutil
import os

eel.init('web')

@eel.expose
def get_system_info():
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory()._asdict(),
        'disk': psutil.disk_usage('/')._asdict()
    }

@eel.expose
def list_processes():
    return [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]

eel.start('sysadmin.html', size=(1000, 800))
```

### 3. File Processing Utility

```python
import eel
import os
from pathlib import Path

eel.init('web')

@eel.expose
def scan_directory(path):
    """JavaScript can't access filesystem - but Python can!"""
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            files.append({
                'name': filename,
                'path': os.path.join(root, filename),
                'size': os.path.getsize(os.path.join(root, filename))
            })
    return files

@eel.expose
def batch_rename(files, pattern):
    # Implement batch file operations safely in Python
    # Return results to beautiful web UI
    pass

eel.start('file_manager.html')
```

---

## Advanced Features

### Custom Bottle App Integration

Add authentication, sessions, or custom routes:

```python
import eel
from bottle import Bottle, request
from beaker.middleware import SessionMiddleware

# Create custom Bottle app with middleware
app = Bottle()

# Add session middleware
session_opts = {
    'session.type': 'file',
    'session.data_dir': './session_data',
}
app = SessionMiddleware(app, session_opts)

# Register Eel routes on your custom app
eel.register_eel_routes(app.app)  # .app gets the wrapped Bottle instance

# Start with custom app
eel.start('main.html', app=app)
```

### Jinja2 Templates

```python
eel.init('web', allowed_extensions=['.js', '.html'])
eel.start(
    'index.html',
    jinja_templates='templates',  # Look for templates here
)
```

Now create `web/templates/dashboard.html` using Jinja2 syntax!

### Multiple Windows

```python
eel.start(
    'main.html',
    geometry={
        'main.html': {'size': (800, 600), 'position': (100, 100)},
        'settings.html': {'size': (400, 300), 'position': (200, 200)}
    }
)

# Open additional windows programmatically
eel.show('settings.html')
```

### Async Python Tasks

```python
import eel

eel.init('web')

def long_running_task():
    while True:
        # Do background work
        eel.sleep(1)  # Use eel.sleep(), not time.sleep()
        eel.update_progress(get_progress())  # Update UI from background task

# Spawn background greenlet
eel.spawn(long_running_task)

eel.start('main.html', block=False)

# Main thread continues here
while True:
    eel.sleep(1)
    print("Main loop running")
```

---

## Configuration Options

```python
eel.start(
    'main.html',
    mode='chrome',                    # Browser mode
    host='localhost',                 # Server host
    port=8000,                        # Server port (0 = auto-assign)
    block=True,                       # Block main thread
    size=(1024, 768),                # Window size
    position=(100, 100),              # Window position
    app_mode=True,                    # Chrome app mode (no browser UI)
    close_callback=my_close_handler,  # Called when window closes
    cmdline_args=['--disable-http-cache'],  # Browser flags
    shutdown_delay=1.0,               # Delay before shutdown when window closes
)
```

---

## Examples

The project includes comprehensive examples:

| Example | Description |
|---------|-------------|
| **01 - hello_world** | Basic Eel application showing function calls |
| **02 - callbacks** | Callback pattern for async returns |
| **03 - sync_callbacks** | Synchronous return values |
| **04 - file_access** | Accessing filesystem from Python (impossible in browser) |
| **05 - input** | Form handling between Python and JS |
| **06 - jinja_templates** | Using Jinja2 for templating |
| **07 - CreateReactApp** | Full React integration with Eel |
| **08 - disable_cache** | Development tips for disabling caching |
| **09 - Eelectron-quick-start** | Using Eel with Electron |
| **10 - custom_app_routes** | Custom Bottle middleware and routes |

Run any example:

```bash
python examples/01\ -\ hello_world/hello.py
```

---

## Modern Development Stack

Eel works beautifully with modern tools:

### Frontend
- **React, Vue, Svelte, Angular** - Build with any framework
- **TypeScript** - Type-safe JavaScript
- **Vite, Webpack, Parcel** - Modern bundlers
- **Tailwind, Bootstrap, Material-UI** - CSS frameworks

### Backend
- **FastAPI, Flask** - Can integrate with other Python frameworks
- **SQLAlchemy, Peewee** - Database ORMs
- **NumPy, Pandas, Scikit-learn** - Data science stack
- **TensorFlow, PyTorch** - Machine learning
- **OpenCV, Pillow** - Image processing

---

## Community & Support

- **Discord**: [Join our community](https://discord.com/invite/3nqXPFX)
- **GitHub Issues**: Report bugs and request features
- **Stack Overflow**: Tag questions with `python-eel`
- **Examples**: Check the `examples/` directory

### Contributing

While the project is unmaintained by the original team, community contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [README-developers.md](README-developers.md) for development setup.

---

## Comparison with Alternatives

### vs. Electron

**Eel Advantages:**
- Much smaller size (~50KB vs ~150MB)
- Simpler: no Node.js, no complex IPC
- Python ecosystem access
- Faster development for Python developers

**Electron Advantages:**
- More mature and actively maintained
- Better for large commercial apps
- Built-in updater, crash reporting
- Chromium bundled (true offline)

### vs. PyQt/PySide

**Eel Advantages:**
- Modern web UI (HTML/CSS/JS)
- Easier to make beautiful UIs
- Use existing web development skills
- Better for data visualization

**PyQt Advantages:**
- More native feel
- Better performance for complex UIs
- Richer widget library
- Better for traditional desktop apps

### vs. Tkinter

**Eel Advantages:**
- Modern, attractive UIs
- Web technologies ecosystem
- Responsive designs
- Better third-party libraries

**Tkinter Advantages:**
- Included with Python
- Simpler for basic UIs
- More traditional desktop patterns

---

## Frequently Asked Questions

**Q: Can I use this for production applications?**
A: Yes, but understand it's unmaintained. Carefully evaluate security, test thoroughly, and be prepared to fork if needed.

**Q: How does it compare to a web app?**
A: Eel gives you desktop integration (file system, system tray, etc.) while web apps are accessible anywhere.

**Q: Can I distribute my app?**
A: Yes! Use PyInstaller (via `python -m eel`) to create standalone executables.

**Q: What about security?**
A: The local server has no authentication by default. Add security via Bottle middleware if exposing sensitive operations.

**Q: Can I use it with my favorite JS framework?**
A: Absolutely! React, Vue, Svelte, Angular all work. See the React example.

**Q: Why isn't it maintained?**
A: The original maintainers have moved on. The project is stable and functional, but new features are unlikely without community effort.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Originally created by [Chris Knott](https://github.com/ChrisKnott). Maintained by the Python Eel community.

Special thanks to all contributors who have helped make Eel what it is today.

---

<div align="center">

**Star this repo if you find it useful!**

Made with Python and ❤️ by the community

</div>
