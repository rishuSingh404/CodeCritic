# Contributing to CodeCritic

Thank you for considering contributing to CodeCritic! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please be respectful and considerate of others.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue on our GitHub repository with the following information:

- Clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements! Please create an issue on our GitHub repository with:

- Clear and descriptive title
- Detailed description of the proposed enhancement
- Any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Format your code (`black .` and `isort .`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Environment Setup

1. Clone the repository
```bash
git clone https://github.com/rishuSingh404/CodeCritic.git
cd CodeCritic
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install -e .  # Install the package in development mode
```

## Coding Guidelines

- Follow PEP 8 style guide for Python code
- Use type hints where appropriate
- Write docstrings for functions, classes, and modules
- Keep functions and methods focused on a single responsibility
- Write tests for new features and bug fixes

## Testing

Run tests using pytest:

```bash
pytest
# With coverage
pytest --cov=codecritic
```

## Documentation

Please update documentation when changing code:

- Update docstrings when changing function behavior
- Update README.md for user-facing changes
- Add examples for new features

Thank you for your contributions!
