from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from services.user_service import create_user_service

router = APIRouter()

@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db) 