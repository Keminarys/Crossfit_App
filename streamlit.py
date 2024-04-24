import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
from st_gsheets_connection import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go


conn = st.experimental_connection("gsheets", type=GSheetsConnection)
pet_owners = conn.read(worksheet="All_mvmt")
st.dataframe(pet_owners)
# gc = gspread.service_account(filename=skey)
# worksheet = gc.open('Database_CF83').All_mvmt
# all_mvt = pd.DataFrame(worksheet.get_all_records())
# list_rm = [1,3,5,10]

# dico_ex = all_mvt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
st.title('Crossfit83 Le Beausset')
# st.dataframe(all_mvt)
# st.write(dico_ex)
