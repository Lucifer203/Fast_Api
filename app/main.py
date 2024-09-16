from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Union
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


## used to set criteria for the data to be sent
class Post(BaseModel):
    title: str
    content: str
    published: bool  = True
    rating: Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host='localhost',database='FastApi',
                                user='postgres',password='Adars123',cursor_factory=RealDictCursor)
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

# path operation
@app.get("/")  ## decorator
def read_root():
    return {"message": "Welcome to my API."}

@app.get("/items/{item_id}")
def read_item(item_id: int,q: Union[str,None]=None):
    return {"item_id":item_id,"q":q}
    

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # cursor.execute("""INSERT INTO posts (title,content) VALUES ('This is my 4th post','This is just tring to post new post') """)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    post = find_post(id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id: {id} not found."}
    return {"post_detail": post}


## deleting a post
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response):
    post_id = find_index_post(id=id)
    if post_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    my_posts.pop(post_id)
    # return {"message":f"Post deleted successfully with id : {id}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## updating a post
@app.put("/posts/{id}")
def update_post(id:int,response:Response,post:Post):
    index = find_index_post(id=id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}



