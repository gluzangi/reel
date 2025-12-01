# Contributing to Eel

Thank you for your interest in contributing to Eel! This guide will help you get started.

## 🎯 Project Status

Eel is undergoing **active revival and modernization**. We're a community-driven project focused on:
- Security hardening
- Modern Python patterns
- AI/LLM integration
- Active maintenance

## 🚀 Quick Start

### 1. Fork and Clone

```bash
git clone git@github.com:YOUR-USERNAME/Eel.git
cd Eel
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt        # Core dependencies
pip install -r requirements-test.txt   # Testing dependencies
pip install -r requirements-meta.txt   # Tox for multi-version testing
```

**Note:** `venv` is in `.gitignore` so it's the recommended name.

### 3. Run Tests

```bash
# Quick test run
pytest

# Test specific version (requires multiple Python versions installed)
tox -e py37

# Test all supported versions
tox

# Type checking
mypy --strict eel
```

### 4. Make Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Add tests
# Update documentation

# Run tests
pytest

# Type check
mypy --strict eel

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

## 📋 What We Need

### High Priority (Immediate Need)

| Area | Description | Skills Needed | Est. Time |
|------|-------------|---------------|-----------|
| **Security fixes** | Authentication, origin validation, HTTPS/WSS | Python, security best practices | 1-2 weeks |
| **Tests** | Increase coverage to 80%+ | Python, pytest | 1-2 weeks |
| **Documentation** | Examples, tutorials, API docs | Technical writing | Ongoing |

### Medium Priority

| Area | Description | Skills Needed | Est. Time |
|------|-------------|---------------|-----------|
| **Remove global state** | Refactor to EelApplication class | Python, architecture | 1 week |
| **Type hints** | Comprehensive typing throughout | Python, mypy | 2 weeks |
| **Error handling** | Better exceptions, user-friendly messages | Python | 3-5 days |

### Opportunities (Exciting!)

| Area | Description | Skills Needed | Est. Time |
|------|-------------|---------------|-----------|
| **AI integration** | eel.ai module, natural language interface | Python, LLMs, AI/ML | 1 month |
| **Plugin system** | Middleware architecture | Python, architecture | 2 weeks |
| **Performance** | Benchmarking, optimization | Python, profiling | 1-2 weeks |

## 🧪 Testing Requirements

### Integration Tests

Integration tests use Selenium and require:
- [Chrome](https://www.google.com/chrome)
- [ChromeDriver](https://chromedriver.chromium.org/)

**Important:** Match ChromeDriver version to your Chrome version!

### Running Tests

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only (requires Chrome/ChromeDriver)
pytest tests/integration/

# All tests
pytest

# With coverage
pytest --cov=eel --cov-report=html
```

## 📝 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(ai): add natural language interface module

Implements basic natural language to function call translation
using local LLM models.

Closes #123
```

```bash
fix(security): add origin validation for WebSocket connections

Validates WebSocket origin header against allowed origins list
to prevent CSRF attacks.

Fixes #456
```

## 🔒 Security Guidelines

### When Adding Features

- ✅ Validate all user inputs
- ✅ Sanitize data before exposing to frontend
- ✅ Add security warnings to documentation
- ✅ Consider OWASP Top 10 vulnerabilities
- ✅ Add examples of secure usage

### When Exposing Functions

```python
# ❌ BAD - No validation
@eel.expose
def execute_command(cmd):
    os.system(cmd)  # DANGEROUS!

# ✅ GOOD - Validated and safe
@eel.expose
def execute_allowed_command(cmd_name):
    allowed_commands = {'status': 'systemctl status', 'info': 'uname -a'}
    if cmd_name in allowed_commands:
        return subprocess.check_output(allowed_commands[cmd_name], shell=False)
    raise ValueError(f"Command not allowed: {cmd_name}")
```

## 📚 Documentation Standards

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Short one-line description.

    Longer description explaining what the function does,
    any important details, and examples if helpful.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer

    Example:
        >>> my_function("test", 42)
        True
    """
    pass
```

### Examples

- Add examples for all new features
- Place in `examples/` directory
- Include README explaining the example
- Keep examples simple and focused

## 🎨 Code Style

### Python

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting (optional)
- Max line length: 100 characters (PEP 8 allows up to 99)
- Use type hints for all new code

### Type Hints

```python
from typing import List, Dict, Optional, Union

@eel.expose
def process_data(
    items: List[str],
    options: Optional[Dict[str, Union[str, int]]] = None
) -> Dict[str, any]:
    """Process items with optional configuration."""
    pass
```

## 🐛 Bug Reports

When reporting bugs, include:

1. **Environment:**
   - OS (Windows/Mac/Linux version)
   - Python version
   - Eel version
   - Browser (Chrome/Edge/etc.)

2. **Steps to Reproduce:**
   - Minimal code example
   - Expected behavior
   - Actual behavior

3. **Additional Context:**
   - Error messages (full traceback)
   - Screenshots if applicable
   - Relevant logs

**Use the bug report template** when creating issues.

## ✨ Feature Requests

When requesting features:

1. **Describe the problem** you're trying to solve
2. **Propose a solution** (if you have one)
3. **Describe alternatives** you've considered
4. **Additional context** - examples, mockups, etc.

**Use the feature request template** when creating issues.

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass (`pytest`)
- [ ] Type checking passes (`mypy --strict eel`)
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for significant changes)
- [ ] Commit messages follow conventions

### PR Description

Include:
- **What** changed
- **Why** it changed
- **How** to test it
- **Screenshots** (if applicable)
- **Related issues** (Closes #123)

### Review Process

1. Automated tests run on all PRs
2. At least one maintainer review required
3. Address review comments
4. Once approved, maintainer will merge

## 📖 Documentation Contributions

Help improve our docs:

- **Tutorials:** Step-by-step guides for common tasks
- **How-To Guides:** Solutions to specific problems
- **API Reference:** Document all public functions
- **Examples:** Real-world use cases

Documentation is in:
- `docs/` - Main documentation
- `examples/` - Working examples
- Inline docstrings - API documentation

## 💬 Getting Help

- **Discord:** [Join our community](https://discord.com/invite/3nqXPFX)
- **Discussions:** [GitHub Discussions](https://github.com/python-eel/Eel/discussions)
- **Issues:** Search existing issues first

## 🎯 Focus Areas

### Phase 1: Security (Weeks 1-2) 🚧 CURRENT

Help us make Eel production-ready:
- Authentication middleware and examples
- HTTPS/WSS support
- Origin validation
- Input validation patterns
- Security documentation

### Phase 2: Modernization (Months 1-3)

Remove technical debt:
- EelApplication class (remove globals)
- Comprehensive type hints
- Better error handling
- Plugin/middleware architecture
- 80%+ test coverage

### Phase 3: AI Integration (Months 3-6)

Build the future:
- `eel.ai` extension module
- Natural language interface
- UI generation from descriptions
- Demo applications
- Performance optimization for LLMs

## 📜 Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). In summary:

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Accept constructive criticism** gracefully
- **Focus on what's best** for the community

## 📞 Questions?

- Check [docs/INDEX.md](INDEX.md) for all documentation
- Ask in [Discord](https://discord.com/invite/3nqXPFX)
- Open a [Discussion](https://github.com/python-eel/Eel/discussions)

## 🙏 Thank You!

Every contribution helps make Eel better. Whether it's code, documentation, bug reports, or spreading the word - **thank you for being part of this project!**

---

**Ready to contribute?** Pick an issue labeled `good first issue` and dive in! 🚀
