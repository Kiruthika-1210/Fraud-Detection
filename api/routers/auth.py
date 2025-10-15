# api/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
import bcrypt
from jose import jwt
import os

router = APIRouter()

SECRET_KEY = os.environ.get("JWT_SECRET", "supersecretkey")

# Request Schemas
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Signup endpoint
@router.post("/signup")
def signup(req: SignupRequest):
    conn = sqlite3.connect("db/wallet_fraud.db")
    c = conn.cursor()
    hashed_pwd = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (email, pwd_hash) VALUES (?, ?)", (req.email, hashed_pwd))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        conn.close()
    return {"message": "User created successfully"}

# Login endpoint
@router.post("/login")
def login(req: LoginRequest):
    conn = sqlite3.connect("db/wallet_fraud.db")
    c = conn.cursor()
    c.execute("SELECT id, pwd_hash FROM users WHERE email=?", (req.email,))
    user = c.fetchone()
    conn.close()
    if not user or not bcrypt.checkpw(req.password.encode(), user[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"user_id": user[0]}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}
