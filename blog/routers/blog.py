from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..database import get_db
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('', status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)

@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)

@router.put('/{id}', status_code=202)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)

@router.delete('/{id}', status_code=204)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)