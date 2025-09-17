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

# Professional CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: none;
    }
    
    .metric-card h3 {
        color: white;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Issue Cards */
    .issue-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .issue-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .issue-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .issue-description {
        color: #6b7280;
        font-size: 0.875rem;
        line-height: 1.5;
        margin: 0 0 0.75rem 0;
    }
    
    .issue-suggestion {
        background: #f8fafc;
        border-left: 3px solid #3b82f6;
        padding: 0.75rem;
        border-radius: 0 4px 4px 0;
        font-size: 0.875rem;
        color: #374151;
    }
    
    /* Severity Badges */
    .severity-critical { 
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .severity-high { 
        background: linear-gradient(135deg, #f97316, #ea580c);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .severity-medium { 
        background: linear-gradient(135deg, #eab308, #ca8a04);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .severity-low { 
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Code Input Area */
    .code-input-container {
        background: #f8fafc;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
    
    /* Status Indicators */
    .status-success {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.875rem;
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown('<h1 class="main-header">🔍 CodeCritic</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered code review and analysis tool</p>', unsafe_allow_html=True)

# Add a subtle divider
st.markdown("---")

# Professional Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Keys Status
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
        st.markdown(f'<div class="status-success">✅ API Keys loaded: {", ".join(available_keys)}</div>', unsafe_allow_html=True)
        api_key = "ENV_LOADED"
    else:
        st.markdown('<div class="status-warning">⚠️ No API keys found in environment</div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Enter your Anthropic or OpenAI API key",
            placeholder="sk-..."
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

# Main content with professional layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="section-header">📝 Input Code</h2>', unsafe_allow_html=True)
    
    # Professional code input container
    st.markdown('<div class="code-input-container">', unsafe_allow_html=True)
    code_input = st.text_area(
        "Paste your code here:",
        height=400,
        placeholder="def example_function():\n    # Your code here\n    return 'Hello, World!'",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    st.markdown('<h2 class="section-header">🔍 Review Results</h2>', unsafe_allow_html=True)
    
    if 'review_result' in st.session_state:
        result = st.session_state.review_result
        
        # Professional metrics cards
        col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)
        
        with col_metrics1:
            st.markdown(f'''
            <div class="metric-card">
                <h3>Total Issues</h3>
                <div class="metric-value">{result["total_issues"]}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_metrics2:
            st.markdown(f'''
            <div class="metric-card">
                <h3>Processing Time</h3>
                <div class="metric-value">{result["processing_time"]:.1f}s</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_metrics3:
            st.markdown(f'''
            <div class="metric-card">
                <h3>Model Used</h3>
                <div class="metric-value">{result["model_used"].split("/")[-1]}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_metrics4:
            st.markdown(f'''
            <div class="metric-card">
                <h3>Modular Analysis</h3>
                <div class="metric-value">{"✅" if result["modular_analysis"] else "❌"}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Summary
        st.markdown("### 📋 Summary")
        st.info(result["summary"])
        
        # Professional feedback display
        st.markdown('<h3 class="section-header">📋 Detailed Feedback</h3>', unsafe_allow_html=True)
        
        for item in result["feedback"]:
            severity = item.get("severity", "medium")
            confidence = item.get("confidence", 0.8)
            
            # Professional issue card
            st.markdown(f'''
            <div class="issue-card">
                <div class="issue-title">
                    <span class="severity-{severity}">{severity.upper()}</span>
                    {item['message']}
                </div>
                <div class="issue-description">
                    Confidence: {confidence:.1%} | Severity: {severity.title()}
                </div>
                {f'<div class="issue-suggestion"><strong>💡 Suggestion:</strong> {item["suggestion"]}</div>' if item.get("suggestion") else ''}
                {f'<div style="margin-top: 0.5rem;"><strong>Function:</strong> <code>{item["function_name"]}</code></div>' if item.get("function_name") else ''}
                {f'<div style="margin-top: 0.5rem;"><strong>Tags:</strong> {", ".join([f"<span style="background: #e5e7eb; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">{tag}</span>" for tag in item.get("tags", [])])}</div>' if item.get("tags") else ''}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("👈 Enter your code and click 'Review Code' to get started!")

# Professional Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>🔍 CodeCritic v1.0.0</strong> | Built with Streamlit & AI</p>
    <p>Deploy your own instance or visit: <a href="https://codecritic-rishu.streamlit.app" style="color: #667eea; text-decoration: none;">codecritic-rishu.streamlit.app</a></p>
    <p style="margin-top: 1rem; font-size: 0.75rem;">© 2025 Rishu Kumar Singh | IIT Patna</p>
</div>
""", unsafe_allow_html=True)
