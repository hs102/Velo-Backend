# CRUD utility functions
from sqlalchemy.orm import Session

from app.models import User, Project
from app.schemas import UserCreate, ProjectCreate, ProjectUpdate
from app.utils.password import hash_password


# ============ USER CRUD ============

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ============ PROJECT CRUD ============

def get_projects(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()


def get_project(db: Session, project_id: int, user_id: int):
    return db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()


def create_project(db: Session, project: ProjectCreate, user_id: int):
    db_project = Project(
        name=project.name,
        description=project.description,
        color=project.color,
        user_id=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate, user_id: int):
    db_project = get_project(db, project_id, user_id)
    if db_project:
        if project.name is not None:
            db_project.name = project.name
        if project.description is not None:
            db_project.description = project.description
        if project.color is not None:
            db_project.color = project.color
        db.commit()
        db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int, user_id: int):
    db_project = get_project(db, project_id, user_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False
