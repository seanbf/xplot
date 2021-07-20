from logging import makeLogRecord
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from palettable.cartocolors.qualitative import Pastel_10
from palettable.colorbrewer.qualitative import Paired_12
from palettable.matplotlib import Inferno_20, Magma_20, Plasma_20, Viridis_20
from palettable.tableau import Tableau_10
from io import StringIO
from scipy.interpolate import griddata
from traitlets.traitlets import default

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

colormap_config = dict({
    'staticPlot' : True
})

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

# Main Page
st.title('CSV Plotter')


checkbox_plot           = st.checkbox('Plot',value = True)
checkbox_table          = st.checkbox('Display selected data as table',value = True)
checkbox_raw_table      = st.checkbox('Display all data as table')

# Functions
# SIGNAL FUNCTIONS
@st.cache
def gain(signal, gain):
    signal_gain = signal*gain
    return signal_gain

@st.cache   
def offset(signal, offset):
    signal_offset = signal + offset
    return signal_offset

@st.cache    
def rms2peak(signal_rms):
    signal_peak = signal_rms * np.sqrt(2)
    return signal_peak

@st.cache    
def peak2rms(signal_peak):
    signal_rms = signal_peak / np.sqrt(2)
    return signal_rms

@st.cache    
def rpm2rads(speed_rpm):
    speed_rads = (speed_rpm / 60) * (2 * np.pi)
    return speed_rads

@st.cache    
def rads2rpm(speed_rads):
    speed_rpm = (speed_rads / (2 * np.pi)) * 60
    return speed_rpm

@st.cache    
def degree2revs(angle_degree):
    angle_revs = angle_degree / 360
    return angle_revs

@st.cache    
def revs2degree(angle_revs):
    angle_degree = angle_revs * 360
    return angle_degree

@st.cache
def time2frequency(time):
    frequency = 1/time
    return frequency


