from typing import List
from fastapi import HTTPException, status
from app.models.user import OfficerProfile
from app.repositories.admin import AdminRepository
from sqlmodel import Session
from app.utils.auth import get_password_hash

from app.repositories.user import UserRepository


class AdminService:
    def __init__(self, session: Session):
        self.admin_repository = AdminRepository(session)
        self.user_repository = UserRepository(Session)

    def create_officer(self, data: dict) -> dict:
        user = self.user_repository.create_user(
            email=data["email"],
            hashed_password=get_password_hash(data["password"] or "password123"),
            full_name=data.get("full_name"),
            role="officer",
            address=data.get("address"),
            phone=data.get("phone"),
        )

        officer_profile = self.admin_repository.create_officer_account(
            officer_profile=OfficerProfile(
                user_id=user.id,
                rank=data.get("rank"),
                badge_number=data.get("badge_number"),
            )
        )
        return {"user": user, "officer_profile": officer_profile}

    def get_officer_by_id(self, officer_id: str) -> OfficerProfile:
        officer = self.admin_repository.get_officer_by_id(officer_id)
        if not officer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found"
            )
        return officer

    def get_all_officers(self) -> List[OfficerProfile]:
        officers = self.admin_repository.get_all_officers()
        return officers
