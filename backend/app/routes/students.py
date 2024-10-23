from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Student
from pydantic import BaseModel
from datetime import date

class StudentModel(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    degree_id: int
    classroom_id: int
    mentor_id: int
    state: str

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    degree_id: int
    classroom_id: int
    mentor_id: int
    state: str

router = APIRouter(
    tags=["Students"]
)

db_dependency = Depends(get_db)

@router.get("/students")
async def get_students(db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students."""
    students = db.query(Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

@router.get("/students/{student_id}")
async def get_student(student_id: int, db: Session = db_dependency) -> StudentResponse:
    """Get a student by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/students")
async def create_student(student: StudentModel, db: Session = db_dependency) -> StudentResponse:
    """Create a new student."""
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        birth_date=student.birth_date,
        degree_id=student.degree_id,
        classroom_id=student.classroom_id,
        mentor_id=student.mentor_id,
        state=student.state
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.put("/students/{student_id}")
async def update_student(student_id: int, student: StudentModel, db: Session = db_dependency) -> StudentResponse:
    """Update a student by ID."""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.first_name = student.first_name
    db_student.last_name = student.last_name
    db_student.birth_date = student.birth_date
    db_student.degree_id = student.degree_id
    db_student.classroom_id = student.classroom_id
    db_student.mentor_id = student.mentor_id
    db_student.state = student.state
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = db_dependency) -> StudentResponse:
    """Delete a student by ID."""
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return db_student

@router.get("/students/degree/{degree_id}")
async def get_students_by_degree(degree_id: int, db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students by degree."""
    students = db.query(Student).filter(Student.degree_id == degree_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this degree")
    return students

@router.get("/students/classroom/{classroom_id}")
async def get_students_by_classroom(classroom_id: int, db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students by classroom."""
    students = db.query(Student).filter(Student.classroom_id == classroom_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this classroom")
    return students

@router.get("/students/mentor/{mentor_id}")
async def get_students_by_mentor(mentor_id: int, db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students by mentor."""
    students = db.query(Student).filter(Student.mentor_id == mentor_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this mentor")
    return students

@router.get("/students/state/{state}")
async def get_students_by_state(state: str, db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students by state."""
    students = db.query(Student).filter(Student.state == state).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this state")
    return students

@router.get("/students/filter")
async def filter_students_by_criteria(degree_id: int = None, classroom_id: int = None, mentor_id: int = None, state: str = None, db: Session = db_dependency) -> list[StudentResponse]:
    """Get all students by criteria."""
    students = db.query(Student)
    if degree_id is not None:
        students = students.filter(Student.degree_id == degree_id)
    if classroom_id is not None:
        students = students.filter(Student.classroom_id == classroom_id)
    if mentor_id is not None:
        students = students.filter(Student.mentor_id == mentor_id)
    if state is not None:
        students = students.filter(Student.state == state)
    students = students.all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for these criteria")
    return students

@router.get("/students/search")
async def search_students(query: str, db: Session = db_dependency) -> list[StudentResponse]:
    """Search students by query."""
    students = db.query(Student).filter(Student.first_name.ilike(f"%{query}%") | Student.last_name.ilike(f"%{query}%")).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this query")
    return students 