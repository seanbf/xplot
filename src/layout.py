import streamlit as st
from src.plot_setup import trace_dict
from src.colors import sequential_color_dict, diverging_color_dict, plot_color_set, qualitive_color_dict
from PIL import Image

def plotly_toolbar_config():
    # PLOTLY TOOLBAR/ BEHAVIOUR
    config = dict   ({
        'scrollZoom'            : True,
        'displayModeBar'        : True,
        'editable'              : True,
        # Issue with streamlit/plotly :(
        #'modeBarButtonsToAdd'   :   [
        #                            'drawline',
        #                            'drawopenpath',
        #                            'drawclosedpath',
        #                            'drawcircle',
        #                            'drawrect',
        #                            'eraseshape'   
        #                            ],
        'toImageButtonOptions'  :   {'format': 'svg'}
                })
    return config 

def view_2d_or_3d(radio_2d_3d):
    """
    Select between 2D and 3D plotter
    """
    
    if radio_2d_3d      == '2D Plot':
        trace           = trace_dict(radio_2d_3d)

    elif radio_2d_3d    == '3D Plot':
        trace           = trace_dict(radio_2d_3d)
    
    return trace

def plot_config_3d(radio_2d_3d, trace, marker_names):
    """
    Container to configure 3D plot, i.e colormapping
    """

    if radio_2d_3d == "3D Plot":
        with st.expander("3D Plot Configuration", expanded=True):
            col_plot_type, col_grid_res, col_fill, col_interp = st.columns(4)
            col_col_type, col_choice, col_preview, col_overlay = st.columns(4)
            trace["Chart_Type"] = col_plot_type.selectbox("Plot Type", ["Contour","3D Scatter","Surface","Heatmap"])
            color_set_type = col_col_type.selectbox('Color Map Type', ['Sequential','Diverging'], key="coltype")

            if color_set_type == 'Sequential':
                color_map = list(sequential_color_dict().keys())
            else:
                color_map = list(diverging_color_dict().keys())

            color_set   = col_choice.selectbox("Color Map", color_map)  
            if color_set_type == 'Sequential':
                color_palette = sequential_color_dict().get(color_set)
            else:
                color_palette = diverging_color_dict().get(color_set)

            colormap_preview = plot_color_set(color_palette, color_set, radio_2d_3d)
            col_preview.image(colormap_preview, use_column_width = True)

            if trace["Chart_Type"] != '3D Scatter':
                trace["Grid_Res"] = col_grid_res.number_input("Grid Resolution", min_value=0.0, max_value=100000.0, value=50.0, step=0.5, key="Grid_Res")
                trace["Fill_Value"] = col_fill.selectbox("Fill Value", ["nan",0], help="fill missing data with the selected value")
                trace["Interp_Method"] = col_interp.selectbox("Interpolation Method", ["linear","nearest","cubic"])

            else:
                trace["Fill_Value"] = None
                trace["Interp_Method"] = None
                trace["Grid_Res"] = None
            
            overlay = col_overlay.checkbox("Overlay Original Data", help="Display scatter of original data overlayed on chart")
            
            if overlay == True:
                col_overlay_alpha, col_overlay_marker, col_overlay_color = st.columns(3)
                overlay_alpha = col_overlay_alpha.slider("Opacity",value=0.5,min_value=0.0, max_value=1.0, step=0.01)
                overlay_marker = col_overlay_marker.selectbox("Style", marker_names, help="https://plotly.com/python/marker-style/")
                overlay_color = col_overlay_color.color_picker('Pick a color ', '#000000')
            else:
                overlay_alpha = None
                overlay_marker = None
                overlay_color = None
    else:
        trace["Chart_Type"] = None
        color_palette = None
        trace["Fill_Value"] = None
        trace["Interp_Method"] = None
        trace["Grid_Res"] = None



    return trace["Chart_Type"], trace["Fill_Value"], trace["Interp_Method"], trace["Grid_Res"], color_palette, overlay, overlay_alpha, overlay_marker, overlay_color

def plot_config_2d(trace, radio_2d_3d):
    with st.expander("2D Plot Configuration", expanded=True):
        col_choice, col_extra_signals, col_preview, col_placeholder = st.columns(4)
        qualitive_color_sets_dict       = qualitive_color_dict()
        qualitive_color_sets_names      = list(qualitive_color_sets_dict.keys())
        color_set = col_choice.selectbox("Color Palette",qualitive_color_sets_names, key='color_set', help = "Recommended: Light Theme use Plotly, Dark Theme use Pastel" )
       
        color_palette = qualitive_color_sets_dict.get(color_set)
    
        colormap_preview = plot_color_set(color_palette, color_set, radio_2d_3d)
        col_preview.image(colormap_preview, use_column_width = True)

        trace["Extra_Signals"] = col_extra_signals.number_input("Extra Signals", min_value=0, max_value=30, value=0, step=1, help = "Generate extra signal containers, useful if your comparing signals with functions applied")

    return trace["Extra_Signals"], color_palette

