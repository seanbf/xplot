import pandas as pd
import numpy as np
import streamlit as st

@st.cache
def load_dataframe(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)


    columns = list(df.columns)
    columns.append(None)

    #Index   = np.arange(0, len(df), 1)
    #df.insert(0, 'Index', Index)

    return df, columns