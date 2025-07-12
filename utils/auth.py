import streamlit as st
import hashlib
from streamlit_gsheets import GSheetsConnection
from streamlit_cookies_manager import EncryptedCookieManager
from utils.functions import get_conn_and_df, UpdateDB

x = get_conn_and_df("Credentials")
x_pass = x.at[x['username'].eq('COOKIES_SECRET').idxmax(), 'password']
cookies = EncryptedCookieManager(
    prefix="crossfit83/",
    password=x_pass
)

if not cookies.ready():
    st.stop()
    
# ---------------------------------------------------------------------------- #
# 1. Load user database from Google Sheets (cached once per session)
# ---------------------------------------------------------------------------- #
def load_user_db():
    """
    Connects to a private GSheet and returns a dict mapping
    username -> password_hash.
    """
  
    records = get_conn_and_df("Credentials")
    return records

# ---------------------------------------------------------------------------- #
# 2. Simple SHA-256 hasher
# ---------------------------------------------------------------------------- #
def hash_password(password: str) -> str:
    """Return the hex SHA-256 digest of the input password."""
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------------------------------------------------------- #
# 3. Combined Login / Sign-Up UI
# ---------------------------------------------------------------------------- #
@st.dialog("🔐 Authentication")
def _auth_dialog():
    mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)

    if mode == "Log In":
        user = st.text_input("Username", "Username")
        pw   = st.text_input("Password", "Password")
        if st.button("Login", type="primary"):
            db = load_user_db()
            if user in list(db.username) and db.at[db['username'].eq(user).idxmax(), 'password'] == hash_password(pw):
                st.session_state.authenticated = True
                st.session_state.athl = user
                cookies["athl"] = user 
                cookies.save()
                st.rerun()
            else:
                st.error("Invalid username or password")

    else:  # Sign Up
        new_user = st.text_input("New Username", "New Username")
        pw1      = st.text_input("Password", "Password")
        pw2      = st.text_input("Repeat Password", "Repeat Password")
        if st.button("Sign Up", type="primary"):
            db = load_user_db()
            if not new_user or not pw1:
                st.error("All fields are required")
            elif new_user in db:
                st.error("Username already exists")
            elif pw1 != pw2:
                st.error("Passwords do not match")
            else:
                password_hashed = hash_password(pw1)
                new_entry = {'username' : new_user, 'password' : password_hashed}
                df = load_user_db()
                UpdateDB(df, new_entry, "Credentials")
                st.session_state.authenticated = True
                st.session_state.athl = new_user
                cookies["athl"] = user 
                cookies.save()
                st.rerun()


def login_ui():
    if "authenticated" not in st.session_state:
        if cookies.get("athl"):
            st.session_state.authenticated = True
            st.session_state.athl = cookies.get("athl")
        else:
            st.session_state.authenticated = False
            
    if not st.session_state.authenticated:
        _auth_dialog()  
        st.stop()       


