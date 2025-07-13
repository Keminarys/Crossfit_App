import streamlit as st
import hashlib
import streamlit_authenticator as stauth
from utils.functions import get_conn_and_df, UpdateDB

# ---------------------------------------------------------------------------- #
# 1. Helpers: Load & Persist Credentials
# ---------------------------------------------------------------------------- #

def load_credentials() -> dict:
    """
    Read your sheet’s 'Credentials' tab and build the dict
    that streamlit-authenticator expects, WITHOUT any email.
    """
    df = get_conn_and_df("Credentials").fillna("")
    creds = {"usernames": {}}

    for _, row in df.iterrows():
        user = row["username"]
        if user == "COOKIES_SECRET":
            continue

        creds["usernames"][user] = {
            "name":     user,
            "password": row["password"],   # already SHA-256 hashed
        }

    return creds


def persist_user(username: str, hashed_pw: str):
    """
    Add or update a row in your 'Credentials' sheet.
    """
    UpdateDB(
        get_conn_and_df("Credentials"),
        {"username": username, "password": hashed_pw},
        sheet_name="Credentials",
    )


# ---------------------------------------------------------------------------- #
# 2. Instantiate Authenticator (cached)
# ---------------------------------------------------------------------------- #

@st.cache_resource(show_spinner=False)
def init_authenticator():
    creds = load_credentials()

    return stauth.Authenticate(
        credentials=creds,
        cookie_name=st.secrets["auth"]["cookie_name"],
        key=st.secrets["auth"]["cookie_key"],
        expiry_days=st.secrets["auth"]["expiry_days"],
        preauthorized={"emails": []},    # no emails in use
    )

authenticator = init_authenticator()


# ---------------------------------------------------------------------------- #
# 3. Login Flow
# ---------------------------------------------------------------------------- #

def login_flow():
    """
    Display the login widget.  
    Return authenticator on success, else None.
    """
    try:
        name, status, user = authenticator.login(
            location="main",
            name="Login"
        )
    except stauth.exceptions.LoginError as e:
        st.error(e)
        return None

    if status:
        st.session_state["username"] = user
        st.session_state["name"]     = name
        return authenticator

    if status is False:
        st.error("Username/password is incorrect")


# ---------------------------------------------------------------------------- #
# 4. Signup Flow
# ---------------------------------------------------------------------------- #

def signup_flow():
    """
    Custom signup UI (no email).  
    Hashes password and writes new user to the sheet.
    """
    st.header("Create a New Account")

    new_user = st.text_input("Username", key="su_user")
    pw1      = st.text_input("Password", type="password", key="su_pw1")
    pw2      = st.text_input("Confirm Password", type="password", key="su_pw2")

    if st.button("Sign up"):
        if not new_user or not pw1:
            st.error("All fields are required")
        elif pw1 != pw2:
            st.error("Passwords don’t match")
        else:
            hashed = hashlib.sha256(pw1.encode()).hexdigest()
            persist_user(new_user, hashed)
            st.success("Account created. Please log in.")
            st.rerun()


# ---------------------------------------------------------------------------- #
# 5. Logout Flow
# ---------------------------------------------------------------------------- #

def logout_flow(authenticator):
    """
    Display the logout button.
    """
    authenticator.logout(location="main", name="Logout")


# ---------------------------------------------------------------------------- #
# 6. App‐Wide Entry Point
# ---------------------------------------------------------------------------- #

def main_auth():
    """
    Call this at the top of your Streamlit app.
    Returns True if the user is now authenticated.
    Otherwise it handles login/signup and stops the app.
    """
    # 1) If user clicked “Sign up” button last run, show signup form
    if st.session_state.get("signup_mode"):
        signup_flow()
        st.stop()

    # 2) Otherwise attempt login
    auth = login_flow()
    if auth:
        # SUCCESS: show logout + welcome
        logout_flow(auth)
        st.write(f"Welcome *{st.session_state['username']}* 👋")
        return True

    # 3) If not yet authenticated, show “Sign up” switch
    if st.button("Sign up"):
        st.session_state["signup_mode"] = True
        st.rerun()

    st.stop()
