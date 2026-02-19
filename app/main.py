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
    cursor.execute("""INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    conn.commit() # commit the transaction to save the changes to the database
    new_post = cursor.fetchone()
    return {"data": new_post, "UserMessage": "Post created successfully"}

@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Perform the delete and get the deleted row back in one go
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit() # Commit the transaction
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    # 204 No Content should not return a body
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/posts/{id}")
def update_post_partial(id: int, post: PostPatch):
    # 1. Convert Pydantic model to a dict, ignoring fields the user didn't send
    update_data = post.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # 2. Build a dynamic SQL query:
    # simplify the "existing data" merge using dictionary unpacking.

    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    existing_post = cursor.fetchone()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")

    # Merge existing data with new data, giving precedence to the new data
    updated_values = {**existing_post, **update_data}

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s 
           WHERE id = %s RETURNING *""",
        (updated_values['title'], updated_values['content'], updated_values['published'], id)
    )
    
    updated_post = cursor.fetchone()
    conn.commit()

    return {"data": updated_post, "UserMessage": "Post updated successfully"}

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post): # ensure that the request comes with the right data structure by using the Post model
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit() # commit the transaction to save the changes to the database
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return {"data": updated_post, "UserMessage": "Post updated successfully"}
