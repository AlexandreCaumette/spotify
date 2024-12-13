import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import polars as pl
import os


base_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

def generate_unique_parquet():
    list_df = []
    
    schema = {
        "ts": pl.String,
        "platform": pl.String,
        "ms_played": pl.Int64,
        "conn_country": pl.String,
        "ip_addr": pl.String,
        "master_metadata_track_name": pl.String,
        "master_metadata_album_artist_name": pl.String,
        "master_metadata_album_album_name": pl.String,
        "spotify_track_uri": pl.String,
        "episode_name": pl.String,
        "episode_show_name": pl.String,
        "spotify_episode_uri": pl.String,
        "reason_start": pl.String,
        "reason_end": pl.String,
        "shuffle": pl.Boolean,
        "skipped": pl.Boolean,
        "offline": pl.Boolean,
        "offline_timestamp": pl.Int64,
        "incognito_mode": pl.Boolean
    }
    
    for f in st.session_state.uploaded_files:
        list_df.append(pl.read_json(f, schema=schema))
        
    df = pl.concat(list_df)
    
    df = df.rename(mapping={
        'master_metadata_album_artist_name': 'ARTISTE',
        'master_metadata_track_name': 'TITRE'
    })
    
    df = df.with_columns(pl.concat_str([pl.col('ARTISTE'), pl.col('TITRE')], separator=' - ').alias('ARTISTE_TITRE'))
        
    df = df.with_columns(pl.Series('duration_seconds', df['ms_played'] / 1000))
    df = df.with_columns(pl.Series('duration_minutes', df['duration_seconds'] / 60))
    
    df = df.filter(df['duration_seconds'] >= 20)
    
    df = df.filter(df['episode_name'].is_null())
    
    df = df.with_columns(pl.Series('ANNEE', df['ts'].str.slice(0, 4)))
    df = df.with_columns(pl.Series('ANNEE_MOIS', df['ts'].str.slice(0, 7)))
    df = df.with_columns(pl.col('ts').str.strptime(pl.Datetime, '%Y-%m-%dT%H:%M:%SZ').alias('DATE'))
    
    st.session_state['initial_dataframe'] = df
        
def render_tab_data(tab: DeltaGenerator):
    tab.header("Chargement de l'historique Spotify")
    
    tab.subheader("Sélection des données partagées par Spotify")
    
    tab.file_uploader(label='Sélectionnez les fichiers de Spotify',
                      type='.json',
                      accept_multiple_files=True,
                      key='uploaded_files',
                      help="VOus avez récupéré de Spotify un .zip, dont vous pouvez extraire plusieurs fichiers .json qui constituent votre historique d'écoute.")

    tab.subheader("Affichage des fichiers audios qui seront chargés")
    
    if 'uploaded_files' in st.session_state:            
        filenames = [f.name for f in st.session_state['uploaded_files'] if 'Audio' in f.name]

        tab.dataframe(pl.DataFrame(filenames, schema=['Fichiers Audio']),
                      width=600)
        
        if len(filenames) > 0:
            tab.button(label='Utiliser ces fichiers',
                on_click=generate_unique_parquet)

    tab.divider()

    tab.header("Exploration des données historisées par Spotify")

    if 'initial_dataframe' in st.session_state:
        df = st.session_state.initial_dataframe
        
        tab.subheader("Données fournies par Spotify")
        
        tab.dataframe(df)
        
        st.divider()