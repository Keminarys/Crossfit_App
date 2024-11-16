### Librairies

import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from pytube import YouTube, Playlist
# import yaml
# from yaml.loader import SafeLoader

# with open('/mount/src/crossfit_app/config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )
### Function 
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas

@st.dialog("Consulter mes RM",  width="large")
def get_best_rm(df, athl) :
    st.write("Voici vos meilleurs performances pour chaque exercice")
    st.divider()
    temp = df.loc[(df.Category == "WEIGHTLIFTING") & (df['Profil'] == athl)]
    temp = temp.groupby(["Exercice", "RM"]).agg({"Perf" : "max"}).reset_index()
    selection = st.pills("Exercice", temp["Exercice"].unique().tolist(), selection_mode="single")
    temp = temp.loc[temp.Exercice == selection]
    return st.dataframe(temp, use_container_width=True, hide_index = True)

### Variable
# authenticator.login()
# if st.session_state["authentication_status"]:
#     authenticator.logout()
conn = get_conn()
all_mvmt = get_df("All_mvmt")
all_mvmt = all_mvmt[['Category','Exercice','Units']].dropna()

df = get_df("Progression")
df = df[['Profil','Category','Exercice','Date','Perf','Unité','RM','Commentaire']].dropna()
    
df_name = get_df("Profils")
df_name = df_name[['Name']].dropna()

df_obj = get_df("Objectif")
df_obj = df_obj[['Name','Task','Description','Start','Finish','Completed']].dropna()
df_obj['Start'] = pd.to_datetime(df_obj['Start'], format='%d/%m/%Y')
df_obj['Finish'] = pd.to_datetime(df_obj['Finish'], format='%d/%m/%Y')

berger = get_df("berger")

list_name = list(df_name["Name"].unique())
list_name = [x for x in list_name if str(x) != "nan"]
list_rm = [i for i in range (1,11)]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
dico_units = all_mvmt[['Exercice','Units']].drop_duplicates().set_index('Exercice').to_dict()['Units']

### Main

st.title('Crossfit83 Le Beausset')
st.divider()
st.subheader('Si c\'est votre première visite merci d\'ajouter votre profil dans la barre latérale')
st.write('_Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
st.divider()
athl = st.selectbox('Choix du profil', list_name)
st.divider()

with st.sidebar.expander("Ajout d'un nouveau profil") :
    
    new_ppl = st.text_input('Ecrire votre nom ici')
    if st.button('Ajouter mon profil') :
        df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl}, index=[len(df_name)])], ignore_index=True)
        df_newname = conn.update(worksheet="Profils",data=df_newname)
        st.cache_data.clear()
        st.rerun()

with st.sidebar.expander("Ajout d'un WOD/Exercice non présent dans la liste") :
    
    new_cat = st.selectbox("Sélectionnez la catégorie", list(dico_ex.keys()))
    new_ex = st.text_input("Nom de l'exercice")
    new_units = st.selectbox("Sélectionnez l'unité adéquat", list(all_mvmt['Units'].unique()))
    if st.button('Ajouter l\'exercice à la base de données') :
        df_newexo = pd.concat([all_mvmt, pd.DataFrame({'Category' : new_cat, 
                                                      'Exercice' : new_ex ,
                                                      'Units' : new_units}, index=[len(all_mvmt)])], ignore_index=True)
        df_newexo = conn.update(worksheet="All_mvmt",data= df_newexo)
        st.write('Ajouté avec succès, la page va se rafraîchir automatiquement ✅')
        st.cache_data.clear()
        st.rerun()

tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(["🎉 Nouvelle Performance", "📈 Aperçu de la progression", "📊 Data", "💪🎯 Objectifs", "🖥️ Table de Berger","🏋️‍♂️🤖 WOD Generator", "🥇🏋️‍♂️ Démonstration Mouvement"])

with tab1 :
    cat = st.selectbox('Choix de la catégorie', list(dico_ex.keys()))
    ex = st.selectbox('Choix de l"exercice', dico_ex[cat])
    if cat == 'WEIGHTLIFTING' : 
        rm = st.selectbox('Choix du RM', list_rm)
    else : rm = 1
    if dico_units[ex] == 'HH:MM:SS' :
       nb = st.text_input('Temps au format HH\:MM\:SS', "00:00:00")
    else : nb = st.number_input('Max reps/charge', step=1)
    date = st.date_input('Date de réalisation', value = "today")
    unit = dico_units[ex]
    if cat == "WOD":
        commentary = st.text_input('Commentaire sur la réalisation', 'Rien')
    else : commentary = 'Rien'
    new_entry = {'Profil' : athl,
                'Category' : cat,
                'Exercice' : ex,
                'Date' : date,
                'Perf' : nb,
                'Unité' : unit,
                'RM' : rm, 
                'Commentaire' : commentary}
    if st.button('Ajouter un nouveau record à mon profil :muscle:') :
        df_record = pd.concat([df, pd.DataFrame(new_entry, index=[len(df)])], ignore_index=True)
        df_record = conn.update(worksheet="Progression",data=df_record)
        st.write('Ajouté avec succès, vous pouvez retrouver toutes vos performances dans l\'onglet Data ✅')
        st.cache_data.clear()
        st.rerun()
  
