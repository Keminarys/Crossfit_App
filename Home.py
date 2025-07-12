import streamlit as st

from utils.auth import login_ui
from utils.functions import get_conn_and_df
from utils.ui_helpers import render_nav_bar

from pages.profiles_page import profilPage
from pages.progress import progressPage
from pages.ressources import RessourcesPage
from pages.scheduleResa import resaPage

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
  
st.set_page_config(layout="wide")

def main():
    TABS = [
        ("Menu Principal", "home"),
        ("Votre Profil", "profiles"),
        ("Votre Progression", "progress"),
        ("Ressources Crossfit", "resources"),
        ("Programmation", "schedule"),
    ]
    
    current_tab = render_nav_bar(TABS, default_key="home")
    
    if current_tab == "home":
        login_ui()  
        title, logo = st.columns([3,1])
        with title :
            st.title('Crossfit83 Le Beausset')
            st.write(f"Bienvenue, {st.session_state.athl}!")
        with logo :
            st.image("LogoCrossfit.jpg")
    elif current_tab == "profiles":
        profilPage()
    elif current_tab == "progress":
        progressPage()     
    elif current_tab == "resources":
        RessourcesPage()
    elif current_tab == "schedule":
        resaPage()
if __name__ == "__main__":
    main()

