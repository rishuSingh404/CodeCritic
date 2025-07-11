"""
Core CodeCritic functionality
"""

import os
import time
import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from collections import defaultdict, deque
import anthropic
import openai
from .models import CodeAnalysis, AnalysisResult, PerformanceMetrics, SecurityIssue, PerformanceIssue, Language, CodeBlock
from .parser import CodeParser
from .prompts import PromptTemplates
from .config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, max_calls_per_minute: int = 10, max_calls_per_hour: int = 100):
        self.max_calls_per_minute = max_calls_per_minute
        self.max_calls_per_hour = max_calls_per_hour
        self.minute_calls = deque()
        self.hour_calls = deque()
    
    def can_make_call(self) -> bool:
        now = time.time()
        
        # Clean old minute calls
        while self.minute_calls and now - self.minute_calls[0] > 60:
            self.minute_calls.popleft()
        
        # Clean old hour calls
        while self.hour_calls and now - self.hour_calls[0] > 3600:
            self.hour_calls.popleft()
        
        # Check limits
        if len(self.minute_calls) >= self.max_calls_per_minute:
            return False
        if len(self.hour_calls) >= self.max_calls_per_hour:
            return False
        
        return True
    
    def record_call(self):
        now = time.time()
        self.minute_calls.append(now)
        self.hour_calls.append(now)

