from fastapi import FastAPI, Header, HTTPException
import os
from dotenv import load_dotenv
import jwt

from app.database import db_ping

load_dotenv()

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")


@app.on_event("startup")
def _startup_db_check():
    try:
        db_ping()
        print("DB OK")
    except Exception as e:
        print(f"DB FAIL: {e}")


@app.get("/sign-token")
def sign_token():
    user = {"id": 1, "username": "test", "password": "test"}
    token = jwt.encode(user, JWT_SECRET, algorithm="HS256")
    return {"token": token}


@app.post("/verify-token")
def verify_token(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        token = Authorization.split(" ")[1]
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return {"user": decoded}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
