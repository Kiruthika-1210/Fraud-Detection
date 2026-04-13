# 💳 Wallet Fraud Guard — Real-Time Fraud Detection System

An end-to-end fraud detection system for digital wallets that combines Machine Learning and rule-based decisioning to evaluate transactions in real time.

This project demonstrates how intelligent backend systems are designed and deployed in real-world fintech environments.

---

## 🚀 Live Demo

* 🌐 Frontend: https://wallet-fraud-dashboard.onrender.com
* ⚙️ Backend API: https://wallet-fraud-api.onrender.com

---

## 📌 Problem Statement

Digital wallet systems are vulnerable to fraud patterns such as:

* High-value abnormal transactions
* Rapid transaction bursts (velocity attacks)
* Deviation from user spending behavior

Pure rule-based systems are rigid, while pure ML systems lack transparency.

👉 This project solves it using a **hybrid ML + rules architecture**.

---

## 🧠 Key Features

* 🔐 JWT-based authentication (signup/login)
* 🤖 ML-based fraud scoring (XGBoost)
* ⚖️ Rule-based overrides (high_amount, high_velocity)
* 📊 Real-time risk scoring for each transaction
* 🧾 Audit logging of decisions and rules triggered
* ⚙️ FastAPI backend with modular architecture
* 💻 Streamlit dashboard for end-to-end interaction
* 🌐 Fully deployed system (frontend + backend)

---

## 🏗️ System Architecture

User → Frontend (Streamlit)
→ FastAPI Backend
→ Feature Builder (DB-based stats)
→ ML Model (risk score)
→ Rule Engine
→ Decision Engine
→ Database (transactions + audit logs)

---

## 🔄 Transaction Flow

1. User logs in using JWT authentication
2. Wallet is created with initial balance
3. Transaction request is submitted
4. Features are generated using historical user data
5. ML model predicts fraud probability
6. Rule engine applies deterministic checks
7. Final risk score is computed
8. Decision is returned:

* APPROVE
* REVIEW
* REJECT

---

## 🤖 Fraud Detection Logic

### ML Model

* Algorithm: XGBoost
* Output: Risk probability (0–1)

### Rule Engine

* `high_amount` → unusually large transaction
* `high_velocity` → multiple rapid transactions

### Final Risk Score

```
final_score = ml_score + rule_penalty
```

---

## 📊 Decision Thresholds

| Risk Score | Decision |
| ---------- | -------- |
| < 0.6      | APPROVE  |
| 0.6 – 0.75 | REVIEW   |
| ≥ 0.75     | REJECT   |

---

## 🗄️ Database Design

* users
* wallets
* transactions
* fraud_audit

Each transaction stores:

* risk score
* triggered rules
* final decision

---

## 🧪 Testing Strategy

The system was validated using:

* Functional tests (wallet creation, transfer)
* Edge cases (invalid inputs, insufficient balance)
* Fraud scenarios:

  * High amount transactions
  * Rapid repeated transactions
  * Behavior deviation patterns

---

## 🚀 Deployment

* Backend deployed using FastAPI on Render
* Frontend deployed using Streamlit on Render
* Environment variables used for secure JWT handling
* Database initialized dynamically at startup

---

## 💡 Key Learnings

* Handling differences between local and production environments
* Designing secure APIs using JWT
* Combining ML predictions with deterministic rules
* Debugging real-world deployment issues (DB initialization, dependencies)

---

## 🧠 Conclusion

This project demonstrates how machine learning models can be integrated into production-ready backend systems to build intelligent, explainable, and secure applications.

---

## 👩‍💻 Author

**Kiruthika M (Kittu)**
AI & Data Science Student
Aspiring Software Development Engineer 🚀
