from typing import Any, Optional, List
import json
from redis import Redis
from redis.exceptions import RedisError

from app.config import settings


class RedisClient:
    def __init__(self):
        self._client: Optional[Redis] = None

    @property
    def client(self) -> Redis:
        """Get Redis client instance."""
        if self._client is None:
            self._client = Redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
        return self._client

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key-value pair in Redis."""
        try:
            if not isinstance(value, (str, int, float)):
                value = json.dumps(value)
            return self.client.set(key, value, ex=expire)
        except RedisError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from Redis."""
        try:
            value = self.client.get(key)
            if value is None:
                return default
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except RedisError:
            return default

    def delete(self, key: str) -> bool:
        """Delete a key from Redis."""
        try:
            return bool(self.client.delete(key))
        except RedisError:
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        try:
            return bool(self.client.exists(key))
        except RedisError:
            return False

    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a counter in Redis."""
        try:
            return self.client.incr(key, amount)
        except RedisError:
            return None

    def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key."""
        try:
            return bool(self.client.expire(key, seconds))
        except RedisError:
            return False

    def sadd(self, key: str, *values: Any) -> bool:
        """Add one or more members to a set."""
        try:
            return bool(self.client.sadd(key, *values))
        except RedisError:
            return False

    def srem(self, key: str, *values: Any) -> bool:
        """Remove one or more members from a set."""
        try:
            return bool(self.client.srem(key, *values))
        except RedisError:
            return False

    def smembers(self, key: str) -> List[str]:
        """Get all members of a set."""
        try:
            return list(self.client.smembers(key))
        except RedisError:
            return []

    def close(self) -> None:
        """Close Redis connection."""
        if self._client is not None:
            self._client.close()
            self._client = None


# Create a singleton instance
redis_client = RedisClient()
