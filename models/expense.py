from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class SplitTypeEnum(str, enum.Enum):
    equal = "equal"
    percentage = "percentage"

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    paid_by = Column(Integer, ForeignKey("users.id"))
    split_type = Column(Enum(SplitTypeEnum))
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense")

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    expense = relationship("Expense", back_populates="splits") 