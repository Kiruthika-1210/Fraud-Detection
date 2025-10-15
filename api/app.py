# api/app.py
from fastapi import FastAPI
from api.routers import auth, wallet, fraud

app = FastAPI(title="Digital Wallet with AI Fraud Detection")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(fraud.router, prefix="/fraud", tags=["Fraud"])

@app.get("/")
def root():
    return {"message": "Wallet Fraud Detection API is running!"}
