import streamlit as st 
import requests 
import json 
from google.oauth2 import service_account 
from utils.functions import get_conn_and_df, load_drive_json, build_pyvis_tree, render_tree, get_clicked_node
from utils.ui_helpers import render_navbar
import graphviz
import tempfile
import streamlit.components.v1 as components


         
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
        all_tree_list = []
        for i in range(0,len(data)):
          tree = data[i]['movements'][0]['skill_tree_links']
          all_tree_list.append(tree[0])
        st.title("Bienvenue sur la page spéciale Calisthénie !")
        st.divider()
        selected_tree = st.selectbox("Quel arbre de compétence voulez vous voir ?", all_tree_list)
        if len(selected_tree) > 0 :
                 idx_skill_tree = all_tree_list.index(selected_tree)
                 movements = data[idx_skill_tree]["movements"]
                 if "completed" not in st.session_state:
                      st.session_state["completed"] = set()
                 col1, col2 = st.columns([3, 2])
                 with col1:
                          st.subheader(f"Arbre interactif : {selected_tree}")
                          render_tree(movements)
                 with col2:
                          st.subheader("Détails du mouvement")
                          clicked_id = get_clicked_node()
                          if clicked_id: 
                                   mv = next((m for m in movements if m["id"] == clicked_id), None)
                                   if mv:
                                       st.markdown(f"### {mv['name']}")
                                       st.write(f"**Niveau :** {mv['level']}")
                                       st.write(f"**Muscles :** {', '.join(mv['muscles'])}")
                                       st.write(f"**Description :** {mv['description']}")
                                       st.write(f"**Progressions vers :** {mv.get('progressions_to', [])}")
                                            
                                       if st.button("Marquer comme complété"):
                                           st.session_state["completed"].add(clicked_id)
                                           st.experimental_rerun()
