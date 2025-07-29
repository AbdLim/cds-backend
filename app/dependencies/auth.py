from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from uuid import UUID

from app.config.database import get_session
from app.config import logger
from app.models.user import User
from app.repositories.user import UserRepository
from app.core.token import token_manager
from app.core.rate_limiter import rate_limiter


security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    logger.info("Starting get_current_user_id")
    token = credentials.credentials
    logger.info(f"Verifying token: {token[:10]}...")
    
    user_id = token_manager.validate_token(token)
    if not user_id:
        logger.error("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = UUID(user_id)
        logger.info(f"Token verified successfully for user_id: {user_id}")
        return user_id
    except ValueError:
        logger.error(f"Invalid UUID format: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> User:
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
        
    return user


async def get_current_user_role(
    user: User = Depends(get_current_user),
) -> str:
    logger.info(f"Getting role for user: {user.email}")
    return user.role


async def require_active_session(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Require an active session for the endpoint."""
    if not current_user.get("session", {}).get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is not active"
        )
    return current_user


def rate_limit_auth_attempts(identifier: str):
    """Rate limit authentication attempts for an identifier (e.g., IP or username)."""
    is_limited, remaining = rate_limiter.is_rate_limited(f"auth_attempts:{identifier}")
    if is_limited:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many authentication attempts. Try again in {remaining} seconds."
        ) 