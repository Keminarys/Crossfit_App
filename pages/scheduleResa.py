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
from utils.functions import get_conn_and_df, UpdateDB, create_heatmap_attend, dropRecordDB
import streamlit.components.v1 as components
#from utils.auth import login_ui, logout_ui
from utils.ui_helpers import render_navbar    

render_navbar([
("Votre Profil",    "profiles_page"),
("Votre Progression","progress"),
("Ressources Crossfit","ressources"),
("Programmation",   "scheduleResa"),
])

st.set_page_config(layout="wide")

planning = get_conn_and_df("WODSemaine")
planning = planning[['WOD', 'Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']].dropna()

# Get current date and determine Monday of the current week
today = date.today()
monday = today - timedelta(days=today.weekday())
days = [monday + timedelta(days=i) for i in range(7)]


daysConvert = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi",
    "Sunday": "Dimanche"
}

# Define example workout details for each day
with st.expander("Planning de la semaine :calendar:"):
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


with st.expander("Inscription au WOD de la semaine :calendar:"):
    poll = get_conn_and_df("Inscription")
    
    if str(st.session_state.athl) not in poll["Nom"].unique() : 
        new_row = {col: False for col in poll.columns}
        new_row["Nom"] = str(st.session_state.athl)
        
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
                    edited[col].replace({False: "", True: "x"}, inplace=True)
            UpdateDB(poll, edited, "Inscription")
            st.cache_data.clear()
            st.rerun() 
    else : 
        st.write("Vous avez déjà rempli le formulaire pour cette semaine.")
        if st.button("Modifier son inscription", key="btn_modify"):
            poll = poll[poll["Nom"] != str(st.session_state.athl)]
            if poll.empty:
                poll = poll.iloc[0:0] 
            dropRecordDB(poll, "Inscription")
            st.cache_data.clear()
            st.rerun()

with st.expander("📊 Personnes présentes cette semaine"):
    st.dataframe(
        poll,
        use_container_width=True
    )

with st.expander("📊 HeatMap"):
    if not poll.empty:
        st.plotly_chart(create_heatmap_attend(poll),use_container_width=True)

