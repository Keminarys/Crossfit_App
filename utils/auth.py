import streamlit as st
import hashlib
from streamlit_gsheets import GSheetsConnection
from utils.functions import get_conn_and_df, UpdateDB
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

def clear_user_db_cache():
    load_user_db.clear()

# ---------------------------------------------------------------------------- #
# 2. Simple SHA-256 hasher
# ---------------------------------------------------------------------------- #
def hash_password(password: str) -> str:
    """Return the hex SHA-256 digest of the input password."""
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------------------------------------------------------- #
# 3. Combined Login / Sign-Up UI
# ---------------------------------------------------------------------------- #
def login_ui():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.dialog("🔐 Authentication"):
            mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)

            # —————————————————— LOGIN ——————————————————
            if mode == "Log In":
                user = st.text_input("Username", "Username")
                pw   = st.text_input("Password","password")
                if st.button("Login", type="primary"):
                    db = load_user_db()
                    if user in db and db[user] == hash_password(pw):
                        st.session_state.authenticated = True
                        st.session_state.athl = user
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")

            # ————————————————— SIGN UP —————————————————
            else:
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
                        # append and clear cache
                        df = load_user_db()
                        new_entry = {'username' : new_user, 'password' : hash_password(pw1)}
                        UpdateDB(df, new_entry, "Credentials")
                        clear_user_db_cache()
                        st.session_state.authenticated = True
                        st.session_state.athl = new_user
                        st.experimental_rerun()

        st.stop()