class Cache:
    """Simple in-memory cache for analysis results"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        self.ttl = ttl
        self.max_size = max_size
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key: str) -> Optional[Dict]:
        if key in self.cache:
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key: str, value: Dict):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = time.time()

class PerformanceTracker:
    """Track performance metrics"""
    
    def __init__(self, log_file: str = "codecritic_performance.log"):
        self.log_file = log_file
        self.metrics = defaultdict(list)
    
    def record_metric(self, metric_type: str, value: float, metadata: Dict = None):
        metric = {
            'timestamp': datetime.now().isoformat(),
            'type': metric_type,
            'value': value,
            'metadata': metadata or {}
        }
        self.metrics[metric_type].append(metric)
        
        # Log to file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(metric) + '\n')
    
    def get_average_metric(self, metric_type: str) -> float:
        if not self.metrics[metric_type]:
            return 0.0
        return sum(m['value'] for m in self.metrics[metric_type]) / len(self.metrics[metric_type])

class CodeCritic:
    """Main CodeCritic class for AI-powered code analysis"""
    
    def __init__(self, model: str = None, temperature: float = None, max_tokens: int = None):
        self.model = model or config.DEFAULT_MODEL
        self.temperature = temperature or config.DEFAULT_TEMPERATURE
        self.max_tokens = max_tokens or config.DEFAULT_MAX_TOKENS
        
        # Initialize API clients
        self.openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        self.anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        
        # Initialize components
        self.parser = CodeParser()
        self.prompts = PromptTemplates()
        self.rate_limiter = RateLimiter(
            config.RATE_LIMIT_PER_MINUTE,
            config.RATE_LIMIT_PER_HOUR
        )
        self.cache = Cache(config.CACHE_TTL, config.CACHE_MAX_SIZE)
        self.performance_tracker = PerformanceTracker(config.PERFORMANCE_LOG_FILE)
        
        # Performance tracking
        if config.ENABLE_PERFORMANCE_TRACKING:
            self.performance_tracker.record_metric('initialization', time.time())
    
    def _get_cache_key(self, code: str, language: str, categories: List[str]) -> str:
        """Generate cache key for analysis"""
        content = f"{code}:{language}:{':'.join(sorted(categories))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _call_llm(self, prompt: str, model: str = None) -> str:
        """Make API call to LLM with rate limiting"""
        if not self.rate_limiter.can_make_call():
            raise Exception("Rate limit exceeded. Please try again later.")
        
        start_time = time.time()
        
        try:
            model_to_use = model or self.model
            if "gpt" in model_to_use:
                response = self.openai_client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                result = response.choices[0].message.content
            else:
                # Use Anthropic Claude as default
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.content[0].text
            
            self.rate_limiter.record_call()
            
            # Track performance
            if config.ENABLE_PERFORMANCE_TRACKING:
                duration = time.time() - start_time
                self.performance_tracker.record_metric('api_call_duration', duration, {
                    'model': model_to_use,
                    'prompt_length': len(prompt)
                })
            
            return result
            
        except Exception as e:
            logger.error(f"API call failed: {e}")
            raise
    
    def analyze_code(self, code: str, language: str = "python", 
                    categories: Optional[List[str]] = None, custom_prompt: Optional[str] = None) -> CodeAnalysis:
        """Analyze code and return comprehensive results"""
        
        if categories is None:
            categories = config.ANALYSIS_CATEGORIES
        
        # Check cache first
        cache_key = self._get_cache_key(code, language, categories)
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return CodeAnalysis(**cached_result)
        
        start_time = time.time()
        
        try:
            # Parse code
            language_enum = Language(language)
            parsed_code = self.parser.parse_code(code, language_enum)
            
            # Generate analysis
            analysis_results = []
            
            for block in parsed_code:
                prompt = self.prompts.get_review_prompt(block.code, language_enum, modular=True, block_name=block.name)
                
                try:
                    analysis_text = self._call_llm(prompt, self.model)
                    # This part needs to be updated to parse the structured response from the new prompts
                    # For now, we'll just put the whole text in a single category
                    result = AnalysisResult(
                        block_name=block.name,
                        block_type=block.type,
                        issues=[analysis_text],
                        suggestions=[]
                    )
                    analysis_results.append(result)
                except Exception as e:
                    logger.error(f"Analysis failed for block {block.name}: {e}")
                    analysis_results.append(AnalysisResult(
                        block_name=block.name,
                        block_type=block.type,
                        issues=[f"Analysis failed: {str(e)}"],
                        suggestions=[]
                    ))
            
            # Generate performance metrics
            performance_metrics = self._calculate_performance_metrics(parsed_code, language_enum)
            
            # Create analysis object
            analysis = CodeAnalysis(
                language=language_enum,
                analysis_results=analysis_results,
                performance_metrics=performance_metrics,
                model_used=self.model,
                processing_time=time.time() - start_time
            )
            
            # Cache result
            self.cache.set(cache_key, analysis.model_dump())
            
            # Track performance
            if config.ENABLE_PERFORMANCE_TRACKING:
                duration = time.time() - start_time
                self.performance_tracker.record_metric('analysis_duration', duration, {
                    'language': language,
                    'categories': categories,
                    'code_length': len(code)
                })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            raise
    
    def _extract_severity(self, analysis_text: str) -> str:
        """Extract severity from analysis text"""
        text_lower = analysis_text.lower()
        if any(word in text_lower for word in ['critical', 'severe', 'fatal']):
            return 'critical'
        elif any(word in text_lower for word in ['high', 'major', 'important']):
            return 'high'
        elif any(word in text_lower for word in ['medium', 'moderate']):
            return 'medium'
        elif any(word in text_lower for word in ['low', 'minor']):
            return 'low'
        else:
            return 'info'
    
    def _extract_confidence(self, analysis_text: str) -> float:
        """Extract confidence score from analysis text"""
        # Simple heuristic - could be improved with more sophisticated parsing
        text_lower = analysis_text.lower()
        if any(word in text_lower for word in ['definitely', 'certainly', 'clear']):
            return 0.9
        elif any(word in text_lower for word in ['likely', 'probably', 'suggest']):
            return 0.7
        elif any(word in text_lower for word in ['maybe', 'possibly', 'could']):
            return 0.5
        else:
            return 0.6
    
    def _calculate_performance_metrics(self, parsed_code: List[CodeBlock], language: Language) -> PerformanceMetrics:
        """Calculate performance metrics for the code"""
        metrics = PerformanceMetrics()
        
        functions = [block for block in parsed_code if block.type == 'function']
        classes = [block for block in parsed_code if block.type == 'class']
        
        metrics.num_functions = len(functions)
        metrics.num_classes = len(classes)
        
        if metrics.num_functions > 0:
            total_func_length = sum(f.lines_of_code for f in functions)
            metrics.avg_function_length = total_func_length / metrics.num_functions
            
            total_complexity = sum(f.complexity_score for f in functions if f.complexity_score is not None)
            metrics.avg_cyclomatic_complexity = total_complexity / metrics.num_functions
        
        return metrics
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        return {
            'avg_api_call_duration': self.performance_tracker.get_average_metric('api_call_duration'),
            'avg_analysis_duration': self.performance_tracker.get_average_metric('analysis_duration'),
            'cache_hit_rate': len(self.cache.cache) / max(self.cache.max_size, 1) if self.cache.max_size > 0 else 0
        }
    
    def clear_cache(self):
        """Clear the analysis cache"""
        self.cache.cache.clear()
        self.cache.timestamps.clear()
    
    def reset_rate_limits(self):
        """Reset rate limiting counters"""
        self.rate_limiter.minute_calls.clear()
        self.rate_limiter.hour_calls.clear() 