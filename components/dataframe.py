import streamlit as st


def dataframe(data):
    st.dataframe(
        data=data,
        column_config={"duration_seconds": None, "duration_minutes": None},
    )
