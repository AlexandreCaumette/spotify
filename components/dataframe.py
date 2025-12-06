import streamlit as st

import data.constants as cst


def dataframe(data):
    st.dataframe(
        data=data,
        width=cst.VISUAL_WIDTH,
        column_config={"duration_seconds": None, "duration_minutes": None},
    )
