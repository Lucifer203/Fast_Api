from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Union
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas,models,utils
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# get_db()



while True:

    try:
        conn = psycopg2.connect(host='localhost',database='FastApi',
                                user='postgres',password='Adarsh@123',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull!!")
        break
    except Exception as error:
        print("Connecting to database failed .")
        print("Error: ",error)
        time.sleep(2)


    
my_posts = [{"title": "title of posts","content":"content of post","id":1},{"title":
                                                                            "my favorite food","content":"daal bhat","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")  ## decorator
def read_root():
    return {"message": "Welcome to my API."}

    
