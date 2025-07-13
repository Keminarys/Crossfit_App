import streamlit as st

from utils.auth import login_ui, logout_ui
from utils.functions import get_conn_and_df
from utils.ui_helpers import render_navbar

import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(layout="wide")

def main():

    login_ui()
    nav_col, logout_col = st.columns([8, 1])

    with nav_col:
        render_navbar([
            ("Votre Profil",    "profiles_page"),
            ("Votre Progression","progress"),
            ("Ressources Crossfit","ressources"),
            ("Programmation",   "scheduleResa"),
        ])

    with logout_col:
        logout_ui()

    title, logo = st.columns([3, 1])
    with title:
        st.title('Crossfit83 Le Beausset')
        st.write(f"Bienvenue, {st.session_state.athl}!")
        st.write(st.session_state)
    with logo:
        st.image("LogoCrossfit.jpg")

if __name__ == "__main__":
    main()
