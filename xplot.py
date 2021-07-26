import streamlit as st
import pandas as pd


from src.image_export import show_export_format
from src.colors import qualitive_color_dict, diverging_color_dict, sequential_color_dict, plot_color_set 
from src.functions import y_functions_dict
from src.layout import plotly_toolbar_config, colormap_config
from src.plotter import get_markers, plot_2D
from src.utils import load_dataframe

page_config = st.set_page_config  (
                page_title              ="CSV Plotter", 
                page_icon               ="📈", 
                layout                  ='wide', 
                initial_sidebar_state   ='auto'
                
                )

colormap_preview_config         = colormap_config()
toolbar                         = plotly_toolbar_config()

qualitive_color_sets_dict       = qualitive_color_dict()
qualitive_color_sets_names      = list(qualitive_color_sets_dict.keys())

diverging_color_sets_dict       = diverging_color_dict()
diverging_color_sets_names      = list(diverging_color_sets_dict.keys())

sequential_color_sets_dict      = sequential_color_dict()
sequential_color_sets_names     = list(sequential_color_sets_dict.keys())

y_functions                     = y_functions_dict()
y_function_names                = list(y_functions.keys())

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

marker_names = get_markers()

# Main Page
st.title('CSV Plotter')

main_left_col, main_right_col = st.beta_columns(2)
checkbox_plot           = main_left_col.checkbox('Plot',value = True)
checkbox_table          = main_left_col.checkbox('Display plotted data as table',value = False)
checkbox_raw_table      = main_left_col.checkbox('Display all data as table')

st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)
   
uploaded_file = st.sidebar.file_uploader(label="Upload your csv or excel file here.",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])

if uploaded_file is None:
    st.warning("Please Upload File")
elif uploaded_file is not None:

    dataframe, columns = load_dataframe(uploaded_file=uploaded_file)

    # Create Index array, to plot against. Not all data has timestamp
    symbols = list(dataframe)
    # Use to NOT plot.
    symbols.insert(0, "Not Selected")

    trace =  dict()
    
    # Side bar items
    threeD = st.sidebar.checkbox("3D Plot",help = "Plot 3D Chart", key="3D")

    # 3D Trace Configuration
    if threeD == True:

        trace["Symbol_X"]   = []
        trace["Symbol_Y"]   = []
        trace["Symbol_Z"]   = []
        
        trace["Name_X"]     = []
        trace["Name_Y"]     = []
        trace["Name_Z"]     = []
        
        trace["Grid_Res"]   = []
        #trace["Function"]  = []
        #trace["Value"]     = []

        y_axis_spec         = []
        trace_function      = []
        signal_functions    = []

        with st.sidebar.beta_expander("Plot Setup", expanded=True):
            plot_3D_type = st.selectbox("3D Type", ["Contour","3D Scatter","Surface","Heatmap"])

            col_coltype, col_choice = st.beta_columns((1,2))
            
            color_set_type = col_coltype.radio('Color Set Type', ['Sequential','Diverging'], key="coltype")
            if color_set_type == 'Sequential':
                color_map = sequential_color_sets_names
            else:
                color_map = diverging_color_sets_names
            
            color_set   = col_choice.selectbox("Color Map", color_map)

            if color_set_type == 'Sequential':
                color_palette = sequential_color_sets_dict.get(color_set)
            else:
                color_palette = diverging_color_sets_dict.get(color_set)
   
            st.plotly_chart(plot_color_set(color_palette, color_set, threeD), config = colormap_preview_config)
        
            if plot_3D_type != '3D Scatter':
                trace["Grid_Res"].append(st.number_input("Grid Resolution", min_value=0.0, max_value=100000.0, value=50.0, step=0.5, key="Grid_Res"))
                fill_value = interpolation_method = st.selectbox("Fill Value", ["nan",0], help="fill missing data with the selected value")
                interpolation_method = st.selectbox("Interpolation Method", ["linear","nearest","cubic"])
            else:
                trace["Grid_Res"].append(0)
                
        with st.sidebar.beta_expander("X", expanded=True):
            trace["Symbol_X"].append(st.selectbox("Symbol", symbols, key="Symbol_X"))
            trace["Name_X"].append(st.text_input("Rename Symbol", "", key="Name_X"))

        with st.sidebar.beta_expander("Y", expanded=True):
            trace["Symbol_Y"].append(st.selectbox("Symbol", symbols, key="Symbol_Y"))
            trace["Name_Y"].append(st.text_input("Rename Symbol", "", key="Name_Y"))

        with st.sidebar.beta_expander("Z", expanded=True):
            trace["Symbol_Z"].append(st.selectbox("Symbol", symbols, key="Symbol_Z"))
            trace["Name_Z"].append(st.text_input("Rename Symbol", "", key="Name_Z"))

    # 2D Trace Configuration
    else:
        with st.sidebar.beta_expander("Plot Setup", expanded=True):
            col_choice, col_show = st.beta_columns((1,2))
            
            color_set = col_choice.selectbox("Color Palette",qualitive_color_sets_names, key='color_set', help = "Recommended: Light Theme use Plotly, Dark Theme use Pastel" )
            
            color_palette = qualitive_color_sets_dict.get(color_set)
    
            col_show.plotly_chart(plot_color_set(color_palette, color_set, threeD), config = colormap_preview_config)


            extra_signals = st.number_input("Extra Signals", min_value=0, max_value=30, value=0, step=1, help = "Generate extra signal containers, useful if your comparing signals with functions applied")

        trace["Symbol"]     = []
        trace["Name"]       = []
        trace["Hex_rep"]    = []
        trace["Bin_rep"]    = []
        trace["Plot_row"]   = []
        trace["Axis"]       = []
        trace["Color"]      = []
        trace["Size"]       = []
        trace["Style"]      = []
        trace["Chart_type"] = []
        trace["Function"]   = []
        trace["Value"]      = []

        y_axis_spec         = []
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
if main_left_col.button("Plot"):
  
    plot_config     = pd.DataFrame(trace)

    if threeD == False:
        plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
        plot_config.reset_index(inplace=True)
    
    plot = plot_2D(dataframe, plot_config, plotted_data, symbol_0)
    st.plotly_chart(plot, use_container_width=True, config=toolbar)