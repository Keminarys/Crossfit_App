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

### Function 
def get_conn() :
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
def get_df(sheet_name) :
    datas = conn.read(worksheet=sheet_name)
    return datas

### Variable

conn = get_conn()
all_mvmt = get_df("All_mvmt")

df = get_df("Progression")
df = df[['Profil','Category','Exercice','Date','Perf','Unité','RM']].dropna()

df_name = get_df("Profils")
df_name = df_name[['Name']].dropna()

df_obj = get_df("Objectif")
df_obj = df_obj[['Name','Task','Description','Start','Finish','Completed']].dropna()
df_obj['Start'] = pd.to_datetime(df_obj['Start'], format='%d/%m/%Y')
df_obj['Finish'] = pd.to_datetime(df_obj['Finish'], format='%d/%m/%Y')


list_name = list(df_name["Name"].unique())
list_name = [x for x in list_name if str(x) != "nan"]
list_rm = [1,3,5,10]
dico_ex = all_mvmt.groupby('Category')['Exercice'].unique().apply(list).to_dict()
dico_units = all_mvmt[['Category','Units']].drop_duplicates().set_index('Category').to_dict()['Units']

### Main

st.title('Crossfit83 Le Beausset')
st.divider()
st.subheader('Si c\'est votre première visite merci d\'ajouter votre profil dans la barre latérale')
st.write('_Par soucis de RGPD merci de ne renseigner que les 3 premières lettre de votre prénom et la première de votre nom de famille_')
st.divider()
athl = st.selectbox('Choix du profil', list_name)
st.divider()

data_full_scoped = df.loc[df['Profil'] == athl]

with st.sidebar :
    
    new_ppl = st.text_input('Ecrire votre nom ici')
    if st.button('Ajouter mon profil') :
        df_newname = pd.concat([df_name, pd.DataFrame({'Name' : new_ppl}, index=[len(df_name)])], ignore_index=True)
        df_newname = conn.update(worksheet="Profils",data=df_newname)
        st.cache_data.clear()
        st.rerun()
  
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎉 Nouvelle Performance", "📈 Aperçu de la progression", "📊 Data","💪🎯 Objectifs", "🏋️‍♂️🤖 WOD Generator"])

with tab1 :
    cat = st.selectbox('Choix de la catégorie', list(dico_ex.keys()))
    ex = st.selectbox('Choix de l"exercice', dico_ex[cat])
    if cat == 'WEIGHTLIFTING' : 
        rm = st.selectbox('Choix du RM', list_rm)
    else : rm = ''
    if cat == 'RUN' :
        nb = st.text_input('Temps au format mm\:ss', "00:00")
    else : nb = st.number_input('Max reps/charge', step=1)
    date = st.date_input('Date de réalisation', value = "today")
    unit = dico_units[cat]
    new_entry = {'Profil' : athl,
                'Category' : cat,
                'Exercice' : ex,
                'Date' : date,
                'Perf' : nb,
                'Unité' : unit,
                'RM' : rm}
    if st.button('Ajouter un nouveau record à mon profil :muscle:') :
        df_record = pd.concat([df, pd.DataFrame(new_entry, index=[len(df)])], ignore_index=True)
        df_record = conn.update(worksheet="Progression",data=df_record)
        st.write('Ajouté avec succès, vous pouvez retrouver toutes vos performances dans l\'onglet Data ✅')
        st.cache_data.clear()
        st.rerun()
    
with tab2 : 
    st.write('Sélectionner un mouvement spécifique pour avoir un aperçu de votre progression')
    
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
    data_graph['Exo_RM'] = data_graph['Exercice'] + '// RM : ' +data_graph['RM'].astype(str)
    fig_line = px.line(data_graph,x="Date", y="Perf", color='Exo_RM', markers=True)
    st.plotly_chart(fig_line,use_container_width=True)
    
with tab3 :
    st.write('Vous pouvez consulter l\'entièreté de vos performances ci dessous.')
    st.dataframe(data_full_scoped)

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
