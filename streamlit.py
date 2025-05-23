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
# import yaml
# from yaml.loader import SafeLoader

# with open('/mount/src/crossfit_app/config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

### Setting up the page 

st.set_page_config(layout="wide")
### Function 
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas
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

@st.dialog("Consulter mes RM",  width="large")
def get_best_rm(df, athl) :
    st.write("Voici vos meilleurs performances pour chaque exercice")
    st.divider()
    temp = df.loc[(df.Category == "WEIGHTLIFTING") & (df['Profil'] == athl)]
    temp = temp.groupby(["Exercice", "RM"]).agg({"Perf" : "max"}).reset_index()
    selection = st.pills("Exercice", temp["Exercice"].unique().tolist(), selection_mode="single")
    temp = temp.loc[temp.Exercice == selection]
    return st.dataframe(temp, use_container_width=True, hide_index = True)

### Variable
# authenticator.login()
# if st.session_state["authentication_status"]:
#     authenticator.logout()
conn = get_conn()
all_mvmt = get_df("All_mvmt")
all_mvmt = all_mvmt[['Category','Exercice','Units']].dropna()

df = get_df("Progression")
df = df[['Profil','Category','Exercice','Date','Perf','Unité','RM','Commentaire']].dropna()
    
df_name = get_df("Profils")
df_name = df_name[['Name']].dropna()

df_obj = get_df("Objectif")
df_obj = df_obj[['Name','Task','Description','Start','Finish','Completed']].dropna()
df_obj['Start'] = pd.to_datetime(df_obj['Start'], format='%d/%m/%Y')
df_obj['Finish'] = pd.to_datetime(df_obj['Finish'], format='%d/%m/%Y')

berger = get_df("berger")
bergerModified = get_df("bergerModified")

list_name = list(df_name["Name"].unique())
list_name = [x for x in list_name if str(x) != "nan"]
list_rm = [i for i in range (1,11)]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
dico_units = all_mvmt[['Exercice','Units']].drop_duplicates().set_index('Exercice').to_dict()['Units']

### Main

st.title('Crossfit83 Le Beausset')
st.divider()
st.subheader('Si c\'est votre première visite merci d\'ajouter votre profil dans la barre latérale')
st.write('_Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
st.divider()
athl = st.selectbox('Choix du profil', list_name)
st.divider()

with st.sidebar.expander("Ajout d'un nouveau profil") :
    
    new_ppl = st.text_input('Ecrire votre nom ici')
    if st.button('Ajouter mon profil') :
        df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl}, index=[len(df_name)])], ignore_index=True)
        df_newname = conn.update(worksheet="Profils",data=df_newname)
        st.cache_data.clear()
        st.rerun()

with st.sidebar.expander("Ajout d'un WOD/Exercice non présent dans la liste") :
    
    new_cat = st.selectbox("Sélectionnez la catégorie", list(dico_ex.keys()))
    new_ex = st.text_input("Nom de l'exercice")
    new_units = st.selectbox("Sélectionnez l'unité adéquat", list(all_mvmt['Units'].unique()))
    if st.button('Ajouter l\'exercice à la base de données') :
        df_newexo = pd.concat([all_mvmt, pd.DataFrame({'Category' : new_cat, 
                                                      'Exercice' : new_ex ,
                                                      'Units' : new_units}, index=[len(all_mvmt)])], ignore_index=True)
        df_newexo = conn.update(worksheet="All_mvmt",data= df_newexo)
        st.write('Ajouté avec succès, la page va se rafraîchir automatiquement ✅')
        st.cache_data.clear()
        st.rerun()

tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(["🎉 Nouvelle Performance", "📈 Aperçu de la progression", "📊 Data", "💪🎯 Objectifs", "🖥️ Table de Berger","🏋️‍♂️ WOD", "🥇🏋️‍♂️ Démonstration Mouvement"])

