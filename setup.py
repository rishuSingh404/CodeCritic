from setuptools import setup, find_packages

setup(
    name="codecritic-app",
    version="0.1.0",
    description="AI-powered code review and analysis tool",
    author="Rishu Kumar Singh",
    author_email="rishu@example.com",
    url="https://github.com/rishuSingh404/CodeCritic",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "anthropic>=0.8.0",
        "openai>=1.1.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.4.2",
    ],
    python_requires=">=3.10",
)
