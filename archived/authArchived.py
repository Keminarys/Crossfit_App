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

# import streamlit as st
# import hashlib
# import uuid
# from streamlit_gsheets import GSheetsConnection
# from streamlit_cookies_manager import EncryptedCookieManager
# from utils.functions import get_conn_and_df, UpdateDB
# import streamlit_cookies_manager
# from datetime import datetime, timedelta


# # ---------------------------------------------------------------------------- #
# # Changing expiry from cookie created
# # ---------------------------------------------------------------------------- #

# _original_init = streamlit_cookies_manager.CookieManager.__init__

# def _patched_init(self, *args, expiry_min=10, **kwargs):
#     _original_init(self, *args, **kwargs)
#     self._default_expiry = datetime.now() + timedelta(minutes=expiry_min)

# streamlit_cookies_manager.CookieManager.__init__ = _patched_init

# # Now all CookieManager (and thus EncryptedCookieManager) use 10 mins by default

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
#     if st.session_state.authenticated == True:
#         if st.button("Logout", key="btn_logout"):
#             st.session_state.authenticated = False
#             if "athl" in cookies:
#                 del cookies["athl"]
#             cookies.save()
#             st.session_state.pop('athl', None)
#             st.session_state.pop('CookieManager.queue', None)
#             st.cache_data.clear()
#             st.rerun()
#             log_in()

# import streamlit as st
# import hashlib
# import uuid
# from datetime import datetime, timedelta

# import streamlit_cookies_manager
# from streamlit_cookies_manager.cookie_manager import CookieManager as _BaseCM
# from streamlit_cookies_manager.encrypted_cookie_manager import EncryptedCookieManager as _BaseECM
# from streamlit_cookies_manager import CookieManager, EncryptedCookieManager

# from utils.functions import get_conn_and_df, UpdateDB


# # -----------------------------------------------------------------------------
# # Patch CookieManager to default to 10-minute expiry
# # -----------------------------------------------------------------------------
# _original_init = streamlit_cookies_manager.CookieManager.__init__
# def _patched_init(self, *args, expiry_min=10, **kwargs):
#     _original_init(self, *args, **kwargs)
#     self._default_expiry = datetime.now() + timedelta(minutes=expiry_min)

# streamlit_cookies_manager.CookieManager.__init__ = _patched_init

# _orig_run = _BaseCM._run_component
# def _patched_run(self, save_only: bool, key: str):
#     """
#     Override the component key to be unique per‐instance, based on prefix.
#     """
#     # strip any trailing slash from prefix for cleaner key
#     p = self._prefix.rstrip("/")
#     suffix = ".save" if save_only else ""
#     unique_key = f"{p or 'cm' }{suffix}"
#     return _orig_run(self, save_only=save_only, key=unique_key)

# # Apply the patch to both the raw and encrypted managers
# _BaseCM._run_component = _patched_run
# _BaseECM._run_component = _patched_run

# # ------------------------------------------------------------
# # 1. Raw CookieManager to hold the session_id in a non‐encrypted cookie
# # ------------------------------------------------------------
# raw_cm = _BaseCM(prefix="crossfit83/session", path="/")
# if not raw_cm.ready():
#     st.stop()

# session_id = raw_cm.get("session_id")
# if session_id is None:
#     session_id = str(uuid.uuid4())
#     raw_cm["session_id"] = session_id
#     raw_cm.save()


# # ------------------------------------------------------------
# # 2. EncryptedCookieManager for storing “athl”
# # ------------------------------------------------------------
# _creds = get_conn_and_df("Credentials")
# _secret = _creds.loc[_creds.username.eq("COOKIES_SECRET"), "password"].iat[0]

# cookies = _BaseECM(
#     prefix=f"crossfit83/{session_id}/", 
#     password=_secret
# )
# if not cookies.ready():
#     st.stop()


# # -----------------------------------------------------------------------------
# # 3. Helpers
# # -----------------------------------------------------------------------------
# def hash_password(pw: str) -> str:
#     return hashlib.sha256(pw.encode()).hexdigest()

# def load_user_db():
#     return get_conn_and_df("Credentials")

# def get_current_user() -> str | None:
#     return cookies.get("athl")

# def is_authenticated() -> bool:
#     resp = False
#     if  get_current_user() is not None :
#         if get_current_user() != 'Relog' :
#             resp = True
#     else :
#         resp = False
#     return resp


# # -----------------------------------------------------------------------------
# # 4. Auth Dialog
# # -----------------------------------------------------------------------------
# @st.dialog("🔐 Authentication")
# def _auth_dialog():
#     choice = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)

#     if choice == "Log In":
#         user = st.text_input("Username")
#         pw   = st.text_input("Password", type="password")
#         if st.button("Login", type="primary"):
#             db = load_user_db()
#             if (
#                 user in db.username.values
#                 and db.loc[db.username.eq(user), "password"].iat[0]
#                     == hash_password(pw)
#             ):
#                 cookies["athl"] = user
#                 cookies.save()
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")

#     else:  # Sign Up
#         new_u = st.text_input("New Username")
#         pw1   = st.text_input("Password", type="password")
#         pw2   = st.text_input("Repeat Password", type="password")
#         if st.button("Sign Up", type="primary"):
#             db = load_user_db()
#             if not new_u or not pw1:
#                 st.error("All fields are required")
#             elif new_u in db.username.values:
#                 st.error("Username already exists")
#             elif pw1 != pw2:
#                 st.error("Passwords do not match")
#             else:
#                 pwd_h = hash_password(pw1)
#                 UpdateDB(db,
#                          {"username": new_u, "password": pwd_h},
#                          sheet_name="Credentials")
#                 cookies["athl"] = new_u
#                 cookies.save()
#                 st.rerun()


# # -----------------------------------------------------------------------------
# # 5. Login / Logout helpers
# # -----------------------------------------------------------------------------
# def require_login():
#     if not is_authenticated():
#         _auth_dialog()
#         st.stop()

# def logout_button():
#     if is_authenticated() and st.button("Logout"):
#         st.session_state.pop('CookieManager.queue', None)
#         st.cache_data.clear()
#         cookies["athl"] = "Relog"
#         st.rerun()
#         require_login()
