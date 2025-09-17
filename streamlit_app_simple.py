"""
Simplified Streamlit app for CodeCritic - No package dependencies
"""

import streamlit as st
import os
import time
from typing import Dict, Any

# Configure page
st.set_page_config(
    page_title="CodeCritic - AI Code Review",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feedback-bug { color: #d62728; }
    .feedback-practice { color: #ff7f0e; }
    .feedback-performance { color: #2ca02c; }
    .feedback-style { color: #9467bd; }
    .feedback-security { color: #e377c2; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .severity-critical { background-color: #ffebee; border-left: 4px solid #f44336; }
    .severity-high { background-color: #fff3e0; border-left: 4px solid #ff9800; }
    .severity-medium { background-color: #fff8e1; border-left: 4px solid #ffc107; }
    .severity-low { background-color: #f1f8e9; border-left: 4px solid #4caf50; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 CodeCritic</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-powered code review and analysis tool</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check if API keys are available from environment
    available_keys = []
    if os.getenv("OPENAI_API_KEY"):
        available_keys.append("OpenAI")
    if os.getenv("ANTHROPIC_API_KEY"):
        available_keys.append("Anthropic")
    if os.getenv("GEMINI_API_KEY"):
        available_keys.append("Gemini")
    if os.getenv("MISTRAL_API_KEY"):
        available_keys.append("Mistral")
    
    if available_keys:
        st.success(f"✅ API Keys loaded: {', '.join(available_keys)}")
        api_key = "ENV_LOADED"
    else:
        st.warning("⚠️ No API keys found in environment")
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Enter your Anthropic or OpenAI API key"
        )
    
    # Model selection
    model = st.selectbox(
        "Model",
        [
            "anthropic/claude-3-sonnet-20240229",
            "anthropic/claude-3-haiku-20240307",
            "gpt-4",
            "gpt-3.5-turbo"
        ],
        index=0
    )
    
    # Language selection
    language = st.selectbox(
        "Programming Language",
        ["python", "javascript", "typescript", "java", "cpp", "c", "csharp", "php", "ruby", "go", "rust"],
        index=0
    )
    
    # Analysis options
    st.subheader("🔧 Analysis Options")
    enable_modular = st.checkbox("Enable Modular Review", value=True)
    include_security = st.checkbox("🔒 Security Analysis", value=True)
    include_performance = st.checkbox("⚡ Performance Analysis", value=True)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ by [Rishu Kumar Singh](https://github.com/rishuSingh404) from IIT Patna**")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Code")
    
    # Code input
    code_input = st.text_area(
        "Paste your code here:",
        height=400,
        placeholder="def example_function():\n    # Your code here\n    return 'Hello, World!'"
    )
    
    # Review button
    if st.button("🔍 Review Code", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("Please enter some code to review.")
        elif api_key != "ENV_LOADED" and not api_key:
            st.error("Please enter your API key in the sidebar or set up environment variables.")
        else:
            with st.spinner("Analyzing your code..."):
                try:
                    # Simulate analysis
                    time.sleep(2)
                    
                    # Mock response
                    mock_response = {
                        "feedback": [
                            {
                                "type": "bug",
                                "message": "Function lacks error handling for edge cases",
                                "line_number": 1,
                                "function_name": "example_function",
                                "severity": "high",
                                "suggestion": "Add try-catch blocks for robust error handling",
                                "confidence": 0.9,
                                "tags": ["error-handling", "robustness"]
                            },
                            {
                                "type": "best_practice",
                                "message": "Consider adding type hints for better code documentation",
                                "line_number": 1,
                                "function_name": "example_function",
                                "severity": "low",
                                "suggestion": "Use typing module for type annotations",
                                "confidence": 0.8,
                                "tags": ["type-safety", "documentation"]
                            }
                        ],
                        "summary": "Found 2 total issues: 🐞 1 potential bug(s), 💡 1 best practice suggestion(s)",
                        "total_issues": 2,
                        "processing_time": 2.1,
                        "model_used": model,
                        "modular_analysis": enable_modular
                    }
                    
                    st.session_state.review_result = mock_response
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")

with col2:
    st.header("🔍 Review Results")
    
    if 'review_result' in st.session_state:
        result = st.session_state.review_result
        
        # Summary metrics
        col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
        
        with col_metrics1:
            st.metric("Total Issues", result["total_issues"])
        
        with col_metrics2:
            st.metric("Processing Time", f"{result['processing_time']:.1f}s")
        
        with col_metrics3:
            st.metric("Model Used", result["model_used"].split("/")[-1])
        
        with col_metrics4:
            st.metric("Modular Analysis", "✅" if result["modular_analysis"] else "❌")
        
        # Summary
        st.markdown("### 📋 Summary")
        st.info(result["summary"])
        
        # Detailed feedback
        st.markdown("### 📋 Detailed Feedback")
        
        for item in result["feedback"]:
            severity = item.get("severity", "medium")
            confidence = item.get("confidence", 0.8)
            
            severity_color = {
                "critical": "🔴",
                "high": "🟠", 
                "medium": "🟡",
                "low": "🟢"
            }.get(severity, "⚪")
            
            severity_class = f"severity-{severity}"
            
            st.markdown(f"""
            <div class="{severity_class}" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                <strong>{severity_color} {item['message']}</strong><br>
                <small>Confidence: {confidence:.1%} | Severity: {severity.title()}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if item.get("function_name"):
                st.markdown(f"*Function: `{item['function_name']}`*")
            
            if item.get("suggestion"):
                st.markdown(f"**💡 Suggestion:** {item['suggestion']}")
            
            if item.get("tags"):
                tags_str = ", ".join([f"`{tag}`" for tag in item["tags"]])
                st.markdown(f"**🏷️ Tags:** {tags_str}")
            
            st.markdown("---")
    else:
        st.info("👈 Enter your code and click 'Review Code' to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔍 CodeCritic v1.0.0 | Built with Streamlit</p>
    <p>Deploy your own instance or visit: <a href="https://codecritic-rishu.streamlit.app">codecritic-rishu.streamlit.app</a></p>
</div>
""", unsafe_allow_html=True)
