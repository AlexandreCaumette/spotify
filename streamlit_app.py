import streamlit as st

from pages.page_accueil import main_accueil
from pages.page_donnees import main_donnees
from pages.page_durees import main_durees
from pages.page_ecoutes import main_ecoutes

# --========================================
# --= Configuration de la page
# --========================================


def main():
    st.set_page_config(
        page_title="Analyse tes données Spotify", page_icon="🟢", layout="wide"
    )

    st.title("Rétrospective de tout mon historique Spotify")

    with st.sidebar:
        page_accueil = st.Page(
            page=main_accueil,
            title="Accueil",
            icon="🏠",
            url_path="accueil",
            default=True,
        )

        page_data = st.Page(
            page=main_donnees,
            title="Données",
            icon="💾",
            url_path="donnees",
        )

        page_ecoutes = st.Page(
            page=main_ecoutes,
            title="Analyse par écoutes",
            icon="📊",
            url_path="ecutes",
        )

        page_durees = st.Page(
            page=main_durees,
            title="Analyse par durées",
            icon="⌚",
            url_path="durees",
        )

        pages = [
            page_accueil,
            page_data,
        ]

        if "initial_dataframe" in st.session_state:
            pages.extend([page_ecoutes, page_durees])

    current_page = st.navigation(pages=pages, expanded=True)

    current_page.run()


if __name__ == "__main__":
    main()
