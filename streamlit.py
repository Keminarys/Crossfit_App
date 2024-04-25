import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import plotly.graph_objects as go


# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(, scope)
client = gspread.authorize(creds)

# Open the Google Sheets file
spreadsheet = client.open('Your Google Sheets File Name')

# Get the first worksheet
worksheet = spreadsheet.get_worksheet(0)
# gc = gspread.service_account(filename=skey)
# worksheet = gc.open('Database_CF83').All_mvmt
# all_mvt = pd.DataFrame(worksheet.get_all_records())
# list_rm = [1,3,5,10]

# dico_ex = all_mvt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
st.title('Crossfit83 Le Beausset')
# st.dataframe(all_mvt)
# st.write(dico_ex)
