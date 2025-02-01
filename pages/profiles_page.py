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
        'BODYWEIGHT': 'background-color: darseagreen;',
        'WEIGHTLIFTING': 'background-color: darkorange;', 
        'DB_KB_WB': 'background-color: sandybrown;', 
        'ROPE': 'background-color: chocolate;', 
        'ERGO': 'background-color: darksalmon;', 
        'WOD': 'background-color: tan;', 
        'RUN': 'background-color: slategray;'
    }
    return [styles.get(row.Category, '')] * len(row)
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
dico_units = all_mvmt[['Exercice','Units']].drop_duplicates().set_index('Exercice').to_dict()['Units']

### Main
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
    
    st.divider()
    st.write("Tu peux visualiser toutes tes performances dans le tableau ci-dessous !")
    st.divider()
    
    data_perso = data_perso(df)
    styled_df = data_perso.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)
