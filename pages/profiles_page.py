### Librairies

import pandas as pd
import numpy as np
import datetime
import random
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from utils.functions import get_conn_and_df, highlight_rows, ChartDataFS, UpdateDB
from utils.ui_helpers import render_navbar
#from utils.auth import login_ui, logout_ui
#from utils.auth import require_login, get_current_user, logout_button   


def data_perso(df) :
    athl = st.user.name
    temp = df.loc[df['Profil'] == athl].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
    return temp


if not st.user.is_logged_in:
        if st.button("Log in with Google"):
            st.login("google")
            st.stop()
nav_col, logout_col = st.columns([8, 1])

with nav_col:
    render_navbar([
        ("Votre Progression","progress"),
        ("Ressources Crossfit","ressources"),
        ("Programmation",   "scheduleResa"),
    ])

with logout_col:
    if st.button("Log out"):
        st.logout()



st.set_page_config(layout="wide")

all_mvmt = get_conn_and_df("All_mvmt")
all_mvmt = all_mvmt[['Category','Exercice','Units']].dropna()

df = get_conn_and_df("Progression")
df = df[['Profil','Category','Exercice','Date','Perf','Unité','RM','Commentaire']].dropna()


list_rm = [i for i in range (1,21)]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
sorted_dico_ex = sorted(list(dico_ex.keys()), key=lambda x: (x != 'WEIGHTLIFTING', x))
dico_units = all_mvmt[['Exercice','Units']].drop_duplicates().set_index('Exercice').to_dict()['Units']
all_units = list(all_mvmt["Units"].unique())

### Main


athl = st.user.name
st.title(f"Bienvenue sur ton profil {athl} :muscle:")

st.divider()
st.write("Cette page te permet de tracker tes PR.")
st.write("Pour ajouter un nouveau PR à ton profil, utilise le formulaire ci-dessous ! :arrow_down:")
st.divider()

cat = st.selectbox('Choix de la catégorie', sorted_dico_ex)
ex = st.selectbox('Choix de l"exercice', sorted(dico_ex[cat]))

if cat == 'AJOUTER UN EXERCICE' : 
    st.divider()
    newCat = st.selectbox('Catégorie de l\'exercice à ajouter', [key for key in sorted_dico_ex if key != "AJOUTER UN EXERCICE"])
    newex = st.text_input('Ajouter votre exercice', 'ici')
    if newCat == 'WEIGHTLIFTING' : 
        newrm = st.selectbox('Choix du RM', list_rm)
    else : newrm = 1  
    newunit = st.selectbox('Unité de l\'exercice', all_units)
    if newunit == 'HH:MM:SS' :
       newnb = st.text_input('Temps au format HH\:MM\:SS', "00:00:00")
    else : newnb = st.number_input('Max reps/charge', step=1)
    newdate = st.date_input('Date de réalisation', value = "today")
    newcommentary = st.text_input('Commentaire sur la réalisation', 'Rien')
    new_entry = {'Profil' : athl,
                'Category' : newCat,
                'Exercice' : newex,
                'Date' : newdate,
                'Perf' : newnb,
                'Unité' : newunit,
                'RM' : newrm, 
                'Commentaire' : newcommentary}
    new_WOD = {
        'Category' : newCat,
        'Exercice' : newex,
        'Units' : newunit
    }
else :

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
    UpdateDB(df, new_entry, "Progression")
    if cat == 'AJOUTER UN EXERCICE' : 
        UpdateDB(all_mvmt, new_WOD, "All_mvmt")
    st.write('Ajouté avec succès, vous pouvez retrouver toutes vos performances dans l\'onglet Data ✅')
    st.cache_data.clear()
    st.rerun()

st.divider()
st.write("Tu peux visualiser toutes tes performances dans le tableau ci-dessous !")
st.divider()

col1, col2 = st.columns(2)

with col1 :
    data_perso = data_perso(df)
    styled_df = data_perso.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

with col2 :
    fig = ChartDataFS(df, athl)
    st.plotly_chart(fig,use_container_width=True)
    
    st.divider()
    data_full_scoped = df.loc[df['Profil'] == st.user.name]
    selected_cat = st.selectbox('Choix de la catégorie', list(data_full_scoped.Category.unique()))
    selected_ex = st.multiselect('Choix de la catégorie', list(data_full_scoped.loc[data_full_scoped['Category'] == selected_cat]['Exercice'].unique()))
   
    data_graph = data_full_scoped.loc[(data_full_scoped['Category'] == selected_cat) & (data_full_scoped['Exercice'].isin(selected_ex))]
    if (len(selected_cat) > 0) and (len(selected_ex) > 0) and (data_graph["Unité"].unique().tolist()[0] == "HH:MM:SS") :
        data_graph = data_graph.assign(**data_graph[['Perf']].apply(pd.to_datetime, format='%H:%M:%S'))
    data_graph['Exo_RM'] = data_graph['Exercice'] + '// RM : ' +data_graph['RM'].astype(str)
    fig_line = px.line(data_graph,x="Date", y="Perf", color='Exo_RM', markers=True)
    st.plotly_chart(fig_line,use_container_width=True)

