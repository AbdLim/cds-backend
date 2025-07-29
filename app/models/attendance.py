from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date


class Attendance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    corper_id: UUID = Field(foreign_key="user.id")
    officer_id: UUID = Field(
        foreign_key="user.id"
    )  # could be officer or general secretary
    cds_group: str  # Stored as textfor now. could normalize

    attendance_date: date = Field(default_factory=lambda: datetime.utcnow().date())

    check_in_time: datetime
    check_out_time: Optional[datetime] = None

    gps_lat: Optional[float] = None
    gps_long: Optional[float] = None

    status: str = Field(default="present")  # present, absent, late, excused
    remarks: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    corper: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Attendance.corper_id]"}
    )
    officer: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Attendance.officer_id]"}
    )
