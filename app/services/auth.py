from fastapi import HTTPException, status
from sqlmodel import Session
from uuid import UUID

from app.repositories.user import UserRepository
from app.utils.auth import get_password_hash, verify_password
from app.core.token import token_manager


class AuthService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    async def authenticate_user(self, email: str, password: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        token = token_manager.create_tokens(user.id)
        token['user'] = user
        return token

    async def register_user(self, user_data: dict) -> dict:
        # Check if user exists
        if self.user_repository.get_by_email(user_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        user = self.user_repository.create_user(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data.get("full_name"),
            role=user_data.get("role"),
            address=user_data.get("address"),
            phone=user_data.get("phone"),
        )

        token = token_manager.create_tokens(user.id)
        token['user'] = user
        return token

    async def refresh_token(self, refresh_token: str) -> dict:
        result = token_manager.refresh_access_token(refresh_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        return result

    async def logout(self, token: str) -> dict:
        # Invalidate the access token
        if not token_manager.invalidate_token(token, "access"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )
        return {"message": "Successfully logged out"} 

    async def logout_all(self, user_id: UUID) -> dict:
        # Invalidate all tokens for the user
        if not token_manager.invalidate_user_tokens(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to invalidate tokens",
            )
        return {"message": "Successfully logged out from all devices"} 