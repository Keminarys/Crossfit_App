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
from utils.functions import go_home, get_conn_and_df
import streamlit.components.v1 as components

    
st.set_page_config(layout="wide")
go_home()


planning = get_conn_and_df("WODSemaine")
url = planning.iloc[0, 8]
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
# Streamlit UI
st.subheader("Planning de la semaine :calendar: ")

# Create seven columns for the buttons
cols = st.columns(7)
selected_day = None

# Generate buttons in respective columns
for i, day in enumerate(days):
    button_label = f"{daysConvert[day.strftime('%A')]} {day.strftime('%d')}"  # Example: "Monday 28"
    if cols[i].button(button_label):
        selected_day = daysConvert[day.strftime('%A')]

# Display workout details for the selected day
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
    
    # Creating vertical scrolling cards
    for i in range(len(selected_planning)):
        with st.container():
            st.markdown(f"""
                <div class="card">
                    <h2>{selected_planning.loc[i, "WOD"]}</h2>
                    <p>{selected_planning.loc[i, selected_day]}</p>
                </div>
            """, unsafe_allow_html=True)


st.divider()

st.subheader("Inscription au cours via PollForAll :calendar: ")
components.iframe(url, height=800, scrolling = True)
