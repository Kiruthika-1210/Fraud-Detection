# api/routers/wallet.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from api.services import db_service, feature_builder, fraud_model, decision_engine

router = APIRouter()

# ----------- Request Schemas -----------
class CreateWalletRequest(BaseModel):
    user_id: int
    balance: float = 0.0

class TransferRequest(BaseModel):
    from_wallet: int
    to_wallet: int
    user_id: int
    amount: float
    timestamp: datetime = None  # optional, defaults to now

# ----------- Response Schema -----------
class TransferResponse(BaseModel):
    txn_id: int
    status: str
    risk_score: float
    rules: list

# ----------- Create Wallet Endpoint -----------
@router.post("/create")
def create_wallet(req: CreateWalletRequest):
    wallet = db_service.create_wallet(req.user_id, req.balance)
    if not wallet:
        raise HTTPException(status_code=400, detail="Wallet creation failed")
    return {"message": "Wallet created", "wallet": wallet}

# ----------- Transfer Endpoint -----------
@router.post("/transfer", response_model=TransferResponse)
def transfer_funds(req: TransferRequest):
    txn_time = req.timestamp or datetime.utcnow()

    # --- 1. Basic validations ---
    if req.from_wallet == req.to_wallet:
        raise HTTPException(status_code=400, detail="Cannot transfer to same wallet")

    from_balance = db_service.get_wallet_balance(req.from_wallet)
    if from_balance is None:
        raise HTTPException(status_code=404, detail="From wallet not found")
    if from_balance < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    to_balance = db_service.get_wallet_balance(req.to_wallet)
    if to_balance is None:
        raise HTTPException(status_code=404, detail="To wallet not found")

    # --- 2. Build features using real DB data ---
    last_10_min_txns = db_service.get_last_10_min_txns(req.user_id)  # implement in db_service
    user_avg, user_std = db_service.get_user_txn_stats(req.user_id)  # implement in db_service
    features = feature_builder.build_features(req.amount, user_avg, user_std, last_10_min_txns)

    # --- 3. Fraud scoring ---
    risk_score = fraud_model.predict(features)  # return numeric score

    # --- 4. Apply rules & thresholds ---
    rules = decision_engine.apply_rules(features)
    decision = decision_engine.make_decision(risk_score, rules)

    # --- 5. Execute transaction safely ---
    txn_status = "APPROVED" if decision == "APPROVE" else decision
    txn_id = db_service.create_transaction(
        from_wallet=req.from_wallet,
        to_wallet=req.to_wallet,
        amount=req.amount,
        status=txn_status,
        risk_score=risk_score,
        meta=str(features)
    )

    return TransferResponse(
        txn_id=txn_id,
        status=decision,
        risk_score=risk_score,
        rules=rules
    )
