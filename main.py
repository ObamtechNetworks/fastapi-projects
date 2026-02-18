from typing import Optional
from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException

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


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1, "published": True, "rating": 5},
            {"title": "favorite foods", "content": "I like pizza", "id": 2, "published": True, "rating": 10}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return {"post_detail": post}
