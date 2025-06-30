from sqlalchemy.orm import Session
import models, schemas

def create_user_service(user: schemas.UserCreate, db: Session):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 