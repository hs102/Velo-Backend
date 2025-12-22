# Auth endpoints
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.schemas import UserCreate, UserResponse, Token, UserLogin
from app.crud import get_user_by_email, get_user_by_username, create_user
from app.core.auth import verify_password, create_access_token
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # check if email already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # check if username already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # create the user
    new_user = create_user(db, user)
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # find user by username
    db_user = get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # create token
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
