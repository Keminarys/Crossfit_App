# import streamlit as st
# import hashlib
# import uuid
# from streamlit_gsheets import GSheetsConnection
# from streamlit_cookies_manager import EncryptedCookieManager
# from utils.functions import get_conn_and_df, UpdateDB

# # ---------------------------------------------------------------------------- #
# # 0. Per-session unique ID
# # ---------------------------------------------------------------------------- #
# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# # Load secret for cookie encryption
# x = get_conn_and_df("Credentials")
# x_pass = x.at[x['username'].eq('COOKIES_SECRET').idxmax(), 'password']

# cookies = EncryptedCookieManager(
#     prefix=f"crossfit83/{st.session_state.session_id}/",
#     password=x_pass
# )
# if not cookies.ready():
#     st.stop()

# # ---------------------------------------------------------------------------- #
# # 1. Load user DB
# # ---------------------------------------------------------------------------- #
# def load_user_db():
#     return get_conn_and_df("Credentials")
    
# # ---------------------------------------------------------------------------- #
# # 2. Hashing
# # ---------------------------------------------------------------------------- #
# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()

# # ---------------------------------------------------------------------------- #
# # 3. Auth Dialog
# # ---------------------------------------------------------------------------- #
# @st.dialog("🔐 Authentication")
# def _auth_dialog():
#     mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)

#     if mode == "Log In":
#         user = st.text_input("Username")
#         pw   = st.text_input("Password", type="password")

#         if st.button("Login", type="primary"):
#             db = load_user_db()
#             is_valid = (
#                 user in list(db.username) and
#                 db.at[db['username'].eq(user).idxmax(), 'password'] == hash_password(pw)
#             )
#             if is_valid:
#                 st.session_state.authenticated = True
#                 st.session_state.athl = user
#                 cookies["athl"] = user
#                 cookies.save()
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")

#     else:  # Sign Up
#         new_user = st.text_input("New Username")
#         pw1      = st.text_input("Password", type="password")
#         pw2      = st.text_input("Repeat Password", type="password")

#         if st.button("Sign Up", type="primary"):
#             db = load_user_db()
#             if not new_user or not pw1:
#                 st.error("All fields are required")
#             elif new_user in list(db.username):
#                 st.error("Username already exists")
#             elif pw1 != pw2:
#                 st.error("Passwords do not match")
#             else:
#                 password_hashed = hash_password(pw1)
#                 UpdateDB(db, {'username': new_user, 'password': password_hashed}, "Credentials")
#                 st.session_state.authenticated = True
#                 st.session_state.athl = new_user
#                 cookies["athl"] = new_user
#                 cookies.save()
#                 st.rerun()

# def login_ui():
#     if "authenticated" not in st.session_state:
#         if cookies.get("athl"):
#             st.session_state.authenticated = True
#             st.session_state.athl = cookies.get("athl")
#         else:
#             st.session_state.authenticated = False

#     if not st.session_state.authenticated:
#         _auth_dialog()
#         st.stop()

# def logout_ui():
#     if st.session_state.get("authenticated"):
#         if st.button("Logout", key="btn_logout"):
#             for k in ("authenticated", "athl"):
#                 st.session_state.pop(k, None)
#             st.session_state.pop("session_id", None)
#             st.rerun()

import streamlit as st
import hashlib
import uuid
import jwt
from datetime import datetime, timedelta
from utils.functions import get_conn_and_df, UpdateDB
from streamlit_cookies_manager import EncryptedCookieManager
# ---------------------------------------------------------------------------- #
# 0. Configuration
# ---------------------------------------------------------------------------- #

SESSION_DURATION_HOURS = 24

# Load JWT secret from your “Credentials” sheet
_creds_df = get_conn_and_df("Credentials")
JWT_SECRET = _creds_df.loc[
    _creds_df["username"] == "COOKIES_SECRET", "password"
].squeeze()

# Setup encrypted cookie manager
cookies = EncryptedCookieManager(
    prefix="crossfit83/auth/",
    password=JWT_SECRET
)
if not cookies.ready():
    st.stop()

# ---------------------------------------------------------------------------- #
# 1. Helpers: Sheets Access & JWT Logic
# ---------------------------------------------------------------------------- #

def load_user_db():
    df = get_conn_and_df("Credentials")
    return df[df["username"] != "COOKIES_SECRET"].copy()

