import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO
st.set_page_config(page_title="CSV Plotter", page_icon="📈", layout='wide', initial_sidebar_state='auto')

# PLOTLY TOOLBAR/ BEHAVIOUR

config = dict({
    'scrollZoom': False,
    'displayModeBar': True,
    'editable': True,
    'modeBarButtonsToAdd':  ['drawline',
                            'drawopenpath',
                            'drawclosedpath',
                            'drawcircle',
                            'drawrect',
                            'eraseshape'
                            ],
    'toImageButtonOptions': {'format': 'svg',}
                })

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

# Functions
# SIGNAL FUNCTIONS
def gain(signal, gain):
    signal_gain = signal*gain
    return signal_gain
    
def offset(signal, offset):
    signal_offset = signal + offset
    return signal_offset
    
def rms2peak(signal_rms):
    signal_peak = signal_rms * np.sqrt(2)
    return signal_peak
    
def peak2rms(signal_peak):
    signal_rms = signal_peak / np.sqrt(2)
    return signal_rms
    
def rpm2rads(speed_rpm):
    speed_rads = (speed_rpm / 60) * (2 * np.pi)
    return speed_rads
    
def rads2rpm(speed_rads):
    speed_rpm = (speed_rads / (2 * np.pi)) * 60
    return speed_rpm
    
def degree2revs(angle_degree):
    angle_revs = angle_degree / 360
    return angle_revs
    
def revs2degree(angle_revs):
    angle_degree = angle_revs * 360
    return angle_degree

# 
def generate(df):

    plot_df = pd.DataFrame(Y_s)
    plot_df = plot_df[plot_df["Signal"]!='Not Selected']
    plot_df.reset_index(inplace=True)
    plot_sum = []
    signal_functions = []
    subplot = 1
    st.write(plot_df["Subplot"])
    if checkbox_plot == True:

        if  plot_df["Subplot"].any() != "Main Plot":
            plot = make_subplots(rows=len(plot_df["Subplot"])+1, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02)
            st.write("subplot!")
        else:
            plot = go.Figure()
            st.write("not sub!")
        for row in range(0,len(plot_df)):
            
            if plot_df["Subplot"][row] == "Subplot 1":
                subplot = 2
            elif plot_df["Subplot"][row] =="Subplot 2":
                subplot = 3
            else:
                subplot = 1

            st.write(plot_df["Subplot"][row])
            st.write(subplot)

            if plot_df["Function"][row] != []:
                signal_function_name = str(plot_df["Signal"][row])
                for items in plot_df["Function"][row]:
                    signal_functions.append(items)
                
                for i in signal_functions:
                    signal_function_name = signal_function_name  + '(' + i + ')'
                    dataframe[signal_function_name] =  dataframe[plot_df["Signal"][row]].apply(y_function_dict[i])
                    plot_df["Signal"][row] = signal_function_name
                    
            if plot_df["Name"][row] == str():
                Name = plot_df["Signal"][row]
            else:
                Name = plot_df["Name"][row]
            
            if plot_df["Type"][row] == 'lines':
                    plot.add_trace	(go.Scatter (  
                                        x       		= dataframe[symbol_0],
                                        y       		= dataframe[plot_df["Signal"][row]],
                                        name 			= Name,
                                        hovertemplate 	= '%{y:.2f} ',
                                        mode            = 'lines',
                                        line            = dict(color=plot_df["Color"][row], dash=plot_df["Style"][row], width = plot_df["Size"][row]),
                                        yaxis           = plot_df["Axis"][row]
                                    ),  row=subplot, col=1          
                                                )
            elif plot_df["Type"][row] == 'markers':
                    plot.add_trace	(go.Scatter (  
                                        x       		= dataframe[symbol_0],
                                        y       		= dataframe[plot_df["Signal"][row]],
                                        name 			= Name,
                                        hovertemplate 	= '%{y:.2f}',
                                        mode            = 'markers',
                                        marker          = dict(color=plot_df["Color"][row], symbol=plot_df["Style"][row]),
                                        yaxis           = plot_df["Axis"][row]
                                    ),  row=subplot, col=1          
                                                )
            else:
                    plot.add_trace	(go.Scatter (  
                                        x       		= dataframe[symbol_0],
                                        y       		= dataframe[plot_df["Signal"][row]],
                                        name 			= Name,
                                        hovertemplate 	= '%{y:.2f} ',
                                        mode            = 'lines+markers',
                                        marker          = dict(color=plot_df["Color"][row]),
                                        line            = dict(color=plot_df["Color"][row]),
                                        yaxis           = plot_df["Axis"][row]
                                    ),  row=subplot, col=1          
                                                    )
            
            
            max_signal = max(dataframe[plot_df["Signal"][row]])
            min_signal = min(dataframe[plot_df["Signal"][row]])
            mean_signal = np.mean(dataframe[plot_df["Signal"][row]])

            plot_sum.append([Name,plot_df["Signal"][row],max_signal,min_signal,mean_signal])

            plot.update_layout	(
                            yaxis2	    = dict( 
                                                side        = 'right'
                                                ),
                            hovermode	= "x",
                            autosize    = True,
                            height      = 720
                            )
                            
            st.plotly_chart(plot, use_container_width=True, config=config)
            plot_summary = pd.DataFrame(plot_sum)
            plot_summary.rename(columns = {0:'Name',1:'Signal',2:"Maximum",3:"Minimum",4:"Mean"}, inplace = True)
            st.table(plot_summary)

    if checkbox_table == True:
        st.subheader("Plotted Data")
        plotted_data = dataframe.loc[:,dataframe.columns.isin(plot_df["Signal"])]
        st.write(plotted_data)

    if checkbox_raw_table == True:
        st.subheader("Raw Data")
        st.write(dataframe)

