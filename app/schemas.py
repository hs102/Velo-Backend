# Pydantic schemas
from datetime import datetime, date
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, field_validator


# ============ USER SCHEMAS ============

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ============ PROJECT SCHEMAS ============

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ TASK SCHEMAS ============

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "todo"
    due_date: Optional[Union[datetime, date, str]] = None
    project_id: int
    
    @field_validator('due_date', mode='before')
    @classmethod
    def parse_due_date(cls, v):
        if v is None or isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[Union[datetime, date, str]] = None
    project_id: Optional[int] = None
    
    @field_validator('due_date', mode='before')
    @classmethod
    def parse_due_date(cls, v):
        if v is None or isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    due_date: Optional[datetime] = None
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
