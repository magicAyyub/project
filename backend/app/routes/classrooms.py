from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Classroom, Student
from pydantic import BaseModel

class ClassroomModel(BaseModel):
    name: str
    degree_id: int
    capacity: int
    day: str
    time_slot: str

class ClassroomResponse(BaseModel):
    id: int
    name: str
    degree_id: int
    capacity: int
    day: str
    time_slot: str

router = APIRouter(
    tags=["Classrooms"]
)

db_dependency = Depends(get_db)

@router.get("/classrooms")
async def get_classrooms(db: Session = db_dependency) -> list[ClassroomResponse]:
    """Get all classrooms."""
    classrooms = db.query(Classroom).all()
    if not classrooms:
        raise HTTPException(status_code=404, detail="No classrooms found")
    return classrooms

@router.get("/classrooms/{classroom_id}")
async def get_classroom(classroom_id: int, db: Session = db_dependency) -> ClassroomResponse:
    """Get a classroom by ID."""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom

@router.post("/classrooms")
async def create_classroom(classroom: ClassroomModel, db: Session = db_dependency) -> ClassroomResponse:
    """Create a new classroom."""
    db_classroom = Classroom(
        name=classroom.name,
        degree_id=classroom.degree_id,
        capacity=classroom.capacity,
        day=classroom.day,
        time_slot=classroom.time_slot
    )
    db.add(db_classroom)
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.put("/classrooms/{classroom_id}")
async def update_classroom(classroom_id: int, classroom: ClassroomModel, db: Session = db_dependency) -> ClassroomResponse:
    """Update a classroom by ID."""
    db_classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db_classroom.name = classroom.name
    db_classroom.degree_id = classroom.degree_id
    db_classroom.capacity = classroom.capacity
    db_classroom.day = classroom.day
    db_classroom.time_slot = classroom.time_slot
    db.commit()
    db.refresh(db_classroom)
    return db_classroom

@router.delete("/classrooms/{classroom_id}")
async def delete_classroom(classroom_id: int, db: Session = db_dependency) -> ClassroomResponse:
    """Delete a classroom by ID."""
    db_classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    db.delete(db_classroom)
    db.commit()
    return db_classroom

@router.get("/classrooms/{classroom_id}/places")
async def get_places_available_in_classroom(classroom_id: int, db: Session = db_dependency) -> int:
    """Get the number of places available in a classroom."""
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    students = db.query(Student).filter(Student.classroom_id== classroom_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this classroom")
    return classroom.capacity - len(students)