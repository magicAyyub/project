from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Course
from pydantic import BaseModel

class CourseModel(BaseModel):
    name: str
    description: str
    duration: int
    degree_id: int  

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    duration: int
    degree_id: int

router = APIRouter(
    tags=["Courses"]
)

db_dependency = Depends(get_db)

@router.get("/courses")
async def get_courses(db: Session = db_dependency) -> list[CourseResponse]:
    """Get all courses."""
    courses = db.query(Course).all()
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses

@router.get("/courses/{course_id}")
async def get_course(course_id: int, db: Session = db_dependency) -> CourseResponse:
    """Get a course by ID."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/courses")
async def create_course(course: CourseModel, db: Session = db_dependency) -> CourseResponse:
    """Create a new course."""
    db_course = Course(
        name=course.name,
        description=course.description,
        duration=course.duration,
        degree_id=course.degree_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.put("/courses/{course_id}")
async def update_course(course_id: int, course: CourseModel, db: Session = db_dependency) -> CourseResponse:
    """Update a course by ID."""
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.name = course.name
    db_course.description = course.description
    db_course.duration = course.duration
    db_course.degree_id = course.degree_id
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: Session = db_dependency) -> CourseResponse:
    """Delete a course by ID."""
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return db_course