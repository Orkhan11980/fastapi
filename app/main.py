from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schema import BaseModel, CreatePost
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


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(posts)
    return {posts}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {new_post}



@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return {"post": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")




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


@app.put("/update/{id}")
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    up_post = post.first()

    if up_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")

    post.update(updated_post.dict())
    db.commit()
    return {post.first()}


