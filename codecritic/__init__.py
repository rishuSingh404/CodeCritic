"""
CodeCritic - AI-powered code review and analysis tool
"""

from .core import CodeCritic
from .models import ReviewRequest, ReviewResponse, FeedbackItem

__version__ = "1.0.0"
__author__ = "Rishu Singh"

__all__ = ["CodeCritic", "ReviewRequest", "ReviewResponse", "FeedbackItem"] 