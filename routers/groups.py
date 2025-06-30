from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

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
