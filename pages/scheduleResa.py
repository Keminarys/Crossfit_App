from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import datetime
import random
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from utils.functions import get_conn_and_df, UpdateDB, create_heatmap_attend, dropRecordDB, pplComingToday
import streamlit.components.v1 as components
from utils.ui_helpers import render_navbar    

if not st.user.is_logged_in:
        if st.button("Log in with Google"):
            st.login("google")
            st.stop() 
nav_col, logout_col = st.columns([8, 1])

with nav_col:
    render_navbar([
        ("Votre Profil",    "profiles_page"),
        ("Votre Progression","progress"),
        ("Ressources Crossfit","ressources")
    ])

with logout_col:
    if st.button("Log out"):
            st.logout()

if st.user.is_logged_in :
        st.set_page_config(layout="wide")
        athl = st.user.name
        planning = get_conn_and_df("WODSemaine")
        planning = planning[['WOD', 'Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']].dropna()
        poll = get_conn_and_df("Inscription")
        
        # Get current date and determine Monday of the current week
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        days = [monday + timedelta(days=i) for i in range(7)]
        
        
        daysConvert = {
            "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
            "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi",
            "Sunday": "Dimanche"
        }
        
        st.subheader("Personnes présentes au cours aujourd'hui")
        attendance_dict = pplComingToday(poll)
        for time_slot, people in attendance_dict.items():
                with st.expander(f"🕒 {time_slot}", expanded=True):
                        if people:
                            cols = st.columns(min(len(people), 4))
                            for idx, name in enumerate(people):
                                with cols[idx % 4]:
                                    st.markdown(f"<div style='background-color:#dff0d8;padding:10px;border-radius:5px;text-align:center;font-weight:bold;'>{name}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("🚫 Personne n'est prévu pour ce créneau.")
        st.div()
        st.subheader("Inscription au WOD de la semaine :calendar:")
        
        
        if athl not in poll["Nom"].unique() : 
            new_row = {col: False for col in poll.columns}
            new_row["Nom"] = athl
            
            edited = st.data_editor(
                pd.DataFrame([new_row]),
                column_config={
                    "Nom": {"disabled": True}, 
                },
                hide_index=True,
                key="attendance_editor"
            )
        
            if st.button("S'inscrire"):
                for col in edited.columns:
                    if edited[col].dtype == "bool":
                        edited[col] = edited[col].replace({False: "", True: "x"})
                dict_edited = {}
                for col in edited.columns :
                  dict_edited[col] = edited[col][0]
                UpdateDB(poll, dict_edited, "Inscription")
                st.cache_data.clear()
                st.rerun() 
        else : 
            st.write("Vous avez déjà rempli le formulaire pour cette semaine.")
            if st.button("Modifier son inscription", key="btn_modify"):
                poll = poll[poll["Nom"] != athl]
                if poll.empty:
                    poll = poll.iloc[0:0] 
                dropRecordDB(poll, "Inscription")
                st.cache_data.clear()
                st.rerun()
        
        # Define example workout details for each day
        st.subheader("Planning de la semaine :calendar:")
        cols = st.columns(7)
        selected_day = None
        for i, day in enumerate(days):
                button_label = f"{daysConvert[day.strftime('%A')]} {day.strftime('%d')}"  # Example: "Monday 28"
                if cols[i].button(button_label):
                        selected_day = daysConvert[day.strftime('%A')]
        
        
        
        if selected_day:
                st.subheader("Workout of the Day")
                selected_planning = planning[['WOD', selected_day]]
                st.markdown("""
                <style>
                .card {
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                background-color: #2E3B4E;
                color: white;
                text-align: center;
                font-size: 18px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
                }
                </style>
                """, unsafe_allow_html=True)
        
        
                for i in range(len(selected_planning)):
                        with st.container():
                                st.markdown(f"""
                                <div class="card">
                                <h2>{selected_planning.loc[i, "WOD"]}</h2>
                                <p>{selected_planning.loc[i, selected_day]}</p>
                                </div>
                                """, unsafe_allow_html=True)
        
        with st.expander("📊 Personnes présentes cette semaine"):
            st.dataframe(
                poll,
                use_container_width=True, 
                hide_index=True
            )
        
        with st.expander("📊 HeatMap"):
            if not poll.empty:
                st.plotly_chart(create_heatmap_attend(poll),use_container_width=True)
        
