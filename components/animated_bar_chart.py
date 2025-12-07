import bar_chart_race as bcr
import polars as pl
import streamlit as st


def main_animated_bar_chart(df: pl.DataFrame):
    st.divider()

    st.subheader("Course des artistes !")

    col_top_n, col_mesure, col_maille = st.columns(3)

    with col_top_n:
        top_n = st.slider(
            label="Garder les N premiers artistes chaque mois :",
            min_value=1,
            max_value=10,
            value=5,
        )

    with col_mesure:
        options_mesure = {
            "Nombre d'écoutes": "NOMBRE_ECOUTES",
            "Nombre d'écoutes cumulées": "NOMBRE_ECOUTES_CUMULEES",
        }

        mesure = st.segmented_control(
            label="Sélectionner la mesure pour compter les écoutes :",
            options=options_mesure.keys(),
            default=list(options_mesure.keys())[1],
        )

        if mesure in options_mesure:
            colonne_count = options_mesure.get(mesure)

        else:
            colonne_count = "NOMBRE_ECOUTES_CUMULEES"

    with col_maille:
        options_maille = {"Jour": "1d", "Mois": "1mo", "Trimestre": "1q", "Année": "1y"}

        maille = st.selectbox(
            label="Sélectionner la maille d'agrégation temporelle :",
            options=options_maille.keys(),
            index=1,
        )

        every = options_maille.get(maille, "1mo")

    df = df.sort("DATE")

    monthly_counts = df.group_by_dynamic(
        index_column="DATE", every=every, group_by="Artiste"
    ).agg(pl.count("Titre").alias("NOMBRE_ECOUTES"))

    top_artists = monthly_counts.with_columns(
        pl.col("NOMBRE_ECOUTES")
        .cum_sum()
        .over("Artiste")
        .alias("NOMBRE_ECOUTES_CUMULEES")
    )

    top_artists = (
        top_artists.sort(["DATE", colonne_count], descending=[False, True])
        .group_by("DATE")
        .head(top_n)
        .sort(["DATE", colonne_count], descending=[False, True])
    )

    df_values, _ = bcr.prepare_long_data(
        df=top_artists.to_pandas(),
        index="DATE",
        columns="Artiste",
        values=colonne_count,
        steps_per_period=1,
        orientation="h",
        sort="desc",
    )

    with st.spinner(show_time=True, text="Préparation de l'animation..."):
        race = bcr.bar_chart_race(
            df=df_values,
            orientation="h",
            sort="desc",
            n_bars=top_n,
            fixed_order=False,
            fixed_max=True,
            steps_per_period=30,
            period_length=4000,
            interpolate_period=False,
            label_bars=True,
            period_label=True,
            period_fmt="%B %Y",
            period_summary_func=lambda v, r: {
                "x": 0.98,
                "y": 0.2,
                "s": f"{mesure} : {v.sum():,.0f}",
                "ha": "right",
                "size": 11,
            },
            perpendicular_bar_func="median",
            title="Classement des artistes les plus écoutés",
            bar_size=0.95,
            shared_fontdict=None,
            scale="linear",
            fig=None,
            writer=None,
            bar_kwargs={"alpha": 0.7},
            filter_column_colors=True,
        )

        st.html(race)
