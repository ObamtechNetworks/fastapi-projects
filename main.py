from fastapi import Body, FastAPI

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_post():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f'title: {payload["title"]}, content: {payload["content"]}'}