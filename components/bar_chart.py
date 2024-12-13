import altair as alt
import data.constants as cst

def bar_chart(data, x: str, y: str, tooltip: list = None):
    if x == cst.MEASURE_DURATION_NAME:
        x = 'duration_minutes'
        x_label = f'{cst.MEASURE_DURATION_NAME} (en minutes)'
    else:
        x_label = x
        
    if tooltip is None:
        tooltip = [x, y]
        
    chart = (
        alt.Chart(data=data)
        .mark_bar()
        .encode(y=alt.Y(y, sort=alt.SortField(x, order='descending')),
                x=alt.X(x).title(x_label),
                tooltip=tooltip)
        .properties(width=cst.VISUAL_WIDTH)
    )
    
    return chart