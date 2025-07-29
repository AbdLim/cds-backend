from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from app.models.user import OfficerProfile, User
from app.repositories.base import BaseRepository


class AdminRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def create_officer_account(
        session: Session, user: User, officer_profile: OfficerProfile
    ) -> User:
        session.add(user)
        session.flush()  # gets the user.id

        officer_profile.user_id = user.id
        session.add(officer_profile)

        session.commit()
        session.refresh(user)
        return user

    def get_officer_by_id(session: Session, user_id: UUID) -> Optional[User]:
        return session.exec(
            select(User).where(User.id == user_id, User.role == "officer")
        ).first()

    def get_all_officers(session: Session) -> list[User]:
        return session.exec(select(User).where(User.role == "officer")).all()
