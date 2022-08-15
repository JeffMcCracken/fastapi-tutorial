from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..repository import user


router = APIRouter(
    prefix='/user',
    tags=['users']
)

@router.post('', status_code=201, response_model=schemas.ShowUser, tags=['users'])
def create(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get('/{id}', response_model=schemas.ShowUser, tags=['users'])
def show(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)