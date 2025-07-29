from fastapi import APIRouter, Depends, HTTPException, status
from locust import User
from sqlmodel import Session

from app.core.rbac import require_permission
from app.db.session import get_session
from app.dependencies.auth import get_current_user


router = APIRouter()


@router.get("/me")
async def view_own_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:own_attendance")),
    session: Session = Depends(get_session),
):
    """View own attendance."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )


@router.get("/group")
async def view_assigned_group_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:assigned_attendance")),
    session: Session = Depends(get_session),
):
    """View CDS group attendance."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )


@router.get("/all")
async def view_all_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:all_attendance")),
    session: Session = Depends(get_session),
):
    """View all attendance."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )


@router.post("/mark")
async def view_assigned_group_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("mark:attendance")),
    session: Session = Depends(get_session),
):
    """."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )
