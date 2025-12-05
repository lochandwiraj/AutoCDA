"""
Performance monitoring and optimization utilities
"""

import time
import functools
import hashlib
from typing import Callable, Any

# Simple in-memory cache
_cache = {}

def measure_performance(name: str):
    """Decorator to measure function execution time"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[Performance] {name}: {(end - start) * 1000:.2f}ms")
            return result
        return wrapper
    return decorator

def cache_result(ttl: int = 300):
    """
    Cache function results with TTL (time to live) in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from function name and arguments
            key_data = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Check cache
            if cache_key in _cache:
                cached_value, cached_time = _cache[cache_key]
                if time.time() - cached_time < ttl:
                    print(f"[Cache Hit] {func.__name__}")
                    return cached_value
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            _cache[cache_key] = (result, time.time())
            return result
        return wrapper
    return decorator

def debounce(wait: float):
    """
    Debounce function calls
    """
    def decorator(func: Callable) -> Callable:
        last_call = [0]
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_time = time.time()
            if current_time - last_call[0] >= wait:
                last_call[0] = current_time
                return func(*args, **kwargs)
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached results"""
    global _cache
    _cache = {}
    print("[Cache] Cleared all cached results")

def get_cache_stats():
    """Get cache statistics"""
    return {
        'size': len(_cache),
        'keys': list(_cache.keys())[:10]  # First 10 keys
    }