def signal_container_3d(trace, symbols):
    '''
    Generate containers for 3d plot.
    '''
    for i in range(0, 3):
        if i == 0:
            Axis = 'X'
        elif i == 1:
            Axis = 'Y'
        elif i == 2:
            Axis = 'Z'

        with st.sidebar.expander(Axis + " Axis", expanded=True):
            trace["Symbol"].append(st.selectbox("Symbol " + str(Axis), symbols, key="Symbol_"+str(Axis)))
            trace["Name"].append(st.text_input("Rename Symbol " + str(Axis), "", key="Name_"+str(Axis)))

    return trace["Symbol"], trace["Name"]

def signal_container_2d(trace, symbols, color_palette, marker_names, y_function_names):

        trace_function      = []
        signal_functions    = []

        # X-Axis
        with st.sidebar.expander("X Axis", expanded=True):
            symbol_0    = st.selectbox("Symbol", symbols, key="symbol_0")
            #function_0  = st.multiselect('Functions', ['time2frequency','gain'], key="function_0" )

        total_signals = 6
        color_counter = 0
        
        if trace["Extra_Signals"] > 0:
            total_signals = total_signals + trace["Extra_Signals"]

        for available_symbols in range(1, total_signals):

            if available_symbols <= 5:
                expand_contaner = True
            else:
                expand_contaner = False

            if color_counter >= len(color_palette):
                color_counter = 0
            
            with st.sidebar.expander("Signal "+str(available_symbols), expanded=expand_contaner):
                # Symbol
                trace["Symbol"].append(st.selectbox("Symbol", symbols, key="symbol_"+str(available_symbols)))

                col_name, col_format = st.columns((2,1))
                # Rename signal
                trace["Name"].append(col_name.text_input("Rename Signal", "", key="name_"+str(available_symbols)))
                col_format.text("Format")
                # Hex representation
                trace["Hex_rep"].append(col_format.checkbox("Hex",help = "Show Hex of Signal", key="hex_"+str(available_symbols)))
                # Binrary representation
                trace["Bin_rep"].append(col_format.checkbox("Binary",help = "Show Binrary of Signal", key="bin_"+str(available_symbols)))

                col_axis,col_color, col_subplot = st.columns(3)
                # Y Axis
                trace["Axis"].append(col_axis.radio('Axis', ['y1','y2'], key="axis_"+str(available_symbols)))
                # Color
                trace["Color"].append(col_color.color_picker('Pick a color ',color_palette[color_counter],help="(Default: "+color_palette[color_counter]+")", key="color_"+str(available_symbols)))
                # Subplot
                trace["Plot_row"].append(col_subplot.selectbox("Subplot",["Main Plot","Subplot 1","Subplot 2"], key="subplot_"+str(available_symbols)))

                ## Formatting
                col_type, col_style, col_size  = st.columns(3)
                trace["Chart_Type"].append(col_type.radio('Type', ['lines','markers','lines+markers'], key="type_"+str(available_symbols) ))
                if  trace["Chart_Type"][available_symbols-1] == 'lines':
                    trace["Style"].append(col_style.selectbox("Style",  ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_"+str(available_symbols)))
                if  trace["Chart_Type"][available_symbols-1] == 'markers':
                    trace["Style"].append(col_style.selectbox("Style", marker_names, help="https://plotly.com/python/marker-style/", key="style_"+str(available_symbols)))
                if  trace["Chart_Type"][available_symbols-1] == 'lines+markers':
                    trace["Style"].append(col_style.selectbox("Style", marker_names, help="https://plotly.com/python/marker-style/", key="style_"+str(available_symbols)))
               
                trace["Size"].append(col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_"+str(available_symbols)))

                # Functions
                col_function, col_function_var = st.columns((2))

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

        return trace["Symbol"],trace["Name"],trace["Hex_rep"],trace["Bin_rep"],trace["Plot_row"],trace["Axis"],trace["Color"],trace["Size"],trace["Style"],trace["Chart_Type"] , trace["Function"],trace["Value"] ,trace["Extra_Signals"] , symbol_0