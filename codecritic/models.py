"""
Data models for CodeCritic
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FeedbackType(str, Enum):
    """Types of feedback that can be provided"""
    BUG = "bug"
    BEST_PRACTICE = "best_practice"
    PERFORMANCE = "performance"
    STYLE = "style"
    SECURITY = "security"


class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    TYPESCRIPT = "typescript"


class Severity(str, Enum):
    """Severity levels for feedback"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PerformanceMetrics(BaseModel):
    """Performance metrics for code review"""
    total_tokens_used: int = 0
    api_calls_made: int = 0
    average_response_time: float = 0.0
    total_cost_estimate: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    num_functions: int = 0
    num_classes: int = 0
    avg_function_length: float = 0.0
    avg_cyclomatic_complexity: float = 0.0


class SecurityIssue(BaseModel):
    """Security issue found in code"""
    issue_type: str
    description: str
    severity: Severity
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    suggestion: str
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID


class PerformanceIssue(BaseModel):
    """Performance issue found in code"""
    issue_type: str
    description: str
    severity: Severity
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    suggestion: str
    impact_score: float = Field(0.5, ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    """Result of analyzing a single code block"""
    block_name: str
    block_type: str
    issues: List[str]
    suggestions: List[str]
    complexity_score: Optional[float] = None
    security_issues: List[SecurityIssue] = Field(default_factory=list)
    performance_issues: List[PerformanceIssue] = Field(default_factory=list)


class CodeAnalysis(BaseModel):
    """Complete analysis result for a code file"""
    file_path: Optional[str] = None
    language: Language = Language.PYTHON
    total_issues: int = 0
    issues_by_category: Dict[str, int] = Field(default_factory=dict)
    analysis_results: List[AnalysisResult] = Field(default_factory=list)
    security_issues: List[SecurityIssue] = Field(default_factory=list)
    performance_issues: List[PerformanceIssue] = Field(default_factory=list)
    performance_metrics: Optional[PerformanceMetrics] = None
    processing_time: float = 0.0
    model_used: str = ""
    summary: str = ""
    recommendations: List[str] = Field(default_factory=list)


class FeedbackItem(BaseModel):
    """Individual feedback item"""
    type: FeedbackType
    message: str
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    severity: Severity = Severity.MEDIUM
    suggestion: Optional[str] = None
    confidence: float = Field(0.8, ge=0.0, le=1.0)  # Confidence score
    tags: List[str] = Field(default_factory=list)  # Additional tags


class CodeBlock(BaseModel):
    """Represents a parsed code block (function, class, etc.)"""
    name: str
    type: str  # "function", "class", "module", "method"
    code: str
    line_start: int
    line_end: int
    language: Language
    complexity_score: Optional[float] = None  # Cyclomatic complexity
    lines_of_code: int = 0


class ReviewRequest(BaseModel):
    """Request for code review"""
    code: str = Field(..., description="The code to review")
    language: Language = Language.PYTHON
    enable_modular_review: bool = Field(True, description="Enable function-by-function analysis")
    model: Optional[str] = Field(None, description="LLM model to use")
    include_performance_metrics: bool = Field(True, description="Include performance analysis")
    include_security_analysis: bool = Field(True, description="Include security analysis")
    custom_prompts: Optional[Dict[str, str]] = Field(None, description="Custom prompts for specific categories")


class ReviewResponse(BaseModel):
    """Response from code review"""
    feedback: List[FeedbackItem]
    summary: str
    total_issues: int
    processing_time: float
    model_used: str
    modular_analysis: bool
    code_blocks_analyzed: int
    performance_metrics: Optional[PerformanceMetrics] = None
    language_specific_insights: Optional[Dict[str, Any]] = None
    code_complexity: Optional[Dict[str, float]] = None


class Config(BaseModel):
    """Configuration for CodeCritic"""
    api_key: Optional[str] = None
    model: str = "anthropic/claude-3-sonnet-20240229"
    max_tokens: int = 4000
    temperature: float = 0.1
    max_iterations: int = 10
    enable_caching: bool = True
    cache_ttl: int = 3600  # Cache TTL in seconds
    rate_limit_per_minute: int = 60
    enable_cost_tracking: bool = True 