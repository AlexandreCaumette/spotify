#################################
###   Import des librairies   ###
#################################


import streamlit as st
from components.tab_home import render_tab_home
from components.tab_data import render_tab_data
from components.tab_analyze import render_tab_analyze
import data.constants as cst

####################################
###   Configuration de la page   ###
####################################


st.set_page_config(page_title='Spotify Analyser',
                   page_icon='🟢ᯤ',
                   layout='wide')

st.title('Rétrospective de tout mon historique Spotify')

tab_home, tab_data, tab_analyze_by_listening, tab_analyze_by_duration = st.tabs([
    '🏠 Accueil',
    '💾 Données',
    '📊 Analyse par écoutes',
    '⌚ Analyse par durées'
])

render_tab_home(tab_home)
render_tab_data(tab_data)

if 'initial_dataframe' in st.session_state:
    render_tab_analyze(tab_analyze_by_listening, measure=cst.MEASURE_COUNT_NAME)
    render_tab_analyze(tab_analyze_by_duration, measure=cst.MEASURE_DURATION_NAME)