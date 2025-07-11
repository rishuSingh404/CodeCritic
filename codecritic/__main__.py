"""
Main entry point for CodeCritic CLI
"""

import sys
import argparse
from pathlib import Path

from .core import CodeCritic
from .models import ReviewRequest, Language


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CodeCritic - AI-powered code review tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codecritic --file mycode.py
  codecritic --code "def hello(): print('world')"
  codecritic --file mycode.py --modular
        """
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Path to file to review"
    )
    
    parser.add_argument(
        "--code", "-c", 
        type=str,
        help="Code string to review"
    )
    
    parser.add_argument(
        "--modular", "-m",
        action="store_true",
        help="Enable modular review (function-by-function analysis)"
    )
    
    parser.add_argument(
        "--language", "-l",
        type=str,
        choices=["python"],
        default="python",
        help="Programming language (default: python)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="LLM model to use"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for LLM service"
    )
    
    args = parser.parse_args()
    
    if not args.file and not args.code:
        parser.error("Either --file or --code must be specified")
    
    # Get code content
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        code = file_path.read_text()
    else:
        code = args.code
    
    # Initialize CodeCritic
    try:
        critic = CodeCritic()
        request = ReviewRequest(
            code=code,
            language=Language(args.language),
            enable_modular_review=args.modular,
            model=args.model
        )
        
        print("🔍 Analyzing code with CodeCritic...")
        response = critic.review(request)
        
        # Display results
        print(f"\n📊 Summary: {response.summary}")
        print(f"⏱️  Processing time: {response.processing_time:.2f}s")
        print(f"🤖 Model used: {response.model_used}")
        print(f"🔧 Modular analysis: {'Yes' if response.modular_analysis else 'No'}")
        
        if response.feedback:
            print(f"\n📋 Found {len(response.feedback)} issues:\n")
            
            for i, item in enumerate(response.feedback, 1):
                icon = {
                    "bug": "🐞",
                    "best_practice": "💡",
                    "performance": "⚡", 
                    "style": "✅"
                }.get(item.type, "📝")
                
                print(f"{i}. {icon} [{item.type.upper()}] {item.message}")
                if item.function_name:
                    print(f"   Function: {item.function_name}")
                if item.suggestion:
                    print(f"   Suggestion: {item.suggestion}")
                print()
        else:
            print("\n✅ No issues found! Your code looks good.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 