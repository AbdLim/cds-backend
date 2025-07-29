from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.config.database import get_session
from app.core.rbac import require_permission
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.users import UserService


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:own_profile")),
):
    """Get current user's profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("update:own_profile")),
    session: Session = Depends(get_session),
):
    """Update current user's profile."""
    user_service = UserService(session)
    return await user_service.update_user(
        current_user.id, user_data.model_dump(exclude_unset=True)
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    _: bool = Depends(require_permission("read:all_profiles")),
    session: Session = Depends(get_session),
):
    """List all users (requires read:all_profiles permission)."""
    user_service = UserService(session)
    return await user_service.get_all_users(skip, limit)


@router.get("/assigned")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    _: bool = Depends(require_permission("read:assigned_corper")),
    session: Session = Depends(get_session),
):
    # throw unimplemented error
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    _: bool = Depends(require_permission("read:all_profiles")),
    session: Session = Depends(get_session),
):
    """Get a specific user's profile (requires read:all_profiles permission)."""
    user_service = UserService(session)
    return await user_service.get_user_by_id(user_id)
