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
from streamlit_authenticator import Authenticate, Hasher
from utils.functions import get_conn_and_df, UpdateDB

# ---------------------------------------------------------------------------- #
# 1. Helpers: Load & Sync Credentials with Google Sheet
# ---------------------------------------------------------------------------- #

def load_credentials():
    """
    Fetches the 'Credentials' sheet and builds the dict
    that streamlit-authenticator expects.
    """
    df = get_conn_and_df("Credentials").fillna("")
    creds = {"usernames": {}}

    for _, row in df.iterrows():
        if row.username == "COOKIES_SECRET":
            continue

        creds["usernames"][row.username] = {
            "name": row.username,
            "password": row.password,  # already hashed
        }

    return creds


def sync_new_user(username: str, plain_password: str):
    """
    Hashes the user’s password, adds the new user both
    to the in-memory creds and the Google Sheet.
    """
    # 1) Generate a secure hash
    hashed = Hasher([plain_password]).generate()[0]

    # 2) Persist to the Google Sheet
    UpdateDB(
        get_conn_and_df("Credentials"),
        {"username": username, "password": hashed},
        sheet_name="Credentials",
    )


# ---------------------------------------------------------------------------- #
# 2. Authenticator Factory
# ---------------------------------------------------------------------------- #

@st.cache_resource(show_spinner=False)
def init_authenticator():
    """
    Builds and returns a configured Authenticate instance.
    Caches to avoid re-creating on every rerun.
    """
    credentials = load_credentials()
    cookie_cfg = {
        "name":           "streamlit_auth",
        "key":            st.secrets["auth"]["cookie_key"],
        "expiry_days":    7,
    }
    preauth_cfg = {"emails": []}  # you can pre-authorize some addresses here

    return Authenticate(
        credentials=credentials,
        cookie=cookie_cfg,
        preauthorized=preauth_cfg,
    )


# ---------------------------------------------------------------------------- #
# 3. Login, Signup, Logout UIs
# ---------------------------------------------------------------------------- #

def login_ui():
    """
    Renders the login widget.  
    On success, returns (authenticator, name, username).
    """
    authenticator = init_authenticator()
    name, auth_status, username = authenticator.login("Login", "main")

    if auth_status:
        st.session_state["name"] = name
        st.session_state["username"] = username
        return authenticator, name, username

    if auth_status is False:
        st.error("Username/password is incorrect")
    return None, None, None


def signup_ui():
    """
    Renders the signup widget.  
    Creates a new user in your Google Sheet on success.
    """
    st.header("Create a New Account")

    username = st.text_input("Choose a username")
    pw1      = st.text_input("Password", type="password")
    pw2      = st.text_input("Confirm password", type="password")

    if st.button("Sign up"):
        if not (username and email and pw1):
            st.error("All fields are required")
        elif pw1 != pw2:
            st.error("Passwords don’t match")
        else:
            # Sync new user & inform
            sync_new_user(username, pw1)
            st.success("Account created. Please log in.")
            st.session_state.pop("register_mode", None)
            st.experimental_rerun()


def logout_ui(authenticator):
    """
    Renders the logout button.
    """
    authenticator.logout("Logout", "main")


# ---------------------------------------------------------------------------- #
# 4. App-Wide Entry Point
# ---------------------------------------------------------------------------- #

def main_auth():
    """
    Call this at the top of your app to guard access.
    Returns True if the user is authenticated, else halts execution.
    """
    # --- If user clicked “Sign up” previously, show signup form
    if st.session_state.get("register_mode"):
        signup_ui()
        st.stop()

    # --- Login form
    authenticator, name, username = login_ui()
    if authenticator:
        # on successful login
        logout_ui(authenticator)
        st.write(f"Welcome *{name}* 👋")
        return True

    # --- Offer switch to signup
    if st.button("Sign up"):
        st.session_state["register_mode"] = True
        st.rerun()

    st.stop()
