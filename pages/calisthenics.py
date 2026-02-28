import streamlit as st 
import requests 
import json 
import dash
import dash_cytoscape as cyto
from dash import html
from google.oauth2 import service_account 
from googleapiclient.discovery import build 

creds = service_account.Credentials.from_service_account_info( st.secrets["connections"]["gsheets"], scopes=["https://www.googleapis.com/auth/drive.readonly"] ) 
drive = build("drive", "v3", credentials=creds) 
file_id = st.secrets["drive"]["json_file_id"] 

request = drive.files().get_media(fileId=file_id) 
content = request.execute() 
data = json.loads(content)

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
