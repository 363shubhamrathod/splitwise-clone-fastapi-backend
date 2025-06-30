from sqlalchemy.orm import Session
import models

def calculate_group_balances(group_id: int, db: Session):
    # Get all members of the group
    members = db.query(models.GroupMember).filter(models.GroupMember.group_id == group_id).all()
    user_ids = [m.user_id for m in members]
    balances = {user_id: 0.0 for user_id in user_ids}

    # Get all expenses in the group
    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).all()
    for expense in expenses:
        # The payer paid the full amount
        balances[expense.paid_by] += expense.amount
        # Each split is what a user owes
        for split in expense.splits:
            balances[split.user_id] -= split.amount
    return balances

def calculate_user_net_balance(user_id: int, db: Session):
    # Get all expenses where user is payer
    paid = db.query(models.Expense).filter(models.Expense.paid_by == user_id).all()
    paid_total = sum(exp.amount for exp in paid)
    # Get all splits where user owes
    splits = db.query(models.ExpenseSplit).filter(models.ExpenseSplit.user_id == user_id).all()
    owed_total = sum(split.amount for split in splits)
    # Net balance: positive means user should collect, negative means user owes
    return paid_total - owed_total 