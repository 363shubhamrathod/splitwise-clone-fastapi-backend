from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    members = relationship("GroupMember", back_populates="group")
    expenses = relationship("Expense", back_populates="group")

class GroupMember(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    group = relationship("Group", back_populates="members") 