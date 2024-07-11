

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, utils
from .database import engine
from .routers import user_route, post_route, auth_router
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

app.include_router(post_route.router)
app.include_router(user_route.router)
app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "Hello World!!"}




