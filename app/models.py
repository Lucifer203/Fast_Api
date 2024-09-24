from sqlalchemy import Boolean,Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Post(Base): 
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content= Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id",ondelete="CASCADE"),nullable=False)
    
    owner = relationship("User")  ## used for building a relationship with another table without using any key


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable= False,primary_key=True)
