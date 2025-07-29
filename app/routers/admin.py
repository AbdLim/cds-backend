from fastapi import APIRouter, Depends, HTTPException, status
from locust import User
from sqlmodel import Session

from app.core.rbac import require_permission
from app.db.session import get_session
from app.dependencies.auth import get_current_user


router = APIRouter()


@router.post("/officers")
async def create_officer(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("create:officer")),
    session: Session = Depends(get_session),
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )


@router.post("/assign-secretary")
async def assign_secretary(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("assign:general_secretary")),
    session: Session = Depends(get_session),
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This endpoint is not implemented yet.",
    )
