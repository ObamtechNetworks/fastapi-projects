from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.oauth2 import get_current_user
from .. import models, schemas
from ..database import engine, get_db

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # 1. Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    # 2. Check if the user has already voted on the post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    already_voted = vote_query.first()

    # 3. If the user is trying to like the post (dir=1) and they haven't already liked it, create a new vote
    if vote.dir == 1:
        if already_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted"}

    else:
        # 4. If the user is trying to unlike the post (dir=0) and they have already liked it, delete the existing vote
        if not already_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully unvoted"}
