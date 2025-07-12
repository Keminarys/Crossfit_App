import streamlit as st

from utils.auth import login_ui
from utils.functions import get_conn_and_df
from utils.ui_helpers import render_page_links

from pages import profiles_page,  progress, ressources, scheduleResa

import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date

 
st.set_page_config(layout="wide")

def main():

    render_page_links([
    ("Menu Principal", "Home"),
    ("Votre Profil", "profiles_page"),
    ("Votre Progression", "progress"),
    ("Ressources Crossfit", "ressources"),
    ("Programmation", "scheduleResa"),
])
    
    if current_tab == "home":
        login_ui()  
        title, logo = st.columns([3,1])
        with title :
            st.title('Crossfit83 Le Beausset')
            st.write(f"Bienvenue, {st.session_state.athl}!")
        with logo :
            st.image("LogoCrossfit.jpg")

if __name__ == "__main__":
    main()

