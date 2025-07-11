import pandas as pd
import numpy as np
import datetime
import random
import ast
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup

def get_conn_and_df(sheet_name) :
    conn = st.connection("gsheets", type=GSheetsConnection)
    datas = conn.read(worksheet=sheet_name)
    return datas


def highlight_rows(row):
    styles = {
        'GYMNASTIC': 'background-color: darkgray;',
        'BODYWEIGHT': 'background-color: darkseagreen;',
        'WEIGHTLIFTING': 'background-color: cadetblue;', 
        'DB_KB_WB': 'background-color: sandybrown;', 
        'ROPE': 'background-color: chocolate;', 
        'ERGO': 'background-color: darksalmon;', 
        'WOD': 'background-color: tan;', 
        'RUN': 'background-color: slategray;'
    }
    return [styles.get(row.Category, '')] * len(row)


def ChartDataFS(df) :
    athl = str(st.session_state.athl)
    data_full_scoped = df.loc[df['Profil'] == athl]
    data_grouped =  data_full_scoped.groupby(['Category', 'Exercice']).count().reset_index()
 
    fig = px.bar(data_grouped, x="Category", y="Perf", color="Exercice")
    fig.update_layout(
            title="Répartitions des performances",
                xaxis_title="Categories",
                yaxis_title="Nombre d\'entrées",
                autosize=False,
                width=500,
                height=300)
    return fig


def WOD_crossfit() :
    url = "https://www.crossfit.com/"
    today = date.today()
    formatted_date = today.strftime('%y%m%d')
    url_today = url+formatted_date
    return url_today

def random_date_url():
    start_date = datetime.datetime.strptime("2001-10-02", "%Y-%m-%d")
    end_date = datetime.datetime.now()
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    random_date = start_date + datetime.timedelta(days=random_days)
    new_format = random_date.strftime("%y%m%d")
    old_format = random_date.strftime("%Y/%m/%d")
    url = "https://www.crossfit.com/workout/"
    url_random_old = url+old_format+"#/comments"
    return url_random_old

def get_all_heroes() : 
    url = 'https://www.crossfit.com/heroes'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        wods = []
        sections = soup.find_all('section', class_='_component_1ugao_79')
      
        for section in sections:
            hr_tag = section.find('hr')
            if hr_tag:
                h3_tag = hr_tag.find_next('h3')
                if h3_tag:
                    wod_name = h3_tag.get_text(strip=True)
                    wod_description = ''

                    for sibling in h3_tag.find_next_siblings():
                        if sibling.name == 'p':
                            text = sibling.get_text(separator="<br/>", strip=True)
                            wod_description += text + '<br/><br/>'
                        else:
                            break
                    wod_description = wod_description.strip('<br/><br/>').replace('<br/><br/>', '\n\n').replace('<br/>', '\n')
                    wods.append({"name": wod_name, "description": wod_description})
    return wods

def wodGirls() :
    wodGirlsPage = get_conn_and_df("benchmarks")
    wodGirlsPage = wodGirlsPage.iloc[0]["Description"]
    wodGirls = ast.literal_eval(wodGirlsPage)
    return wodGirls

def UpdateDB(df, new_entry, sheet_name):
    conn = st.connection("gsheets", type=GSheetsConnection)
    updatedDB = pd.concat([df, pd.DataFrame(new_entry, index=[len(df)])], ignore_index=True)
    updatedDB = conn.update(worksheet=sheet_name,data=updatedDB)

