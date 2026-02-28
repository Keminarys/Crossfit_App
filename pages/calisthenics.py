import streamlit as st 
import requests 
import json 
import dash
import dash_cytoscape as cyto
from dash import html
from google.oauth2 import service_account 
from utils.functions import load_drive_json
from utils.ui_helpers import render_navbar

if not st.user.is_logged_in:
        if st.button("Log in with Google"):
            st.login("google")
            st.stop()
nav, log = st.columns([8,1])
with nav : 
    render_navbar([
        ("Votre Profil",    "profiles_page"),
        ("Votre Progression","progress"),
        ("Ressources Crossfit","ressources"),
        ("Programmation",   "scheduleResa"),
    ])

with log:
    if st.button("Log out"):
            st.logout()

if st.user.is_logged_in :
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]["gsheets"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    file_id = st.secrets["drive"]["json_file_id"]
    data = load_drive_json(file_id, creds)
    
    testnode = data[0]['movements']
    elements = []
    for item in testnode:
        elements.append({"data": {"id": item["id"], "label": item["name"]}})
        for nxt in item.get("progressions_to", []):
            elements.append({"data": {"source": item["id"], "target": nxt}})
    
    app = dash.Dash(__name__)
    app.layout = html.Div([
        cyto.Cytoscape(
            id="skill-tree",
            elements=elements,
            layout={"name": "breadthfirst"},
            style={"width": "100%", "height": "800px"},
            stylesheet=[
                {"selector": "node", "style": {"background-color": "#88c", "label": "data(label)"}},
                {"selector": ".mastered", "style": {"background-color": "green"}}
            ]
        )
    ])
    
    # Run Dash inside Streamlit
    from dash.dependencies import Input, Output, State
    
    @app.callback(
        Output("skill-tree", "elements"),
        Input("skill-tree", "tapNodeData"),
        State("skill-tree", "elements")
    )
    def mark_mastered(node, elements):
        if node:
            for el in elements:
                if el.get("data", {}).get("id") == node["id"]:
                    el["classes"] = "mastered"
        return elements
    
    # Embed
    st.components.v1.html(app.index(), height=900, scrolling=True)
