from io import open
from setuptools import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
    name='Eel',
    version='0.18.2',
    author='Python Eel Organisation',
    author_email='python-eel@protonmail.com',
    url='https://github.com/python-eel/Eel',
    packages=['eel'],
    package_data={
        'eel': ['eel.js', 'py.typed'],
    },
    install_requires=[
        'bottle>=0.12.19,<1.0',
        'bottle-websocket>=0.2.9,<1.0',
        'pyparsing>=3.0.0,<4.0',
        'typing_extensions>=4.3.0',
        'gevent>=21.0.0,<25.0',
        'gevent-websocket>=0.10.0,<1.0.0',
        'greenlet>=1.0.0,<4.0.0',
        'importlib_resources>=5.0;python_version<"3.9"',
    ],
    extras_require={
        "ai": [
            "genkit>=0.4.0",
            "google-genai>=0.1.0",
            "llama-cpp-python>=0.2.0",
            "ollama>=0.1.0",
            "pandas>=2.0.0",
            "polars[pyarrow]>=0.19.0",
            "sentence-transformers>=2.2.0",
            "sqlite-vector[ai]>=0.1.0",
        ],
        "jinja2": ['jinja2>=2.10'],
        "security": [
            "cryptography>=3.4.0",
        ],
    },
    python_requires='>=3.7',
    description='For Reel HTML GUI applications, with easy Python/JS interop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gui', 'html', 'javascript', 'electron'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
)