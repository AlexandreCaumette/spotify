from streamlit.delta_generator import DeltaGenerator
import data.constants as cst

def dataframe(parent: DeltaGenerator, data):
    parent.dataframe(data=data,
                     width=cst.VISUAL_WIDTH,
                     column_config={
                         'duration_seconds': None,
                         'duration_minutes': None
                         })