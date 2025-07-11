import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration for CodeCritic"""
    
    # API Keys - Load from environment variables only
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")
    
    # Default model configurations
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_MAX_TOKENS = 4000
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = 10
    RATE_LIMIT_PER_HOUR = 100
    
    # Cache settings
    CACHE_TTL = 3600  # 1 hour
    CACHE_MAX_SIZE = 1000
    
    # Performance tracking
    ENABLE_PERFORMANCE_TRACKING = True
    PERFORMANCE_LOG_FILE = "codecritic_performance.log"
    
    # Security settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs', 
        '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.m', '.sql'
    }
    
    # UI settings
    DEFAULT_LANGUAGE = "python"
    SUPPORTED_LANGUAGES = [
        "python", "javascript", "typescript", "java", "cpp", "c", "csharp",
        "php", "ruby", "go", "rust", "swift", "kotlin", "scala", "r", "matlab", "sql"
    ]
    
    # Analysis categories
    ANALYSIS_CATEGORIES = [
        "bug", "best_practice", "performance", "style", "security"
    ]
    
    # Severity levels
    SEVERITY_LEVELS = [
        "critical", "high", "medium", "low", "info"
    ]

# Global config instance
config = Config() 