# Project controller
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.models import User
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app import crud

router = APIRouter(prefix="/api/projects", tags=["projects"])


# Get all projects for current user
@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = crud.get_projects(db, current_user.id)
    return projects


# Get a single project by id
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = crud.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# Create a new project
@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = crud.create_project(db, project, current_user.id)
    return new_project


# Update an existing project
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_project = crud.update_project(db, project_id, project, current_user.id)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


# Delete a project
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = crud.delete_project(db, project_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
