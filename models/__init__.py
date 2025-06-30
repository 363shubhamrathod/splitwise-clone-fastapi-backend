from .user import User
from .group import Group, GroupMember
from .expense import Expense, ExpenseSplit, SplitTypeEnum 
from database import engine, Base

Base.metadata.create_all(bind=engine) 