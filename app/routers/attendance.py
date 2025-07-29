from fastapi import APIRouter, Depends
from locust import User
from sqlmodel import Session

from app.core.rbac import require_permission
from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.services.attendance import AttendanceService


router = APIRouter()


@router.get("/me")
async def view_own_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:own_attendance")),
    session: Session = Depends(get_session),
):
    """View own attendance."""
    attendance_service = AttendanceService(session)
    return await attendance_service.get_attendance_by_corper(current_user.id)


@router.get("/group")
async def view_assigned_group_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:assigned_attendance")),
    session: Session = Depends(get_session),
):
    """View CDS group attendance."""
    attendance_service = AttendanceService(session)
    return await attendance_service.get_attendance_by_date(
        cds_group=current_user.cds_group, target_date=current_user.attendance_date
    )


@router.get("/all")
async def view_all_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("read:all_attendance")),
    session: Session = Depends(get_session),
):
    """View all attendance."""
    attendance_service = AttendanceService(session)
    return await attendance_service.get_group_attendance_by_date(
        cds_group=current_user.cds_group, target_date=current_user.attendance_date
    )


@router.post("/mark")
async def view_assigned_group_attendance(
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_permission("mark:attendance")),
    session: Session = Depends(get_session),
):
    """."""
    attendance_service = AttendanceService(session)
    return await attendance_service.mark_attendance_status(
        attendance_id=current_user.attendance_id,
        status=current_user.status,
        remarks=current_user.remarks,
    )
