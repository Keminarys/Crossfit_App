import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa
from utils.auth import login_ui
from utils.functions import get_conn_and_df
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

def fab_selector():
    st.markdown("""
        <style>
            .fab-container {
                position: fixed;
                bottom: 30px;
                right: 30px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                z-index: 1000;
            }

            .fab-button {
                width: 55px;
                height: 55px;
                border-radius: 50%;
                background: linear-gradient(135deg, #FF6B6B, #F06543);
                color: white;
                font-size: 22px;
                font-weight: bold;
                border: none;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .fab-button:hover {
                transform: scale(1.1);
                box-shadow: 0px 6px 12px rgba(0,0,0,0.4);
            }
        </style>

        <div class="fab-container">
            <button class="fab-button" onclick="window.location.href='/pages/profiles_page.py'">👤</button>
            <button class="fab-button" onclick="window.location.href='/pages/progress.py'">📊</button>
            <button class="fab-button" onclick="window.location.href='/pages/ressources.py'">📚</button>
            <button class="fab-button" onclick="window.location.href='/pages/scheduleResa.py'">📅</button>
        </div>
    """, unsafe_allow_html=True)
    
st.set_page_config(layout="wide")
### Function 
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
    
    login_ui()  
    fab_selector()
    title, logo = st.columns([3,1])
    with title :
        st.title('Crossfit83 Le Beausset')
        st.write(f"Bienvenue, {st.session_state.athl}!")
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

