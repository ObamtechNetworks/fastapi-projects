from time import sleep
from typing import Optional
from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

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
    
class PostPatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed")
        print("Error: " + str(e))
        sleep(2)

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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post_partial(id: int, post: PostPatch):
    update_data = post.model_dump(exclude_unset=True) # exclude_unset=True ensures that only the fields that are provided in the request are included in the post_dict
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="PATCH body cannot be empty"
        )
    found_post = find_post(id)
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    index = my_posts.index(found_post)
    updated_post = {**found_post, **update_data} # merge the existing post with the new data
    my_posts[index] = updated_post
    return {"data": updated_post, "UserMessage": "Post updated successfully"}

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post): # ensure that the request comes with the right data structure by using the Post model
    post_dict = post.model_dump()
    post_dict["id"] = id
    found_post = find_post(id)
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    index = my_posts.index(found_post)
    my_posts[index] = post_dict
    return {"data": post_dict, "UserMessage": "Post updated successfully"}
