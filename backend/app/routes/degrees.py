from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Degree
from pydantic import BaseModel

class DegreeModel(BaseModel):
    name: str
    level: str

class DegreeResponse(BaseModel):
    id: int
    name: str   
    level: str

router = APIRouter(
    tags=["Degrees"]
)

db_dependency = Depends(get_db)

@router.get("/degrees")
async def get_degrees(db: Session = db_dependency) -> list[DegreeResponse]:
    """Get all degrees."""
    degrees = db.query(Degree).all()
    if not degrees:
        raise HTTPException(status_code=404, detail="No degrees found")
    return degrees

@router.get("/degrees/{degree_id}")
async def get_degree(degree_id: int, db: Session = db_dependency) -> DegreeResponse:
    """Get a degree by ID."""
    degree = db.query(Degree).filter(Degree.id == degree_id).first()
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")
    return degree

@router.post("/degrees")
async def create_degree(degree: DegreeModel, db: Session = db_dependency) -> DegreeResponse:
    """Create a new degree."""
    db_degree = Degree(
        name=degree.name,
        level=degree.level
    )
    db.add(db_degree)
    db.commit()
    db.refresh(db_degree)
    return db_degree

@router.put("/degrees/{degree_id}")
async def update_degree(degree_id: int, degree: DegreeModel, db: Session = db_dependency) -> DegreeResponse:
    """Update a degree by ID."""
    db_degree = db.query(Degree).filter(Degree.id == degree_id).first()
    if not db_degree:
        raise HTTPException(status_code=404, detail="Degree not found")
    db_degree.name = degree.name
    db_degree.level = degree.level
    db.commit()
    db.refresh(db_degree)
    return db_degree

@router.delete("/degrees/{degree_id}")
async def delete_degree(degree_id: int, db: Session = db_dependency) -> DegreeResponse:
    """Delete a degree by ID."""
    db_degree = db.query(Degree).filter(Degree.id == degree_id).first()
    if not db_degree:
        raise HTTPException(status_code=404, detail="Degree not found")
    db.delete(db_degree)
    db.commit()
    return db_degree