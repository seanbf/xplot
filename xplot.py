from typing import Container
import streamlit as st
import pandas as pd

from src.functions import y_functions_dict
from src.layout import plotly_toolbar_config, view_2d_or_3d, plot_config_3d, plot_config_2d,  signal_container_3d, signal_container_2d
from src.plotter import plot_2D, plot_3D
from src.plot_setup import get_markers
from src.utils import load_dataframe, plotted_analysis_simple, raw_data_display, plotted_data_display

page_config = st.set_page_config  (
                page_title              ="xPlot", 
                page_icon               ="📈", 
                layout                  ='wide', 
                initial_sidebar_state   ='auto'
                )
# Main Page
st.sidebar.title('xPlot')
st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

toolbar                         = plotly_toolbar_config()
y_functions                     = y_functions_dict()
y_function_names                = list(y_functions.keys())

marker_names = get_markers()

# SIDEBAR BEHAVIOUR
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 650px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 650px;
        margin-left: -650px;
    }   
    </style>
    """,
    unsafe_allow_html=True,)

radio_2d_3d         = st.sidebar.radio('', ['2D Plot','3D Plot'], key="2Dor3D")

trace = view_2d_or_3d(radio_2d_3d)

if radio_2d_3d == '3D Plot':
    trace["Chart_Type"], trace["Fill_Value"], trace["Interp_Method"], trace["Grid_Res"], color_palette  = plot_config_3d(radio_2d_3d, trace)
else:
    color_palette, extra_signals  = plot_config_2d(radio_2d_3d)
   
uploaded_file = st.sidebar.file_uploader(label="",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])

if uploaded_file is None:
    st.warning("Please upload file(s) in the sidebar")
    st.stop()

elif uploaded_file is not None:

    dataframe, columns = load_dataframe(uploaded_file=uploaded_file)

    # Create Index array, to plot against. Not all data has timestamp
    symbols = list(dataframe)

    # Use to NOT plot.
    symbols.insert(0, "Not Selected")
    
    # Side bar items
    trace_function      = []
    signal_functions    = []
    
    # 3D Trace Configuration
    if radio_2d_3d == '3D Plot':
        
        trace["Symbol_X"], trace["Symbol_Y"], trace["Symbol_Z"], trace["Name_X"], trace["Name_Y"], trace["Name_Z"] = signal_container_3d(trace, symbols)
        
    # 2D Trace Configuration
    elif radio_2d_3d == '2D Plot':

        trace["Symbol"],trace["Name"],trace["Hex_rep"],trace["Bin_rep"],trace["Plot_row"],trace["Axis"],trace["Color"],trace["Size"],trace["Style"],trace["Chart_Type"] , trace["Function"],trace["Value"] ,trace["Extra_Signals"], symbol_0 = signal_container_2d(trace, symbols, color_palette, marker_names, y_function_names)    


plotted_data        = pd.DataFrame()
plot_sum            = []
plot_config     = pd.DataFrame(trace)

if radio_2d_3d == '2D Plot':
    plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
    plot_config.reset_index(inplace=True)

    plot = plot_2D(dataframe, plot_config, plotted_data, symbol_0)

else:
    plot = plot_3D(dataframe, plot_config, color_palette)

st.plotly_chart(plot, use_container_width=True, config=toolbar)
checkbox_raw = st.checkbox(label= "Display Raw Data as Table", key="Raw_Data")
checkbox_plotted = st.checkbox(label= "Display Plotted Data as Table", key="Plotted_Data")
plotted_analysis_simple(dataframe, plot_config)

if checkbox_plotted == True:
    plotted_data_display(dataframe, plot_config)

if checkbox_raw == True:
    raw_data_display(dataframe)