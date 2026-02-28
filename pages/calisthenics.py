import streamlit as st 
import requests 
import json 
import dash
import dash_cytoscape as cyto
from dash import html
from google.oauth2 import service_account 
from utils.functions import load_drive_json
from utils.ui_helpers import render_navbar

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

with log:
    if st.button("Log out"):
            st.logout()

if st.user.is_logged_in :
        st.set_page_config(layout="wide")
        creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["gsheets"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        file_id = st.secrets["drive"]["json_file_id"]
        data = load_drive_json(file_id, creds)
        
