from sqlalchemy.orm import Session
import models
from services.balance_service import calculate_group_balances

def add_user_to_group(group_id: int, user_id: int, db: Session):
    # Check if already a member
    exists = db.query(models.GroupMember).filter_by(group_id=group_id, user_id=user_id).first()
    if exists:
        return False  # Already a member
    member = models.GroupMember(group_id=group_id, user_id=user_id)
    db.add(member)
    db.commit()
    return True

def remove_user_from_group_if_cleared(group_id: int, user_id: int, db: Session):
    balances = calculate_group_balances(group_id, db)
    if balances.get(user_id, 0) != 0:
        return False  # Cannot remove, balance not cleared
    member = db.query(models.GroupMember).filter_by(group_id=group_id, user_id=user_id).first()
    if member:
        db.delete(member)
        db.commit()
        return True
    return False 