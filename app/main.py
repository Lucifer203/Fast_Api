from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Union
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas

from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db


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



@app.get("/")  ## decorator
def read_root():
    return {"message": "Welcome to my API."}

    

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,response: Response,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
       
    return post


## deleting a post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response,db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)



    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    # return {"message":f"Post deleted successfully with id : {id}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## updating a post
@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,response:Response,post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    post_query.update(post.model_dump(),synchronize_session=False)

    # post_query.update({'title':'this is updated title',
    #                    'content':'this is the updated content'},synchronize_session=False)
    
    db.commit()
    return post_query.first()

################################ creating api's for users ##########################
@app.post('/users',status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db: Session= Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
 
 





#  new_post = models.Post(**post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post