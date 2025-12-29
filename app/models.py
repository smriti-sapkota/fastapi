from sqlmodel import SQLModel, Field, String , Column , TIMESTAMP, Integer, ForeignKey,Relationship
from pydantic import EmailStr
from datetime import datetime
from typing import Optional


class UserBase(SQLModel):
    email : EmailStr = Field(sa_column=Column(String, unique=True))
    password : str

class User(UserBase , table=True):
    __tablename__="users"
    id : int | None = Field(default= None , primary_key=True)
    created_at : datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=True, server_default=("now()")))

class UserCreate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class UserResponse(SQLModel):
    id : int
    email : EmailStr
    created_at : datetime

class PostBase(SQLModel):
    title : str 
    content : str
    published : bool | None = Field(default=True)

class Post(PostBase, table=True):
    __tablename__="posts"
    id : int | None = Field(default=None , primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    owner_id : int | None = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))  
    owner : User = Relationship() 

class CreatePost(PostBase):
    pass 

class UpdatePost(PostBase):
    pass

class PatchPost(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class PostResponse(PostBase):
    id : int 
    created_at: datetime
    owner_id: int
    owner : UserResponse


class PostOut(SQLModel) :
    Post : PostResponse
    votes:int 


class Token(SQLModel):
    access_token: str
    token_type : str

class TokenData(SQLModel):
    id : Optional[int] = None           

class VoteBase(SQLModel):
    post_id : int
    direction : int = Field(ge=0,le=1)  #allow 0 and 1 

class Vote(SQLModel, table=True ):
    __tablename__ = 'vote'
    user_id : int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True))
    post_id : int = Field(sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True))