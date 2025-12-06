import streamlit as st

from data.spotify_cube import Cube


def main_chiffres_cles(cube: Cube):
    st.subheader("Chiffres clés de mes écoutes")

    columns_metrics = st.columns(3, border=True)

    columns_metrics[0].metric(
        label="Nombre d'artistes écoutés",
        value=cube.number_of_artists(),
    )

    columns_metrics[1].metric(
        label="Nombre de titres écoutés",
        value=cube.number_of_titles(),
    )

    columns_metrics[2].metric(label="Durée d'écoute", value=cube.duration())

    st.divider()
