# api/routers/fraud.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "Fraud router is working!"}
