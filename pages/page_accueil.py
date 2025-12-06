import streamlit as st

APP_NAME = "**:red[Spotify Analyzer]**"
SPOTIFY_NAME = "**:green[Spotify] 🟢**"
DATA_TAB_NAME = "**:orange[Données] 💾**"


def main_accueil():
    st.header("Bienvenu sur Spotify Analyzer !")

    st.subheader("Qu'est-ce que c'est ?")

    first_body = f"""
    {APP_NAME} est un outil d'analyse d'historique d'écoute {SPOTIFY_NAME}.
    
    Chaque fin d'année, {SPOTIFY_NAME} publie pour tout un chacun sa rétrospective de l'année,
    mais ne fait pas de lien avec les statistiques de l'année précédente.
    
    {APP_NAME} intervient pour compléter la rétrospective de l'année, et afficher des statistiques clés
    sur les habitudes d'écoute sur tout votre historique.
    """

    st.markdown(body=first_body)

    st.divider()

    st.subheader("Comment ça marche ?")

    second_body = f"""
    Il est possible de récupérer auprès de {SPOTIFY_NAME} son historique intégral d'écoute, sous la forme de fichiers `.json`.
    
    Dans l'onglet {DATA_TAB_NAME} de {APP_NAME}, vous pouvez charger vos fichiers `.json`, et {APP_NAME} s'occupe de les charger dans un DataFrame polars.
    
    Vous pourrez ensuite consulter les onglets :orange[Analyses par écoutes] 📊 et :orange[Analyses par durées] ⌚, pour découvrir des statistiques
    intéressantes sur vos habitudes d'écoute.
    
    De manière arbitraire, il a été décidé que seules les écoutes supérieures à **20 secondes** sont prises en compte dans les statistiques.
    """

    st.markdown(body=second_body)

    st.divider()

    st.subheader("Qu'est-ce que je dois faire ?")

    third_body = f"""
    **1. Obtenir son historique d'écoute**
    
    - Il faut se rendre sur https://www.spotify.com/fr/account/privacy/ et se connecter à son compte {SPOTIFY_NAME}.
    - Il faut ensuite cocher la case pour demander l'intégralité de son historique d'écoute.
    - Puis demander l'envoi de ses données.
    
    **2. Récupérer son historique d'écoute**
    
    - Après quelques jours, vous recevrez un mail de {SPOTIFY_NAME} avec un lien pour télécharger un `.zip` de votre historique d'écoute.
    - Il faut cliquer sur le lien pour télécharger l'historique.
    - Une fois téléchargé, vous pourrez le dézipper pour extraire le dossier :blue[Spotify Extended Streaming History], qui contient les `.json`
    mentionnés plus haut.
    
    **3. Uploader son historique dans {APP_NAME}**
    
    - Vous n'avez plus qu'à uploader ces fichiers .json dans l'onglet {DATA_TAB_NAME}.
    """

    st.markdown(body=third_body)
