# AI controller
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import google.generativeai as genai
import os
from datetime import datetime

from app.dependencies import get_db, get_current_user
from app.models import User
from app import crud

router = APIRouter(prefix="/api/ai", tags=["ai"])

# Configure Gemini
genai.configure(api_key=os.getenv("llm"))


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's projects and tasks
    projects = crud.get_projects(db, current_user.id)
    all_tasks = crud.get_tasks(db, current_user.id)
    
    # Build context
    context = f"""You are a helpful task manager assistant for {current_user.username}.
Current date: {datetime.now().strftime('%Y-%m-%d')}

USER'S PROJECTS:
"""
    
    for project in projects:
        project_tasks = [t for t in all_tasks if t.project_id == project.id]
        context += f"\n- Project: {project.name}"
        if project.description:
            context += f" ({project.description})"
        context += f"\n  Tasks ({len(project_tasks)}):"
        
        for task in project_tasks:
            context += f"\n    • {task.title} - Status: {task.status}, Priority: {task.priority}"
            if task.due_date:
                context += f", Due: {task.due_date.strftime('%Y-%m-%d')}"
    
    if not projects:
        context += "\n(No projects yet)"
    
    context += f"\n\nUser question: {request.message}"
    
    # Call Gemini
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(context)
    
    return {
        "response": response.text,
        "user": current_user.username
    }
