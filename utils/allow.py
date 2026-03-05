import hmac, hashlib
from utils.functions import get_conn_and_df, UpdateDB
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import numpy as np

def hmac_email(email: str) -> str:
    secret_key = st.secrets["key_h"]["allowlist_hmac_key"]
    normalized = email.strip().lower().encode()
    return hmac.new(secret_key.encode(), normalized, hashlib.sha256).hexdigest()
  
def add_allowed_email(email: str, sheet_name: str):
    df = get_conn_and_df(sheet_name)
    new_entry = {
        "email_hmac": hmac_email(email)
    }
    UpdateDB(df, new_entry, sheet_name)
  
def is_email_allowed(email: str, sheet_name: str) -> bool:
    df = get_conn_and_df(sheet_name)
    if df.empty:
        return False
    hashed = hmac_email(email)
    return hashed in df["email_hmac"].astype(str).values
