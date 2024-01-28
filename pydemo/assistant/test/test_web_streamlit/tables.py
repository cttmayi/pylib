import streamlit as st
import numpy as np
import pandas as pd


import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


data_df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        #"title": [3, 4, 5, 6],
        "title": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)


edited_df = st.data_editor(
    data_df.style.highlight_max(axis=0),
    use_container_width=True,
    # width=1440,
    column_order=['id', 'title', "category"],
    column_config={
        "id": st.column_config.Column(
            "ID",
            help="Streamlit **widget** commands 🎈",
            width="medium",
            required=True,
            disabled=True
        ),
        "title": st.column_config.Column(
            "Title",
            help="Streamlit **widget** commands 🎈",
            width="large",
            required=True,
            disabled=False
        ),
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="small",
            options=[
                "📊 Data Exploration", "📈 Data Visualization", "🤖 LLM",
            ],
            required=True,
        )
    },
    # hide_index=True,
    # num_rows="dynamic",
)

def callback():
    print('---')