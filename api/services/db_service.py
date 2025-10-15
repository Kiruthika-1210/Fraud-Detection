# api/services/db_service.py
import sqlite3
import math

DB_PATH = "db/wallet_fraud.db"

# -------- Users --------
def create_user(email: str, hashed_pwd: bytes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, pwd_hash) VALUES (?, ?)", (email, hashed_pwd))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, pwd_hash FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user

# -------- Wallets --------
def create_wallet(user_id: int, balance: float = 0.0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO wallets (user_id, balance) VALUES (?, ?)", (user_id, balance))
    conn.commit()
    wallet_id = c.lastrowid
    conn.close()
    return wallet_id

def get_wallet_balance(wallet_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT balance FROM wallets WHERE id=?", (wallet_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# -------- Transactions --------
def create_transaction(from_wallet: int, to_wallet: int, amount: float, status: str, risk_score: float = 0.0, meta: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO transactions (from_wallet, to_wallet, amount, status, risk_score, meta)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (from_wallet, to_wallet, amount, status, risk_score, meta))
    conn.commit()
    txn_id = c.lastrowid
    conn.close()
    return txn_id

# --- Get last 10 min transactions for a user ---
def get_last_10_min_txns(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT amount, timestamp FROM transactions t
        JOIN wallets w ON t.from_wallet = w.id
        WHERE w.user_id=? AND timestamp >= datetime('now','-10 minutes')
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# --- Get user transaction stats ---
def get_user_txn_stats(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT amount FROM transactions t
        JOIN wallets w ON t.from_wallet = w.id
        WHERE w.user_id=?
    """, (user_id,))
    amounts = [row[0] for row in c.fetchall()]
    conn.close()

    if not amounts:
        return (0, 0)

    avg = sum(amounts) / len(amounts)
    std = math.sqrt(sum((x - avg) ** 2 for x in amounts) / len(amounts))
    return (avg, std)


