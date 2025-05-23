### Librairies

import pandas as pd
import ast
import numpy as np
import datetime
import random
import re
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import streamlit_authenticator as stauth
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import yt_dlp
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
from utils.functions import go_home

def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas

def WOD() :
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
    #url_random_new = "https://www.crossfit.com/"+new_format
    return url_random_old#, url_random_new 

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
    wodGirlsPage = get_df("benchmarks")
    wodGirlsPage = wodGirlsPage.iloc[0]["Description"]
    wodGirls = ast.literal_eval(wodGirlsPage)
    return wodGirls
    
st.set_page_config(layout="wide")
go_home()
conn = get_conn()
st.title("Cette page vous sera utile lors de vos sessions open gym ou bien si vous souhaitez vous challenger sur des WODs références !")
st.divider()

st.write("Vous pouvez voir chaque mouvement officiel issu de la chaîne YouTube officielle de CrossFit©️")
on = st.toggle("Voir la liste des mouvements ?")

if on : 
    @st.cache_data  
    def getVideoLink() : 
        ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True, 'force_generic_extractor': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info('https://www.youtube.com/playlist?list=PLdWvFCOAvyr1qYhgPz_-wnCcxTO7VHdFo', download=False)
        titles_and_urls = []
        for entry in info['entries']:
            title = entry['title']
            url = f"https://www.youtube.com/watch?v={entry['id']}"
            titles_and_urls.append((title, url))
        return titles_and_urls

    with st.status("Chargement de la playlist CrossFit©️ ...", expanded=True) as status:
        st.write("Création de la liste contenant les titres des vidéos ...")
        titles_and_urls = getVideoLink() 
        status.update(label="Chargement Terminé !", state="complete", expanded=False)
    list_title = [title for title, _ in titles_and_urls]
    title_id = st.selectbox('Quel mouvement voulez vous voir ?',list_title)
    video_url = [url for title, url in titles_and_urls if title == title_id][0]
    st.video(video_url)

st.divider()
st.subheader("Tous les wods présentés ici sont issus du site officiel de Crossfit.com ©️")
st.write("Crossfit.com ©️ étant un site américain, les charges sont en lbs.")
st.write("Pour les convertir en Kg, il faut soit diviser la charge par 2.2, sinon vous pouvez utiliser le convertisseur ci dessous")
col1, col2 = st.columns([1,3],vertical_alignment="center")
with col1:
    lbs = st.number_input("Charge en lbs")
with col2 : 
    st.write("Votre charge en kg est de :", lbs*0.453592)
st.divider()
st.write("Vous trouverez des WOD Crossfit.com ©️ ci dessous")
with st.expander(":red[Choississez entre le WOD du jour ou un Random]") :
    random_on = st.toggle("Voulez vous voir un WOD random ?")
    if random_on :
        components.iframe(random_date_url(), height=400, scrolling = True)
    else :
        components.iframe(WOD(), height=400, scrolling = True)
        
st.divider()
st.write("Vous trouverez ci dessous les WODs HERO")
expanderWODHero = st.expander(":red[Tous les WOD Hero]")
wods = get_all_heroes()
chosen_hero = expanderWODHero.selectbox("Quel WOD Hero voulez vous voir", [i["name"] for i in wods])
if len(chosen_hero) > 0 : 
    wod = next((wod for wod in wods if wod['name'] == chosen_hero), None)
    expanderWODHero.markdown(wod['description'].replace('\n', '<br>'), unsafe_allow_html=True)
st.divider()

st.write("Vous trouverez ci dessous les WODs GIRL")
expanderWODGirl = st.expander(":red[Tous les WOD Girl]")
wodGirls = wodGirls()
chosen_wod = expanderWODGirl.selectbox("Quel WOD Girl voulez vous voir", [i["title"] for i in wodGirls])
if len(chosen_wod) > 0 : 
    wodgirlchosen = next((wod for wod in wodGirls if wod['title'] == chosen_wod), None)
    expanderWODGirl.markdown(wodgirlchosen['description'].replace('\n', '<br>'), unsafe_allow_html=True)
    expanderWODGirl.markdown(wodgirlchosen['mvmt'].replace('\n', '<br>'), unsafe_allow_html=True)
