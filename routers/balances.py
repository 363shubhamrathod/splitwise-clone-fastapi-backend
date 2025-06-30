from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.balance_service import calculate_group_balances
import models

router = APIRouter()

@router.get("/groups/{group_id}/balances")
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    balances = calculate_group_balances(group_id, db)
    # Optionally, return user names as well
    users = db.query(models.User).filter(models.User.id.in_(balances.keys())).all()
    user_map = {user.id: user.name for user in users}
    return [
        {"user_id": user_id, "user_name": user_map.get(user_id, "Unknown"), "balance": balance}
        for user_id, balance in balances.items()
    ]
