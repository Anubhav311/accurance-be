from fastapi import APIRouter
from sqlalchemy import text
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db  # <-- IMPORTANT

router = APIRouter()

@router.get("/")
def health():
    return {"status": "ok"}

@router.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "connected to neon"}
