"""
This module contains the FastAPI application and its configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from utils.database import engine
# import utils.models as models
# from app.routes import students, mentors, degrees, classrooms, courses, attendances, payments
from utils.settings import ORIGINS


# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include all routes



# Root endpoint to verify API connection
@app.get("/")
async def root() -> dict[str, str]:
    """Basic root endpoint to verify API connection."""
    return {"Connexion": "ok"}

