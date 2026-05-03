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
from utils.functions import get_conn_and_df, UpdateDB, create_heatmap_attend, dropRecordDB, pplComingToday, newName
from utils.allow import is_email_allowed, get_user_role, add_allowed_email
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
        ("Ressources Crossfit","ressources"),
        ("Calisthenics",   "calisthenics"),
    ])

with logout_col:
    if st.button("Log out"):
            st.logout()

if st.user.is_logged_in :
        user_email = st.user.email
        allowed, role = get_user_role(user_email, "allowList")
        if not allowed:
            st.error("Authenticated but NOT authorized.")
            st.stop()
            
        else : 
                st.set_page_config(layout="wide")
                athl = newName()
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
                st.subheader("Planning de la semaine :calendar:")

                # Build weekday labels with dates
                header_labels = [f"{daysConvert[d.strftime('%A')]} {d.strftime('%d')}" for d in days]
                week_days = [daysConvert[d.strftime('%A')] for d in days]
                
                # Copy relevant columns
                table = planning[['WOD'] + week_days].copy()
                
                
                # Replace line breaks for HTML display
                for day in week_days:
                    table[day] = table[day].str.replace("\n", "<br>")
                
                # Color palette per day
                day_colors = {
                    "Lundi": "#7A2E2E",
                    "Mardi": "#8C3A3A",
                    "Mercredi": "#9E4A4A",
                    "Jeudi": "#B05C5C",
                    "Vendredi": "#C26E6E",
                    "Samedi": "#A05252",
                    "Dimanche": "#6E2B2B",
                }
                
                # CSS styling
                st.markdown("""
                <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    text-align: center;
                }
                th {
                    background-color: #2E3B4E;
                    color: white;
                    padding: 12px;
                    text-align: center;
                    font-size: 18px;
                }
                td {
                    background-color: #1F2937;
                    color: white;
                    padding: 10px;
                    border: 1px solid #444;
                    vertical-align: top;
                    text-align: center;
                }
                
                /* Bubble style */
                .bubble {
                    padding: 12px;
                    margin-bottom: 10px;
                    border-radius: 12px;
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
                    text-align: center;
                }
                .bubble h4 {
                    margin: 0 0 6px 0;
                    font-size: 16px;
                    color: #FFD166;
                }
                .bubble p {
                    margin: 0;
                    font-size: 14px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Build HTML table
                html = "<table><tr>"
                
                # Header row with dates
                for label in header_labels:
                    html += f"<th>{label}</th>"
                html += "</tr><tr>"
                
                # One row containing all days
                for day, label in zip(week_days, header_labels):
                    gtg = "<br>".join(table.loc[0, day].split("<br>")) if table.loc[0, day] else ""
                    freq = "<br>".join(table.loc[1, day].split("<br>")) if table.loc[1, day] else ""
                    method = "<br>".join(table.loc[2, day].split("<br>")) if table.loc[2, day] else ""

                
                    color = day_colors.get(day, "#2E3B4E")
                
                    html += (
                        f"<td>"
                        f"<div class='bubble' style='background-color:{color};'><h4>Grease the Groove</h4><p>{gtg}</p></div>"
                        f"<div class='bubble' style='background-color:{color};'><h4>Méthode</h4><p>{freq}</p></div>"
                        f"<div class='bubble' style='background-color:{color};'><h4>Fréquence</h4><p>{method}</p></div>"
                        "</td>"
                    )
                
                html += "</tr></table>"
                
                st.markdown(html, unsafe_allow_html=True)

                
                with st.expander("Personnes présentes au cours aujourd'hui") : 
                        attendance_dict = pplComingToday(poll)
                        for time_slot, people in attendance_dict.items():
                                with st.expander(f"🕒 {time_slot}", expanded=True):
                                        if people:
                                            cols = st.columns(min(len(people), 4))
                                            for idx, name in enumerate(people):
                                                with cols[idx % 4]:
                                                    st.markdown(f"<div style='background-color:#8B0000;padding:10px;border-radius:5px;text-align:center;font-weight:bold;'>{name}</div>", unsafe_allow_html=True)
                                        else:
                                            st.markdown("🚫 Personne n'est prévu pour ce créneau.")
                        
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
                
                with st.expander("📊 Personnes présentes cette semaine"):
                    st.dataframe(
                        poll,
                        use_container_width=True, 
                        hide_index=True
                    )
                
                with st.expander("📊 HeatMap"):
                    if not poll.empty:
                        st.plotly_chart(create_heatmap_attend(poll),use_container_width=True)
                
