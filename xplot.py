import streamlit as st
import pandas as pd

from src.colors import qualitive_color_dict, plot_color_set 
from src.functions import y_functions_dict
from src.layout import plotly_toolbar_config, view_2d_or_3d, plot_config_3d, plot_config_2d,  signal_container_3d
from src.plotter import plot_2D
from src.plot_setup import get_markers
from src.utils import load_dataframe

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
    plot_3D_type, color_palette, fill_value, interpolation_method, trace["Grid_Res"] = plot_config_3d(radio_2d_3d,trace)
else:
    color_palette, extra_signals  = plot_config_2d(radio_2d_3d)

checkbox_table          = st.checkbox('Display plotted data as table',value = False)
checkbox_raw_table      = st.checkbox('Display all data as table')


   
uploaded_file = st.sidebar.file_uploader(label="",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])

if uploaded_file is None:
    st.sidebar.warning("Please Upload File Above")
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

        trace_function      = []
        signal_functions    = []

        # X-Axis
        with st.sidebar.beta_expander("X Axis", expanded=True):
            symbol_0    = st.selectbox("Symbol", symbols, key="symbol_0")
            #function_0  = st.multiselect('Functions', ['time2frequency','gain'], key="function_0" )

        total_signals = 6
        color_counter = 0

        if extra_signals > 0:
            total_signals = total_signals + extra_signals

        for available_symbols in range(1, total_signals):

            if available_symbols <= 5:
                expand_contaner = True
            else:
                expand_contaner = False

            if color_counter > len(color_palette):
                color_counter = 0

            with st.sidebar.beta_expander("Signal "+str(available_symbols), expanded=expand_contaner):
                # Symbol
                trace["Symbol"].append(st.selectbox("Symbol", symbols, key="symbol_"+str(available_symbols)))

                col_name, col_format = st.beta_columns((2,1))
                # Rename signal
                trace["Name"].append(col_name.text_input("Rename Signal", "", key="name_"+str(available_symbols)))
                col_format.text("Format")
                # Hex representation
                trace["Hex_rep"].append(col_format.checkbox("Hex",help = "Show Hex of Signal", key="hex_"+str(available_symbols)))
                # Binrary representation
                trace["Bin_rep"].append(col_format.checkbox("Binary",help = "Show Binrary of Signal", key="bin_"+str(available_symbols)))

                col_axis,col_color, col_subplot = st.beta_columns(3)
                # Y Axis
                trace["Axis"].append(col_axis.radio('Axis', ['y1','y2'], key="axis_"+str(available_symbols)))
                # Color
                trace["Color"].append(col_color.color_picker('Pick a color ',color_palette[color_counter],help="(Default:"+color_palette[color_counter]+")", key="color_"+str(available_symbols)))
                # Subplot
                trace["Plot_row"].append(col_subplot.selectbox("Subplot",["Main Plot","Subplot 1","Subplot 2"], key="subplot_"+str(available_symbols)))

                ## Formatting
                col_type, col_style, col_size  = st.beta_columns(3)
                trace["Chart_type"].append(col_type.radio('Type', ['lines','markers','lines+markers'], key="type_"+str(available_symbols) ))
                if  trace["Chart_type"][available_symbols-1] == 'lines':
                    trace["Style"].append(col_style.selectbox("Style",  ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_"+str(available_symbols)))
                if  trace["Chart_type"][available_symbols-1] == 'markers':
                    trace["Style"].append(col_style.selectbox("Style", marker_names, help="https://plotly.com/python/marker-style/", key="style_"+str(available_symbols)))
                if  trace["Chart_type"][available_symbols-1] == 'lines+markers':
                    trace["Style"].append(col_style.selectbox("Style", marker_names, help="https://plotly.com/python/marker-style/", key="style_"+str(available_symbols)))
               
                trace["Size"].append(col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_"+str(available_symbols)))

                # Functions
                col_function, col_function_var = st.beta_columns((2))

                function_chosen = (col_function.multiselect('Functions', y_function_names ,default=[], key="function_"+str(available_symbols) ) )

                trace_function = []
                trace_function_value = []

                if len(function_chosen) != 0:            

                    for functions in range(0, len(function_chosen)):
                        if 'gain' in function_chosen[functions]:
                            trace_function.append("gain")
                            trace_function_value.append(float(col_function_var.text_input("Gain",0, key="gain_"+str(available_symbols))) )

                        if 'offset' in function_chosen[functions]:
                            trace_function.append("offset")
                            trace_function_value.append(float(col_function_var.text_input("Offset",0, key="offset_"+str(available_symbols))) )

                        if 'rms2peak' in function_chosen[functions]:
                            trace_function.append("rms2peak")
                            trace_function_value.append("None")

                        if 'peak2rms' in function_chosen[functions]:
                            trace_function.append("peak2rms")
                            trace_function_value.append("None")

                        if 'rpm2rads' in function_chosen[functions]:
                            trace_function.append("rpm2rads")
                            trace_function_value.append("None")

                        if 'rads2rpm' in function_chosen[functions]:
                            trace_function.append("rads2rpm")
                            trace_function_value.append("None")

                        if 'degree2revs' in function_chosen[functions]: 
                            trace_function.append("degree2revs")
                            trace_function_value.append("None")

                        if 'revs2degree' in function_chosen[functions]: 
                            trace_function.append("revs2degree")
                            trace_function_value.append("None")

                    trace["Function"].append(trace_function)
                    trace["Value"].append(trace_function_value)

                else:
                    trace["Function"].append('Not Selected')
                    trace["Value"].append("None")

            color_counter = color_counter + 1      


plotted_data        = pd.DataFrame()
plot_sum            = []

# Generate
if st.button("Plot"):
  
    plot_config     = pd.DataFrame(trace)

    if radio_2d_3d == '2D Plot':
        plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
        plot_config.reset_index(inplace=True)
    
    plot = plot_2D(dataframe, plot_config, plotted_data, symbol_0)
    st.plotly_chart(plot, use_container_width=True, config=toolbar)