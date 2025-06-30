from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from services.user_service import create_user_service
from services.balance_service import calculate_user_net_balance

router = APIRouter()

@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)

@router.get("/users/{user_id}/net-balance")
def get_user_net_balance(user_id: int, db: Session = Depends(get_db)):
    net_balance = calculate_user_net_balance(user_id, db)
    return {"user_id": user_id, "net_balance": net_balance} 