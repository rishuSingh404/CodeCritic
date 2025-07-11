# CodeCritic 🔍

An AI-powered code review and analysis tool that provides intelligent feedback on your code with modular processing capabilities.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io)

## ✨ Features

- **🐞 Bug Detection**: Identifies potential bugs and issues in your code
- **💡 Best Practices**: Suggests improvements based on coding standards
- **⚡ Performance**: Highlights performance optimization opportunities
- **✅ Style**: Provides style and formatting recommendations
- **🔧 Modular Review**: Analyze code function-by-function for detailed insights
- **🌐 Multi-language Support**: Currently supports Python (more languages coming soon)
- **🔒 Security Analysis**: Identifies potential security vulnerabilities
- **📊 Performance Metrics**: Provides detailed performance insights

## 🏗️ Architecture

*[Architecture diagram and detailed system design will be added here]*

### System Components:
- **Core Engine**: AI-powered code analysis using multiple LLM providers
- **Parser Module**: Multi-language code parsing and AST analysis
- **Cache System**: Intelligent caching for improved performance
- **Rate Limiting**: API call management and cost control
- **Web Interface**: Streamlit-based user interface
- **API Backend**: FastAPI REST API for programmatic access

## 🚀 Quick Start

### Web Interface
Visit our live demo: [codecritic-rishu.streamlit.app](https://codecritic-rishu.streamlit.app)

### Local Installation
```bash
# Clone the repository
git clone https://github.com/rishuSingh404/CodeCritic.git
cd CodeCritic

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run codecritic/ui/streamlit_app.py
```

### API Usage
```python
from codecritic import CodeCritic

# Initialize with your API key
critic = CodeCritic()

# Analyze your code
feedback = critic.analyze_code("""
def calculate_sum(a, b):
    return a + b
""", language="python")

print(feedback.analysis_results)
```

## 🔧 Configuration

Set your API keys as environment variables:
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
export MISTRAL_API_KEY="your-mistral-api-key"
```

## 🧠 How It Works

CodeCritic uses advanced LLM technology to analyze your code:

1. **Code Parsing**: Splits your code into functions and classes using AST
2. **Modular Analysis**: Reviews each component individually (when enabled)
3. **Categorized Feedback**: Organizes suggestions by type (Bug, Performance, Style, etc.)
4. **Intelligent Merging**: Combines insights into comprehensive recommendations

## 🛠️ Development

### Project Structure
```
CodeCritic/
├── codecritic/           # Main package
│   ├── __init__.py
│   ├── core.py          # Core analysis engine
│   ├── models.py        # Data models
│   ├── parser.py        # Code parsing utilities
│   ├── prompts.py       # LLM prompt templates
│   ├── config.py        # Configuration management
│   ├── api.py           # FastAPI backend
│   └── ui/              # User interface
│       └── streamlit_app.py
├── tests/               # Test suite
├── requirements.txt     # Dependencies
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run the FastAPI backend
uvicorn codecritic.api:app --reload

# Run the Streamlit frontend
streamlit run codecritic/ui/streamlit_app.py
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=codecritic
```

## 🚀 Deployment

### Streamlit Cloud
1. Fork this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create new app and connect your repository
4. Set main file path to: `codecritic/ui/streamlit_app.py`
5. Add your API keys as secrets
6. Deploy!

### Docker (Coming Soon)
```bash
docker build -t codecritic .
docker run -p 8501:8501 codecritic
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Performance

- **Response Time**: Average 2-5 seconds per analysis
- **Supported Languages**: Python, JavaScript, TypeScript, Java, C++, Go, Rust
- **API Providers**: OpenAI, Anthropic, Google Gemini, Mistral AI

## 🔗 Links

- **Repository**: [https://github.com/rishuSingh404/CodeCritic](https://github.com/rishuSingh404/CodeCritic)
- **Live Demo**: [https://codecritic-rishu.streamlit.app](https://codecritic-rishu.streamlit.app)
- **Issues**: [https://github.com/rishuSingh404/CodeCritic/issues](https://github.com/rishuSingh404/CodeCritic/issues)

---

**Built with ❤️ by [Rishu Kumar Singh](https://github.com/rishuSingh404) from IIT Patna**
