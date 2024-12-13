#################################
###   Import des librairies   ###
#################################


import streamlit as st
from components.tab_data import render_tab_data
from components.tab_analyze import render_tab_analyze

####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title='Spotify Analyser',
                   page_icon='🟢ᯤ',
                   layout='wide')

st.title('Rétrospective de tout mon historique Spotify')

tab_data, tab_analyze_by_listening, tab_analyze_by_duration = st.tabs(['💾 Données', '📊 Analyse par écoutes', '⌚ Analyse par durées'])

render_tab_data(tab_data)

if 'initial_dataframe' in st.session_state:
    render_tab_analyze(tab_analyze_by_listening, measure='Nombre de titres écoutés')
    render_tab_analyze(tab_analyze_by_duration, measure="Durée d'écoute")