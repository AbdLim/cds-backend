from datetime import datetime
from typing import Tuple

from app.core.redis import redis_client
from app.config import settings

class RateLimiter:
    def __init__(self):
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW

    def is_rate_limited(self, key: str) -> Tuple[bool, int]:
        """
        Check if a key is rate limited.
        Returns (is_limited, remaining_attempts)
        """
        current = datetime.utcnow().timestamp()
        window_key = f"rate_limit:{key}:{int(current / self.window_seconds)}"
        
        # Get current count
        count = redis_client.increment(window_key, 1) or 1
        
        # Set expiration if this is the first request
        if count == 1:
            redis_client.expire(window_key, self.window_seconds)
        
        # Calculate remaining attempts
        remaining = max(0, self.max_requests - count)
        
        return count > self.max_requests, remaining

    def get_remaining_attempts(self, key: str) -> int:
        """Get remaining attempts for a key."""
        current = datetime.utcnow().timestamp()
        window_key = f"rate_limit:{key}:{int(current / self.window_seconds)}"
        
        count = redis_client.get(window_key) or 0
        return max(0, self.max_requests - int(count))

    def reset_attempts(self, key: str) -> None:
        """Reset rate limit attempts for a key."""
        current = datetime.utcnow().timestamp()
        window_key = f"rate_limit:{key}:{int(current / self.window_seconds)}"
        redis_client.delete(window_key)

# Create a singleton instance
rate_limiter = RateLimiter() 