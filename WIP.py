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

def display_card(page_name, page_link):
    st.markdown(f"""
        <a href='{page_link}' style="text-decoration: none;'>
            <div style='
                background-color: #E63946; 
                padding: 20px; 
                margin: 10px; 
                border-radius: 10px; 
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                color: white;
                box-shadow: 5px 5px 10px rgba(0,0,0,0.3);
                transition: 0.3s ease-in-out;
                '>
                {page_name}
            </div>
        </a>
    """, unsafe_allow_html=True)


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

    col1, col2 = st.columns(2) 
    with col1 :
        display_card(pages[0], f"/{pages[0]}")
    with col2 :
        display_card(pages[1], f"/{pages[1]}")
    col3, col4 = st.columns(2)    
    with col3 :
        display_card(pages[2], f"/{pages[2]}")
    with col4 :
        display_card(pages[3], f"/{pages[3]}")
if __name__ == "__main__":
    main()

