from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

@router.post("/groups/{group_id}/expenses", response_model=schemas.Expense)
def add_expense(group_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        paid_by=expense.paid_by,
        split_type=expense.split_type,
        group_id=group_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    if expense.split_type == schemas.SplitTypeEnum.equal:
        members = db.query(models.GroupMember).filter(models.GroupMember.group_id == group_id).all()
        split_amount = expense.amount / len(members)
        for member in members:
            split = models.ExpenseSplit(expense_id=db_expense.id, user_id=member.user_id, amount=split_amount)
            db.add(split)
    elif expense.split_type == schemas.SplitTypeEnum.percentage:
        for split in expense.splits:
            split_amount = expense.amount * (split['percentage'] / 100)
            new_split = models.ExpenseSplit(expense_id=db_expense.id, user_id=split['user_id'], amount=split_amount)
            db.add(new_split)
    db.commit()
    return db_expense
