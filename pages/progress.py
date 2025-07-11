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
    
# def data_perso(df) :
#     athl = str(st.session_state.athl)
#     temp = df.loc[df['Profil'] == athl].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
#     return temp

def data_perso(df, str) :
    temp = df.loc[df['Profil'] == str].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
    return temp
st.subheader("💪 Travail de Force")

# @st.dialog("Choisis ton profil")
# def SelectProfile() :
#     athl = st.selectbox('Choix du profil', list_name)
#     if st.button("Valider"):
#         st.session_state.athl = athl
#         st.rerun()
#     st.divider()
#     st.write('Si c\'est votre première visite merci d\'ajouter votre profil. \n _Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
#     new_ppl = st.text_input('Ecrire votre nom ici')
#     if st.button('Ajouter mon profil') :
#         df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl}, index=[len(df_name)])], ignore_index=True)
#         df_newname = conn.update(worksheet="Profils",data=df_newname)
#         st.cache_data.clear()
#         st.rerun()
#     return athl    
conn = get_conn()

df = get_df("Progression")
df = df[['Profil','Category','Exercice','Date','Perf','Unité','RM','Commentaire']].dropna()

berger = get_df("berger")
bergerModified = get_df("bergerModified")

st.write("Si vous souhaitez faire du travail de force, vous pouvez vous aider des onglets ci-dessous suivant le but de votre séance.")

@st.dialog("Consulter mes RM",  width="large")
def get_best_rm(df, athl) :
    st.write("Voici vos meilleurs performances pour chaque exercice")
    st.divider()
    temp = df.loc[(df.Category == "WEIGHTLIFTING") & (df['Profil'] == athl)]
    temp = temp.groupby(["Exercice", "RM"]).agg({"Perf" : "max"}).reset_index()
    selection = st.pills("Exercice", temp["Exercice"].unique().tolist(), selection_mode="single")
    temp = temp.loc[temp.Exercice == selection]
    return st.dataframe(temp, use_container_width=True, hide_index = True)
    
# --- RM Consultation ---
if "get_best_rm" not in st.session_state:
    if st.button("Consulter mes RM"):
        get_best_rm(data_perso, "DylL")

# --- Expander: Berger Table for One Set ---
with st.expander("Table de Berger pour une seule série"):
    st.write("Utilisez cette table de Berger personnalisée pour atteindre votre charge de travail efficacement.")

    explanation = pd.DataFrame({
        "REPS": ["1 à 6", "7 à 10", "11 à 15"],
        "Benefice": ["Force", "Volume Hypertrophie", "Endurance"],
        "Repos": ["3'+", "2'-3'", "2'"],
        "Nb de séries": ["3 à 5", "6", "8"]
    })
    st.dataframe(explanation, hide_index=True, use_container_width=True)

    st.divider()
    repMax = st.number_input('Votre RM max (RM1/2/3/5 etc)', step=1)
    chargeMax = st.number_input('Votre charge max pour ce RM', step=1)

    if repMax and chargeMax != 0:
        updatedBerger = berger.copy()
        updatedBerger.at[int(repMax), "Charge"] = chargeMax
        rm1_calulated = int(chargeMax / updatedBerger.iloc[int(repMax)]["Pourcentage"])
        updatedBerger.loc[1:, "Charge"] = updatedBerger.loc[1:, "Pourcentage"] * rm1_calulated
        updatedBerger = updatedBerger[updatedBerger.Charge > 0].astype({"Charge": int})
        st.dataframe(updatedBerger, use_container_width=True, hide_index=True)

# --- Expander: Berger Table for Multiple Sets ---
with st.expander("Table de Berger pour plusieurs séries"):
    st.write("Utilisez cette table personnalisée adaptée à un travail sur plusieurs séries.")

    code = pd.DataFrame({
        "Difficulty": ["RM1", "RM2-3", "RM4-5", "RM6-7", "RM8-9", "RM10-11", "RM12-13", "RM14-15"],
        "Recommendations": [
            "True Test Sets, 1-8/12 weeks, Peaking LOW-OPT",
            "Test Sets, Evaluation Sets, 0-1/4 weeks, Peaking LOW-OPT",
            "Evaluation Sets, Occasional Load Weeks, 0-1/4 weeks, Peaking LOW-OPT",
            "Majority of Load Weeks, Occasional Open Sets, 1-3/4 weeks, Peaking LOW-HIGH",
            "Majority of Base Work, Occasional Unload Work, 0-1/4 weeks, Peaking LOW-HIGH",
            "Majority of Unload Work, Occasional Base Work, 1-2/4 weeks",
            "Super Unload, 0-1/4 weeks, Seldom used as Unload",
            "Rarely used in Cycles, 0-1/4 weeks, Not enough load to yield adaptation"
        ]
    })
    st.dataframe(code, hide_index=True, use_container_width=True)

    st.divider()
    repMaxMulti = st.number_input('Votre RM max pour la session de travail', step=1)
    chargeMaxMulti = st.number_input('Votre Charge max pour la session de travail', step=1)
    Serie_nb = st.selectbox('Nb de séries', (1, 2, 3, 4, 5, 6, 7, 8, 10))

    if repMaxMulti and chargeMaxMulti != 0:
        updatedbergerModified = bergerModified.copy().iloc[:, [0, Serie_nb]]
        rm1_calulated_multi = int(chargeMaxMulti / berger.iloc[int(repMaxMulti)]["Pourcentage"])
        updatedbergerModified["Charge"] = updatedbergerModified[Serie_nb] * rm1_calulated_multi
        updatedbergerModified = updatedbergerModified[updatedbergerModified["Charge"] > 0].astype({"Charge": int})
        updatedbergerModified = updatedbergerModified.rename(columns={Serie_nb: f"Pourcentage pour {Serie_nb} séries"})
        st.dataframe(updatedbergerModified, use_container_width=True, hide_index=True)
