import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from palettable.cartocolors.qualitative import Pastel_10
from palettable.colorbrewer.qualitative import Paired_12
from palettable.tableau import Tableau_10
from io import StringIO

st.set_page_config  (
                    page_title              ="CSV Plotter", 
                    page_icon               ="📈", 
                    layout                  ='wide', 
                    initial_sidebar_state   ='auto'
                    
                    )

# PLOTLY TOOLBAR/ BEHAVIOUR
config = dict   ({
    'scrollZoom'            : True,
    'displayModeBar'        : True,
    'editable'              : False,
    'modeBarButtonsToAdd'   :   [
                                'drawline',
                                'drawopenpath',
                                'drawclosedpath',
                                'drawcircle',
                                'drawrect',
                                'eraseshape'
                                ],
    'toImageButtonOptions'  :   {'format': 'svg'}
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

# Main Page
st.title('CSV Plotter')

col_checks, col_colors  = st.beta_columns((2,1))
checkbox_plot           = col_checks.checkbox('Plot',value = True)
checkbox_table          = col_checks.checkbox('Display selected data as table',value = True)
checkbox_raw_table      = col_checks.checkbox('Display all data as table')

color_set = col_colors.selectbox("Color Palette", ['Default','Pastel','Paired','MS Office','Light','Dark'], key='color_set',help = "Recommended: Light Theme use Plotly, Dark Theme use Pastel" )
extra_signals = col_colors.number_input("Extra Signals", min_value=0, max_value=10, value=0, step=1, help = "Generate extra signal containers, useful if your comparing signals with functions applied")

color_palaette = []

if color_set == 'Default':
    for  i in range(0,len(px.colors.qualitative.Plotly)):
        color_palaette.append(px.colors.qualitative.Plotly[i])

if color_set == 'Pastel':
    for  i in range(0,len(Pastel_10.hex_colors)):
        color_palaette.append(Pastel_10.hex_colors[i])

if color_set == 'Paired':
    for  i in range(0,len(Paired_12.hex_colors)):
        color_palaette.append(Paired_12.hex_colors[i])

if color_set == 'MS Office':
    for  i in range(0,len(Tableau_10.hex_colors)):
        color_palaette.append(Tableau_10.hex_colors[i])

if color_set == 'Light':
    for  i in range(0,len(px.colors.qualitative.Light24)):
        color_palaette.append(px.colors.qualitative.Light24[i])

if color_set == 'Dark':
    for  i in range(0,len(px.colors.qualitative.Dark24)):
        color_palaette.append(px.colors.qualitative.Dark24[i])

trace =  dict()
trace["Symbol"] = []
trace["Name"] = []
trace["Hex_rep"] = []
trace["Bin_rep"] = []
trace["Plot_row"] = []
trace["Axis"] = []
trace["Color"] = []
trace["Size"] = []
trace["Style"] = []
trace["Chart_type"] = []

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

def generate(df, plot_df):
    
    y_axis_spec = []

    secondary_y =  plot_df.loc[plot_df['Plot_row'] == 'Main Plot']
    if secondary_y["Axis"].all() == 'y1':
            y_axis_spec.append([{'secondary_y': False}])
    elif secondary_y["Axis"].any() == 'y1':
            y_axis_spec.append([{'secondary_y': True}])
    else:
            pass

    secondary_y =  plot_df.loc[plot_df['Plot_row'] == 'Subplot 1']
    if secondary_y["Axis"].all() == 'y1':
            y_axis_spec.append([{'secondary_y': False}])
    elif secondary_y["Axis"].any() == 'y1':
            y_axis_spec.append([{'secondary_y': True}])
    else:
            pass

    secondary_y =  plot_df.loc[plot_df['Plot_row'] == 'Subplot 2']
    if secondary_y["Axis"].all() == 'y1':
            y_axis_spec.append([{'secondary_y': False}])
    elif secondary_y["Axis"].any() == 'y1':
            y_axis_spec.append([{'secondary_y': True}])
    else:
            pass

    if checkbox_plot == True:
        
        plot = make_subplots(   
                            rows                = len(plot_df["Plot_row"].unique()), 
                            cols                = 1,
                            shared_xaxes        = True,
                            specs               = y_axis_spec,
                            vertical_spacing    = 0.05
                            )
        
        # For each signal config.
        for row in range(0,len(plot_df)):
            
            # Determine subplots
            if plot_df["Plot_row"][row] == "Subplot 1":
                subplot = 2
                plotheight = 900

            elif plot_df["Plot_row"][row] =="Subplot 2":
                subplot = 3
                plotheight = 1080

            else:
                subplot = 1
                plotheight = 720
            
            # Determine y-axis
            if plot_df["Axis"][row] == "y1":
                y_axis_plot = False

            else:
                y_axis_plot = True

            # Apply function(s) to signal
            #if plot_df["Function"][row] != []:
            #    signal_function_name = str(plot_df["Signal"][row])

            #    for items in plot_df["Function"][row]:
            #        signal_functions.append(items)
            #    
            #    for i in signal_functions:
            #        signal_function_name = signal_function_name  + '[' + i + ']'
            #        dataframe[signal_function_name] =  dataframe[plot_df["Signal"][row]].apply(y_function_dict[i])
            #        plot_df["Signal"][row] = signal_function_name
            
            # Show hex / binrary 
            if plot_df["Hex_rep"][row] & plot_df["Bin_rep"][row]  == True:
                hovertip    = "Raw: %{y:,.0f}<br>" + "Hex: %{y:.0x }<br>" + "Bin: %{y:.0b}<br>"

            elif (plot_df["Hex_rep"][row] == True) & (plot_df["Bin_rep"][row]  == False):
                hovertip    = "Raw: %{y:,.0f}<br>" + "Hex: %{y:.0x}<br>"
                             
            elif (plot_df["Hex_rep"][row] == False) & (plot_df["Bin_rep"][row]  == True):
                hovertip    = "Raw: %{y:,.0f}<br>" + "Bin: %{y:.0b}<br>"
                                  
            else:
                hovertip    = "%{y:,.0f}"
                     
            # Rename Signals
            if plot_df["Name"][row] == str():
                Name = plot_df["Symbol"][row]
            else:
                Name = plot_df["Name"][row]

            # Plot type
            if plot_df["Chart_type"][row] == 'lines':
                    plot.add_trace	(go.Scatter (  
                                        x       		= df[symbol_0],
                                        y       		= df[plot_df["Symbol"][row]],
                                        name 			= Name,
                                        hovertemplate 	= hovertip,
                                        mode            = 'lines',
                                        line            = dict  (
                                                                color   = plot_df["Color"][row], 
                                                                dash    = plot_df["Style"][row], 
                                                                width   = plot_df["Size"][row]
                                                                ),
                                                ),
                                    row                 = subplot,
                                    col                 = 1,
                                    secondary_y         = y_axis_plot
                                    )

            elif plot_df["Chart_type"][row] == 'markers':
                    plot.add_trace	(go.Scatter (  
                                        x       		= df[symbol_0],
                                        y       		= df[plot_df["Symbol"][row]],
                                        name 			= Name,
                                        hovertemplate 	= hovertip,
                                        mode            = 'markers',
                                        marker          = dict  (
                                                                color   = plot_df["Color"][row], 
                                                                symbol  = plot_df["Style"][row]
                                                                ),
                                        yaxis           = plot_df["Axis"][row]
                                                ),  
                                        row             = subplot, 
                                        col             = 1,
                                        secondary_y     = y_axis_plot          
                                    )
            else:
                    plot.add_trace	(go.Scatter (  
                                        x       		= df[symbol_0],
                                        y       		= df[plot_df["Symbol"][row]],
                                        name 			= Name,
                                        hovertemplate 	= hovertip,
                                        mode            = 'lines+markers',
                                        marker          = dict  (
                                                                color   = plot_df["Color"][row]
                                                                ),
                                        line            = dict(color=plot_df["Color"][row]),
                                        yaxis           = plot_df["Axis"][row]
                                                ),  
                                        row             = subplot, 
                                        col             = 1,
                                        secondary_y     = y_axis_plot         
                                    )

            # Summary table
            max_signal      = max(dataframe[plot_df["Symbol"][row]])
            min_signal      = min(dataframe[plot_df["Symbol"][row]])
            mean_signal     = np.mean(dataframe[plot_df["Symbol"][row]])
            plotted_signal  = plot_df["Symbol"][row]
            
            plot_sum.append([Name, plotted_signal, max_signal, min_signal ,mean_signal])

            # Table for plotted table
            plotted_data[plot_df["Symbol"][row]] = df[plot_df["Symbol"][row]]

            plot.update_layout	(
                                hovermode	= "x",
                                autosize    = True,
                                height      = plotheight
                                )
            

        st.plotly_chart(plot, use_container_width=True, config=config)

        plot_summary                = pd.DataFrame(plot_sum)
        plot_summary.rename(columns = {0:'Name',1:'Signal',2:"Maximum",3:"Minimum",4:"Mean"}, inplace = True)
        st.table(plot_summary)

    if checkbox_table == True:
        st.subheader("Plotted Data")
        st.write(plotted_data)

    if checkbox_raw_table == True:
        st.subheader("Raw Data")
        st.write(dataframe)

# Functions
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

st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

with st.sidebar.beta_expander("📝 To Do"):
    st.write("- Make .exe")
    st.write("- Add support for differnt formats (.blf, m4f)")
    st.write("- Dynamic generation of number of signals and their properties (i.e more than 5) ✔️")
    st.write("- Add functions")
    st.write("- Allow deletion of annotation/shapes ✔️")
    st.write("- Export as HTML")
    st.write("- Plotted data table generation ✔️")
    st.write("- Fix Multi Y axis ✔️")
    st.write("- Rename signal ✔️")
    st.write("- Add Line/maker styles ✔️")
    st.write("- Add hovertip options (Hex, bin)✔️")
    st.write("- Add subplot✔️")
    st.write("- Add color palattes ✔️")
    
file_uploader = st.sidebar.file_uploader("")

if file_uploader is not None:
    # To read file as bytes:
    bytes_data  = file_uploader.getvalue()   
    # To convert to a string based IO:
    stringio    = StringIO(file_uploader.getvalue().decode("utf-8"))   
    # To read file as string:
    string_data = stringio.read()   
    # Can be used wherever a "file-like" object is accepted:
    dataframe   = pd.read_csv(file_uploader)

    # Create Index array, to plot against. Not all data has timestamp
    Index   = np.arange(0, len(dataframe), 1)
    dataframe.insert(0, 'Index', Index)
    symbols = list(dataframe)

    # Use to NOT plot.
    symbols.insert(0, "Not Selected")

    # Side bar items
    # X-Axis
    with st.sidebar.beta_expander("X Axis", expanded=True):
        symbol_0    = st.selectbox("Symbol", symbols, key="symbol_0")
        function_0  = st.multiselect('Functions', ['example:time2frequency'], key="function_0" )

    total_signals = len(dataframe.columns)
    color_counter = 0
    if extra_signals > 0:
        total_signals = total_signals + extra_signals

    for available_symbols in range(1, total_signals):
        color_counter = color_counter + 1

        if available_symbols <= 4:
            expand_contaner = True
        else:
            expand_contaner = False

        if color_counter > len(color_palaette)-1:
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
            trace["Color"].append(col_color.color_picker('Pick a color ',color_palaette[color_counter],help="(Default:"+color_palaette[color_counter]+")", key="color_"+str(available_symbols)))
            # Subplot
            trace["Plot_row"].append(col_subplot.selectbox("Subplot",["Main Plot","Subplot 1","Subplot 2"], key="subplot_"+str(available_symbols)))

            ## Formatting
            col_type, col_style, col_size  = st.beta_columns(3)
            trace["Chart_type"].append(col_type.radio('Type', ['lines','markers','lines+markers'], key="type_"+str(available_symbols) ))
            if  trace["Chart_type"][available_symbols-1] == 'lines':
                trace["Style"].append(col_style.selectbox("Style", ["solid", "dot", "dash", "longdash", "dashdot","longdashdot"], key="style_"+str(available_symbols)))
            if  trace["Chart_type"][available_symbols-1] == 'markers':
                trace["Style"].append(col_style.selectbox("Style", ["circle", "square", "diamond", "cross", "x","cross-thin","x-thin","triangle-up","triangle-down","triangle-left","triangle-right",'y-up','y-down'], key="style_"+str(available_symbols)))
            trace["Size"].append(col_size.number_input("Size", min_value=0.0, max_value=10.0, value=2.0, step=0.5, key="size_"+str(available_symbols)))

# Generate
if st.button("Generate"):   
    plot_sum = []
    plotted_data        = pd.DataFrame()
    subplot             = 1
    plot_df             = pd.DataFrame(trace)
    plot_df             = plot_df[plot_df["Symbol"]!='Not Selected']
    plot_df.reset_index(inplace=True)
    
    generate(dataframe, plot_df)

st.markdown("""---""")
