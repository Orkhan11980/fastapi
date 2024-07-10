from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validate_email, EmailStr


class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

