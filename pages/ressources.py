### Librairies

import pandas as pd
import numpy as np
import datetime
import random
import re
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import yt_dlp
import requests
from bs4 import BeautifulSoup


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
    
def format_text(text):
    formatted_text = re.sub(r'Compare to', '\n\nCompare to', text)
    formatted_text = re.sub(r'Scaling:', '\n\nScaling:\n', formatted_text)
    formatted_text = re.sub(r'Intermediate option:', '\n\nIntermediate option:\n', formatted_text)
    formatted_text = re.sub(r'Beginner option:', '\n\nBeginner option:\n', formatted_text)
    formatted_text = re.sub(r'Coaching cues:', '\n\nCoaching cues:\n', formatted_text)
    return formatted_text
    
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
    url_random_new = "https://www.crossfit.com/"+new_format
    return url_random_old, url_random_new  
    
def WOD() :
    url = "https://www.crossfit.com/"
    today = date.today()
    formatted_date = today.strftime('%y%m%d')
    url_today = url+formatted_date
    return url_today

def UniqueWOD_OldFormat(url) :
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        wod_container = soup.find('div', class_='col-sm-7', id='wodContainer')
        wod_content = wod_container.find('div', class_='wod active')
        wod_description = wod_content.get_text(separator=" ", strip=True).replace('.', '.\n').replace(':', ':\n\n')
        return wod_description
        
def UniqueWOD(url): 
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        h1_tag = soup.find('title')
        if h1_tag:
            wod_name = h1_tag.get_text(strip=True)
            description_div = soup.find('div', class_='_wrapper_3kipy_96 _text-block_1ex2o_95')
            
            if description_div:
                wod_description = description_div.get_text(separator=" ", strip=True).replace('.', '.\n').replace(':', ':\n\n')
                lines = wod_description.split('\n')
                filtered_lines = []
                
                for line in lines:
                    if line.startswith("Resources:"):
                        break
                    filtered_lines.append(line.strip())
                
                if filtered_lines:
                    formatted_description = "\n".join([line for line in filtered_lines if line])
                    formatted_description = format_text(formatted_description)
                else:
                    formatted_description = "Il y a une erreur sur le site Crossfit.com"
            else:
                formatted_description = "Il y a une erreur sur le site Crossfit.com"
        else:
            formatted_description = "Il y a une erreur sur le site Crossfit.com"
    except requests.exceptions.RequestException as e:
        formatted_description = f"An error occurred: {e}"

    return formatted_description

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

expanderWODDAY = st.expander(":red[Workout of the day]")
wod_description_today = UniqueWOD(WOD())
expanderWODDAY.write(f"{wod_description_today}")
st.divider()

expanderWODRandom = st.expander(":red[WOD au hasard]")
if expanderWODRandom.button("Générer un WOD au hasard"):
    url_random_old, url_random_new = random_date_url()
    try :
      wod_description_random = UniqueWOD(url_random_new)
      expanderWODRandom.write(f"{wod_description_random}")
    except :
      try :
        wod_description_random = UniqueWOD_OldFormat(url_random_new)
        expanderWODRandom.write(f"{wod_description_random}")
      except :
        try :
          wod_description_random = UniqueWOD_OldFormat(url_random_old)
          expanderWODRandom.write(f"{wod_description_random}")
        except :
          expanderWODRandom.write("Il y a eu une erreur réessayer")
st.divider()

st.write("Vous trouverez ci dessous les WODs HERO")
expanderWODHero = st.expander(":red[Tous les WOD Hero]")
wods = get_all_heroes()
chosen_hero = expanderWODHero.selectbox("Quel WOD Hero voulez vous voir", [i["name"] for i in wods])
if len(chosen_hero) > 0 : 
    wod = next((wod for wod in wods if wod['name'] == chosen_hero), None)
    expanderWODHero.markdown(wod['description'].replace('\n', '<br>'), unsafe_allow_html=True)