def generate(df, plot_config):

    if threeD == False:
        
        # Main Plot Secondary Y's
        secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Main Plot']

        if len(secondary_y["Axis"].unique()) == 1:
            y_axis_spec.append([{'secondary_y': False}])

        elif len(secondary_y["Axis"].unique()) == 2:
            y_axis_spec.append([{'secondary_y': True}])
        else:
            pass

        # Subplot 1 Secondary Y's
        secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 1']

        if len(secondary_y["Axis"].unique()) == 1:
            y_axis_spec.append([{'secondary_y': False}])

        elif len(secondary_y["Axis"].unique()) == 2:
            y_axis_spec.append([{'secondary_y': True}])
        else:
            pass
        
        # Subplot 2 Secondary Y's
        secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 2']

        if len(secondary_y["Axis"].unique()) == 1:
            y_axis_spec.append([{'secondary_y': False}])

        elif len(secondary_y["Axis"].unique()) == 2:
            y_axis_spec.append([{'secondary_y': True}])
        else:
            pass

        if checkbox_plot == True:

                plot = make_subplots(   
                                    rows                = len(plot_config["Plot_row"].unique()), 
                                    cols                = 1,
                                    shared_xaxes        = True,
                                    specs               = y_axis_spec,
                                    vertical_spacing    = 0.05
                                    )

                # For each signal config.
                for row in range(0,len(plot_config)):

                    # Determine subplots
                    if plot_config["Plot_row"][row] == "Subplot 1":
                        subplot = 2
                        plotheight = 900

                    elif plot_config["Plot_row"][row] =="Subplot 2":
                        subplot = 3
                        plotheight = 1080

                    else:
                        subplot = 1
                        plotheight = 720

                    # Determine y-axis
                    if plot_config["Axis"][row] == "y1":
                        y_axis_plot = False

                    else:
                        y_axis_plot = True

                    # Show hex / binrary 
                    if plot_config["Hex_rep"][row] & plot_config["Bin_rep"][row]  == True:
                        hovertip    = "Raw: %{y:,.0f}<br>" + "Hex: %{y:.0x }<br>" + "Bin: %{y:.0b}<br>"

                    elif (plot_config["Hex_rep"][row] == True) & (plot_config["Bin_rep"][row]  == False):
                        hovertip    = "Raw: %{y:,.0f}<br>" + "Hex: %{y:.0x}<br>"

                    elif (plot_config["Hex_rep"][row] == False) & (plot_config["Bin_rep"][row]  == True):
                        hovertip    = "Raw: %{y:,.0f}<br>" + "Bin: %{y:.0b}<br>"

                    else:
                        hovertip    = "%{y:,.0f}"

                    # Rename Signals
                    if plot_config["Name"][row] == str():
                        Name = plot_config["Symbol"][row]
                    else:
                        Name = plot_config["Name"][row]

                    ## Apply function(s) to signal
                    # Function signal name
                    Function_and_Value  = []
                    Function_Value_String         = ''

                    if plot_config["Function"][row] != 'Not Selected':
                        
                        for j in range(0, len(plot_config["Function"][row])):

                            if plot_config["Value"][row][j] != "None":
                                Value_string = '(' + str(plot_config["Value"][row][j]) + ')'

                            else:
                                Value_string = ''

                            Function_string = str(plot_config["Function"][row][j])

                            Function_and_Value.append(' {' + Function_string + Value_string + '}')

                        for k in Function_and_Value:
                            Function_Value_String = Function_Value_String + k

                        Name = str(Name) + Function_Value_String
                        temp_col = df[plot_config["Symbol"][row]]
                        for j in range(0, len(plot_config["Function"][row])):
                            if plot_config["Value"][row][j] == "None":
                                temp_col = np.vectorize(y_function_dict[plot_config["Function"][row][j]])(temp_col)
                            else:
                                temp_col = np.vectorize(y_function_dict[plot_config["Function"][row][j]])(temp_col, plot_config["Value"][row][j] )

                        df[Name] = temp_col
                        y_axis_symbol = df[Name]
                        plotted_data[Name] = y_axis_symbol
                    else:
                        y_axis_symbol = df[plot_config["Symbol"][row]]
                        plotted_data[Name] = y_axis_symbol

                    # Plot type
                    if plot_config["Chart_type"][row] == 'lines':
                            plot.add_trace	(go.Scatter (  
                                                x       		= df[symbol_0],
                                                y       		= y_axis_symbol,
                                                name 			= Name,
                                                hovertemplate 	= hovertip,
                                                mode            = 'lines',
                                                line            = dict  (
                                                                        color   = plot_config["Color"][row], 
                                                                        dash    = plot_config["Style"][row], 
                                                                        width   = plot_config["Size"][row]
                                                                        ),
                                                        ),
                                            row                 = subplot,
                                            col                 = 1,
                                            secondary_y         = y_axis_plot
                                            )

                    elif plot_config["Chart_type"][row] == 'markers':
                            plot.add_trace	(go.Scatter (  
                                                x       		= df[symbol_0],
                                                y       		= y_axis_symbol,
                                                name 			= Name,
                                                hovertemplate 	= hovertip,
                                                mode            = 'markers',
                                                marker          = dict  (
                                                                        color   = plot_config["Color"][row], 
                                                                        symbol  = plot_config["Style"][row]
                                                                        ),
                                                yaxis           = plot_config["Axis"][row]
                                                        ),  
                                                row             = subplot, 
                                                col             = 1,
                                                secondary_y     = y_axis_plot          
                                            )
                    else:
                            plot.add_trace	(go.Scatter (  
                                                x       		= df[symbol_0],
                                                y       		= y_axis_symbol,
                                                name 			= Name,
                                                hovertemplate 	= hovertip,
                                                mode            = 'lines+markers',
                                                marker          = dict  (
                                                                        color   = plot_config["Color"][row]
                                                                        ),
                                                line            = dict(color=plot_config["Color"][row]),
                                                yaxis           = plot_config["Axis"][row]
                                                        ),  
                                                row             = subplot, 
                                                col             = 1,
                                                secondary_y     = y_axis_plot         
                                            )

                    # Summary table
                    max_signal      = max(y_axis_symbol)
                    min_signal      = min(y_axis_symbol)
                    mean_signal     = np.mean(y_axis_symbol)

                    plot_sum.append([Name, max_signal, min_signal ,mean_signal])

                    # Table for plotted table
                    

                    plot.update_layout	(
                                        hovermode	= "x",
                                        autosize    = True,
                                        height      = plotheight
                                        )


                st.plotly_chart(plot, use_container_width=True, config=config)

                plot_summary                = pd.DataFrame(plot_sum)
                plot_summary.rename(columns = {0:'Signal',1:"Maximum",2:"Minimum",3:"Mean"}, inplace = True)
                st.table(plot_summary)

        if checkbox_table == True:
            st.subheader("Plotted Data")
            st.write(plotted_data)

        if checkbox_raw_table == True:
            st.subheader("Raw Data")
            st.write(dataframe)

    if threeD == True:

        st.warning("3D plotting is under development")

        x = df[plot_config["Symbol_X"][0]]
        y = df[plot_config["Symbol_Y"][0]]
        z = df[plot_config["Symbol_Z"][0]]

        if plot_3D_type != '3D Scatter':
    
            xi = np.linspace( float(min(x)), float(max(x)), int(trace["Grid_Res"][0])) 
            yi = np.linspace( float(min(y)), float(max(y)), int(trace["Grid_Res"][0]))
    
            X,Y = np.meshgrid(xi,yi)
    
            Z = griddata((x,y),z,(X,Y), fill_value=fill_value,method='linear') 

        plot_3D = go.Figure()

        if plot_3D_type == 'Contour':
            plot_3D.add_trace(go.Contour  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                colorscale  = color_palaette,
                                hovertemplate = str(plot_config["Symbol_X"][0]) + ': %{x:.2f}' + 
                                                '<br>' + str(plot_config["Symbol_Y"][0])+ ': %{y:.2f}</br>' +
                                                str(plot_config["Symbol_Z"][0]) + ': %{z:.2f}',
                                contours    = dict  (
                                                    coloring    ='heatmap',
                                                    showlabels  = True,
                                                    labelfont   = dict  (
                                                                        size = 10,
                                                                        color = 'white',
                                                                        )
                                                    ), 

                                colorbar    = dict  (
                                                    title       = str(plot_config["Symbol_Z"][0]),
                                                    titleside   = 'right',
                                                    titlefont   = dict  (
                                                                        size=12,
                                                                        family='Arial, sans'
                                                                        )
                                                    )
                    )           )

        if plot_3D_type == '3D Scatter':
            plot_3D.add_trace(go.Scatter3d  (
                                z           = z,
                                x           = x, 
                                y           = y,
                                mode        = 'markers',
                                marker      = dict(
                                            color = z,
                                            colorscale  = color_palaette,
                                            opacity = 0.7
                                                    ),
                                            
                                hovertemplate = str(plot_config["Symbol_X"][0]) + ': %{x:.2f}' + 
                                                '<br>' + str(plot_config["Symbol_Y"][0])+ ': %{y:.2f}</br>' +
                                                str(plot_config["Symbol_Z"][0]) + ': %{z:.2f}',               

                                )           )

        if plot_3D_type == 'Surface':
                        plot_3D.add_trace(go.Surface  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                colorscale  = color_palaette,
                                            
                                hovertemplate = str(plot_config["Symbol_X"][0]) + ': %{x:.2f}' + 
                                                '<br>' + str(plot_config["Symbol_Y"][0])+ ': %{y:.2f}</br>' +
                                                str(plot_config["Symbol_Z"][0]) + ': %{z:.2f}',               
                                colorbar    = dict  (
                                                    title       = str(plot_config["Symbol_Z"][0]),
                                                    titleside   = 'right',
                                                    titlefont   = dict  (
                                                                        size=12,
                                                                        family='Arial, sans'
                                                                        )
                                                    )
                                )           )
        if plot_3D_type == 'Heatmap':
                        plot_3D.add_trace(go.Heatmap  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                
                                colorscale  = color_palaette,
                                            
                                hovertemplate = str(plot_config["Symbol_X"][0]) + ': %{x:.2f}' + 
                                                '<br>' + str(plot_config["Symbol_Y"][0])+ ': %{y:.2f}</br>' +
                                                str(plot_config["Symbol_Z"][0]) + ': %{z:.2f}', 

                                colorbar    = dict  (
                                                    title       = str(plot_config["Symbol_Z"][0]),
                                                    titleside   = 'right',
                                                    titlefont   = dict  (
                                                                        size=12,
                                                                        family='Arial, sans'
                                                                        )
                                                    )
                                )           )
                                
        plot_3D.update_layout	(
                    autosize    = True,
                    height      = 720,
                    width       = 1080,
                    title       = plot_3D_type ,
                    xaxis       = dict(title=str(plot_config["Symbol_X"][0])),
                    yaxis       = dict(title=str(plot_config["Symbol_Y"][0]))
                    
                    )

        st.plotly_chart(plot_3D)

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

