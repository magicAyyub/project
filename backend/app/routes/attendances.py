from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Attendance
from pydantic import BaseModel
from datetime import date
class AttendanceModel(BaseModel):
    student_id: int
    course_id: int
    date: date

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    date: date

router = APIRouter(
    tags=["Attendances"]
)

db_dependency = Depends(get_db)

@router.get("/attendances")
async def get_attendances(db: Session = db_dependency) -> list[AttendanceResponse]:
    """Get all attendances."""
    attendances = db.query(Attendance).all()
    if not attendances:
        raise HTTPException(status_code=404, detail="No attendances found")
    return attendances

@router.get("/attendances/{attendance_id}")
async def get_attendance(attendance_id: int, db: Session = db_dependency) -> AttendanceResponse:
    """Get an attendance by ID."""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.post("/attendances")
async def create_attendance(attendance: AttendanceModel, db: Session = db_dependency) -> AttendanceResponse:
    """Create a new attendance."""
    db_attendance = Attendance(
        student_id=attendance.student_id,
        course_id=attendance.course_id,
        date=attendance.date
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.put("/attendances/{attendance_id}")
async def update_attendance(attendance_id: int, attendance: AttendanceModel, db: Session = db_dependency) -> AttendanceResponse:
    """Update an attendance by ID."""
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db_attendance.student_id = attendance.student_id
    db_attendance.course_id = attendance.course_id
    db_attendance.date = attendance.date
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.delete("/attendances/{attendance_id}")
async def delete_attendance(attendance_id: int, db: Session = db_dependency) -> AttendanceResponse:
    """Delete an attendance by ID."""
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    db.delete(db_attendance)
    db.commit()
    return db_attendance

