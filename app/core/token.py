from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID

from app.core.redis import redis_client
from app.config import settings
from app.utils.auth import create_access_token, create_refresh_token, verify_token

class TokenManager:
    def __init__(self):
        self.expire_seconds = settings.SESSION_EXPIRE_SECONDS

    def create_tokens(self, user_id: UUID) -> Dict[str, str]:
        """Create access and refresh tokens for a user."""
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        
        # Store tokens in Redis
        token_data = {
            "user_id": str(user_id),
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=self.expire_seconds)).isoformat(),
        }
        
        # Store access token
        redis_client.set(
            f"access_token:{access_token}",
            token_data,
            expire=self.expire_seconds
        )
        
        # Store refresh token with longer expiration
        redis_client.set(
            f"refresh_token:{refresh_token}",
            token_data,
            expire=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600  # Convert days to seconds
        )
        
        # Add tokens to user's active tokens
        redis_client.sadd(f"user_tokens:{user_id}", access_token)
        redis_client.sadd(f"user_tokens:{user_id}", refresh_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def validate_token(self, token: str, token_type: str = "access") -> Optional[str]:
        """Validate a token and return the user_id if valid."""
        # First verify the JWT token
        user_id = verify_token(token)
        if not user_id:
            return None
            
        # Then check if token exists in Redis
        token_key = f"{token_type}_token:{token}"
        if not redis_client.exists(token_key):
            return None
            
        return user_id

    def invalidate_token(self, token: str, token_type: str = "access") -> bool:
        """Invalidate a token."""
        token_key = f"{token_type}_token:{token}"
        token_data = redis_client.get(token_key)
        
        if token_data:
            user_id = token_data.get("user_id")
            if user_id:
                redis_client.srem(f"user_tokens:{user_id}", token)
            return redis_client.delete(token_key)
        return False

    def invalidate_user_tokens(self, user_id: UUID) -> bool:
        """Invalidate all tokens for a user."""
        token_key = f"user_tokens:{user_id}"
        tokens = redis_client.smembers(token_key)
        
        if tokens:
            for token in tokens:
                # Try both access and refresh token keys
                redis_client.delete(f"access_token:{token}")
                redis_client.delete(f"refresh_token:{token}")
            return redis_client.delete(token_key)
        return False

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Create a new access token using a refresh token."""
        user_id = self.validate_token(refresh_token, "refresh")
        if not user_id:
            return None
            
        # Create new access token
        access_token = create_access_token(user_id)
        
        # Store new access token
        token_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=self.expire_seconds)).isoformat(),
        }
        
        redis_client.set(
            f"access_token:{access_token}",
            token_data,
            expire=self.expire_seconds
        )
        
        # Add to user's active tokens
        redis_client.sadd(f"user_tokens:{user_id}", access_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

# Create a singleton instance
token_manager = TokenManager() 