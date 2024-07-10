from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass
