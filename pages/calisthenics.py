import streamlit as st 
import requests 
import json 
from google.oauth2 import service_account 
from utils.functions import get_conn_and_df, load_drive_json, render_tree, newName, show_calisthenics_tab, save_and_show_html_with_debug
from utils.allow import is_email_allowed, get_user_role, add_allowed_email
from utils.ui_helpers import render_navbar
import tempfile
import streamlit.components.v1 as components
import sys
from streamlit_agraph import agraph, Node, Edge, Config

def build_agraph_nodes_edges(movements):
    nodes = []
    edges = []
    for mv in movements:
        nid = str(mv["id"])
        nodes.append(Node(id=nid, label=mv.get("name", nid), size=22, color=mv.get("color", None)))
        for tgt in mv.get("progressions_to", []):
            edges.append(Edge(source=nid, target=str(tgt)))
    return nodes, edges
         
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
        user_email = st.user.email
        allowed, role = get_user_role(user_email, "allowList")
        if not allowed:
            st.error("Authenticated but NOT authorized.")
            st.stop()
            
        else : 
                 st.set_page_config(layout="wide")
                 creds = service_account.Credentials.from_service_account_info(
                 st.secrets["connections"]["gsheets"],
                 scopes=["https://www.googleapis.com/auth/drive.readonly"]
                 )
                 file_id = st.secrets["drive"]["json_file_id"]
                 data = load_drive_json(file_id, creds)
                 all_tree_list = []
                 mastered_df = get_conn_and_df("calistenicPathway")
                 athl = newName()
                 for i in range(0,len(data)):
                   tree = data[i]['movements'][0]['skill_tree_links']
                   all_tree_list.append(tree[0])
                 st.title(f"Bienvenue sur la page spéciale Calisthénie {athl}!")
                 st.divider()
                 if athl in mastered_df.id.unique().tolist() : 
                          progressState = mastered_df[mastered_df['id'] == athl].iloc[0].to_dict()
                 else : 
                          progressState = {'id' : athl, 
                            'mastered' : []}
                 selected_tree = st.selectbox("Quel arbre de compétence voulez vous voir ?", all_tree_list)
                 if "selected_node" not in st.session_state:
                      st.session_state["selected_node"] = None
                  
                 st.subheader("Arbre interactif")
                 nodes, edges = build_agraph_nodes_edges(movements)
                  
                 config = Config(
                      width="100%",
                      height=550,
                      directed=True,
                      physics=False,
                      hierarchical=True,  # active si vous voulez layout hiérarchique
                      nodeHighlightBehavior=True
                  )
                  
                 clicked_node = agraph(nodes=nodes, edges=edges, config=config)
                  
                  # agraph renvoie l'id du nœud cliqué (ou None)
                 if clicked_node:
                      st.session_state["selected_node"] = clicked_node
                  
                 selected = st.session_state.get("selected_node")
                 id_to_video = {str(mv["id"]): mv.get("video") or mv.get("video_url") for mv in movements}
                  
                 if selected:
                      st.markdown(f"**Sélectionné :** {selected}")
                      video_url = id_to_video.get(selected)
                      if video_url:
                          st.video(video_url)
                      else:
                          st.info("Aucune vidéo configurée pour ce mouvement.")
                 else:
                      st.info("Cliquez sur un nœud pour afficher sa vidéo.")


                 # if len(selected_tree) > 0 :
                 #          idx_skill_tree = all_tree_list.index(selected_tree)
                 #          movements = data[idx_skill_tree]["movements"]
                 #          st.subheader(f"Arbre interactif : {selected_tree}")
                 #          save_and_show_html_with_debug(movements)
                          
                          #show_calisthenics_tab(movements)


