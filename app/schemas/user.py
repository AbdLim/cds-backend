from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    is_active: bool
    role: str
    created_at: datetime
    updated_at: datetime 