with tab1 :
    cat = st.selectbox('Choix de la catégorie', list(dico_ex.keys()))
    ex = st.selectbox('Choix de l"exercice', dico_ex[cat])
    if cat == 'WEIGHTLIFTING' : 
        rm = st.selectbox('Choix du RM', list_rm)
    else : rm = 1
    if dico_units[ex] == 'HH:MM:SS' :
       nb = st.text_input('Temps au format HH\:MM\:SS', "00:00:00")
    else : nb = st.number_input('Max reps/charge', step=1)
    date = st.date_input('Date de réalisation', value = "today")
    unit = dico_units[ex]
    if cat == "WOD":
        commentary = st.text_input('Commentaire sur la réalisation', 'Rien')
    else : commentary = 'Rien'
    new_entry = {'Profil' : athl,
                'Category' : cat,
                'Exercice' : ex,
                'Date' : date,
                'Perf' : nb,
                'Unité' : unit,
                'RM' : rm, 
                'Commentaire' : commentary}
    if st.button('Ajouter un nouveau record à mon profil :muscle:') :
        df_record = pd.concat([df, pd.DataFrame(new_entry, index=[len(df)])], ignore_index=True)
        df_record = conn.update(worksheet="Progression",data=df_record)
        st.write('Ajouté avec succès, vous pouvez retrouver toutes vos performances dans l\'onglet Data ✅')
        st.cache_data.clear()
        st.rerun()
  
with tab2 : 
    st.write('Sélectionner un mouvement spécifique pour avoir un aperçu de votre progression')
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
    st.plotly_chart(fig,use_container_width=True)
    st.divider()
    selected_cat = st.selectbox('Choix de la catégorie', list(data_full_scoped.Category.unique()))
    selected_ex = st.multiselect('Choix de la catégorie', list(data_full_scoped.loc[data_full_scoped['Category'] == selected_cat]['Exercice'].unique()))
   
    data_graph = data_full_scoped.loc[(data_full_scoped['Category'] == selected_cat) & (data_full_scoped['Exercice'].isin(selected_ex))]
    if (len(selected_cat) > 0) and (len(selected_ex) > 0) and (data_graph["Unité"].unique().tolist()[0] == "HH:MM:SS") :
        data_graph = data_graph.assign(**data_graph[['Perf']].apply(pd.to_datetime, format='%H:%M:%S'))
    data_graph['Exo_RM'] = data_graph['Exercice'] + '// RM : ' +data_graph['RM'].astype(str)
    fig_line = px.line(data_graph,x="Date", y="Perf", color='Exo_RM', markers=True)
    st.plotly_chart(fig_line,use_container_width=True)
  
with tab3 :
    st.write('Vous pouvez consulter l\'entièreté de vos performances ci dessous.')
    data_perso = df.loc[df['Profil'] == athl].sort_values(by=["Category", "Exercice", "Date"], ascending = [True, True, False])
    st.dataframe(data_perso)

with tab4 :
    st.write('Vous pouvez alimenter le tableau ci dessous pour définir un programme pour atteindre un objectif')
    edited_obj = st.data_editor(df_obj, num_rows='dynamic', hide_index=True)
    if st.button('Mettre à jour mes objectifs') :
        df_obj_edit = conn.update(worksheet="Objectif",data=edited_obj)
        st.cache_data.clear()
        st.rerun()
    st.divider()
    st.write('Ici vous retrouverez la visualisation graphique !')
    fig_gantt = px.timeline(df_obj[df_obj['Name'] == athl], x_start="Start", x_end="Finish", y="Description", color="Task")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt,use_container_width=True)

