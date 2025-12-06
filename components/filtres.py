import datetime as dt
from typing import Tuple

import streamlit as st


def main_filtres() -> Tuple[dt.date, dt.date]:
    st.subheader("**:green[Filtres] 🟢**")

    df = st.session_state.initial_dataframe

    min_value = df["DATE"].min()
    max_value = df["DATE"].max()
    debut_annee = dt.datetime.now().replace(month=1, day=1)

    col_date_debut, col_date_fin = st.columns(2)

    with col_date_debut:
        date_debut = st.date_input(
            label="Sélectionner une date de début :",
            min_value=min_value,
            value=max(debut_annee, min_value),
            max_value=max_value,
        )

    with col_date_fin:
        date_fin = st.date_input(
            label="Sélectionner une date de fin :",
            min_value=date_debut,
            value=max_value,
            max_value=max_value,
        )

    st.divider()

    return date_debut, date_fin
