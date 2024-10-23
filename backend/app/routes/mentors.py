from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Mentor
from pydantic import BaseModel

class MentorModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str      

class MentorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str

router = APIRouter(
    tags=["Mentors"]
)

db_dependency = Depends(get_db)

@router.get("/mentors")
async def get_mentors(db: Session = db_dependency) -> list[MentorResponse]:
    """Get all mentors."""
    mentors = db.query(Mentor).all()
    if not mentors:
        raise HTTPException(status_code=404, detail="No mentors found")
    return mentors

@router.get("/mentors/{mentor_id}")
async def get_mentor(mentor_id: int, db: Session = db_dependency) -> MentorResponse:
    """Get a mentor by ID."""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor

@router.post("/mentors")
async def create_mentor(mentor: MentorModel, db: Session = db_dependency) -> MentorResponse:
    """Create a new mentor."""
    db_mentor = Mentor(
        first_name=mentor.first_name,
        last_name=mentor.last_name,
        email=mentor.email,
        phone=mentor.phone
    )
    db.add(db_mentor)
    db.commit()
    db.refresh(db_mentor)
    return db_mentor

@router.put("/mentors/{mentor_id}")
async def update_mentor(mentor_id: int, mentor: MentorModel, db: Session = db_dependency) -> MentorResponse:
    """Update a mentor by ID."""
    db_mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not db_mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    db_mentor.first_name = mentor.first_name
    db_mentor.last_name = mentor.last_name
    db_mentor.email = mentor.email
    db_mentor.phone = mentor.phone
    db.commit()
    db.refresh(db_mentor)
    return db_mentor

@router.delete("/mentors/{mentor_id}")
async def delete_mentor(mentor_id: int, db: Session = db_dependency) -> MentorResponse:
    """Delete a mentor by ID."""
    db_mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not db_mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    db.delete(db_mentor)
    db.commit()
    return db_mentor