from pydantic import BaseModel
from datetime import datetime

## used to set criteria for the data to be sent

class PostBase(BaseModel):
    title: str
    content: str
    published: bool  = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass 