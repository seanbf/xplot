from numpy import empty
import streamlit as st
import pandas as pd
from streamlit.type_util import Key

from src.functions import y_functions_dict
from src.layout import sidebar_md, plotly_toolbar_config, view_select, plot_config_3d, plot_config_2d,  signal_container_3d, signal_container_2d
from src.plotter import plot_2D, plot_3D
from src.plot_setup import get_markers
from src.utils import load_dataframe, plotted_analysis_simple_2d, plotted_analysis_simple_3d, raw_data, plotted_data, z_col_or_grid, plotted_data_3d
from src.image_export import show_export_format, export_name, download_chart

page_config = st.set_page_config(
                                page_title              ="xPlot", 
                                page_icon               ="📈", 
                                layout                  ='wide', 
                                initial_sidebar_state   ='auto'
                                )

st.sidebar.title('xPlot')
st.sidebar.markdown('''<small>v1.0</small>''', unsafe_allow_html=True)


#Set up sidebar.
st.markdown(sidebar_md(), unsafe_allow_html=True)

toolbar             = plotly_toolbar_config()
y_functions         = y_functions_dict()
y_function_names    = list(y_functions.keys())

marker_names = get_markers()




#Determine if user wanted 2D or 3D plot.
st.sidebar.radio('', ['2D Plot','3D Plot'], key="View")

trace = view_select(st.session_state["View"])

# Initialization
if 'trace' not in st.session_state:
    st.session_state['trace'] = trace

if 'Color_Palette' not in st.session_state:
    st.session_state['Color_Palette'] = []

if "Export_File_Name" not in st.session_state:
    st.session_state["Export_File_Name"] = str()

if "Export_File_Type" not in st.session_state:
    st.session_state["Export_File_Type"] = str()

if "Plot" not in st.session_state:
    st.session_state["Plot"] = dict()

if st.session_state["View"] == '3D Plot':
    trace["Chart_Type"], trace["Fill_Value"], trace["Interp_Method"], trace["Grid_Res"], st.session_state["Color_Palette"], trace["Overlay"], trace["Overlay_Alpha"] ,trace["Overlay_Marker"] ,trace["Overlay_Color"]  = plot_config_3d(st.session_state["View"], trace, marker_names)

else:
    trace["Extra_Signals"], st.session_state["Color_Palette"]  = plot_config_2d(trace, st.session_state["View"])

#Ask for file upload and read.
st.sidebar.file_uploader(   
                                        label="",
                                        accept_multiple_files=False,
                                        type=['csv', 'xlsx'],
                                        key = "Uploaded File"
                                        )

if st.session_state["Uploaded File"] is None:
    st.info("Please upload file(s) in the sidebar")
    st.stop()

elif st.session_state["Uploaded File"] is not None:

    original_file_name  = st.session_state["Uploaded File"].name

    dataframe, columns  = load_dataframe(st.session_state["Uploaded File"])

    symbols             = list(dataframe)

    symbols.insert(0, "Not Selected")
    
    trace_function      = []
    signal_functions    = []

    if st.session_state["View"] == '3D Plot':
        trace["Symbol"],trace["Name"] = signal_container_3d(trace, symbols)

    elif st.session_state["View"] == '2D Plot':
        trace["Symbol"],trace["Name"],trace["Hex_rep"],trace["Bin_rep"],trace["Plot_row"],trace["Axis"],trace["Color"],trace["Size"],trace["Style"],trace["Chart_Type"] , trace["Function"],trace["Value"] ,trace["Extra_Signals"], symbol_0 = signal_container_2d(trace, symbols, st.session_state["Color_Palette"], marker_names, y_function_names)    




#Determine plot configuration based on user selection.
plot_config     = pd.DataFrame(trace)

if st.session_state["View"] == '2D Plot':
    plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
    plot_config.reset_index(inplace=True)

    if len(plot_config["Plot_row"]) == 0:
        st.info("Select an <X-axis> symbol and at least one <Y-axis> symbol")
        st.stop()
    
    plot = plot_2D(dataframe, plot_config, symbol_0)

else:
    if (plot_config["Symbol"][0] == 'Not Selected') or (plot_config["Symbol"][1] == 'Not Selected') or (plot_config["Symbol"][2] == 'Not Selected'):
        st.info("Select an <X-axis> symbol, <Y-axis> symbol and <Z-axis> symbol")
        st.stop()

    x, y, z = z_col_or_grid(dataframe, plot_config)
    plot = plot_3D(x, y, z,dataframe, plot_config, st.session_state["Color_Palette"], trace["Overlay"], trace["Overlay_Alpha"] ,trace["Overlay_Marker"] ,trace["Overlay_Color"] )


#Plot resulting chart

if st.session_state["Plot"] == {}:
        st.session_state["Plot"] = plot 
else:
    if st.button(label = "Update Plot"):
        st.session_state["Plot"] = plot 

st.session_state["Plot_Container"] = st.plotly_chart(st.session_state["Plot"], use_container_width=True, config=toolbar)


#Display analysis of plotted data
st.subheader("Quick Analysis")
if st.session_state["View"] == '2D Plot':
    quick_analysis_result = plotted_analysis_simple_2d(dataframe, plot_config)
    st.write(quick_analysis_result)
else:
    quick_analysis_result = plotted_analysis_simple_3d(dataframe, plot_config)
    st.write(quick_analysis_result)

#Prompt user with export options and links.
with st.expander("Export", expanded=True):
    col_export_name,col_export_format, col_datetime, col_generate_link, col_export_link = st.columns(5)
    
    col_export_name.text_input(label="Export Name: ", key = "Export Name")
    col_datetime.checkbox(label="Include datetime", key = "Export Datetime")

    st.session_state["Export_File_Name"] = export_name(st.session_state["Export Name"], st.session_state["Export Datetime"], original_file_name)
    st.session_state["Export_File_Type"] = show_export_format(col_export_format)

    st.checkbox("Export Plotted Data", value=False, key = "Export Plotted Data")
    st.checkbox("Export Raw Data", value=False, key = "Export Raw Data")

st.checkbox(label= "Display Raw Data as Table", key="Display Raw")
st.checkbox(label= "Display Plotted Data as Table", key="Display Plotted")

if st.session_state["Display Plotted"] == True: 
    st.subheader("Plotted Data") 

    if st.session_state["View"] == '3D Plot':
        plotted_table = plotted_data_3d(x,y,z,plot_config)
        st.write(plotted_table)
    else:
        plotted_table = plotted_data(dataframe, plot_config)
        st.write(plotted_table)

if st.session_state["Display Raw"] == True:
        st.subheader("Raw Data")
        raw_table = raw_data(dataframe)
        st.write(raw_table)

if col_generate_link.button("Generate File") == True:
    try:
        download_chart(st.session_state["Plot"], quick_analysis_result, st.session_state["Export Plotted Data"], st.session_state["Export Raw Data"], plotted_table, raw_table, st.session_state["Export_File_Type"], st.session_state["Export_File_Name"], col_export_link )
    except:
        raw_table = raw_data(dataframe)
        if st.session_state["View"] == '3D Plot':
            plotted_table = plotted_data_3d(x,y,z,plot_config)
        else:
            plotted_table = plotted_data(dataframe, plot_config)
        download_chart(st.session_state["Plot"], quick_analysis_result, st.session_state["Export Plotted Data"], st.session_state["Export Raw Data"], plotted_table, raw_table, st.session_state["Export_File_Type"], st.session_state["Export_File_Name"], col_export_link )