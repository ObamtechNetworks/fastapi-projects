from operator import le
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint

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

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    owner: UserOut # This will include the owner's email and created_at fields in the response when we return a post. The owner field is of type UserOut, which is a Pydantic model that includes the id, email, and created_at fields of the user who created the post.
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # This is CRITICAL for SQLAlchemy. 
        # It tells Pydantic to read data even if it's an ORM object, not a dict.
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str | int] = None
    
class TokenResponse(Token):
    pass

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # This means dir can only be 0 or 1. If it's 1, it means the user wants to like the post. If it's 0, it means the user wants to unlike the post.
