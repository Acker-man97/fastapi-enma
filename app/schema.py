from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal, Optional



class Posts(BaseModel):
    title: str
    content: str
    published: bool = True



class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Response(Posts):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int



class Likes(BaseModel):
    post_id: int
    dir: Literal[0,1]



class Comments(BaseModel):
    post_id: int
    content: str


class CommentsOut(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime
    response: Response

    class Config:
            from_attributes = True


class PostOut(BaseModel):
    Posts: Response
    comments: int
    likes: int

    class Config:
        from_attributes = True
    