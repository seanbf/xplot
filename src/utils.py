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

def plotted_analysis_simple(df, plot_config):
    '''
    Summary table
    '''
    plot_summary = pd.DataFrame()
    for row in plot_config:
        if plot_config["Symbol"][row] != "Not Selected":
            max_signal      = max(df(plot_config["Symbol"][row]))
            min_signal      = min(df(plot_config["Symbol"][row]))
            mean_signal     = np.mean(df(plot_config["Symbol"][row]))
            
            if df(plot_config["Name"][row]) != "":
                Name        = df(plot_config["Name"][row])
            else:
                Name        = df(plot_config["Symbol"][row])

        plot_summary.append([Name, max_signal, min_signal ,mean_signal])

    return plot_summary