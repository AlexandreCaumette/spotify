import streamlit as st
from data.spotify_cube import Cube
import altair as alt
from streamlit.delta_generator import DeltaGenerator
from components.bar_chart import bar_chart

cube = Cube()

def render_tab_analyze(tab: DeltaGenerator, measure: str):
    ################################################################################################
    
    tab.header("Statistiques sur tout l'historique")
    
    columns_metrics = tab.columns([1, 1, 1])
    
    columns_metrics[0].metric(label="Nombre d'artistes écoutés sur tout l'historique",
              value=cube.number_of_artists())
    
    columns_metrics[1].metric(label="Nombre de titres écoutés sur tout l'historique",
              value=cube.number_of_titles())
    
    columns_metrics[2].metric(label="Durée d'écoute sur tout l'historique",
              value=cube.duration())
    
    tab.subheader("Classement des écoutes par artiste sur tout l'historique")

    tab.dataframe(data=cube.artists_ranking(over=measure),
                  width=None)
    
    tab.subheader("Classement des écoutes par titre sur tout l'historique")
    
    tab.dataframe(data=cube.titles_ranking(over=measure),
                  width=None)
    
    tab.divider()
    
    ################################################################################################
    
    tab.header("Statistiques annuelles")
    
    tab.subheader("Classement du top 5 des écoutes par année")
    
    tab.multiselect(label='Sélectionner les années à afficher',
                    options=cube.years(),
                    key=f'multiselect_years_{measure}',
                    default=cube.years()[:3])
    
    container = tab.container()
    
    columns_years = container.columns([1, 1])

    for year in sorted(st.session_state[f'multiselect_years_{measure}'], reverse=True):
        columns_years[0].text(f"Classement artistes pour l'année {year}")
        columns_years[1].text(f"Classement titres pour l'année {year}")

        chart = bar_chart(data=cube.artists_ranking_by_year(years=[year]),
                          y='ARTISTE',
                          x='Nombre de titres écoutés')
        columns_years[0].altair_chart(chart)

        chart = bar_chart(data=cube.titles_ranking_by_year(years=[year]),
                          y='TITRE',
                          x='Nombre de titres écoutés',
                          tooltip=['ARTISTE', 'TITRE', 'Nombre de titres écoutés'])
        columns_years[1].altair_chart(chart)
        
    columns_years[0].subheader("Classement du top 5 des écoutes par artiste par année")
        
    columns_years[0].dataframe(data=cube.artists_ranking_by_year(years=st.session_state[f'multiselect_years_{measure}']),
                  width=None)
    
    columns_years[1].subheader("Classement du top 5 des écoutes par titre par année")
        
    columns_years[1].dataframe(data=cube.titles_ranking_by_year(years=st.session_state[f'multiselect_years_{measure}']),
                  width=None)
    
    tab.divider()
    
    ################################################################################################
    
    tab.header("Statistiques mensuelles")
    
    tab.subheader("Classement du top 5 des écoutes par mois")
    
    tab.multiselect(label='Sélectionner les mois à afficher',
                    options=cube.months(),
                    key=f'multiselect_months_{measure}',
                    default=cube.months()[:3])
    
    container = tab.container()
    
    columns_months = container.columns([1, 1])

    for month in sorted(st.session_state[f'multiselect_months_{measure}'], reverse=True):
        columns_months[0].text(f"Classement artistes pour l'année {month}")
        columns_months[1].text(f"Classement titres pour l'année {month}")

        chart = bar_chart(data=cube.artists_ranking_by_month(months=[month]),
                          y='ARTISTE',
                          x='Nombre de titres écoutés')
        columns_months[0].altair_chart(chart)

        chart = bar_chart(data=cube.titles_ranking_by_month(months=[month]),
                          y='TITRE',
                          x='Nombre de titres écoutés',
                          tooltip=['ARTISTE', 'TITRE', 'Nombre de titres écoutés'])
        columns_months[1].altair_chart(chart)
        
    columns_months[0].subheader("Classement du top 5 des écoutes par artiste par mois")
        
    columns_months[0].dataframe(data=cube.artists_ranking_by_month(months=st.session_state[f'multiselect_months_{measure}']),
                  width=None)
    
    columns_months[1].subheader("Classement du top 5 des écoutes par titre par mois")
        
    columns_months[1].dataframe(data=cube.titles_ranking_by_month(months=st.session_state[f'multiselect_months_{measure}']),
                  width=None)