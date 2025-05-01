import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa
import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date


PAGES = {
    "Votre Profil": profiles_page,
    "Votre Progession": progress,
    "Ressources Technique Crossfit": ressources,
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

def display_card(page_name, page_key):
    button_style = """
        <style>
            div.stButton > button {
                background-color: #E63946;
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 30px;
                border-radius: 20px;
                border: none;
                box-shadow: 6px 6px 12px rgba(0,0,0,0.3);
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background-color: #D62828;
                box-shadow: 8px 8px 16px rgba(0,0,0,0.4);
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    if st.button(page_name, key=page_key):
        st.switch_page(page_key)



def main():
    
    # conn = get_conn()
    # df_name = get_df("Profils")
    # df_name = df_name[['Name']].dropna()
    title, logo = st.columns([3,1])
    with title :
        st.title('Crossfit83 Le Beausset')
    with logo :
        st.image("LogoCrossfit.jpg")
    st.divider()
    st.header("Menu")
    pages = list(PAGES.keys())
    page_key = list(PAGES.values())
    col1, col2 = st.columns(2) 
    with col1 :
        display_card(pages[0], page_key[0])
    with col2 :
        display_card(pages[1], page_key[1])
    col3, col4 = st.columns(2)    
    with col3 :
        display_card(pages[2], page_key[2])
    with col4 :
        display_card(pages[3], page_key[3])
if __name__ == "__main__":
    main()

