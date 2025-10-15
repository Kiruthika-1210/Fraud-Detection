# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from api.app import app
from api.services.db_service import create_user, create_wallet, get_wallet_balance

client = TestClient(app)

# ---------------- Test Data ----------------
test_transactions = [
    # each txn now includes from_wallet, to_wallet, user_id
    ({"user_id": 1, "from_wallet": 7, "to_wallet": 8, "amount": 50, "timestamp": "2025-09-07T14:00:00Z"}, "APPROVE"),
    ({"user_id": 1, "from_wallet": 7, "to_wallet": 8, "amount": 2000, "timestamp": "2025-09-07T03:00:00Z"}, "REJECT"),
    ({"user_id": 1, "from_wallet": 7, "to_wallet": 8, "amount": 1200, "timestamp": "2025-09-07T10:00:00Z"}, "REVIEW"),
    ({"user_id": 1, "from_wallet": 7, "to_wallet": 8, "amount": 10, "timestamp": "2025-09-07T23:00:00Z"}, "REJECT"),
]

# ---------------- Fixtures ----------------
@pytest.fixture(scope="module", autouse=True)
def setup_wallets():
    # Ensure wallets exist with enough balance for tests
    balance = 5000
    # Use your db_service functions
    # If wallet 7 or 8 exists, you may need to reset balance
    from api.services.db_service import update_wallet_balance
    try:
        update_wallet_balance(wallet_id=7, amount=balance)
    except Exception:
        create_wallet(user_id=1, balance=balance)
    try:
        update_wallet_balance(wallet_id=8, amount=balance)
    except Exception:
        create_wallet(user_id=1, balance=balance)

# ---------------- Test ----------------
@pytest.mark.parametrize("txn, expected_decision", test_transactions)
def test_wallet_transfer(txn, expected_decision):
    response = client.post("/wallet/transfer", json=txn)
    
    if response.status_code != 200:
        pytest.fail(f"API Error {response.status_code}: {response.text}")
    
    # Now safe to assert decision
    assert response.json().get("decision") == expected_decision
