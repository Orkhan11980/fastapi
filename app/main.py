from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schema import BaseModel, CreatePost, PostResponse, UserCreate, UserCreateOut
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='1233', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succcesfull")
        break
    except Exception as error:
        print("connection failed", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(posts)
    return posts


@app.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return post




@app.delete("/post/delete/{id}")
def remove_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")
    else:
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    up_post = post.first()

    if up_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")

    post.update(updated_post.dict())
    db.commit()
    return post.first()


@app.post("/users",status_code=status.HTTP_201_CREATED, response_model= UserCreateOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/get_users", response_model=List[UserCreateOut])
def get_users( db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                        , detail="Not found")
    return users