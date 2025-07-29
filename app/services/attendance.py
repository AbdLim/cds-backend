from datetime import date, datetime
from http.client import HTTPException, status
from sqlmodel import Session
from app.models.attendance import Attendance
from app.repositories.attendance import AttendanceRepository


class AttendanceService:
    def __init__(self, session: Session):
        self.attendance_repository = AttendanceRepository(session)

    def submit_attendance(self, attendance_data: dict) -> dict:
        today = attendance_data.get("attendance_date") or date.today()

        existing = self.attendance_repository.get_attendance_by_date(
            cds_group=attendance_data["cds_group"], target_date=today
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance for this date already exists.",
            )

        attendance = self.attendance_repository.create_attendance(
            attendance=Attendance(
                corper_id=attendance_data.get("corper_id"),
                officer_id=attendance_data.get("officer_id"),
                cds_group=attendance_data.get("cds_group"),
                gps_lat=attendance_data.get("gps_lat"),
                gps_long=attendance_data.get("gps_long"),
                status=attendance_data.get("status", "present"),
                attendance_date=today,
                check_in_time=datetime.utcnow(),
            )
        )
        return {"attendance": attendance}

    def get_corper_attendance(self, corper_id: str) -> list:
        attendance_records = self.attendance_repository.get_attendance_by_corper(
            corper_id=corper_id
        )
        if not attendance_records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No attendance records found for this corper.",
            )
        return attendance_records

    def get_group_attendance_by_date(self, cds_group: str, target_date: date) -> list:
        attendance_records = self.attendance_repository.get_attendance_by_date(
            cds_group=cds_group, target_date=target_date
        )
        if not attendance_records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No attendance records found for this group on the specified date.",
            )
        return attendance_records

    def mark_attendance_status(
        self, attendance_id: str, status: str, remarks: str = None
    ) -> dict:
        updated_attendance = self.attendance_repository.update_attendance_status(
            attendance_id=attendance_id, status=status, remarks=remarks
        )
        if not updated_attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance record not found.",
            )
        return {"attendance": updated_attendance}
