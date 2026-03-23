import streamlit as st 
import requests 
import json 
from google.oauth2 import service_account 
from utils.functions import get_conn_and_df, load_drive_json, newName, build_agraph_nodes_edges, get_video_for_movement
from utils.allow import is_email_allowed, get_user_role, add_allowed_email
from utils.ui_helpers import render_navbar
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Config
         
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
                 if "selected_nodes" not in st.session_state:
                          st.session_state["selected_nodes"] = []  # liste de strings
                 if "last_clicked" not in st.session_state:
                          st.session_state["last_clicked"] = None
                 if len(selected_tree) > 0 :
                     idx_skill_tree = all_tree_list.index(selected_tree)
                     movements = data[idx_skill_tree]["movements"]                 
                     st.subheader("Arbre interactif")
                     nodes, edges = build_agraph_nodes_edges(movements)
                     config = Config(
                                    width="100%",
                                    height=550,
                                    directed=True,
                                    physics=False,
                                    hierarchical={
                                            "enabled": True,
                                            "direction": "LR",
                                            "sortMethod": "directed",
                                            "nodeSpacing": 180,
                                            "levelSeparation": 220,
                                            "blockShifting": True,
                                            "edgeMinimization": True},
                                    nodeHighlightBehavior=True,
                                    highlightColor="#FFFFFF"
                                )
                     clicked_node = agraph(nodes=nodes, edges=edges, config=config)
                     if clicked_node:
                              nid = str(clicked_node)
                              st.session_state["last_clicked"] = nid
                              if nid in st.session_state["selected_nodes"]:
                                       st.session_state["selected_nodes"].remove(nid)
                              else:
                                       st.session_state["selected_nodes"].append(nid)
                              selected = st.session_state.get("last_clicked")
                              if selected:
                                       mv = next((m for m in movements if str(m["id"]) == str(selected)), None)
                                       video_url = get_video_for_movement(mv, lang='en')
                                       with st.expander("Video démonstration") :
                                                if video_url:
                                                         st.video(video_url)
                                                else:
                                                         st.info("Aucune vidéo trouvée.")
                     else:
                              st.info("Cliquez sur un nœud pour afficher sa vidéo.")
                     if len(st.session_state["selected_nodes"]) > 0 :
                              list_mastered = [x for x in st.session_state["selected_nodes"]]
                              st.markdown(f"Les exercices suivant sont renseignés comme maitrisés : {list_mastered}")



