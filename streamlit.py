### Librairies

import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

conn = st.connection("gsheets", type=GSheetsConnection)
all_mvmt = conn.read(worksheet="All_mvmt")
df = conn.read(worksheet="Progression")
df_name = conn.read(worksheet="Profils").dropna()
st.dataframe(df_name)
list_name = list(df_name["Name"].unique())
list_name = [x for x in list_name if str(x) != "nan"]
list_rm = [1,3,5,10]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()

st.title('Crossfit83 Le Beausset')
st.divider()
st.subheader('Si c\'est votre première visite merci d\'ajouter votre profil dans la barre latérale')
st.write('_Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
st.divider()

with st.sidebar :
    
    new_ppl = st.text_input('Ecrire votre nom ici')
    if st.button('Ajouter mon profil') :
        df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl})], ignore_index=True)
        df_newname = conn.update(
            worksheet="Profils",
            data=df_newname)
        st.experimental_rerun()
  
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎉 Nouvelle Performance", "📈 Aperçu de la progression", "📊 Data","💪🎯 Objectifs", "🏋️‍♂️🤖 WOD Generator"])

with tab1 :
  cat = st.selectbox('Choix de la catégorie', list(dico_ex.keys()))
  ex = st.selectbox('Choix de l"exercice', dico_ex[cat])
  athl = st.selectbox('Choix du profil', list_name)
  if cat == 'WEIGHTLIFTING' : 
    rm = st.selectbox('Choix du RM', list_rm)
  nb = st.number_input('Valeur de la performance', step=1)
