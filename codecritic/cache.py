"""
Caching system for CodeCritic
"""

import hashlib
import json
import time
from typing import Optional, Dict, Any
from .models import ReviewRequest, ReviewResponse


class CodeCache:
    """Cache for code review results"""
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
    
    def _generate_key(self, request: ReviewRequest) -> str:
        """Generate cache key from request"""
        # Create a hash of the request parameters
        key_data = {
            'code': request.code,
            'language': request.language.value,
            'enable_modular_review': request.enable_modular_review,
            'model': request.model,
            'include_performance_metrics': request.include_performance_metrics,
            'include_security_analysis': request.include_security_analysis
        }
        
        # Add custom prompts if present
        if request.custom_prompts:
            key_data['custom_prompts'] = request.custom_prompts
        
        # Create hash
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, request: ReviewRequest) -> Optional[ReviewResponse]:
        """Get cached result for request"""
        key = self._generate_key(request)
        
        if key in self.cache:
            cached_data = self.cache[key]
            
            # Check if cache is still valid
            if time.time() - cached_data['timestamp'] < self.ttl:
                # Reconstruct ReviewResponse from cached data
                return ReviewResponse(**cached_data['response'])
            else:
                # Remove expired cache entry
                del self.cache[key]
        
        return None
    
    def set(self, request: ReviewRequest, response: ReviewResponse):
        """Cache result for request"""
        key = self._generate_key(request)
        
        # Convert response to dict for caching
        response_dict = response.dict()
        
        self.cache[key] = {
            'response': response_dict,
            'timestamp': time.time()
        }
    
    def clear(self):
        """Clear all cached data"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        valid_entries = 0
        expired_entries = 0
        
        for entry in self.cache.values():
            if current_time - entry['timestamp'] < self.ttl:
                valid_entries += 1
            else:
                expired_entries += 1
        
        return {
            'total_entries': len(self.cache),
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'cache_size_mb': self._estimate_size() / (1024 * 1024)
        }
    
    def _estimate_size(self) -> int:
        """Estimate cache size in bytes"""
        return len(json.dumps(self.cache, default=str).encode())


class PerformanceTracker:
    """Track performance metrics for code reviews"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all metrics"""
        self.start_time = None
        self.end_time = None
        self.api_calls = 0
        self.total_tokens = 0
        self.response_times = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.estimated_costs = 0.0
    
    def start_review(self):
        """Start timing a review"""
        self.start_time = time.time()
    
    def end_review(self):
        """End timing a review"""
        self.end_time = time.time()
    
    def add_api_call(self, tokens_used: int, response_time: float, model: str):
        """Record an API call"""
        self.api_calls += 1
        self.total_tokens += tokens_used
        self.response_times.append(response_time)
        
        # Estimate cost (rough estimates)
        cost_per_1k_tokens = self._get_cost_per_1k_tokens(model)
        self.estimated_costs += (tokens_used / 1000) * cost_per_1k_tokens
    
    def add_cache_hit(self):
        """Record a cache hit"""
        self.cache_hits += 1
    
    def add_cache_miss(self):
        """Record a cache miss"""
        self.cache_misses += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        total_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            'total_tokens_used': self.total_tokens,
            'api_calls_made': self.api_calls,
            'average_response_time': avg_response_time,
            'total_cost_estimate': self.estimated_costs,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'total_time': total_time,
            'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0
        }
    
    def _get_cost_per_1k_tokens(self, model: str) -> float:
        """Get estimated cost per 1k tokens for a model"""
        # Rough cost estimates (these would need to be updated regularly)
        cost_map = {
            'gpt-4': 0.03,  # $0.03 per 1k input tokens
            'gpt-3.5-turbo': 0.0015,  # $0.0015 per 1k input tokens
            'claude-3-sonnet': 0.015,  # $0.015 per 1k input tokens
            'claude-3-haiku': 0.00025,  # $0.00025 per 1k input tokens
        }
        
        # Try to match model name
        for model_name, cost in cost_map.items():
            if model_name in model.lower():
                return cost
        
        # Default cost
        return 0.01


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls_per_minute: int = 60):
        self.max_calls = max_calls_per_minute
        self.calls = []
    
    def can_make_call(self) -> bool:
        """Check if we can make an API call"""
        current_time = time.time()
        
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls if current_time - call_time < 60]
        
        return len(self.calls) < self.max_calls
    
    def record_call(self):
        """Record an API call"""
        self.calls.append(time.time())
    
    def get_wait_time(self) -> float:
        """Get time to wait before next call"""
        if not self.calls:
            return 0
        
        current_time = time.time()
        oldest_call = min(self.calls)
        
        if current_time - oldest_call >= 60:
            return 0
        
        return 60 - (current_time - oldest_call) 