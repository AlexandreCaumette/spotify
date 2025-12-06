import streamlit as st

from components.bar_chart import bar_chart
from components.dataframe import dataframe
from data.spotify_cube import Cube

cube = Cube()


def main_ecoutes():
    measure = "Nombre de titres écoutés"
    ################################################################################################

    st.header("Statistiques sur tout l'historique")

    columns_metrics = st.columns([1, 1, 1])

    columns_metrics[0].metric(
        label="Nombre d'artistes écoutés sur tout l'historique",
        value=cube.number_of_artists(),
    )

    columns_metrics[1].metric(
        label="Nombre de titres écoutés sur tout l'historique",
        value=cube.number_of_titles(),
    )

    columns_metrics[2].metric(
        label="Durée d'écoute sur tout l'historique", value=cube.duration()
    )

    st.subheader("Classement des écoutes par artiste sur tout l'historique")

    dataframe(data=cube.artists_ranking(over=measure))

    st.subheader("Classement des écoutes par titre sur tout l'historique")

    dataframe(data=cube.titles_ranking(over=measure))

    st.divider()

    ################################################################################################

    st.header("Statistiques annuelles")

    st.subheader("Classement du top 5 des écoutes par année")

    st.multiselect(
        label="Sélectionner les années à afficher",
        options=cube.years(),
        key=f"multiselect_years_{measure}",
        default=cube.years()[:3],
    )

    container = st.container()

    columns_years = container.columns([1, 1])

    for year in sorted(st.session_state[f"multiselect_years_{measure}"], reverse=True):
        columns_years[0].text(f"Classement artistes pour l'année {year}")
        columns_years[1].text(f"Classement titres pour l'année {year}")

        chart = bar_chart(
            data=cube.artists_ranking_by_year(years=[year], over=measure),
            y="Artiste",
            x=measure,
            tooltip=["Artiste", measure],
        )
        columns_years[0].altair_chart(chart)

        chart = bar_chart(
            data=cube.titles_ranking_by_year(years=[year], over=measure),
            y="Titre",
            x=measure,
            tooltip=["Artiste", "Titre", measure],
        )
        columns_years[1].altair_chart(chart)

    columns_years[0].subheader("Classement du top 5 des écoutes par artiste par année")

    with columns_years[0]:
        dataframe(
            data=cube.artists_ranking_by_year(
                years=st.session_state[f"multiselect_years_{measure}"], over=measure
            ),
        )

    columns_years[1].subheader("Classement du top 5 des écoutes par titre par année")

    with columns_years[1]:
        dataframe(
            data=cube.titles_ranking_by_year(
                years=st.session_state[f"multiselect_years_{measure}"], over=measure
            ),
        )

    st.divider()

    ################################################################################################

    st.header("Statistiques mensuelles")

    st.subheader("Classement du top 5 des écoutes par mois")

    st.multiselect(
        label="Sélectionner les mois à afficher",
        options=cube.months(),
        key=f"multiselect_months_{measure}",
        default=cube.months()[:3],
    )

    container = st.container()

    columns_months = container.columns([1, 1])

    for month in sorted(
        st.session_state[f"multiselect_months_{measure}"], reverse=True
    ):
        columns_months[0].text(f"Classement artistes pour l'année {month}")
        columns_months[1].text(f"Classement titres pour l'année {month}")

        chart = bar_chart(
            data=cube.artists_ranking_by_month(months=[month], over=measure),
            y="Artiste",
            x=measure,
            tooltip=["Artiste", measure],
        )
        columns_months[0].altair_chart(chart)

        chart = bar_chart(
            data=cube.titles_ranking_by_month(months=[month], over=measure),
            y="Titre",
            x=measure,
            tooltip=["Artiste", "Titre", measure],
        )
        columns_months[1].altair_chart(chart)

    columns_months[0].subheader("Classement du top 5 des écoutes par artiste par mois")

    with columns_months[0]:
        dataframe(
            data=cube.artists_ranking_by_month(
                months=st.session_state[f"multiselect_months_{measure}"], over=measure
            ),
        )

    columns_months[1].subheader("Classement du top 5 des écoutes par titre par mois")

    with columns_months[1]:
        dataframe(
            data=cube.titles_ranking_by_month(
                months=st.session_state[f"multiselect_months_{measure}"], over=measure
            ),
        )
