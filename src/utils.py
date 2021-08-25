import pandas as pd
import numpy as np
import streamlit as st

@st.cache
def load_dataframe(uploaded_file):
    try:
        dataframe = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        dataframe = pd.read_excel(uploaded_file)


    columns = list(dataframe.columns)
    columns.append(None)

    Index   = np.arange(0, len(dataframe), 1)
    dataframe.insert(0, 'Index', Index)

    return dataframe, columns

def plotted_analysis_simple_2d(dataframe, plot_config):
    '''
    Summary table
    '''

    
    with st.spinner("Calculating Summary Table"):
        plot_summary = pd.DataFrame(columns=['Symbol','Name','Min','Mean','Max'])

        for row in range(0,len(plot_config)):
            if plot_config["Symbol"][row] != "Not Selected":
                #if plot_config["Hex_rep"][row] == True:
                #    st.write("true: "+str(plot_config["Hex_rep"][row]))
                #    plot_summary = plot_summary.append({
                #                                            'Symbol'    : plot_config["Symbol"][row],
                #                                            'Name'      : plot_config["Name"][row],
                #                                            'Min'       : str(min(dataframe[plot_config["Symbol"][row]]))       + " (" + str( hex ( int( min(dataframe[plot_config["Symbol"][row]]) ) ) )     + ")",
                #                                            'Mean'      : str(np.mean(dataframe[plot_config["Symbol"][row]]))   + " (" + str( float.hex(np.mean(dataframe[plot_config["Symbol"][row]])))   + ")",
                #                                            'Max'       : str(max(dataframe[plot_config["Symbol"][row]]))       + " (" + str( hex(int(max(dataframe[plot_config["Symbol"][row]]))))       + ")"
                #                                            },
                #                                            ignore_index=True)

                
                    
                plot_summary = plot_summary.append({
                                                        'Symbol'    : plot_config["Symbol"][row],
                                                        'Name'      : plot_config["Name"][row],
                                                        'Min'       : min(dataframe[plot_config["Symbol"][row]]),
                                                        'Mean'      : np.mean(dataframe[plot_config["Symbol"][row]]),
                                                        'Max'       : max(dataframe[plot_config["Symbol"][row]])
                                                        },
                                                        ignore_index=True)               


    return st.subheader("Quick Analysis"), st.write(plot_summary)

def plotted_analysis_simple_3d(dataframe, plot_config):
    '''
    Summary table
    '''
    with st.spinner("Calculating Summary Table"):
        plot_summary = pd.DataFrame(columns=['Symbol','Name','Min','Mean','Max'])

        for row in range(0,3):
                    plot_summary = plot_summary.append({
                                                            'Symbol'    :plot_config["Symbol"][row],
                                                            'Name'      :plot_config["Name"][row],
                                                            'Min'       : min(dataframe[plot_config["Symbol"][row]]),
                                                            'Mean'      : np.mean(dataframe[plot_config["Symbol"][row]]),
                                                            'Max'       : max(dataframe[plot_config["Symbol"][row]])
                                                            },
                                                            ignore_index=True)               


    return st.subheader("Quick Analysis"), st.write(plot_summary)


def raw_data_display(dataframe):
    '''
    Display Raw Data as table
    '''
    with st.spinner("Loading Raw Data as Table"):
        return st.subheader("Raw Data"), st.write(dataframe)

def plotted_data_display(dataframe, plot_config):
    '''
    Display Plotted Data as table
    '''

    with st.spinner("Loading Plotted Data as Table"):
        plotted_data = pd.DataFrame()

        for rows in range(0,len(plot_config)):
            plotted_data[plot_config["Symbol"][rows]] = (dataframe[plot_config["Symbol"][rows]])

    return st.subheader("Plotted Data"), st.write(plotted_data)