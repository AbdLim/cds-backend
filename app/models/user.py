from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


# Base user model
class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    role: str = Field(
        default="corper"
    )  # corper, officer, general_secretary, super_admin


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # One-to-one relationships
    corper_profile: Optional["CorperProfile"] = Relationship(back_populates="user")
    officer_profile: Optional["OfficerProfile"] = Relationship(back_populates="user")


class OfficerProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True)

    designation: str  # e.g. LGI, ZI, CDS Coordinator
    phone_number: Optional[str] = None
    zone: Optional[str] = None  # Area/Zone Assigned
    username: Optional[str] = None

    user: "User" = Relationship(back_populates="officer_profile")


class CorperProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True)

    call_up_number: str
    state_code: str
    batch: str
    stream: str
    gender: str
    passport_url: Optional[str] = None
    lga_primary_assignment: str
    cds_group: str
    zone: str  # LGI Zone or CDS Cluster
    cds_day: str  # e.g. Tuesday
    current_status: str = Field(default="active")  # active, relocated, exited
    date_of_registration: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="corper_profile")
