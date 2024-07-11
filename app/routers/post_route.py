from typing import List
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.schema import CreatePost, PostResponse
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(posts)
    return posts


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return post


@router.delete("/delete/{id}")
def remove_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")
    else:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    up_post = post.first()

    if up_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")

    post.update(updated_post.dict())
    db.commit()
    return post.first()