def load_sessions_db():
    return get_conn_and_df("Sessions")

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def create_token(username: str):
    """Generate a JWT and corresponding session payload."""
    jti = str(uuid.uuid4())
    now = datetime.utcnow()
    exp = now + timedelta(hours=SESSION_DURATION_HOURS)

    # Use UNIX timestamps in token
    token_payload = {
        "sub": username,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")
    return token, token_payload

def verify_token(token: str):
    """Decode JWT and return payload with datetime fields, or None."""
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # Convert UNIX timestamps back to datetime
        data["iat"] = datetime.utcfromtimestamp(data["iat"])
        data["exp"] = datetime.utcfromtimestamp(data["exp"])
        return data
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def is_session_active(jti: str) -> bool:
    df = load_sessions_db()
    row = df[df["jti"] == jti]
    if row.empty or not row.iloc[0]["active"]:
        return False
    expires = datetime.fromisoformat(row.iloc[0]["expires_at"])
    return expires > datetime.utcnow()

def record_session(payload: dict):
    UpdateDB(
        load_sessions_db(),
        {
            "jti":        payload["jti"],
            "user":       payload["sub"],
            "issued_at":  datetime.utcfromtimestamp(payload["iat"]).isoformat(),
            "expires_at": datetime.utcfromtimestamp(payload["exp"]).isoformat(),
            "active":     True
        },
        sheet_name="Sessions",
    )

def deactivate_session(jti: str):
    UpdateDB(
        load_sessions_db(),
        {"jti": jti, "active": False},
        sheet_name="Sessions",
    )
# ---------------------------------------------------------------------------- #
# 2. Login / Sign-Up Dialog
# ---------------------------------------------------------------------------- #
@st.dialog("🔐 Authentication")
def _auth_dialog():
    mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)
    db = load_user_db()

    if mode == "Log In":
        user = st.text_input("Username")
        pw   = st.text_input("Password", type="password")

        if st.button("Login", type="primary"):
            pw_hash = hash_password(pw)
            valid = (
                user in list(db.username) and
                db.loc[db['username'] == user, 'password'].squeeze() == pw_hash
            )
            if not valid:
                st.error("Invalid username or password")
                return

            token, payload = create_token(user)
            record_session(payload)
            cookies["token"] = token
            cookies.save()
            st.session_state.authenticated = True
            st.session_state.user = user
            st.rerun()

    else:  # Sign Up
        new_user = st.text_input("New Username")
        pw1      = st.text_input("Password", type="password")
        pw2      = st.text_input("Repeat Password", type="password")

        if st.button("Sign Up", type="primary"):
            if not new_user or not pw1:
                st.error("All fields are required")
            elif new_user in list(db.username):
                st.error("Username already exists")
            elif pw1 != pw2:
                st.error("Passwords do not match")
            else:
                password_hashed = hash_password(pw1)
                UpdateDB(db, {'username': new_user, 'password': password_hashed}, "Credentials")

                token, payload = create_token(new_user)
                record_session(payload)
                cookies["token"] = token
                cookies.save()
                st.session_state.authenticated = True
                st.session_state.user = new_user
                st.rerun()

# ---------------------------------------------------------------------------- #
# 3. Login UI Wrapper
# ---------------------------------------------------------------------------- #
def login_ui():
    # Attempt silent login via existing cookie
    token = cookies.get("token")
    if token:
        payload = verify_token(token)
        if payload and is_session_active(payload['jti']):
            st.session_state.authenticated = True
            st.session_state.user = payload['sub']
        else:
            # expired or revoked
            cookies.delete("token")
            cookies.save()
            st.session_state.authenticated = False

    if not st.session_state.get("authenticated", False):
        _auth_dialog()
        st.stop()

# ---------------------------------------------------------------------------- #
# 4. Logout Button
# ---------------------------------------------------------------------------- #
def logout_ui():
    if st.session_state.get("authenticated"):
        if st.button("Logout", key="btn_logout"):
            token = cookies.get("token")
            if token:
                payload = verify_token(token)
                if payload:
                    deactivate_session(payload['jti'])
            if "token" in cookies:
                del cookies["token"]
            cookies.save()
            for key in ("authenticated", "user"):
                st.session_state.pop(key, None)
            st.rerun()

