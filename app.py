"""
Main Streamlit app for CodeCritic
This file is used for Streamlit Cloud deployment
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main app
from codecritic.ui.streamlit_app import main

if __name__ == "__main__":
    main()
