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
list_rm = [i for i in range (1,11)]
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
st.title(f"Bienvenue sur ton profil {athl} :muscle:")

