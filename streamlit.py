import pandas as pd
import numpy as np
import datetime
import re
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import plotly.graph_objects as go


conn = st.connection("gsheets", type=GSheetsConnection)
all_mvt = conn.read(worksheet="All_mvmt")
progression = conn.read(worksheet="Progression")
list_rm = [1,3,5,10]

dico_ex = all_mvt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
