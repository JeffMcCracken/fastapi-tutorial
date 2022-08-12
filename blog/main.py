from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(404, f'Blog with id {id} not found')
    return blog

@app.delete('/blog/{id}', status_code=204)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(404, f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return {'Done'}

@app.put('/blog/{id}', status_code=202)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(404, f'Blog with id {id} not found')
    blog.update(request, synchronize_session=False)
    db.commit()
    return 'updated'

@app.post('/user', status_code=201)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user