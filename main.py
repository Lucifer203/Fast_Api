from fastapi import FastAPI
from fastapi.params import Body
from typing import Union
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


## used to set criteria for the data to be sent
class Post(BaseModel):
    title: str
    content: str
    published: bool  = True
    rating: Optional[int] = None


my_posts = [{"title": "title of posts","content":"content of post","id":1},{"title":
                                                                            "my favorite food","content":"daal bhat","id":2}]


# path operation
@app.get("/")  ## decorator
def read_root():
    return {"message": "Welcome to my API."}

@app.get("/items/{item_id}")
def read_item(item_id: int,q: Union[str,None]=None):
    return {"item_id":item_id,"q":q}
    

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    

# title  str , content str, category , Bool published or draft