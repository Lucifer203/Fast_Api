from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

## used to set criteria for the data to be sent
class User(BaseModel):
    email: EmailStr
    id: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool  = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)
    