import streamlit as st
import altair as alt

CHART_WIDTH = 600

def bar_chart(data, x: str, y: str, tooltip: list = None):
    if tooltip is None:
        tooltip = [x, y]
        
    chart = (
        alt.Chart(data=data)
        .mark_bar()
        .encode(y=alt.Y(y, sort=alt.SortField(x, order='descending')),
                x=x,
                tooltip=tooltip)
        .properties(width=CHART_WIDTH)
    )
    
    return chart