with tab5 : 
    st.write("Si vous souhaitez faire du travail de force, vous pouvez vous aider des onglets ci dessous suivant le but de votre séance.")

    if "get_best_rm" not in st.session_state:
        if st.button("Consulter mes RM"):
            get_best_rm(data_perso, athl)
            
    expander1 = st.expander("Table de Berger pour une seule série")

    expander1.write("Afin d'atteindre votre charge de travail le plus efficacement possible, vous pouvez utiliser cette table de Berger personnalisée")
    explaination = pd.DataFrame(
    {
        "REPS": ["1 à 6", "7 à 10", "11 à 15"],
        "Benefice": ["Force", "Volume Hypertrophie", "Endurance"],
        "Repos": ["3'+", "2'-3'", "2'"],
        "Nb de series": ["3 à 5", "6", "8"]
    }
)
    expander1.dataframe(explaination,hide_index=True, use_container_width=True)
    expander1.divider()
    expander1.write("Si vous souhaitez consulter vos meilleurs RM, cliquez sur le bouton ci dessous")
    repMax = expander1.number_input('Votre RM max (RM1/2/3/5 etc) (indiquez seulement le chiffre)', step=1)
    chargeMax = expander1.number_input('Votre charge max pour ce RM (indiquez seulement le chiffre)', step=1)

    if repMax and chargeMax != 0 :
        updatedBerger = berger.copy()
        updatedBerger.at[int(repMax), "Charge"] = chargeMax
        rm1_calulated = int((chargeMax) / (updatedBerger.iloc[int(repMax)]["Pourcentage"]))
        updatedBerger.loc[1:, "Charge"] = updatedBerger.loc[1:, "Pourcentage"] * rm1_calulated
        updatedBerger = updatedBerger.loc[updatedBerger.Charge > 0]
        updatedBerger['Charge'] = updatedBerger['Charge'].astype(int)
        expander1.dataframe(updatedBerger, use_container_width=True, hide_index = True)

    expander2 = st.expander("Table de Berger pour plusieurs séries")
    expander2.write("Afin d'atteindre votre charge de travail le plus efficacement possible, vous pouvez utiliser cette table de Berger personnalisée et adaptée à un travail sur plusieurs séries")


    code = {
        "Difficulty": ["RM1", "RM2-3", "RM4-5", "RM6-7", "RM8-9", "RM10-11", "RM12-13", "RM14-15"],
        "Recommendations": [
            "True Test Sets, 1-8/12 weeks, Peaking LOW-OPT",
            "Test Sets, Evaluation Sets, 0-1/4 weeks, Peaking LOW-OPT",
            "Evaluation Sets, Occasional Load Weeks, 0-1/4 weeks, Peaking LOW-OPT",
            "Majority of Load Weeks, Occasional Open Sets, 1-3/4 weeks, Peaking LOW-HIGH",
            "Majority of Base Work, Occasional Unload Work, 0-1/4 weeks, Peaking LOW-HIGH",
            "Majority of Unload Work, Occasional Base Work, 1-2/4 weeks",
            "Super Unload, 0-1/4 weeks, Seldom used as Unload",
            "Rarely used in Cycles, 0-1/4 weeks, Not enough load to yield adaptation"
        ]
    }
    
    code = pd.DataFrame(code)
    expander2.dataframe(code,hide_index=True, use_container_width=True)
    expander2.divider()
    expander2.write("Si vous souhaitez consulter vos meilleurs RM, cliquez sur le bouton ci dessous")
    repMaxMulti = expander2.number_input('Votre RM max pour la session de travail', step=1)
    chargeMaxMulti = expander2.number_input('Votre Charge max pour la session de travail', step=1)
    Serie_nb = expander2.selectbox('Nb de séries', (1,2,3,4,5,6,7,8,10)) 
    if repMaxMulti and chargeMaxMulti != 0 : 
        updatedbergerModified = bergerModified.copy()
        updatedbergerModified = updatedbergerModified.iloc[:,[0,Serie_nb]]
        
        updatedBergerTemp = berger.copy()
        rm1_calulated_multi = int((chargeMaxMulti) / (updatedBerger.iloc[int(repMaxMulti)]["Pourcentage"]))
        
        updatedbergerModified["Charge"] = updatedbergerModified[Serie_nb] * rm1_calulated_multi
        updatedbergerModified['Charge'] = updatedbergerModified['Charge'].astype(int)
        updatedbergerModified = updatedbergerModified.loc[updatedbergerModified.Charge > 0]
        updatedbergerModified = updatedbergerModified.rename(columns={Serie_nb: "Pourcentage pour "+str(Serie_nb)+" séries"})
        expander2.dataframe(updatedbergerModified, use_container_width=True, hide_index = True)


with tab6 : 
    st.subheader("Tous les wods présentés ici sont issus du site officiel de Crossfit.com ©️")
    st.write("Crossfit.com ©️ étant un site américain, les charges sont en lbs.")
    st.write("Pour les convertir en Kg, il faut soit diviser la charge par 2.2, sinon vous pouvez utiliser le convertisseur ci dessous")
    col1, col2 = st.columns([1,3],vertical_alignment="center")
    with col1:
        lbs = st.number_input("Charge en lbs")
    with col2 : 
        st.write("Votre charge en kg est de :", lbs*0.453592)
    
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
    expanderWODHero = st.expander(":red[Tous les WOD Hero]")
    wods = get_all_heroes()
    chosen_hero = expanderWODHero.selectbox("Quel WOD Hero voulez vous voir", [i["name"] for i in wods])
    if len(chosen_hero) > 0 : 
        wod = next((wod for wod in wods if wod['name'] == chosen_hero), None)
        expanderWODHero.markdown(wod['description'].replace('\n', '<br>'), unsafe_allow_html=True)

with tab7 :
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
# elif st.session_state["authentication_status"] is False:
#    st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')
