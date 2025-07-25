import streamlit as st

from utils.functions import get_conn_and_df, UpdateDB
from utils.ui_helpers import render_navbar

import pandas as pd
import numpy as np
import datetime
import re
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(layout="wide")

def main():
    
    if not st.user.is_logged_in:
        if st.button("Log in with Google"):
            st.login("google")
            st.stop()
    nav, log = st.columns([8,1])
    with nav : 
        render_navbar([
            ("Votre Profil",    "profiles_page"),
            ("Votre Progression","progress"),
            ("Ressources Crossfit","ressources"),
            ("Programmation",   "scheduleResa"),
        ])
    with log : 
        if st.button("Log out"):
            st.logout()

    if st.user.is_logged_in :
        title, logo = st.columns([3, 1])
        with title:
            stUserChangeDF = get_conn_and_df("CorrespondanceSTUser")
            OgDict = dict(zip(stUserChangeDF['Original'], stUserChangeDF['NewValue']))
            if st.user.name in OgDict.keys() : 
                athl = OgDict[st.user.name]
            else : athl = st.user.name
            st.title('Crossfit83 Le Beausset')
            st.write(f"Bienvenue, {athl}!")
            if st.user.name not in OgList.keys() : 
                st.write(f"Le nom associé à votre compte google est le suivant : {st.user.name}, souhaitez vous apparaître sous un autre nom ?")
                on = st.toggle("Changer de Nom")
                if on :
                    newname = st.text_input("Nouveau Nom")
                    if st.button("Valider"):
                        change = {"Original" : st.user.name,
                            "NewValue" : newname}
                        UpdateDB(stUserChangeDF, change, "CorrespondanceSTUser")
        with logo:
            st.image("LogoCrossfit.jpg")

if __name__ == "__main__":
    main()
