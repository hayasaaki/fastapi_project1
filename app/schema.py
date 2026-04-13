from typing import Annotated, Optional
from unittest.mock import Base

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint

from app.models import User

class PostBase(BaseModel): 
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    class Config:
        from_attributes = True

class Post(PostBase):
    id : int
    # owner_id : int
    owner : UserOut
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir : Annotated[int, Field(ge=0, le=1)]

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        from_attributes = True