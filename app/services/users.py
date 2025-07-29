from fastapi import HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    async def get_user_by_id(self, user_id: str) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.get_active_users(skip, limit)

    async def update_user(self, user_id: str, user_data: dict) -> User:
        user = self.user_repository.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    async def update_user_role(self, user_id: str, new_role: str) -> User:
        user = self.user_repository.update_user(user_id, {"role": new_role})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user 