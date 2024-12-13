import streamlit as st
import polars as pl
import os


base_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

def update_spotify_folder():
    st.session_state['spotify_folder'] = os.path.join(base_dir, st.session_state['spotify_folder_selectbox'])

def generate_unique_parquet(filenames):
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
    
    for f in filenames:
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
        
def render_tab_data(tab):
    tab.header("Sélection du dossier d'historique partagé par Spotify")

    filenames = os.listdir(base_dir)
    filenames = [f for f in filenames if os.path.isdir(os.path.join(base_dir, f))]
    folder_names = [f for f in filenames if 'spotify' in f.lower()]

    tab.selectbox(label='Sélectionnez le dossier extrait de Spotify',
                                        options=folder_names,
                                        key='spotify_folder_selectbox',
                                        help="Spotify vous a envoyé un mail avec un lien pour télécharger un .zip de votre historique, vous devez sélectionner le dossier qui contient l'extraction de ce zip (par défaut dans votre dossier téléchargement).",
                                        on_change=update_spotify_folder)

    if 'spotify_folder' in st.session_state:
        tab.write('Vous avez sélectionné le dossier : `%s`' % st.session_state.spotify_folder)
        
        spotify_history_folder = os.path.join(st.session_state.spotify_folder, 'Spotify Extended Streaming History')
            
        filenames = [os.path.join(spotify_history_folder, f) for f in os.listdir(spotify_history_folder) if 'Audio' in f]

        tab.dataframe(pl.DataFrame(filenames, schema=['Fichiers Audio']))
        
        tab.button(label='Utiliser ces fichiers',
            on_click=generate_unique_parquet,
            args=[filenames])

    tab.divider()

    tab.header("Exploration des données historisées par Spotify")

    if 'initial_dataframe' in st.session_state:
        df = st.session_state.initial_dataframe
        
        tab.subheader("Données fournies par Spotify")
        
        tab.dataframe(df)
        
        st.divider()