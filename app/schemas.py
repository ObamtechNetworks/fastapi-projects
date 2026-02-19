from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostPatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # This is CRITICAL for SQLAlchemy. 
        # It tells Pydantic to read data even if it's an ORM object, not a dict.
        from_attributes = True
