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
list_rm = [1,3,5,10]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()

st.title('Crossfit83 Le Beausset')
st.selectbox('Select a category', dico_ex.key())
# st.dataframe(all_mvt)
# st.write(dico_ex)
