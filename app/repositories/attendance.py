from datetime import date
from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select


from app.models.attendance import Attendance
from app.repositories.base import BaseRepository


class AttendanceRepository(BaseRepository[Attendance]):
    def __init__(self, session: Session):
        super().__init__(session, Attendance)

    def get_attendance_by_corper(self, corper_id: UUID) -> List[Attendance]:
        return self.session.exec(
            select(Attendance).where(Attendance.corper_id == corper_id)
        ).all()

    def get_attendance_by_date(
        self, cds_group: str, target_date: date
    ) -> List[Attendance]:
        return self.session.exec(
            select(Attendance)
            .where(Attendance.cds_group == cds_group)
            .where(Attendance.attendance_date == target_date)
        ).all()

    def create_attendance(self, attendance: Attendance) -> Attendance:
        self.session.add(attendance)
        self.session.commit()
        self.session.refresh(attendance)
        return attendance

    def get_attendance_by_id(self, attendance_id: UUID) -> Optional[Attendance]:
        return self.session.get(Attendance, attendance_id)

    def update_attendance_status(
        self,
        attendance_id: UUID,
        status: str,
        remarks: Optional[str] = None,
    ) -> Optional[Attendance]:
        attendance = self.session.get(Attendance, attendance_id)
        if not attendance:
            return None
        attendance.status = status
        if remarks:
            attendance.remarks = remarks
        self.session.add(attendance)
        self.session.commit()
        self.session.refresh(attendance)
        return attendance
