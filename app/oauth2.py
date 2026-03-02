from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from .database import get_db
from . import models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY
# ALGORITHM
# EXPIRATION_TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # Copy the data to encode, so we don't modify the original data
    to_encode = data.copy()
    
    # Set the expiration time for the token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add the expiration time to the data to encode
    to_encode.update({"exp": expire})
    
    # Encode the token using the SECRET_KEY and ALGORITHM
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return the encoded JWT token
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the user ID from the token payload
        id: str = payload.get("user_id")
        
        # If the user ID is not found in the token payload, raise the credentials exception
        if id is None:
            raise credentials_exception
        
        # Create a TokenData object with the user ID extracted from the token payload
        token_data = schemas.TokenData(id=id)

    # If there is an error decoding the token (e.g., invalid token, expired token), raise the credentials exception
    except JWTError:
        raise credentials_exception
    
    # Return the token data (which contains the user ID) if the token is valid
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1 — cryptographic validation
    token_data = verify_access_token(token, credentials_exception)

    # Step 2 — application validation
    user = db.query(models.User).filter(
        models.User.id == token_data.id
    ).first()

    if user is None:
        raise credentials_exception

    return user
