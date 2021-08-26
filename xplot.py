from typing import Container
import streamlit as st
import pandas as pd

from src.functions import y_functions_dict
from src.layout import plotly_toolbar_config, view_2d_or_3d, plot_config_3d, plot_config_2d,  signal_container_3d, signal_container_2d
from src.plotter import plot_2D, plot_3D
from src.plot_setup import get_markers
from src.utils import load_dataframe, plotted_analysis_simple_2d, plotted_analysis_simple_3d, raw_data_display, plotted_data_display, z_col_or_grid, plotted_data_display_3d
from src.image_export import show_export_format, export_name, download_chart

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
        width: 600px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 600px;
        margin-left: -600px;
    }   
    </style>
    """,
    unsafe_allow_html=True,)

radio_2d_3d         = st.sidebar.radio('', ['2D Plot','3D Plot'], key="2Dor3D")

trace = view_2d_or_3d(radio_2d_3d)

if radio_2d_3d == '3D Plot':
    trace["Chart_Type"], trace["Fill_Value"], trace["Interp_Method"], trace["Grid_Res"], color_palette, overlay  = plot_config_3d(radio_2d_3d, trace)
else:
    trace["Extra_Signals"], color_palette  = plot_config_2d(trace, radio_2d_3d)
   
uploaded_file = st.sidebar.file_uploader(label="",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])

if uploaded_file is None:
    st.info("Please upload file(s) in the sidebar")
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
        
        trace["Symbol"],trace["Name"] = signal_container_3d(trace, symbols)
        
    # 2D Trace Configuration
    elif radio_2d_3d == '2D Plot':

        trace["Symbol"],trace["Name"],trace["Hex_rep"],trace["Bin_rep"],trace["Plot_row"],trace["Axis"],trace["Color"],trace["Size"],trace["Style"],trace["Chart_Type"] , trace["Function"],trace["Value"] ,trace["Extra_Signals"], symbol_0 = signal_container_2d(trace, symbols, color_palette, marker_names, y_function_names)    


plotted_data        = pd.DataFrame()
plot_sum            = []
plot_config     = pd.DataFrame(trace)

if radio_2d_3d == '2D Plot':
    plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
    plot_config.reset_index(inplace=True)

    if len(plot_config["Plot_row"]) == 0:
        st.info("Select an <X-axis> symbol and at least one <Y-axis> symbol")
        st.stop()
    plot = plot_2D(dataframe, plot_config, plotted_data, symbol_0)

else:
    if (plot_config["Symbol"][0] == 'Not Selected') or (plot_config["Symbol"][1] == 'Not Selected') or (plot_config["Symbol"][2] == 'Not Selected'):
        st.info("Select an <X-axis> symbol, <Y-axis> symbol and <Z-axis> symbol")
        st.stop()

    x, y, z = z_col_or_grid(dataframe, plot_config)
    plot = plot_3D(x, y, z,dataframe, plot_config, color_palette, overlay)

st.plotly_chart(plot, use_container_width=True, config=toolbar)

if radio_2d_3d == '2D Plot':
    plotted_analysis_simple_2d(dataframe, plot_config)
else:
    plotted_analysis_simple_3d(dataframe, plot_config)


checkbox_raw = st.checkbox(label= "Display Raw Data as Table", key="Raw_Data")
checkbox_plotted = st.checkbox(label= "Display Plotted Data as Table", key="Plotted_Data")

with st.expander("Export", expanded=True):
    col_export_name,col_export_format, col_datetime, col_generate_link, col_export_link = st.columns(5)
    file_name       = export_name(col_export_name, col_datetime)
    export_format   = show_export_format(col_export_format)

if col_generate_link.button("Generate File") == True:
    download_chart(plot, export_format, file_name, col_export_link )

if checkbox_plotted == True:   
    if radio_2d_3d == '3D Plot':
        plotted_data_display_3d(x,y,z,plot_config)
    else:
        plotted_data_display(dataframe, plot_config)

if checkbox_raw == True:
    raw_data_display(dataframe)