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


def ChartDataFS(df, athl) :
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


def dropRecordDB(df, sheet_name):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.update(worksheet=sheet_name,data=df)
    
def create_heatmap_attend(df: pd.DataFrame) -> px.imshow:

    color_continuous_scale_perso=[[0, '#99ccff'], [0.5, '#ff8533'], [1, '#b30000']]
    df = df.replace("x", 1).infer_objects(copy=False)
    df = df.replace('', 0).infer_objects(copy=False)
    df.iloc[:, 1:] = df.iloc[:, 1:].fillna(0).astype(int)

    poll_long = df.melt(
        id_vars='Nom',
        var_name='jour_creneau',
        value_name='dispo'
    )

    poll_long[['Jour', 'Créneau']] = poll_long['jour_creneau'].str.split(' ', n=1, expand=True)

    pivot = poll_long.pivot_table(
        index='Créneau',
        columns='Jour',
        values='dispo',
        aggfunc='sum'
    ).fillna(0).astype(int)

    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    creneaux = ["10:00 - 11:00",
                "11:00 - 12:00",
                "12:15 - 13:15",
                "18:00 - 19:00",
                "19:00 - 20:00"]
    pivot = pivot.reindex(index=creneaux, columns=jours, fill_value=0)

    fig = px.imshow(
        pivot,
        labels={
            'x': 'Jour',
            'y': 'Créneau',
            'color': 'Nb de personnes'
        },
        x=pivot.columns,
        y=pivot.index,
        text_auto=True,
        aspect='auto',
        color_continuous_scale=color_continuous_scale_perso
    )

    fig.update_layout(
        title="Nb d'inscrits par jour et crénau",
        xaxis_title="Jour",
        yaxis_title="Créneau",
        yaxis=dict(tickmode='array', tickvals=creneaux)
    )

    return fig

def pplComingToday(df) :
    days_map = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }
    today_english = datetime.datetime.today().strftime('%A')
    today_french = days_map[today_english]

    filtered_columns = ["Nom"]
    filtered_columns += [col for col in df.columns if today_french in col]
    
    filteredDF = df[filtered_columns]
    input_dict = filteredDF.to_dict()
    names = input_dict['Nom']
    output_dict = {}
    for time_slot, attendance in input_dict.items():
        if time_slot == 'Nom':
            continue
        output_dict[time_slot] = {
            names[idx] for idx, val in attendance.items() if val == 1
        }
    return output_dict
