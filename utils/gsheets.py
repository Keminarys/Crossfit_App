import pandas as pd
from streamlit_gsheets import GSheetsConnection

def get_conn() -> GSheetsConnection:
    return st.connection("gsheets", type=GSheetsConnection)

def get_df(sheet_name: str, conn: GSheetsConnection) -> pd.DataFrame:
    df = conn.read(worksheet=sheet_name)
    return df.dropna()
