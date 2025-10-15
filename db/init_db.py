# db/init_db.py
import sqlite3

DB_PATH = "db/wallet_fraud.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        pwd_hash BLOB NOT NULL
    )
    """)

    # Wallets table
    c.execute("""
    CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        balance REAL DEFAULT 0.0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Transactions table (with timestamp)
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_wallet INTEGER NOT NULL,
        to_wallet INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        risk_score REAL,
        meta TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(from_wallet) REFERENCES wallets(id),
        FOREIGN KEY(to_wallet) REFERENCES wallets(id)
    )
    """)

    # Fraud Audit table
    c.execute("""
    CREATE TABLE IF NOT EXISTS fraud_audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        txn_id INTEGER NOT NULL,
        score REAL,
        rules TEXT,
        decision TEXT,
        explanation TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(txn_id) REFERENCES transactions(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
