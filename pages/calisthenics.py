import streamlit as st 
import requests 
import json 
import dash
import dash_cytoscape as cyto
from dash import html
from google.oauth2 import service_account 
from utils.functions import get_conn_and_df, load_drive_json
from utils.ui_helpers import render_navbar
from streamlit_cytoscapejs import st_cytoscapejs

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
                elements = []
                for item in movements:
                        node_id = item["id"]
                        node_classes = ""
                        #node_classes = "mastered" if node_id in st.session_state.selected_nodes else ""
        
                        elements.append({
                            "data": {"id": node_id, "label": item["name"]},
                            "classes": node_classes
                        })
                
                for nxt in item.get("progressions_to", []):
                        elements.append({
                        "data": {"source": node_id, "target": nxt}})
                clicked = st_cytoscapejs(
                    elements=elements,
                    layout={"name": "breadthfirst"},
                    stylesheet=[
                        {"selector": "node", "style": {"background-color": "#88c", "label": "data(label)"}},
                        {"selector": ".mastered", "style": {"background-color": "green"}}
                    ],
                    key="skilltree"
                )

        
# if st.user.is_logged_in:
#         st.set_page_config(layout="wide")
#         athl = newName()
#         creds = service_account.Credentials.from_service_account_info(
#         st.secrets["connections"]["gsheets"],
#         scopes=["https://www.googleapis.com/auth/drive"]
#         )
#         file_id = st.secrets["drive"]["json_file_id"]
#         data = load_drive_json(file_id, creds)
#         movements = data[0]["movements"]
#         progress_data = get_conn_and_df("calistenicPathway")
#         try:
#                 progress_data_id = progress_data.loc[progress_data.id == athl].to_dict()
#         except:
#                 progress_data = {"id": athl, "mastered": []}
        
#         mastered = set(progress_data["mastered"])
#         if "selected_nodes" not in st.session_state:
#                 st.session_state.selected_nodes = set(mastered)
#         elements = []
#         for item in movements:
#                 node_id = item["id"]
#                 node_classes = "mastered" if node_id in st.session_state.selected_nodes else ""
        
#                 elements.append({
#                     "data": {"id": node_id, "label": item["name"]},
#                     "classes": node_classes
#                 })
                
#         for nxt in item.get("progressions_to", []):
#                 elements.append({
#                 "data": {"source": node_id, "target": nxt}})
#                 st.subheader("Votre Skill Tree")
#                 clicked = cytoscape(
#                         elements=elements,
#                         layout={"name": "breadthfirst"},
#                         stylesheet=[
#                             {"selector": "node", "style": {"background-color": "#88c", "label": "data(label)"}},
#                             {"selector": ".mastered", "style": {"background-color": "green"}}
#                         ],
#                         key="skilltree")
#         if clicked and "id" in clicked:
#                 node_id = clicked["id"]
        
#         if node_id in st.session_state.selected_nodes:
#                 st.session_state.selected_nodes.remove(node_id)
#         else:
#                 st.session_state.selected_nodes.add(node_id)
#                 st.rerun()
#         st.markdown("---")
#         if st.button("💾 Sauvegarder la progression"):
#                 new_mastered = list(st.session_state.selected_nodes)
#                 progressCalistenics(progress_data, athl, new_mastered, 'calistenicPathway')
#                 st.success("Progression sauvegardée !")