st.sidebar.markdown('''<small>v0.1</small>''', unsafe_allow_html=True)

with st.sidebar.beta_expander("📝 To Do"):
    st.write("- Add 3d plot support (Meshgrid to plot contour, 3d scatter, heatmap etc), also display as table ✔️")
    st.write("- Make .exe")
    st.write("- Add support for differnt formats (.blf, m4f)")
    st.write("- Dynamic generation of number of signals and their properties (i.e more than 5) ✔️")
    st.write("- Add functions ✔️")
    st.write("- Allow annotation/shapes ⚠️: Can't be done in plotly yet (conflicts with placeholder labels)")
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

        colors = px.colors.named_colorscales()

        mylist = colors
        myorder = [21,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93]
        colors = [colors[i] for i in myorder]

        with st.sidebar.beta_expander("Plot Setup", expanded=True):
            plot_3D_type = st.selectbox("3D Type", ["Contour","3D Scatter","Surface","Heatmap"])
            col_choice, col_show = st.beta_columns((1,2))
            color_set= col_choice.selectbox("Color Map", colors)
            n = 100
            fig = go.Figure(
                data=[go.Bar(
                orientation="h",
                y=[color_set] * n,
                x=[1] * n,
                customdata=[(x + 1) / n for x in range(n)],
                marker=dict(color=list(range(n)), colorscale=color_set, line_width=0),
                name=color_set,
                
                            )
                ],
                
                layout=dict(
                            xaxis=dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                            yaxis=dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                            height=85,
                            width=340,
                            margin=dict(l=0,r=0,b=0,t=25),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        ),
                
                    )
                    
            col_show.plotly_chart(fig, config = colormap_config)
            color_palaette = color_set
            
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
            
            color_set = col_choice.selectbox("Color Palette", ['Default','Pastel','Paired','MS Office','Light','Dark'], key='color_set',help = "Recommended: Light Theme use Plotly, Dark Theme use Pastel" )
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
            
            extra_signals = st.number_input("Extra Signals", min_value=0, max_value=30, value=0, step=1, help = "Generate extra signal containers, useful if your comparing signals with functions applied")
            
            n = len(color_palaette)
            fig = go.Figure(
                data=[go.Bar(
                orientation="v",
                x=[color_palaette] * n,
                y=[1] * n,
                customdata=[(x + 1) / n for x in range(n)],
                marker=dict(color=list(range(n)), colorscale=color_palaette, line_width=0),
                name=color_set,
                
                            )
                ],
                
                layout=dict(
                            xaxis=dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                            yaxis=dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                            height=80,
                            width=340,
                            margin=dict(l=0,r=0,b=0,t=30),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        ),
                
                
                    )

            col_show.plotly_chart(fig, config = colormap_config)

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
            function_0  = st.multiselect('Functions', ['time2frequency','gain'], key="function_0" )

        total_signals = 6
        color_counter = -1

        if extra_signals > 0:
            total_signals = total_signals + extra_signals

        for available_symbols in range(1, total_signals):
            color_counter = color_counter + 1

            if available_symbols <= 5:
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

                # Functions
                col_function, col_function_var = st.beta_columns((2))

                function_chosen = (col_function.multiselect('Functions', list(y_function_dict.keys()) ,default=[], key="function_"+str(available_symbols) ) )

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

# Generate
if st.button("Generate"):
  
    plot_config     = pd.DataFrame(trace)

    if threeD == False:
        plot_config     = plot_config[plot_config["Symbol"]!='Not Selected']
        plot_config.reset_index(inplace=True)
    
    plot_sum            = []

    plotted_data        = pd.DataFrame()
    subplot             = 1

    generate(dataframe, plot_config)

st.markdown("""---""")
