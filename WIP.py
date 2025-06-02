import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa
import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date


PAGES = {
    "Votre Profil": "pages/profiles_page.py",
    "Votre Progression": "pages/progress.py",
    "Ressources Technique Crossfit": "pages/ressources.py",
    "Prog de la semaine": "pages/scheduleResa.py"
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
                background: linear-gradient(45deg, #D62828, #E63946); /* Fiery gradient */
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Bebas Neue', sans-serif; /* Strong athletic font */
                padding: 35px;
                border-radius: 15px;
                border: 2px solid black;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0px 5px 10px rgba(0,0,0,0.4);
                transition: 0.3s;
            }
            div.stButton > button:hover {
                background: linear-gradient(45deg, #C70039, #900D0D); /* Darker punch effect */
                box-shadow: 0px 8px 16px rgba(0,0,0,0.5);
                transform: scale(1.05);
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

