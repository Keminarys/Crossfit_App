import streamlit as st 
import requests 
import json 
from google.oauth2 import service_account 
from utils.functions import get_conn_and_df, load_drive_json, newName, build_agraph_nodes_edges, get_video_for_movement, get_name_from_id, UpdateDB, compute_weighted_progress
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
                 mastered_df["mastered"] = mastered_df["mastered"].apply(json.loads)
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
                     progress = compute_weighted_progress(movements, progressState["mastered"])
                     st.markdown(f"### 📊 Progression pondérée : **{progress['progress_pct']}%**")
                     st.progress(progress["progress_pct"] / 100)
                     st.subheader("Arbre interactif")
                     nodes, edges = build_agraph_nodes_edges(movements, progressState.get('mastered', None))
                     config = Config(
                               width="100%",
                               height=650,
                               directed=True,
                               physics=False,
                               hierarchical={
                                   "enabled": True,
                                   "direction": "UD",         
                                   "sortMethod": "directed",
                                   "nodeSpacing": 120,        
                                   "levelSeparation": 180,    
                                   "treeSpacing": 200,         
                                   "blockShifting": False,    
                                   "edgeMinimization": False, 
                                   "parentCentralization": True
                               },
                               nodeHighlightBehavior=True,
                               highlightColor="#FFFFFF"
                           )

                     clicked_node = agraph(nodes=nodes, edges=edges, config=config)
                     if clicked_node:
                              nid = str(clicked_node)
                              st.session_state["last_clicked"] = nid
                              mv = next((m for m in movements if str(m["id"]) == nid), None)
                              if mv:
                                       st.subheader(f"📌 {mv['name']}")
                                       video_url = get_video_for_movement(mv, lang='en')
                                       with st.expander("Vidéo démonstration"):
                                                if video_url:
                                                         st.video(video_url)
                                                else:
                                                         st.info("Aucune vidéo trouvée.")
                                       if nid in st.session_state["selected_nodes"]:
                                                st.session_state["selected_nodes"].remove(nid)
                                       else:
                                                st.session_state["selected_nodes"].append(nid)
                           
                     else:
                              st.info("Cliquez sur un nœud pour afficher sa vidéo.")

                 @st.dialog("Enregistrer mes progrès",  width="large")
                 def save_mastered_skills(df, athl) :
                          mastered_names = [get_name_from_id(movements, nid)for nid in st.session_state["selected_nodes"]]
                          mastered_id = [x for x in st.session_state["selected_nodes"]]
                          st.markdown(f"### 🟩 Exercices maîtrisés \n{mastered_names}")
                          st.write("Sauvegarder le progrès dans la base de données ?")
                          if st.button('Oui !') :
                                   df_new = df.loc[df.id != athl]
                                   if athl in df.id.unique():
                                            already_mastered = df.loc[df.id == athl]['mastered'].tolist() 
                                            mastered_id = mastered_id + already_mastered
                                   new_entry = {
                                            "id" : athl,
                                            "mastered" : json.dumps(mastered_id)
                                   }
                                   UpdateDB(df_new, new_entry, "calistenicPathway")
                                   st.cache_data.clear()
                                   del st.session_state["selected_nodes"]
                                   st.rerun()
                          
                 if len(st.session_state["selected_nodes"]) > 0 :
                          if st.button("Consulter et Enregistrer mes progrès"):
                                   save_mastered_skills(mastered_df, athl)
                     
                              


