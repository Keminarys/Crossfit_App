import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa
import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date


PAGES = {
    "Profile": profiles_page,
    "Progession": progress,
    "Ressources Technique": ressources,
    "Prog de la semaine": scheduleResa
}

### Setting up the page 

st.set_page_config(layout="wide")
### Function 
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas

def display_card(page_name):
    st.markdown(f"""
    <a href='/{page_name}' style='text-decoration: none;'>
    <div style='background-color: red; padding: 20px; margin: 10px; border-radius: 0; text-align: center;'>
    <h2 style='color: white;'>{page_name}</h2>
    </div>
    </a>
    """, unsafe_allow_html=True)

def main():
    
    # conn = get_conn()
    # df_name = get_df("Profils")
    # df_name = df_name[['Name']].dropna()
    
    st.title('Crossfit83 Le Beausset')
    st.divider()
    st.header("Pages")
    pages = PAGES.keys()
    for page in pages:
        display_card(page)

if __name__ == "__main__":
    main()
