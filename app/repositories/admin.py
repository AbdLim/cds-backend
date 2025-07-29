from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.user import OfficerProfile, User
from app.repositories.base import BaseRepository


class AdminRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def create_officer_account(self, officer_profile: OfficerProfile) -> OfficerProfile:
        return self.create(officer_profile)

    def get_officer_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.exec(
            select(User).where(User.id == user_id, User.role == "officer")
        ).first()

    def get_all_officers(self) -> list[User]:
        return self.session.exec(select(User).where(User.role == "officer")).all()
