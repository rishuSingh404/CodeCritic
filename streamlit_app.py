"""
Streamlit UI for CodeCritic
"""

import streamlit as st
import requests
import json
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

# Import config to get API keys from environment
from codecritic.config import config

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check if API keys are available from environment
    available_keys = []
    if config.OPENAI_API_KEY:
        available_keys.append("OpenAI")
    if config.ANTHROPIC_API_KEY:
        available_keys.append("Anthropic")
    if config.GEMINI_API_KEY:
        available_keys.append("Gemini")
    if config.MISTRAL_API_KEY:
        available_keys.append("Mistral")
    
    if available_keys:
        st.success(f"✅ API Keys loaded: {', '.join(available_keys)}")
        # Use environment API keys
        api_key = "ENV_LOADED"
    else:
        st.warning("⚠️ No API keys found in environment")
        # Fallback to manual input
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
    
    # Language selection with auto-detection
    st.subheader("🌐 Language Selection")
    
    # Language selection with icons and categories
    language_categories = {
        "🐍 Python & Data": ["python", "r", "matlab"],
        "🌐 Web Development": ["javascript", "typescript", "php", "ruby"],
        "☕ Enterprise": ["java", "csharp", "scala"],
        "⚡ Systems": ["cpp", "c", "go", "rust"],
        "📱 Mobile": ["swift", "kotlin"],
        "🗄️ Database": ["sql"]
    }
    
    # Flatten all languages
    all_languages = []
    for category, langs in language_categories.items():
        all_languages.extend(langs)
    
    language = st.selectbox(
        "Programming Language",
        all_languages,
        index=0,
        format_func=lambda x: x.title(),
        help="Select the programming language for better analysis"
    )
    
    # Show language-specific information
    language_info = {
        "python": "🐍 Python - Best practices, PEP 8, type hints",
        "javascript": "🌐 JavaScript - ES6+, async/await, best practices",
        "typescript": "📘 TypeScript - Type safety, interfaces, generics",
        "java": "☕ Java - OOP principles, design patterns, conventions",
        "cpp": "⚡ C++ - Memory management, STL, modern C++",
        "c": "🔧 C - Memory safety, pointer usage, standards",
        "csharp": "💎 C# - .NET conventions, LINQ, async patterns",
        "php": "🐘 PHP - PSR standards, security, modern PHP",
        "ruby": "💎 Ruby - Ruby conventions, gems, metaprogramming",
        "go": "🐹 Go - Go idioms, concurrency, error handling",
        "rust": "🦀 Rust - Memory safety, ownership, lifetimes",
        "swift": "🍎 Swift - iOS conventions, optionals, protocols",
        "kotlin": "🔷 Kotlin - Android conventions, null safety",
        "scala": "⚡ Scala - Functional programming, JVM",
        "r": "📊 R - Data science, tidyverse, statistics",
        "matlab": "🔢 MATLAB - Matrix operations, toolboxes",
        "sql": "🗄️ SQL - Query optimization, indexing, normalization"
    }
    
    if language in language_info:
        st.caption(language_info[language])
    
    # Analysis options
    st.subheader("🔧 Analysis Options")
    
    enable_modular = st.checkbox(
        "Enable Modular Review (MCP)",
        value=True,
        help="Analyze code function-by-function for detailed insights"
    )
    
    include_security = st.checkbox(
        "🔒 Security Analysis",
        value=True,
        help="Include security vulnerability analysis"
    )
    
    include_performance = st.checkbox(
        "⚡ Performance Analysis",
        value=True,
        help="Include performance optimization analysis"
    )
    
    # Advanced options
    with st.expander("Advanced Options"):
        max_tokens = st.slider(
            "Max Tokens",
            min_value=1000,
            max_value=8000,
            value=4000,
            step=500
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1
        )
    
    st.markdown("---")
    st.markdown("**Built with ❤️ by [Rishu Kumar Singh](https://github.com/rishuSingh404) from IIT Patna**")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Code")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["📝 Paste Code", "📁 Upload Files"],
        horizontal=True
    )
    
    if input_method == "📝 Paste Code":
        # Language-specific placeholders
        placeholders = {
            "python": "def example_function():\n    # Your Python code here\n    return 'Hello, World!'",
            "javascript": "function exampleFunction() {\n    // Your JavaScript code here\n    return 'Hello, World!';\n}",
            "typescript": "function exampleFunction(): string {\n    // Your TypeScript code here\n    return 'Hello, World!';\n}",
            "java": "public class Example {\n    public static void main(String[] args) {\n        // Your Java code here\n        System.out.println(\"Hello, World!\");\n    }\n}",
            "cpp": "#include <iostream>\n\nint main() {\n    // Your C++ code here\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}",
            "c": "#include <stdio.h>\n\nint main() {\n    // Your C code here\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
            "csharp": "using System;\n\nclass Program {\n    static void Main() {\n        // Your C# code here\n        Console.WriteLine(\"Hello, World!\");\n    }\n}",
            "php": "<?php\n// Your PHP code here\nfunction exampleFunction() {\n    return 'Hello, World!';\n}\n?>",
            "ruby": "# Your Ruby code here\ndef example_function\n  'Hello, World!'\nend",
            "go": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    // Your Go code here\n    fmt.Println(\"Hello, World!\")\n}",
            "rust": "fn main() {\n    // Your Rust code here\n    println!(\"Hello, World!\");\n}",
            "swift": "import Foundation\n\n// Your Swift code here\nfunc exampleFunction() -> String {\n    return \"Hello, World!\"\n}",
            "kotlin": "fun main() {\n    // Your Kotlin code here\n    println(\"Hello, World!\")\n}",
            "scala": "object Main {\n  def main(args: Array[String]): Unit = {\n    // Your Scala code here\n    println(\"Hello, World!\")\n  }\n}",
            "r": "# Your R code here\nexample_function <- function() {\n  return(\"Hello, World!\")\n}",
            "matlab": "% Your MATLAB code here\nfunction result = example_function()\n    result = 'Hello, World!';\nend",
            "sql": "-- Your SQL code here\nSELECT 'Hello, World!' AS message;"
        }
        
        placeholder = placeholders.get(language, "// Your code here")
        
        # Single code input
        code_input = st.text_area(
            "Paste your code here:",
            height=400,
            placeholder=placeholder
        )
        uploaded_files = None
        selected_file = None
        
    else:
        # Multiple file upload
        uploaded_files = st.file_uploader(
            "Upload code files",
            type=['py', 'js', 'ts', 'jsx', 'tsx', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'scala', 'r', 'm', 'sql'],
            accept_multiple_files=True,
            help="Upload multiple code files for analysis"
        )
        
        if uploaded_files:
            # File selection dropdown
            file_names = [f.name for f in uploaded_files]
            selected_file = st.selectbox(
                "Select file to analyze:",
                file_names,
                help="Choose which file to analyze from your uploaded files"
            )
            
            # Display selected file content
            selected_file_obj = next(f for f in uploaded_files if f.name == selected_file)
            file_content = selected_file_obj.read().decode('utf-8')
            code_input = st.text_area(
                f"Content of {selected_file}:",
                value=file_content,
                height=400,
                key="file_content"
            )
        else:
            code_input = ""
            selected_file = None
            st.info("📁 Upload one or more code files to get started with batch analysis!")
    
    # Review buttons
    col_button1, col_button2 = st.columns([1, 1])
    
    with col_button1:
        if st.button("🔍 Review Code", type="primary", use_container_width=True):
            if not code_input.strip():
                st.error("Please enter some code to review.")
            elif api_key != "ENV_LOADED" and not api_key:
                st.error("Please enter your API key in the sidebar or set up environment variables.")
            else:
                with st.spinner("Analyzing your code..."):
                    try:
                        # Prepare request
                        request_data = {
                            "code": code_input,
                            "language": language,
                            "enable_modular_review": enable_modular,
                            "model": model,
                            "include_security_analysis": include_security,
                            "include_performance_metrics": include_performance
                        }
                        
                        # For demo purposes, we'll simulate the API call
                        # In production, you'd call your FastAPI backend
                        time.sleep(2)  # Simulate processing time
                        
                        # Mock response for demonstration with Phase 3 features
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
                                },
                                {
                                    "type": "performance",
                                    "message": "Function could be optimized for better performance",
                                    "line_number": 1,
                                    "function_name": "example_function",
                                    "severity": "medium",
                                    "suggestion": "Consider using more efficient algorithms",
                                    "confidence": 0.85,
                                    "tags": ["optimization", "algorithms"]
                                },
                                {
                                    "type": "style",
                                    "message": "Follow PEP 8 naming conventions",
                                    "line_number": 1,
                                    "function_name": "example_function",
                                    "severity": "low",
                                    "suggestion": "Use snake_case for function names",
                                    "confidence": 0.9,
                                    "tags": ["style", "conventions"]
                                },
                                {
                                    "type": "security",
                                    "message": "Potential input validation vulnerability",
                                    "line_number": 1,
                                    "function_name": "example_function",
                                    "severity": "critical",
                                    "suggestion": "Validate all user inputs before processing",
                                    "confidence": 0.95,
                                    "tags": ["security", "input-validation"]
                                }
                            ],
                            "summary": "Found 5 total issues: 🐞 1 potential bug(s), 💡 1 best practice suggestion(s), ⚡ 1 performance improvement(s), ✅ 1 style recommendation(s), 🔒 1 security issue(s) (Severity: 1 critical, 1 high, 1 medium, 2 low)",
                            "total_issues": 5,
                            "processing_time": 2.1,
                            "model_used": model,
                            "modular_analysis": enable_modular,
                            "code_blocks_analyzed": 1,
                            "performance_metrics": {
                                "total_tokens_used": 1500,
                                "api_calls_made": 3,
                                "average_response_time": 0.7,
                                "total_cost_estimate": 0.0225,
                                "cache_hits": 0,
                                "cache_misses": 1,
                                "cache_hit_rate": 0.0
                            },
                            "language_specific_insights": {
                                "language": language,
                                "total_functions": 1,
                                "total_classes": 0,
                                "average_function_length": 3.0,
                                "language_specific_recommendations": [
                                    "Consider breaking down long functions (>50 lines) for better readability"
                                ]
                            },
                            "code_complexity": {
                                "average_complexity": 1.0,
                                "max_complexity": 1.0,
                                "min_complexity": 1.0,
                                "high_complexity_functions": 0,
                                "very_high_complexity_functions": 0
                            }
                        }
                        
                        # Add file information if multiple files
                        if uploaded_files and selected_file:
                            mock_response["file_analyzed"] = selected_file
                            mock_response["total_files"] = len(uploaded_files)
                        
                        st.session_state.review_result = mock_response
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
    
    # Batch analysis button (only show if multiple files are uploaded)
    if uploaded_files and len(uploaded_files) > 1:
        with col_button2:
            if st.button("📁 Batch Analyze All", type="secondary", use_container_width=True):
                if api_key != "ENV_LOADED" and not api_key:
                    st.error("Please enter your API key in the sidebar or set up environment variables.")
                else:
                    with st.spinner(f"Analyzing {len(uploaded_files)} files..."):
                        try:
                            # Simulate batch analysis
                            time.sleep(len(uploaded_files) * 1.5)  # Simulate processing time
                            
                            # Mock batch response
                            batch_results = []
                            total_issues = 0
                            
                            for file in uploaded_files:
                                file_content = file.read().decode('utf-8')
                                file.seek(0)  # Reset file pointer
                                
                                # Simulate analysis for each file
                                file_issues = len(file_content.split('\n')) // 10  # Mock issue count
                                total_issues += file_issues
                                
                                batch_results.append({
                                    "filename": file.name,
                                    "issues": file_issues,
                                    "size_kb": len(file_content) / 1024,
                                    "language": file.name.split('.')[-1] if '.' in file.name else "unknown"
                                })
                            
                            # Store batch results
                            st.session_state.batch_results = {
                                "total_files": len(uploaded_files),
                                "total_issues": total_issues,
                                "files": batch_results,
                                "processing_time": len(uploaded_files) * 1.5
                            }
                            
                            st.success(f"✅ Batch analysis complete! Analyzed {len(uploaded_files)} files with {total_issues} total issues.")
                            
                        except Exception as e:
                            st.error(f"Error during batch analysis: {str(e)}")

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
        
        # Performance metrics
        if "performance_metrics" in result:
            st.markdown("### 📊 Performance Metrics")
            perf_metrics = result["performance_metrics"]
            
            col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
            
            with col_perf1:
                st.metric("Tokens Used", f"{perf_metrics['total_tokens_used']:,}")
            
            with col_perf2:
                st.metric("API Calls", perf_metrics['api_calls_made'])
            
            with col_perf3:
                st.metric("Avg Response", f"{perf_metrics['average_response_time']:.2f}s")
            
            with col_perf4:
                st.metric("Est. Cost", f"${perf_metrics['total_cost_estimate']:.4f}")
        
        # Summary
        st.markdown("### 📋 Summary")
        st.info(result["summary"])
        
        # File information (if multiple files were uploaded)
        if uploaded_files and len(uploaded_files) > 1:
            st.markdown("### 📁 File Information")
            st.info(f"📄 Currently analyzing: **{selected_file}**")
            st.info(f"📂 Total files uploaded: **{len(uploaded_files)}**")
            
            # Show all uploaded files
            with st.expander("📋 View all uploaded files"):
                for i, file in enumerate(uploaded_files, 1):
                    file_size = len(file.read()) / 1024  # Size in KB
                    file.seek(0)  # Reset file pointer
                    st.markdown(f"{i}. **{file.name}** ({file_size:.1f} KB)")
                    
                    # Add a button to switch to this file
                    if st.button(f"Switch to {file.name}", key=f"switch_{i}"):
                        st.session_state.selected_file = file.name
                        st.rerun()
        
        # Language insights
        if "language_specific_insights" in result:
            insights = result["language_specific_insights"]
            st.markdown("### 🌐 Language Insights")
            
            col_insights1, col_insights2 = st.columns(2)
            
            with col_insights1:
                st.metric("Functions", insights.get("total_functions", 0))
                st.metric("Classes", insights.get("total_classes", 0))
            
            with col_insights2:
                st.metric("Avg Function Length", f"{insights.get('average_function_length', 0):.1f} lines")
            
            if insights.get("language_specific_recommendations"):
                st.markdown("**Language-specific recommendations:**")
                for rec in insights["language_specific_recommendations"]:
                    st.markdown(f"- {rec}")
        
        # Complexity metrics
        if "code_complexity" in result:
            complexity = result["code_complexity"]
            st.markdown("### 🧮 Complexity Analysis")
            
            col_comp1, col_comp2, col_comp3 = st.columns(3)
            
            with col_comp1:
                st.metric("Avg Complexity", f"{complexity.get('average_complexity', 0):.1f}")
            
            with col_comp2:
                st.metric("Max Complexity", f"{complexity.get('max_complexity', 0):.1f}")
            
            with col_comp3:
                st.metric("High Complexity", complexity.get('high_complexity_functions', 0))
        
        # Detailed feedback
        st.markdown("### 📋 Detailed Feedback")
        
        # Group feedback by type
        feedback_by_type = {}
        for item in result["feedback"]:
            feedback_type = item["type"]
            if feedback_type not in feedback_by_type:
                feedback_by_type[feedback_type] = []
            feedback_by_type[feedback_type].append(item)
        
        # Display feedback by category
        type_icons = {
            "bug": "🐞",
            "best_practice": "💡", 
            "performance": "⚡",
            "style": "✅",
            "security": "🔒"
        }
        
        type_titles = {
            "bug": "Bug Detection",
            "best_practice": "Best Practices",
            "performance": "Performance",
            "style": "Style & Formatting",
            "security": "Security"
        }
        
        for feedback_type, items in feedback_by_type.items():
            with st.expander(f"{type_icons[feedback_type]} {type_titles[feedback_type]} ({len(items)} issues)", expanded=True):
                for item in items:
                    severity = item.get("severity", "medium")
                    confidence = item.get("confidence", 0.8)
                    
                    severity_color = {
                        "critical": "🔴",
                        "high": "🟠", 
                        "medium": "🟡",
                        "low": "🟢"
                    }.get(severity, "⚪")
                    
                    # Create severity-specific styling
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

    # Batch results display
    if 'batch_results' in st.session_state:
        batch_result = st.session_state.batch_results
        
        st.markdown("---")
        st.markdown("### 📁 Batch Analysis Results")
        
        # Batch summary metrics
        col_batch1, col_batch2, col_batch3, col_batch4 = st.columns(4)
        
        with col_batch1:
            st.metric("Files Analyzed", batch_result["total_files"])
        
        with col_batch2:
            st.metric("Total Issues", batch_result["total_issues"])
        
        with col_batch3:
            st.metric("Processing Time", f"{batch_result['processing_time']:.1f}s")
        
        with col_batch4:
            avg_issues = batch_result["total_issues"] / batch_result["total_files"] if batch_result["total_files"] > 0 else 0
            st.metric("Avg Issues/File", f"{avg_issues:.1f}")
        
        # File-by-file breakdown
        st.markdown("### 📋 File-by-File Breakdown")
        
        for file_result in batch_result["files"]:
            with st.expander(f"📄 {file_result['filename']} ({file_result['language']}) - {file_result['issues']} issues"):
                col_file1, col_file2, col_file3 = st.columns(3)
                
                with col_file1:
                    st.metric("Issues", file_result["issues"])
                
                with col_file2:
                    st.metric("Size", f"{file_result['size_kb']:.1f} KB")
                
                with col_file3:
                    st.metric("Language", file_result["language"].upper())
                
                # Progress bar for issues
                if file_result["issues"] > 0:
                    st.progress(min(file_result["issues"] / 10, 1.0))  # Normalize to 0-1
                    st.caption(f"Code quality score: {max(0, 10 - file_result['issues'])}/10")
                else:
                    st.success("✅ No issues found!")
                    st.caption("Code quality score: 10/10")
        
        # Overall quality assessment
        st.markdown("### 🎯 Overall Quality Assessment")
        
        if batch_result["total_issues"] == 0:
            st.success("🎉 Excellent! All files passed the analysis with no issues.")
        elif batch_result["total_issues"] < batch_result["total_files"] * 3:
            st.info("👍 Good code quality! Minor improvements suggested.")
        elif batch_result["total_issues"] < batch_result["total_files"] * 7:
            st.warning("⚠️ Moderate issues detected. Consider addressing the suggestions.")
        else:
            st.error("🚨 Multiple issues detected. Code review recommended.")
        
        # Clear batch results button
        if st.button("🗑️ Clear Batch Results"):
            del st.session_state.batch_results
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🔍 CodeCritic v1.0.0 | Built with FastAPI & Streamlit</p>
    <p>Deploy your own instance or visit: <a href="https://codecritic-rishu.streamlit.app">codecritic-rishu.streamlit.app</a></p>
</div>
""", unsafe_allow_html=True) 