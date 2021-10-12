import pandas as pd
import numpy as np
import streamlit as st
from scipy.interpolate import griddata

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


    return plot_summary

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


    return plot_summary


def raw_data(dataframe):
    '''
    Display Raw Data as table
    '''
    with st.spinner("Loading Raw Data as Table"):
        return dataframe

def plotted_data(dataframe, plot_config):
    '''
    Display Plotted Data as table
    '''

    with st.spinner("Loading Plotted Data as Table"):
        plotted_data = pd.DataFrame()

        for rows in range(0,len(plot_config)):
            plotted_data[plot_config["Symbol"][rows]] = (dataframe[plot_config["Symbol"][rows]])

    return plotted_data

def z_col_or_grid(dataframe, plot_config):
    '''
    Depending on graph wanted, format data as grid or columns
    '''
    x = dataframe[plot_config["Symbol"][0]]
    y = dataframe[plot_config["Symbol"][1]]
    z = dataframe[plot_config["Symbol"][2]]

    if plot_config["Chart_Type"][0] != '3D Scatter':

        xi = np.linspace( float(min(x)), float(max(x)), int(plot_config["Grid_Res"][0]) )
        yi = np.linspace( float(min(y)), float(max(y)), int(plot_config["Grid_Res"][0]) )

        X,Y = np.meshgrid(xi,yi)

        z = griddata( (x,y),z,(X,Y), fill_value=plot_config["Fill_Value"][0], method='linear')  
        x = xi
        y = yi

    return x, y, z

def plotted_data_3d(x, y , z, plot_config):
    '''
    Display data plotted 3d graph in correct format.
    '''
    if plot_config["Chart_Type"][0] == '3D Scatter':
        table_3d = pd.DataFrame([x,y,z])
        table_3d.rename(columns={'x':str(plot_config["Symbol"][0]),'y':str(plot_config["Symbol"][1]),'z':str(plot_config["Symbol"][2])}, inplace = True)
    else:
        x = np.round(x, 4)
        table_3d = pd.DataFrame(z)
        table_3d.columns = [x]
        table_3d.index = [y]
        table_3d = table_3d.sort_index(ascending=False)
    return table_3d