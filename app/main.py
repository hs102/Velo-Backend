# main.py - FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import db_ping
from app.controllers import auth, projects, tasks, ai

app = FastAPI(title="Task Manager API", version="1.0.0")

# CORS setup - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for debugging
    allow_credentials=False,  # Must be False when using wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# include controllers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(ai.router)


@app.on_event("startup")
def startup():
    try:
        db_ping()
        print("Database connection: OK")
    except Exception as e:
        print(f"Database connection: FAILED - {e}")


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Task Manager API is running"}

