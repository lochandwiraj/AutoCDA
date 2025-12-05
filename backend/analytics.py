"""
Analytics module to track and showcase project metrics for bonus submissions.
"""

import time
from functools import wraps
from typing import Callable, Any
import json
from pathlib import Path

class PerformanceMetrics:
    """Track performance metrics for technical complexity bonus."""
    
    def __init__(self):
        self.metrics = {
            "generation_times": [],
            "pipeline_stages": {},
            "cache_hits": 0,
            "total_requests": 0
        }
    
    def timing_decorator(self, stage_name: str):
        """Decorator to measure execution time of pipeline stages."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                
                if stage_name not in self.metrics["pipeline_stages"]:
                    self.metrics["pipeline_stages"][stage_name] = []
                
                self.metrics["pipeline_stages"][stage_name].append({
                    "duration_ms": round(duration * 1000, 2),
                    "timestamp": time.time()
                })
                
                return result
            return wrapper
        return decorator
    
    def record_generation(self, total_time: float):
        """Record total circuit generation time."""
        self.metrics["generation_times"].append(round(total_time * 1000, 2))
        self.metrics["total_requests"] += 1
    
    def record_cache_hit(self):
        """Record cache hit for performance optimization."""
        self.metrics["cache_hits"] += 1
    
    def get_statistics(self) -> dict:
        """Calculate performance statistics."""
        if not self.metrics["generation_times"]:
            return {"error": "No data collected yet"}
        
        times = self.metrics["generation_times"]
        return {
            "total_requests": self.metrics["total_requests"],
            "cache_hit_rate": round(self.metrics["cache_hits"] / max(self.metrics["total_requests"], 1) * 100, 2),
            "avg_generation_time_ms": round(sum(times) / len(times), 2),
            "min_generation_time_ms": min(times),
            "max_generation_time_ms": max(times),
            "p95_generation_time_ms": round(sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0], 2),
            "pipeline_breakdown": {
                stage: {
                    "avg_ms": round(sum(t["duration_ms"] for t in timings) / len(timings), 2),
                    "count": len(timings)
                }
                for stage, timings in self.metrics["pipeline_stages"].items()
            }
        }
    
    def save_metrics(self, filepath: str = "performance_metrics.json"):
        """Save metrics to file for bonus submission."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                "raw_metrics": self.metrics,
                "statistics": self.get_statistics()
            }, f, indent=2)

# Global metrics instance
metrics = PerformanceMetrics()