def plotsignals():
    trace_1 = dict([('Signal', symbol_1), ('Name', name_1), ('Axis', axis_1), ('Color', color_1), ('Type', type_1),("Subplot",subplot_1), ("Style", style_1),("Size", size_1), ('Function', function_1) ])
    trace_2 = dict([('Signal', symbol_2), ('Name', name_2), ('Axis', axis_2), ('Color', color_2), ('Type', type_2),("Subplot",subplot_2), ("Style", style_2),("Size", size_2), ('Function', function_2) ])
    trace_3 = dict([('Signal', symbol_3), ('Name', name_3), ('Axis', axis_3), ('Color', color_3), ('Type', type_3),("Subplot",subplot_3), ("Style", style_3),("Size", size_3), ('Function', function_3) ])
    trace_4 = dict([('Signal', symbol_4), ('Name', name_4), ('Axis', axis_4), ('Color', color_4), ('Type', type_4),("Subplot",subplot_4), ("Style", style_4),("Size", size_4), ('Function', function_4) ])
    trace_5 = dict([('Signal', symbol_5), ('Name', name_5), ('Axis', axis_5), ('Color', color_5), ('Type', type_5),("Subplot",subplot_5), ("Style", style_5),("Size", size_5), ('Function', function_5) ])
    return(trace_1,trace_2, trace_3,trace_4,trace_5)

y_function_dict = {
                'gain':gain,
                'offset':offset,
                'rms2peak':rms2peak,
                'peak2rms':peak2rms,
                'rpm2rads':rpm2rads,
                'rads2rpm':rads2rpm,
                'degree2revs':degree2revs,
                'revs2degree':revs2degree
                }
                
y_functions = pd.DataFrame(y_function_dict.keys())

st.title('CSV Plotter')

st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

with st.sidebar.beta_expander("📝 To Do"):
    st.write("- Dynamic generation of number of signals depending on amount of colomns in data file")
    st.write("- Plotted data table generation ✔️")
    st.write("- Multi Y axis ✔️")
    st.write("- Rename signal ✔️")
    st.write("- Add functions")
    st.write("- Allow deletion of annotation/shapes")
    st.write("- Export as HTML")
    st.write("- Add Line/maker styles ✔️")
    st.write("- Make .exe")
    st.write("- Add support for differnt formats (.blf, m4f)")
    st.write("- Add hovertip options (Hex, bin)")
    st.write("- Add subplot")
    
file_uploader = st.sidebar.file_uploader("")

