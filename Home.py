import streamlit as st
from pages import profiles_page, progress, ressources, scheduleResa
from utils.auth import login_ui
from utils.functions import get_conn_and_df
from utils.ui_helpers import display_card, render_nav_bar
import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date

render_nav_bar()

PAGES = {
    "Votre Profil": "pages/profiles_page.py",
    "Votre Progression": "pages/progress.py",
    "Ressources Technique Crossfit": "pages/ressources.py",
    "Prog de la semaine": "pages/scheduleResa.py"
}
  
st.set_page_config(layout="wide")

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

