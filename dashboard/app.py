# dashboard/app.py
import streamlit as st
import requests

BASE_URL = "https://wallet-fraud-api.onrender.com/"

st.set_page_config(page_title="Wallet Fraud Dashboard", layout="centered")
st.title("💳 Wallet Fraud Detection Dashboard")

# ---------------- SESSION STATE ----------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- AUTH SECTION ----------------
st.header("🔐 Authentication")

tab_login, tab_signup = st.tabs(["Login", "Signup"])

# -------- LOGIN --------
with tab_login:
    with st.form("login_form"):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pwd")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            res = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": login_email,
                    "password": login_password,
                },
            )
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("✅ Login successful")
            else:
                st.error("❌ Invalid credentials")

# -------- SIGNUP --------
with tab_signup:
    with st.form("signup_form"):
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_pwd")
        signup_btn = st.form_submit_button("Signup")

        if signup_btn:
            res = requests.post(
                f"{BASE_URL}/auth/signup",
                json={
                    "email": signup_email,
                    "password": signup_password,
                },
            )
            if res.status_code == 200:
                st.success("✅ Signup successful. Please login.")
            else:
                st.error(res.text)

# ---------------- AUTH HEADER ----------------
if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    st.success("🔓 Authenticated")
else:
    headers = {}
    st.warning("🔒 Please login to continue")

st.divider()

# ---------------- CREATE WALLET ----------------
st.header("👛 Create Wallet")

balance = st.number_input("Initial Balance", min_value=0.0, value=1000.0)

if st.button("Create Wallet"):
    if not st.session_state.token:
        st.error("Please login first")
    else:
        res = requests.post(
            f"{BASE_URL}/wallet/create",
            json={"balance": balance},
            headers=headers,
        )
        if res.status_code == 200:
            st.success(f"Wallet created with ID: {res.json()['wallet']}")
        else:
            st.error(res.text)

st.divider()

# ---------------- TRANSFER ----------------
st.header("💸 Simulate Transaction")

from_wallet = st.number_input("From Wallet ID", min_value=1, step=1)
to_wallet = st.number_input("To Wallet ID", min_value=1, step=1)
amount = st.number_input("Amount", min_value=0.0, value=100.0)

if st.button("Transfer"):
    if not st.session_state.token:
        st.error("Please login first")
    else:
        payload = {
            "from_wallet": int(from_wallet),
            "to_wallet": int(to_wallet),
            "amount": amount,
        }

        res = requests.post(
            f"{BASE_URL}/wallet/transfer",
            json=payload,
            headers=headers,
        )

        if res.status_code == 200:
            data = res.json()
            st.success(f"Decision: {data['status']}")
            st.metric("Risk Score", round(data["risk_score"], 4))
            st.write("Rules Triggered:", data["rules"])
        else:
            st.error(res.text)    