with tab2 : 
    st.write('Sélectionner un mouvement spécifique pour avoir un aperçu de votre progression')
    data_full_scoped = df.loc[df['Profil'] == athl]
    data_grouped =  data_full_scoped.groupby(['Category', 'Exercice']).count().reset_index()
 
    fig = px.bar(data_grouped, x="Category", y="Perf", color="Exercice")
    fig.update_layout(
            title="Répartitions des performances",
                xaxis_title="Categories",
                yaxis_title="Nombre d\'entrées",
                autosize=False,
                width=500,
                height=300)
    st.plotly_chart(fig,use_container_width=True)
    st.divider()
    selected_cat = st.selectbox('Choix de la catégorie', list(data_full_scoped.Category.unique()))
    selected_ex = st.multiselect('Choix de la catégorie', list(data_full_scoped.loc[data_full_scoped['Category'] == selected_cat]['Exercice'].unique()))
   
    data_graph = data_full_scoped.loc[(data_full_scoped['Category'] == selected_cat) & (data_full_scoped['Exercice'].isin(selected_ex))]
    data_graph['Exo_RM'] = data_graph['Exercice'] + '// RM : ' +data_graph['RM'].astype(str)
    fig_line = px.line(data_graph,x="Date", y="Perf", color='Exo_RM', markers=True)
    st.plotly_chart(fig_line,use_container_width=True)
  
with tab3 :
    st.write('Vous pouvez consulter l\'entièreté de vos performances ci dessous.')
    data_perso = df.loc[df['Profil'] == athl].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
    st.dataframe(data_perso)

with tab4 :
    st.write('Vous pouvez alimenter le tableau ci dessous pour définir un programme pour atteindre un objectif')
    edited_obj = st.data_editor(df_obj, num_rows='dynamic', hide_index=True)
    if st.button('Mettre à jour mes objectifs') :
        df_obj_edit = conn.update(worksheet="Objectif",data=edited_obj)
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.write('Ici vous retrouverez la visualisation graphique !')
    fig_gantt = px.timeline(df_obj[df_obj['Name'] == athl], x_start="Start", x_end="Finish", y="Description", color="Task")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt,use_container_width=True)

with tab5 : 
    st.write("Afin d'atteindre votre charge de travail le plus efficacement possible, vous pouvez utiliser cette table de Berger personnalisée")
    explaination = pd.DataFrame(
    {
        "REPS": ["1 à 6", "7 à 10", "11 à 15"],
        "Benefice": ["Force", "Volume Hypertrophie", "Endurance"],
        "Repos": ["3'+", "2'-3'", "2'"],
        "Nb de series": ["3 à 5", "6", "8"]
    }
)
    st.dataframe(explaination,hide_index=True, use_container_width=True)
    st.divider()
    st.write("Si vous souhaitez consulter vos meilleurs RM, cliquez sur le bouton ci dessous")
    
    if "get_best_rm" not in st.session_state:
        if st.button("Consulter mes RM"):
            get_best_rm(data_perso, athl)
    repMax = st.number_input('Votre RM max (RM1/2/3/5 etc) (indiquez seulement le chiffre)', step=1)
    chargeMax = st.number_input('Votre charge max pour ce RM (indiquez seulement le chiffre)', step=1)

    if repMax and chargeMax != 0 :
        updatedBerger = berger.copy()
        updatedBerger.at[int(repMax), "Charge"] = chargeMax
        st.dataframe(updatedBerger, use_container_width=True, hide_index = True)

with tab7 :
    st.write("Vous pouvez voir chaque mouvement officiel issu de la chaîne YouTube officielle de CrossFit©️")
    on = st.toggle("Voir la liste des mouvements ?")

    if on : 
        @st.cache_data  
        def getVideoLink() : 
            video_links = Playlist("https://www.youtube.com/playlist?list=PLdWvFCOAvyr1qYhgPz_-wnCcxTO7VHdFo").video_urls
            return list(video_links)
        @st.cache_data 
        def getVideoTitle(video_links):
            video_titles = []
            for link in video_links:
                video_titles.append(YouTube(link).title)
            return video_titles

        with st.status("Chargement de la playlist CrossFit©️ ...", expanded=True) as status:
            st.write("Recherche de la playlist YouTube ...")
            video_links = getVideoLink() 
            st.write("Création de la liste contenant les titres des vidéos ...")
            video_titles = getVideoTitle(video_links)
            status.update(label="Chargement Terminé !", state="complete", expanded=False)
        
        title_id = st.selectbox('Quel mouvement voulez vous voir ?',video_titles)
        video_url = video_links[video_titles.index(title_id)]
        st.video(video_url)
# elif st.session_state["authentication_status"] is False:
#    st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')
