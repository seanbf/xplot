import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from scipy.interpolate import griddata
from plotly.subplots import make_subplots
from src.functions import y_functions_dict

@st.cache
def get_hovertip(Hex, Bin):
    ''' 
    Show hex / bin on plot
    ''' 

    if Hex & Bin  == True:
        hovertip    = "Raw: %{y:,.3f}<br>" + "Hex: %{y:.0x }<br>" + "Bin: %{y:.0b}<br>"

    elif (Hex == True) & (Bin  == False):
        hovertip    = "Raw: %{y:,.3f}<br>" + "Hex: %{y:.0x}<br>"

    elif (Hex == False) & (Bin  == True):
        hovertip    = "Raw: %{y:,.3f}<br>" + "Bin: %{y:.0b}<br>"

    else:
        hovertip    = "%{y:,.3f}"

    return hovertip

@st.cache
def get_name(renamed_name,symbol_name):
    ''' 
    Get name of signal or new name, input by user.
    ''' 
    
    if renamed_name == str():
        Name = symbol_name
    else:
        Name = renamed_name
    return Name

@st.cache
def get_y_axis(y_axis):
    ''' 
    Get name of signal or new name, input by user.
    ''' 

    if y_axis == "y1":
        y_axis_plot = False

    else:
        y_axis_plot = True

@st.cache
def get_y_axis_config(plot_config):
    ''' 
    Get configuration for y axis / subplot
    ''' 
    
    y_axis_config = []

    # Main Plot Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Main Plot']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass

    # Subplot 1 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 1']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass
    
    # Subplot 2 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 2']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass

    return y_axis_config

@st.cache
def get_subplot(Subplot):
            # Determine subplots
    if Subplot == "Subplot 1":
        subplot = 2
        plotheight = 900

    elif Subplot =="Subplot 2":
        subplot = 3
        plotheight = 1080

    else:
        subplot = 1
        plotheight = 720
    
    return subplot, plotheight

#def get_functions(function_string, function_value, signal_name):
#        Function_and_Value  = []
#        Function_Value_String         = ''
#
#        if function_string != 'Not Selected':
#            
#            for j in range(0, len(function_string)):
#
#                if function_value[j] != "None":
#                    Value_string = '(' + str(function_value[j]) + ')'
#
#                else:
#                    Value_string = ''
#
#                Function_string = str(function_string[j])
#
#                Function_and_Value.append(' {' + Function_string + Value_string + '}')
#
#            for k in Function_and_Value:
#                Function_Value_String = Function_Value_String + k
#
#            Name = str(signal_name) + Function_Value_String
#            temp_col = df[plot_config["Symbol"][row]]
#            for j in range(0, len(plot_config["Function"][row])):
#                if plot_config["Value"][row][j] == "None":
#                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col)
#                else:
#                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col, plot_config["Value"][row][j] )
#
#            df[Name] = temp_col
#            y_axis_symbol = df[Name]
#            plotted_data[Name] = y_axis_symbol
#        else:
#            y_axis_symbol = df[plot_config["Symbol"][row]]
#            plotted_data[Name] = y_axis_symbol

def plot_2D(df, plot_config, plotted_data, symbol_0):

    y_axis_config = get_y_axis_config(plot_config)
    
    plot = make_subplots(   
                        rows                = len(plot_config["Plot_row"].unique()), 
                        cols                = 1,
                        shared_xaxes        = True,
                        specs               = y_axis_config,
                        vertical_spacing    = 0.05
                        )

    # For each signal config.
    for row in range(0,len(plot_config)):

        # Determine subplots
        subplot, plotheight = get_subplot(plot_config["Plot_row"][row])

        # Determine y-axis
        y_axis_plot = get_y_axis(plot_config["Axis"][row])

        # Show hex / binary 
        hovertip = get_hovertip(plot_config["Hex_rep"][row], plot_config["Bin_rep"][row])

        # Rename Signals
        Name = get_name(plot_config["Name"][row], plot_config["Symbol"][row])

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
                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col)
                else:
                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col, plot_config["Value"][row][j] )

            df[Name] = temp_col
            y_axis_symbol = df[Name]
            plotted_data[Name] = y_axis_symbol
        else:
            y_axis_symbol = df[plot_config["Symbol"][row]]
            plotted_data[Name] = y_axis_symbol

        # Plot type
        if plot_config["Chart_Type"][row] == 'lines':
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

        elif plot_config["Chart_Type"][row] == 'markers':
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
        elif plot_config["Chart_Type"][row] == 'lines+markers':
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
        else:
            st.warning("Chart_Type Failure")
        
        plot.update_layout	(
                            hovermode	= "x",  
                            autosize    = True,
                            height      = plotheight
                            )


    return plot
    

    #plot_summary                = pd.DataFrame(plot_sum)
    #plot_summary.rename(columns = {0:'Signal',1:"Maximum",2:"Minimum",3:"Mean"}, inplace = True)

    #sum_col_left, sum_col_right = st.columns((2,1))
    #sum_col_left.table(plot_summary)
    #sum_col_right.selectbox(label='Select download plot format', options=['.png', '.jpeg', '.pdf', '.svg', '.html', '.json'])
    #sum_col_right.button(label='Download Plot')
    #sum_col_right.selectbox(label='Export plot data format', options=['.csv', '.txt', '.pdf', '.html'])
    #sum_col_right.button(label='Export Data')

@st.cache
def plot_3D(df, plot_config, color_palette):

        x = df[plot_config["Symbol_X"][0]]
        y = df[plot_config["Symbol_Y"][0]]
        z = df[plot_config["Symbol_Z"][0]]

        if plot_config["Chart_Type"][0] != '3D Scatter':
    
            xi = np.linspace( float(min(x)), float(max(x)), int(plot_config["Grid_Res"]) )
            yi = np.linspace( float(min(y)), float(max(y)), int(plot_config["Grid_Res"]) )
    
            X,Y = np.meshgrid(xi,yi)
    
            Z = griddata( (x,y),z,(X,Y), fill_value=plot_config["Fill_Value"], method='linear')

        plot_3D = go.Figure()

        if plot_config["Chart_Type"][0] == 'Contour':
            plot_3D.add_trace(go.Contour  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                colorscale  = color_palette,
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

        if plot_config["Chart_Type"][0] == '3D Scatter':
            plot_3D.add_trace(go.Scatter3d  (
                                z           = z,
                                x           = x, 
                                y           = y,
                                mode        = 'markers',
                                marker      = dict(
                                            color = z,
                                            colorscale  = color_palette,
                                            opacity = 0.7
                                                    ),
                                            
                                hovertemplate = str(plot_config["Symbol_X"][0]) + ': %{x:.2f}' + 
                                                '<br>' + str(plot_config["Symbol_Y"][0])+ ': %{y:.2f}</br>' +
                                                str(plot_config["Symbol_Z"][0]) + ': %{z:.2f}',               

                                )           )

        if plot_config["Chart_Type"][0] == 'Surface':
                        plot_3D.add_trace(go.Surface  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                colorscale  = color_palette,
                                            
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
        if plot_config["Chart_Type"][0] == 'Heatmap':
                        plot_3D.add_trace(go.Heatmap  (
                                z           = Z,
                                x           = xi, 
                                y           = yi,
                                
                                colorscale  = color_palette,
                                            
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
                    title       = plot_config["Chart_Type"][0] ,
                    xaxis       = dict(title=str(plot_config["Symbol_X"][0])),
                    yaxis       = dict(title=str(plot_config["Symbol_Y"][0]))
                    
                    )

        return plot_3D