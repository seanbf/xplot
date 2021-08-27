import streamlit as st
import pandas as pd

from src.functions import y_functions_dict
from src.layout import sidebar_config, plotly_toolbar_config, view_2d_or_3d, plot_config_3d, plot_config_2d,  signal_container_3d, signal_container_2d
from src.plotter import plot_2D, plot_3D
from src.plot_setup import get_markers
from src.utils import load_dataframe, raw_data, plotted_data, z_col_or_grid, plotted_data_3d, plotted_analysis
from src.image_export import show_export_format, export_name, download_chart

page_config = st.set_page_config  (
                page_title              ="xPlot", 
                page_icon               ="📈", 
                layout                  ='wide', 
                initial_sidebar_state   ='auto'
                )

sidebar_config()

# Main Page
st.sidebar.title('xPlot')
st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

toolbar                         = plotly_toolbar_config()
y_functions                     = y_functions_dict()
y_function_names                = list(y_functions.keys())

marker_names    = get_markers()

radio_2d_3d     = st.sidebar.radio('', ['2D Plot','3D Plot'], key="2Dor3D")

trace           = view_2d_or_3d(radio_2d_3d)

if radio_2d_3d == '3D Plot':
    trace, color_palette, overlay, overlay_alpha, overlay_marker, overlay_color = plot_config_3d(radio_2d_3d, trace, marker_names)
else:
    trace, color_palette  = plot_config_2d(trace, radio_2d_3d)
   
uploaded_file = st.sidebar.file_uploader(label="",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])

if uploaded_file is None:
    st.info("Please upload file(s) in the sidebar")
    st.stop()

elif uploaded_file is not None:

    dataframe, columns = load_dataframe(uploaded_file=uploaded_file)

    symbols = list(dataframe)

    # Use to NOT plot.
    symbols.insert(0, "Not Selected")
    
    # Side bar items
    trace_function      = []
    signal_functions    = []
    
    # 3D Trace Configuration
    if radio_2d_3d == '3D Plot':
        
        trace = signal_container_3d(trace, symbols)
        
    # 2D Trace Configuration
    elif radio_2d_3d == '2D Plot':

        trace, symbol_x = signal_container_2d(trace, symbols, color_palette, marker_names, y_function_names)    

plot_sum        = []
plot_config     = pd.DataFrame(trace)

if radio_2d_3d == '2D Plot':
    plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
    plot_config.reset_index(inplace=True)

    if len(plot_config["Plot_row"]) == 0:
        st.info("Select an <X-axis> symbol and at least one <Y-axis> symbol")
        st.stop()
    plot = plot_2D(dataframe, plot_config, symbol_x)

else:
    if (plot_config["Symbol"][0] == 'Not Selected') or (plot_config["Symbol"][1] == 'Not Selected') or (plot_config["Symbol"][2] == 'Not Selected'):
        st.info("Select an <X-axis> symbol, <Y-axis> symbol and <Z-axis> symbol")
        st.stop()

    x, y, z = z_col_or_grid(dataframe, plot_config)
    plot = plot_3D(x, y, z,dataframe, plot_config, color_palette, overlay, overlay_alpha, overlay_marker, overlay_color )

st.plotly_chart(plot, use_container_width=True, config=toolbar)

st.subheader("Quick Analysis")

quick_analysis_result = plotted_analysis(dataframe, plot_config)
st.write(quick_analysis_result)

checkbox_raw = st.checkbox(label= "Display Raw Data as Table", key="Raw_Data")
checkbox_plotted = st.checkbox(label= "Display Plotted Data as Table", key="Plotted_Data")

with st.expander("Export", expanded=True):
    col_export_name,col_export_format, col_datetime, col_generate_link, col_export_link = st.columns(5)
    file_name               = export_name(col_export_name, col_datetime)
    export_format           = show_export_format(col_export_format)
    include_plotted_data    = st.checkbox("Export Plotted Data", value=True)
    include_raw_data        = st.checkbox("Export Raw Data", value=False)

if checkbox_plotted == True: 
    st.subheader("Plotted Data") 

    if radio_2d_3d == '3D Plot':
        plotted_table = plotted_data_3d(x,y,z,plot_config)
        st.write(plotted_table)
    else:
        plotted_table = plotted_data(dataframe, plot_config)
        st.write(plotted_table)

if checkbox_raw == True:
        st.subheader("Raw Data")
        raw_table = raw_data(dataframe)
        st.write(raw_table)

if col_generate_link.button("Generate File") == True:
    try:
        download_chart(plot, quick_analysis_result, include_plotted_data, include_raw_data, plotted_table, raw_table, export_format, file_name, col_export_link )
    except:
        raw_table = raw_data(dataframe)
        if radio_2d_3d == '3D Plot':
            plotted_table = plotted_data_3d(x,y,z,plot_config)
        else:
            plotted_table = plotted_data(dataframe, plot_config)
        download_chart(plot, quick_analysis_result, include_plotted_data, include_raw_data, plotted_table, raw_table, export_format, file_name, col_export_link )