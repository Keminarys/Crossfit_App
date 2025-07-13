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
