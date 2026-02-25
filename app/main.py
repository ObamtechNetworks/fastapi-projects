from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .utils import hash_password
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine) # create the tables in the database based on the models defined in models.py

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")

def root():
    return {"message": "Welcome to my API"}
