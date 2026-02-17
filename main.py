from typing import Optional
from fastapi import Body, FastAPI

from pydantic import BaseModel

app = FastAPI()

# Pydantic models are used to define the structure of the data that we expect to receive in our API.
# They also provide validation and serialization of the data. In this example, we define a Post model with three fields: title, content, and published.
# The published field has a default value of True.
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_post():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.model_dump())
    return {"data": post}