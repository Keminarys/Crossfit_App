### Librairies

import pandas as pd
import numpy as np
import datetime
import random
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import yt_dlp
import requests
from bs4 import BeautifulSoup
from utils.functions import go_home
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
    
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas
    
def data_perso(df) :
    athl = str(st.session_state.athl)
    temp = df.loc[df['Profil'] == athl].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
    return temp

def highlight_rows(row):
    styles = {
        'GYMNASTIC': 'background-color: darkgray;',
        'BODYWEIGHT': 'background-color: darkseagreen;',
        'WEIGHTLIFTING': 'background-color: cadetblue;', 
        'DB_KB_WB': 'background-color: sandybrown;', 
        'ROPE': 'background-color: chocolate;', 
        'ERGO': 'background-color: darksalmon;', 
        'WOD': 'background-color: tan;', 
        'RUN': 'background-color: slategray;'
    }
    return [styles.get(row.Category, '')] * len(row)

def ChartDataFS(df) :
    athl = str(st.session_state.athl)
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
    return fig

st.set_page_config(layout="wide")
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
bergerModified = get_df("bergerModified")

list_name = list(df_name["Name"].unique())
list_name = [x for x in list_name if str(x) != "nan"]
list_rm = [i for i in range (1,21)]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
sorted_dico_ex = sorted(list(dico_ex.keys()), key=lambda x: (x != 'WEIGHTLIFTING', x))
dico_units = all_mvmt[['Exercice','Units']].drop_duplicates().set_index('Exercice').to_dict()['Units']
all_units = list(all_mvmt["Units"].unique())

### Main
### Home Button 
go_home()


@st.dialog("Choisis ton profil")
def SelectProfile() :
    athl = st.selectbox('Choix du profil', list_name)
    if st.button("Valider"):
        st.session_state.athl = athl
        st.rerun()
    st.divider()
    st.write('Si c\'est votre première visite merci d\'ajouter votre profil. \n _Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
    new_ppl = st.text_input('Ecrire votre nom ici')
    if st.button('Ajouter mon profil') :
        df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl}, index=[len(df_name)])], ignore_index=True)
        df_newname = conn.update(worksheet="Profils",data=df_newname)
        st.cache_data.clear()
        st.rerun()
    return athl
    
if "athl" not in st.session_state : 
    athl = SelectProfile()
if "athl" in st.session_state :
    st.title(f"Bienvenue sur ton profil {st.session_state.athl} :muscle:")
    athl = str(st.session_state.athl)
    
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
        df_record = pd.concat([df, pd.DataFrame(new_entry, index=[len(df)])], ignore_index=True)
        df_record = conn.update(worksheet="Progression",data=df_record)
        if cat == 'AJOUTER UN EXERCICE' : 
            df_wod = pd.concat([all_mvmt, pd.DataFrame(new_WOD, index=[len(all_mvmt)])], ignore_index=True)
            df_wod = conn.update(worksheet="All_mvmt",data=df_wod)
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
        st.dataframe(styled_df, use_container_width=True)
    
    with col2 :
        fig = ChartDataFS(df)
        st.plotly_chart(fig,use_container_width=True)
        
        st.divider()
        data_full_scoped = df.loc[df['Profil'] == str(st.session_state.athl)]
        selected_cat = st.selectbox('Choix de la catégorie', list(data_full_scoped.Category.unique()))
        selected_ex = st.multiselect('Choix de la catégorie', list(data_full_scoped.loc[data_full_scoped['Category'] == selected_cat]['Exercice'].unique()))
       
        data_graph = data_full_scoped.loc[(data_full_scoped['Category'] == selected_cat) & (data_full_scoped['Exercice'].isin(selected_ex))]
        if (len(selected_cat) > 0) and (len(selected_ex) > 0) and (data_graph["Unité"].unique().tolist()[0] == "HH:MM:SS") :
            data_graph = data_graph.assign(**data_graph[['Perf']].apply(pd.to_datetime, format='%H:%M:%S'))
        data_graph['Exo_RM'] = data_graph['Exercice'] + '// RM : ' +data_graph['RM'].astype(str)
        fig_line = px.line(data_graph,x="Date", y="Perf", color='Exo_RM', markers=True)
        st.plotly_chart(fig_line,use_container_width=True)
    
