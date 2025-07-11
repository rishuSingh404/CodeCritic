#!/usr/bin/env python3
"""
Basic tests for CodeCritic
"""

import pytest
from codecritic import CodeCritic


def test_codecritic_initialization():
    """Test that CodeCritic can be initialized"""
    critic = CodeCritic()
    assert critic is not None


def test_basic_analysis():
    """Test basic code analysis functionality"""
    critic = CodeCritic()
    
    test_code = """
def hello_world():
    print("Hello, World!")
"""
    
    analysis = critic.analyze_code(
        code=test_code,
        language="python"
    )
    
    assert analysis is not None
    assert hasattr(analysis, 'analysis_results')


def test_api_keys_configuration():
    """Test that API keys are properly configured"""
    from codecritic.config import config
    
    # Check if API keys are set
    keys_to_check = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'GEMINI_API_KEY',
        'MISTRAL_API_KEY'
    ]
    
    for key_name in keys_to_check:
        key_value = getattr(config, key_name, None)
        assert key_value is not None, f"{key_name} is not configured"
        assert key_value != "your-api-key-here", f"{key_name} has default value"


if __name__ == "__main__":
    pytest.main([__file__]) 