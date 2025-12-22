# main.py - FastAPI application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import db_ping
from app.controllers import auth, projects, tasks

app = FastAPI(title="Task Manager API", version="1.0.0")

# CORS setup - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include controllers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)


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

