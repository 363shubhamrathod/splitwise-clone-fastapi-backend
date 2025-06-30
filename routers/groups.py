from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from services.group_service import add_user_to_group, remove_user_from_group_if_cleared

router = APIRouter()

@router.post("/groups", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    for user_id in group.user_ids:
        member = models.GroupMember(group_id=db_group.id, user_id=user_id)
        db.add(member)
    db.commit()
    return db_group

@router.get("/groups/{group_id}", response_model=schemas.Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("/groups/{group_id}/members/{user_id}")
def add_member_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    success = add_user_to_group(group_id, user_id, db)
    if not success:
        raise HTTPException(status_code=400, detail="User is already a member of the group")
    return {"message": "User added to group"}

@router.delete("/groups/{group_id}/members/{user_id}")
def remove_member_from_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    success = remove_user_from_group_if_cleared(group_id, user_id, db)
    if not success:
        raise HTTPException(status_code=400, detail="User cannot be removed: balance not cleared or not a member")
    return {"message": "User removed from group"}
