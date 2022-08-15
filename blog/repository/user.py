from sqlalchemy.orm import Session
from fastapi import HTTPException

from .. import models, schemas
from ..hashing import Hash

def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(404, f'User with id {id} not found')
    return user