if file_uploader is not None:
    # To read file as bytes:
    bytes_data = file_uploader.getvalue()   
    # To convert to a string based IO:
    stringio = StringIO(file_uploader.getvalue().decode("utf-8"))   
    # To read file as string:
    string_data = stringio.read()   
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(file_uploader)

    Index = np.arange(0, len(dataframe), 1)
    dataframe.insert(0, 'Index', Index)
    symbols = list(dataframe)
    symbols.insert(0, "Not Selected")

    with st.sidebar.beta_expander("X Axis", expanded=True):
        name_0      = st.text_input("Rename Signal", "", key="name_0")
        symbol_0    = st.selectbox("Symbol", symbols, key="symbol_0")
        function_0   = st.multiselect('Functions', ['example:time2frequency'], key="function_0" )

    with st.sidebar.beta_expander("Signal 1", expanded=True):
        symbol_1    = st.selectbox("Symbol", symbols, key="symbol_1")

        col_name, col_format = st.beta_columns((2,1))
        name_1      = col_name.text_input("Rename Signal", "", key="name_1")
        col_format.text("Format")
        hex_1       = col_format.checkbox("Hex")
        bin_1       = col_format.checkbox("Binary")
        
        col_axis, col_type, col_subplot = st.beta_columns(3)
        axis_1      = col_axis.radio('Axis', ['y1','y2'], key="axis_1")
        type_1      = col_type.radio('Type', ['lines','markers','lines+markers'], key="type_1" )
        col_subplot.text("Subplot")
        if col_subplot.checkbox("As Subplot") == True:
            subplot_1       = col_subplot.selectbox("As Subplot",["Not Available Yet","Subplot 1","Subplot 2"])
        else:
            subplot_1       = "Main Plot"

        col_style, col_size, col_color = st.beta_columns(3)
        color_1     = col_color.color_picker('Pick a color ','#636EFA',help="(Default: #636EFA)", key="color_1")
        size_1      = col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_1")

        if type_1   == 'lines':
            style_1 = col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_1")
        if type_1   == 'markers':
            style_1 = col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_1")
        
        col_function, col_function_var = st.beta_columns((2,1))
        function_1  = col_function.multiselect('Functions', y_functions, key="function_1" )
        
        if function_1   == 'gain':
            col_function_var.write("ss")
            function_1_var = col_function_var.number_input("Gain", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_1")
        if function_1   == 'offset':
            function_1_var = col_function_var.number_input("Offset", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_1")       
        
    with st.sidebar.beta_expander("Signal 2"):
        symbol_2    = st.selectbox("Symbol", symbols, key="symbol_2")

        col_name, col_format = st.beta_columns((2,1))
        name_2      = col_name.text_input("Rename Signal", "", key="name_2")
        col_format.text("Format")
        hex_2       = col_format.checkbox("Hex",key="hex_2")
        bin_2       = col_format.checkbox("Binary",key="bin_2")
        
        col_axis, col_type, col_subplot = st.beta_columns(3)
        axis_2      = col_axis.radio('Axis', ['y1','y2'], key="axis_2")
        type_2      = col_type.radio('Type', ['lines','markers','lines+markers'], key="type_2" )
        col_subplot.text("Subplot")
        if col_subplot.checkbox("As Subplot",key="subplot_2") == True:
            subplot_2       = col_subplot.selectbox("As Subplot",["Not Available Yet","Subplot 1","Subplot 2"])
        else:
            subplot_2       = "Main Plot"

        col_style, col_size, col_color = st.beta_columns(3)
        color_2     = col_color.color_picker('Pick a color ','#636EFA',help="(Default: #636EFA)", key="color_2")
        size_2      = col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_2")

        if type_2   == 'lines':
            style_2 = col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_2")
        if type_2   == 'markers':
            style_2 = col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_2")
        
        col_function, col_function_var = st.beta_columns((2,1))
        function_2  = col_function.multiselect('Functions', y_functions, key="function_2" )
        
        if function_2   == 'gain':
            col_function_var.write("ss")
            function_2_var = col_function_var.number_input("Gain", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_2")
        if function_2   == 'offset':
            function_2_var = col_function_var.number_input("Offset", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_2")    
        
    with st.sidebar.beta_expander("Signal 3"):
        symbol_3    = st.selectbox("Symbol", symbols, key="symbol_3")

        col_name, col_format = st.beta_columns((2,1))
        name_3      = col_name.text_input("Rename Signal", "", key="name_3")
        col_format.text("Format")
        hex_3       = col_format.checkbox("Hex",key="hex_3")
        bin_3       = col_format.checkbox("Binary",key="bin_3")
        
        col_axis, col_type, col_subplot = st.beta_columns(3)
        axis_3      = col_axis.radio('Axis', ['y1','y2'], key="axis_3")
        type_3      = col_type.radio('Type', ['lines','markers','lines+markers'], key="type_3" )
        col_subplot.text("Subplot")
        if col_subplot.checkbox("As Subplot",key="subplot_3") == True:
            subplot_3       = col_subplot.selectbox("As Subplot",["Not Available Yet","Subplot 1","Subplot 2"])
        else:
            subplot_3       = "Main Plot"

        col_style, col_size, col_color = st.beta_columns(3)
        color_3     = col_color.color_picker('Pick a color ','#636EFA',help="(Default: #636EFA)", key="color_3")
        size_3      = col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_3")

        if type_3   == 'lines':
            style_3 = col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_3")
        if type_3   == 'markers':
            style_3 = col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_3")
        
        col_function, col_function_var = st.beta_columns((2,1))
        function_3  = col_function.multiselect('Functions', y_functions, key="function_3" )
        
        if function_3   == 'gain':
            col_function_var.write("ss")
            function_3_var = col_function_var.number_input("Gain", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_3")
        if function_3   == 'offset':
            function_3_var = col_function_var.number_input("Offset", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_3")  

    with st.sidebar.beta_expander("Signal 4"):
        symbol_4    = st.selectbox("Symbol", symbols, key="symbol_4")

        col_name, col_format = st.beta_columns((2,1))
        name_4      = col_name.text_input("Rename Signal", "", key="name_4")
        col_format.text("Format")
        hex_4       = col_format.checkbox("Hex",key="hex_4")
        bin_4       = col_format.checkbox("Binary",key="bin_4")
        
        col_axis, col_type, col_subplot = st.beta_columns(3)
        axis_4      = col_axis.radio('Axis', ['y1','y2'], key="axis_4")
        type_4      = col_type.radio('Type', ['lines','markers','lines+markers'], key="type_4" )
        col_subplot.text("Subplot")
        if col_subplot.checkbox("As Subplot",key="subplot_4") == True:
            subplot_4       = col_subplot.selectbox("As Subplot",["Not Available Yet","Subplot 1","Subplot 2"])
        else:
            subplot_4       = "Main Plot"

        col_style, col_size, col_color = st.beta_columns(3)
        color_4     = col_color.color_picker('Pick a color ','#636EFA',help="(Default: #636EFA)", key="color_4")
        size_4      = col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_4")

        if type_4   == 'lines':
            style_4 = col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_4")
        if type_4   == 'markers':
            style_4 = col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_4")
        
        col_function, col_function_var = st.beta_columns((2,1))
        function_4  = col_function.multiselect('Functions', y_functions, key="function_4" )
        
        if function_4   == 'gain':
            col_function_var.write("ss")
            function_4_var = col_function_var.number_input("Gain", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_4")
        if function_4   == 'offset':
            function_4_var = col_function_var.number_input("Offset", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_4")     
        
    with st.sidebar.beta_expander("Signal 5"):
        symbol_5    = st.selectbox("Symbol", symbols, key="symbol_5")

        col_name, col_format = st.beta_columns((2,1))
        name_5      = col_name.text_input("Rename Signal", "", key="name_5")
        col_format.text("Format")
        hex_5       = col_format.checkbox("Hex",key="hex_5")
        bin_5       = col_format.checkbox("Binary",key="bin_5")
        
        col_axis, col_type, col_subplot = st.beta_columns(3)
        axis_5      = col_axis.radio('Axis', ['y1','y2'], key="axis_5")
        type_5      = col_type.radio('Type', ['lines','markers','lines+markers'], key="type_5" )
        col_subplot.text("Subplot")
        if col_subplot.checkbox("As Subplot",key="subplot_5") == True:
            subplot_5       = col_subplot.selectbox("As Subplot",["Not Available Yet","Subplot 1","Subplot 2"])
        else:
            subplot_5       = "Main Plot"

        col_style, col_size, col_color = st.beta_columns(3)
        color_5     = col_color.color_picker('Pick a color ','#636EFA',help="(Default: #636EFA)", key="color_5")
        size_5      = col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_5")

        if type_5   == 'lines':
            style_5 = col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_5")
        if type_5   == 'markers':
            style_5 = col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_5")
        
        col_function, col_function_var = st.beta_columns((2,1))
        function_5  = col_function.multiselect('Functions', y_functions, key="function_5" )
        
        if function_5   == 'gain':
            col_function_var.write("ss")
            function_5_var = col_function_var.number_input("Gain", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_5")
        if function_5   == 'offset':
            function_5_var = col_function_var.number_input("Offset", min_value=-100000.0, max_value=100000.0, value=1.0, step=0.00001, key="size_5")    

# Item Selection
checkbox_plot = st.checkbox('Plot',value = True)
checkbox_table = st.checkbox('Display selected data as table',value = True)
checkbox_raw_table = st.checkbox('Display all data as table')

# Generate

if st.button("Generate"):
    Y_s = plotsignals()

    generate(dataframe)

st.markdown("""---""")
