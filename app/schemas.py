from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import ConfigDict
from typing import Optional, Literal

class PostBase(BaseModel):
    title: str
    content: str
    # published: bool=True

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config=ConfigDict(from_attributes=True)

class PostResponseCreate(PostBase):
    id:int
    created_at:datetime
    owner:UserOut
    model_config=ConfigDict(from_attributes=True)
class ResponsePost(PostBase):
    # created_at: datetime
    id: int 
    created_at: datetime
    owner: UserOut
    votes: int
    model_config=ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode=True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None=None

