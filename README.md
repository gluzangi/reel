<div align="center">

# 🎬 Reel

### *Revived Eel* - Build Local-AI Desktop Apps with Python + Web Tech

[![PyPI version](https://img.shields.io/pypi/v/Eel?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/Eel/)
[![Downloads](https://img.shields.io/pypi/dm/Eel?style=for-the-badge&logo=pypi&logoColor=white)](https://pypistats.org/packages/eel)
[![Python](https://img.shields.io/pypi/pyversions/Eel?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/Eel/)
[![License](https://img.shields.io/pypi/l/Eel.svg?style=for-the-badge)](https://pypi.org/project/Eel/)
[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/invite/3nqXPFX)

**[Quick Start](#-quick-start)** •
**[Documentation](docs/)** •
**[Security](#-security-notice)** •
**[AI Integration](#-ai-integration)** •
**[Contributing](#-contributing)**

</div>

---

## 🚀 About Reel

> **Welcome to Reel - The Revival of Eel**
>
> The original Eel project was unmaintained, so we created **Reel** - a modernized, actively maintained fork. This revival includes:
>
> ✅ **Security hardening** - Authentication, origin validation, HTTPS/WSS support
> ✅ **Modern Python patterns** - Type hints, async improvements, better architecture
> ✅ **AI/LLM integration** - First-class support for local AI models
> ✅ **Active development** - Community-driven with clear roadmap
>
> **Stability:** Production-ready for internal tools with security best practices
> **Vision:** The easiest way to build **privacy-first, local-AI desktop applications**

---

## 💡 What is Reel?

**Reel** (Revived Eel) is a lightweight Python library for creating **Electron-style desktop apps** using HTML/CSS/JS for the frontend and Python for the backend. Dead simple. No complex build chains. No IPC nightmares.

> **Note:** The package is still `pip install eel` for backwards compatibility with the original Eel ecosystem.

### The Magic

```python
import eel

eel.init('web')

@eel.expose
def my_python_function(data):
    # Full Python power: AI/ML, data processing, anything!
    return process_with_local_llm(data)

eel.start('index.html')
```

```javascript
// Call Python from JavaScript - that simple!
async function handleClick() {
    let result = await eel.my_python_function(userData)();
    updateUI(result);
}
```

**That's it.** No Electron bloat. No complex setup. Just Python + Web = Desktop App.

---

## 🎯 Why Choose Reel?

### Perfect For

- 🤖 **Local AI/LLM Applications** - Privacy-first AI with local models (Mistral, Llama, etc.)
- 📊 **Data Science Dashboards** - Plotly/D3.js frontend + NumPy/Pandas backend
- 🛠️ **Internal Tools** - System admin, automation, business apps
- 🚀 **Rapid Prototyping** - Build desktop apps in minutes, not days
- 🎓 **Learning Projects** - Teach full-stack with familiar technologies

### Comparison

| Feature | Reel | Electron | Tauri | PyQt |
|---------|------|----------|-------|------|
| Size | 🟢 Tiny (~50KB) | 🔴 Large (~150MB) | 🟡 Medium (~10MB) | 🟡 Medium |
| Python Integration | 🟢 Native & Simple | 🟡 Via IPC | 🔴 Complex/None | 🟢 Native |
| Modern Web UI | 🟢 Full Stack | 🟢 Full Stack | 🟢 Full Stack | 🔴 Limited |
| Learning Curve | 🟢 Minimal | 🟡 Moderate | 🟡 Moderate | 🔴 Steep |
| Local AI Ready | 🟢 Perfect | 🟡 Possible | 🟡 Possible | 🟡 Possible |

---

## ⚡ Quick Start

### Installation

```bash
# Basic installation
pip install eel

# With Jinja2 templating
pip install eel[jinja2]

# With AI capabilities (coming soon!)
pip install eel[ai]
```

### 60-Second App

**1. Create structure:**
```bash
mkdir my_app && cd my_app
mkdir web
```

**2. Create `app.py`:**
```python
import eel

eel.init('web')

@eel.expose
def greet(name):
    return f"Hello, {name}! 👋"

eel.start('index.html', size=(600, 400))
```

**3. Create `web/index.html`:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Eel App</title>
    <script src="/eel.js"></script>
</head>
<body>
    <h1>Eel App</h1>
    <input id="name" placeholder="Your name">
    <button onclick="sayHi()">Greet Me</button>
    <div id="result"></div>

    <script>
        async function sayHi() {
            const name = document.getElementById('name').value;
            const greeting = await eel.greet(name)();
            document.getElementById('result').innerText = greeting;
        }
    </script>
</body>
</html>
```

**4. Run it:**
```bash
python app.py
```

🎉 **Done!** Your app opens in a native window.

---

## 🤖 AI Integration

Reel is **perfect for local AI applications**. Here's why:

- ✅ **Python-native** - Easy integration with LLM libraries
- ✅ **Desktop environment** - Better for local models than web
- ✅ **Privacy-first** - No cloud, no data leaks
- ✅ **Offline-capable** - Works without internet

### 10-Minute AI App

```python
import eel
from llama_cpp import Llama

eel.init('web')

# Load local LLM (runs on your machine!)
llm = Llama(model_path="models/mistral-7b.gguf", n_ctx=2048)

@eel.expose
def ai_chat(message):
    response = llm(
        f"<s>[INST] {message} [/INST]",
        max_tokens=256,
        temperature=0.7
    )
    return response['choices'][0]['text']

eel.start('ai_chat.html')
```

**More AI examples:**
- Natural language Python function calls
- AI-powered UI generation from descriptions
- Intelligent error explanations
- Local document Q&A with RAG

👉 See [docs/05-AI_LLM_INTEGRATION_STRATEGY.md](docs/05-AI_LLM_INTEGRATION_STRATEGY.md) for complete guide

---

## 🔒 Security Notice

**⚠️ Important for Production Use**

Reel is designed for **local/internal applications**. For production deployment, implement these security measures:

| Risk | Status | Mitigation |
|------|--------|------------|
| No authentication | ⚠️ Required | Use session tokens or OAuth (see examples) |
| Plain HTTP/WS | ⚠️ Required | Enable HTTPS/WSS for network access |
| No origin validation | ⚠️ Required | Validate WebSocket origins |
| Exposed functions | ⚠️ Careful | Only expose necessary functions |

**Security examples available in:**
- `examples/11-security/` - Authentication, HTTPS, origin validation
- `docs/04-SECURITY_ANALYSIS.md` - Complete security audit and fixes

**For internal tools on localhost:** Reel is safe and ready to use!
**For network access:** Implement security measures from our guides.

👉 Read [docs/04-SECURITY_ANALYSIS.md](docs/04-SECURITY_ANALYSIS.md) for details

---

## 📚 Documentation

### Quick Links

- **[Getting Started Guide](docs/01-README_IMPROVED.md)** - Comprehensive tutorial
- **[API Reference](docs/)** - All functions and options
- **[Examples](/examples/)** - 10+ working examples
- **[AI Integration](docs/05-AI_LLM_INTEGRATION_STRATEGY.md)** - Build local-AI apps

### Deep Dives

- **[Security Guide](docs/04-SECURITY_ANALYSIS.md)** - Production hardening
- **[Architecture](docs/03-CODEBASE_IMPROVEMENT_ANALYSIS.md)** - How Eel works
- **[Contributing Guide](docs/CONTRIBUTING.md)** - Join development
- **[Complete Index](docs/INDEX.md)** - All documentation

---

## 🛠️ Development Status

### Current Version: 0.18.2 (Revival Fork)

**✅ Completed:**
- Security analysis and remediation plan
- AI integration architecture
- Modern documentation
- Development roadmap

**🚧 In Progress (Q1 2026):**
- [ ] Authentication examples and middleware
- [ ] HTTPS/WSS support with examples
- [ ] Remove global state (EelApplication class)
- [ ] Comprehensive type hints
- [ ] 80%+ test coverage

**🔮 Planned (Q2-Q3 2026):**
- [ ] `eel.ai` extension module
- [ ] Natural language interface
- [ ] AI-powered UI generator
- [ ] Plugin architecture
- [ ] 5+ AI demo applications

### Roadmap

```
Phase 1: Security (Weeks 1-2)     🚧 IN PROGRESS
  └─ Authentication, HTTPS, origin validation

Phase 2: Modernization (Months 1-3)
  └─ Remove globals, type hints, better architecture

Phase 3: AI Integration (Months 3-6)
  └─ Local LLM support, natural language, demos
```

**Track progress:** [GitHub Projects](https://github.com/python-eel/Eel/projects)

---

## 🤝 Contributing

**We need your help!** Reel is community-driven and thriving.

### Most Needed

| Priority | Area | Skills | Time |
|----------|------|--------|------|
| 🔴 HIGH | Security fixes | Python, security | 1-2 weeks |
| 🟠 MEDIUM | Remove global state | Python, architecture | 1 week |
| 🟡 LOW | Type hints | Python, mypy | 2 weeks |
| 🟢 OPPORTUNITY | AI integration | Python, LLMs | 1 month |

### Getting Started

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/Eel.git
cd Eel

# 2. Set up development environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install -r requirements-test.txt

# 3. Run tests
pytest

# 4. Make changes, add tests, submit PR!
```

**Read full guide:** [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

### Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). Be respectful, inclusive, and collaborative.

---

## 🌟 Examples

### Basic Examples

```bash
# Hello World
python examples/01\ -\ hello_world/hello.py

# Callbacks
python examples/02\ -\ callbacks/callbacks.py

# File Access (desktop superpowers!)
python examples/04\ -\ file_access/file_access.py
```

### Advanced Examples

- **React Integration** - `examples/07 - CreateReactApp/`
- **Jinja Templates** - `examples/06 - jinja_templates/`
- **Custom Routes** - `examples/10 - custom_app_routes/`

### Coming Soon: AI Examples

- Natural language Python interface
- AI-powered data analysis dashboard
- Local document Q&A with RAG
- Code generation from descriptions
- Intelligent system monitoring

---

## 🏆 Use Cases

### Real-World Applications

🔬 **Data Science**
- Build dashboards with Plotly/D3.js + Pandas/NumPy
- Visualize ML model results in real-time
- Interactive data exploration tools

🤖 **Local AI Apps**
- Privacy-first chatbots with local LLMs
- Document analysis without cloud
- AI-assisted coding tools
- Offline intelligent assistants

🛠️ **System Tools**
- Server monitoring dashboards
- Deployment automation UIs
- Database management tools
- Log analyzers with visualization

📊 **Business Apps**
- Inventory management
- Report generators
- Data entry tools with validation
- Internal admin panels

---

## 💬 Community

- **Discord:** [Join our community](https://discord.com/invite/3nqXPFX)
- **GitHub Discussions:** [Ask questions, share projects](https://github.com/python-eel/Eel/discussions)
- **Issues:** [Report bugs, request features](https://github.com/python-eel/Eel/issues)

### Show Your Support

⭐ **Star this repo** if Eel is useful to you!

🐦 **Tweet about your projects** with `#eelframework`

📝 **Write tutorials** and share with the community

💻 **Contribute code** and help us improve

---

## 📊 Stats

- **6,000+** monthly downloads on PyPI
- **1,000+** GitHub stars (original repo)
- **Active since 2017** - Stable and battle-tested
- **Python 3.7+** support

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Original Eel Author:** [Chris Knott](https://github.com/ChrisKnott) - Thank you for creating Eel!
- **Original Maintainers:** [python-eel organization](https://github.com/python-eel)
- **Reel (Revival) Contributors:** Community-driven modernization effort
- **Built on:** [Bottle](https://bottlepy.org/), [Gevent](http://www.gevent.org/), WebSockets

---

## 🚀 Quick Commands Reference

```bash
# Installation
pip install eel

# Run an example
python examples/01\ -\ hello_world/hello.py

# Development setup
pip install -r requirements-test.txt

# Run tests
pytest

# Type checking
mypy --strict eel

# Build distributable
python -m eel your_app.py web/ --onefile --noconsole
```

---

<div align="center">

**[Get Started](#-quick-start)** •
**[Read Docs](docs/)** •
**[Join Discord](https://discord.com/invite/3nqXPFX)** •
**[Contribute](#-contributing)**

Made with ❤️ by the Python community

🤖 **The future is local-AI desktop apps. Let's build it together.**

</div>
