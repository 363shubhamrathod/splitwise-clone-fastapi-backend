from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SplitTypeEnum(str, Enum):
    equal = "equal"
    percentage = "percentage"

class UserCreate(BaseModel):
    name: str

class User(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class GroupCreate(BaseModel):
    name: str
    user_ids: List[int]

class Group(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: int
    split_type: SplitTypeEnum
    splits: Optional[List[dict]]  # for percentage

class Expense(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: int
    split_type: SplitTypeEnum
    class Config:
        orm_mode = True
