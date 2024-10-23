from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.models import Payment
from pydantic import BaseModel
from datetime import datetime

class PaymentModel(BaseModel):
    amount: float
    date: datetime = datetime.now()
    mentor_id: int  

class PaymentResponse(BaseModel):
    id: int
    amount: float
    date: datetime 
    mentor_id: int

router = APIRouter(
    tags=["Payments"]
)

db_dependency = Depends(get_db)

@router.get("/payments")
async def get_payments(db: Session = db_dependency) -> list[PaymentResponse]:
    """Get all payments."""
    payments = db.query(Payment).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found")
    return payments

@router.get("/payments/{payment_id}")
async def get_payment(payment_id: int, db: Session = db_dependency) -> PaymentResponse:
    """Get a payment by ID."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/payments/{mentor_id}")
async def create_payment(payment: PaymentModel, db: Session = db_dependency) -> PaymentResponse:
    """Create a new payment."""
    db_payment = Payment(
        amount=payment.amount,
        date=payment.date,
        user_id=payment.mentor_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment   

@router.put("/payments/{payment_id}")
async def update_payment(payment_id: int, payment: PaymentModel, db: Session = db_dependency) -> PaymentResponse:
    """Update a payment by ID."""
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db_payment.amount = payment.amount
    db_payment.date = payment.date
    db_payment.user_id = payment.mentor_id
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/payments/{payment_id}")
async def delete_payment(payment_id: int, db: Session = db_dependency) -> PaymentResponse:
    """Delete a payment by ID."""
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return db_payment

@router.get("/payments/mentors/{mentor_id}")
async def get_payments_by_mentor(mentor_id: int, db: Session = db_dependency) -> list[PaymentResponse]:
    """Get all payments by mentor ID."""
    payments = db.query(Payment).filter(Payment.mentor_id == mentor_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this mentor")
    return payments

@router.get("/payments/students/{student_id}")
async def get_payments_by_student(student_id: int, db: Session = db_dependency) -> list[PaymentResponse]:
    """Get all payments by student ID."""
    payments = db.query(Payment).filter(Payment.student_id == student_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this student")
    return payments


