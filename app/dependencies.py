# Dependency functions
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.core.auth import verify_token
from app.crud import get_user_by_id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not authorization:
        raise credentials_exception
    
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise credentials_exception
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return user
