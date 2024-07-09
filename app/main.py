from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Posts(BaseModel):
    title: Optional[str] = None
    content: str
    published: bool = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: str
    published: bool = True


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

my_posts = [{"id": 1, "content": "content of post1", "title": "title of post1"},
            {"id": 2, "content": "content of post3", "title": "title of post3"}]


def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post: Posts):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/latest")
def last_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    post_test = cursor.fetchone()
    print(post_test)
    post = find_post(id)
    if post:
        return {"post": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


def find_index(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/post/delete/{id}")
def remove_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update/{id}")
def update_post(id: int, post: UpdatePost):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail="Not found")

    return {"data": updated_post}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"succes"}