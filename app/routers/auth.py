from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from .. import models, schemas, oauth2
from ..utils import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials")
    
    # Here you would normally verify the password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials")
    
    # create a JWT token and return it to the client
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
