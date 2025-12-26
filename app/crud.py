# CRUD utility functions
from sqlalchemy.orm import Session

from app.models import User, Project, Task
from app.schemas import UserCreate, UserUpdate, ProjectCreate, ProjectUpdate, TaskCreate, TaskUpdate
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


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # Update email if provided
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.id != user_id
        ).first()
        if existing:
            return None  # Email taken
        db_user.email = user_update.email
    
    # Update username if provided
    if user_update.username is not None:
        # Check if username is already taken by another user
        existing = db.query(User).filter(
            User.username == user_update.username,
            User.id != user_id
        ).first()
        if existing:
            return None  # Username taken
        db_user.username = user_update.username
    
    # Update password if provided
    if user_update.password is not None:
        db_user.hashed_password = hash_password(user_update.password)
    
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


# ============ TASK CRUD ============

def get_tasks(db: Session, user_id: int, project_id: int = None, status: str = None, priority: str = None):
    query = db.query(Task).join(Project).filter(Project.user_id == user_id)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    return query.all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.user_id == user_id
    ).first()


def create_task(db: Session, task: TaskCreate, user_id: int):
    # verify project belongs to user
    project = get_project(db, task.project_id, user_id)
    if not project:
        return None
    
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date,
        project_id=task.project_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        if task.title is not None:
            db_task.title = task.title
        if task.description is not None:
            db_task.description = task.description
        if task.priority is not None:
            db_task.priority = task.priority
        if task.status is not None:
            db_task.status = task.status
        if task.due_date is not None:
            db_task.due_date = task.due_date
        if task.project_id is not None:
            # verify new project belongs to user
            project = get_project(db, task.project_id, user_id)
            if project:
                db_task.project_id = task.project_id
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
