
import streamlit as st
import numpy as np
import pandas as pd


import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
    }
)

edited_df = st.data_editor(
    data_df,
    column_config={
        "widgets": st.column_config.Column(
            "Streamlit Widgets",
            help="Streamlit **widget** commands 🎈",
            width="medium",
            required=True,
            disabled=True
        )
    },
    hide_index=True,
    num_rows="dynamic",
)

def callback():
    print('---')


# edited_df = st.data_editor(df, on_change=callback)

#favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
#st.markdown(f"Your favorite command is **{favorite_command}** 🎈")


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))


st.write("Here's our first attempt at using data to create a table:")
st.write(dataframe)

st.dataframe(dataframe.style.highlight_max(axis=0))


st.table(dataframe)