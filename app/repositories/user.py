from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select, and_, or_
from sqlalchemy import func

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        statement = (
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def search_users(self, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        search_term = f"%{query}%"
        statement = (
            select(User)
            .where(
                and_(
                    User.is_active == True,
                    or_(
                        User.email.ilike(search_term),
                        User.full_name.ilike(search_term)
                    )
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_active_user_count(self) -> int:
        statement = select(func.count()).select_from(User).where(User.is_active == True)
        return self.session.exec(statement).first()

    def get_by_id(self, id: UUID) -> Optional[User]:
        return super().get_by_id(id)

    def create_user(self, email: str, hashed_password: str, role: str, address: str, phone: str, full_name: Optional[str] = None) -> User:
        user = User(
            email=email,
            password=hashed_password,
            full_name=full_name,
            role=role,
            address=address,
            phone=phone,
        )
        return self.create(user)

    def update_user(self, id: UUID, user_data: dict) -> Optional[User]:
        return self.update(id, user_data) 