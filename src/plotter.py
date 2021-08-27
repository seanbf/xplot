import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.functions import y_functions_dict
from src.plot_setup import get_y_axis, get_hovertip, get_name, get_subplot, get_y_axis_config

@st.cache
def plot_2D(dataframe, plot_config, symbol_x):
    '''
    Plot requested 2d chart using configuration
    '''
    with st.spinner('Generating Interactive Plot'):
        plotted_data        = pd.DataFrame()
        symbol              = plot_config["Symbol"]
        y_axis              = plot_config["Axis"]
        hex_rep             = plot_config["Hex_rep"]
        bin_rep             = plot_config["Bin_rep"]
        name                = plot_config["Name"]
        function_applied    = plot_config["Function"]
        function_value      = plot_config["Value"]
        color               = plot_config["Color"]
        style               = plot_config["Style"]
        size                = plot_config["Size"]
        
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
            y_axis_plot         = get_y_axis(y_axis[row])

            # Show hex / binary 
            hovertip            = get_hovertip(hex_rep[row], bin_rep[row])

            # Rename Signals
            Name                = get_name(name[row], symbol[row])

            ## Apply function(s) to signal - this is slow/ not acceptable atm.
            # Function signal name
            Function_and_Value      = []
            Function_Value_String   = ''

            if function_applied[row] != 'Not Selected':

                for j in range(0, len(function_applied[row])):

                    if function_value[row][j] != "None":
                        Value_string = '(' + str(function_value[row][j]) + ')'

                    else:
                        Value_string = ''

                    Function_string = str(function_applied[row][j])

                    Function_and_Value.append(' {' + Function_string + Value_string + '}')

                for k in Function_and_Value:
                    Function_Value_String = Function_Value_String + k

                Name = str(Name) + Function_Value_String
                temp_col = dataframe[symbol[row]]
                for j in range(0, len(function_applied[row])):
                    if function_value[row][j] == "None":
                        temp_col = np.vectorize(y_functions_dict[function_applied[row][j]])(temp_col)
                    else:
                        temp_col = np.vectorize(y_functions_dict[function_applied[row][j]])(temp_col, function_value[row][j] )

                dataframe[Name] = temp_col
                y_axis_symbol = dataframe[Name]
                plotted_data[Name] = y_axis_symbol
            else:
                y_axis_symbol = dataframe[symbol[row]]
                plotted_data[Name] = y_axis_symbol

            # Plot type

            if plot_config["Chart_Type"][row] == 'lines':
                
                plot.add_trace	(go.Scatter (  
                                            x       		= dataframe[symbol_x],
                                            y       		= y_axis_symbol,
                                            name 			= Name,
                                            hovertemplate 	= hovertip,
                                            mode            = 'lines',
                                            line            = dict  (
                                                                    color   = color[row], 
                                                                    dash    = style[row], 
                                                                    width   = size[row]
                                                                    ),
                                            ),
                                row                 = subplot,
                                col                 = 1,
                                secondary_y         = y_axis_plot
                                )

            elif plot_config["Chart_Type"][row] == 'markers':
                plot.add_trace	(go.Scatter (  
                                            x       		= dataframe[symbol_x],
                                            y       		= y_axis_symbol,
                                            name 			= Name,
                                            hovertemplate 	= hovertip,
                                            mode            = 'markers',
                                            marker          = dict  (
                                                                    color   = color[row], 
                                                                    symbol  = style[row]
                                                                    ),
                                            yaxis           = y_axis[row]
                                            ),  
                                row             = subplot, 
                                col             = 1,
                                secondary_y     = y_axis_plot          
                                )

            elif plot_config["Chart_Type"][row] == 'lines+markers':
                plot.add_trace	(go.Scatter (  
                                            x       		= dataframe[symbol_x],
                                            y       		= y_axis_symbol,
                                            name 			= Name,
                                            hovertemplate 	= hovertip,
                                            mode            = 'lines+markers',
                                            marker          = dict  (
                                                                    color   = color[row]
                                                                    ),
                                            line            = dict(color=color[row]),
                                            yaxis           = y_axis[row]
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

@st.cache
def plot_3D(x_data, y_data, z_data, dataframe, plot_config, color_palette, overlay, overlay_alpha, overlay_marker, overlay_color):
    '''
    Plot requested 3d chart using configuration
    '''
    with st.spinner("Generating 3D Plot"):
        
        symbol_x = str(plot_config["Symbol"][0])
        symbol_y = str(plot_config["Symbol"][1])
        symbol_z = str(plot_config["Symbol"][2])
        plot_type = plot_config["Chart_Type"][0]

        plot_3D = go.Figure()

        if plot_type == 'Contour':
            plot_3D.add_trace(go.Contour    (
                                            z           = z_data,
                                            x           = x_data, 
                                            y           = y_data,
                                            colorscale  = color_palette,
                                            hovertemplate =             symbol_x + ': %{x:.2f}' +
                                                            '<br>' +    symbol_y + ': %{y:.2f}' +
                                                            '<br>' +    symbol_z + ': %{z:.2f}',   

                                            contours    = dict  (
                                                                coloring    ='heatmap',
                                                                showlabels  = True,
                                                                labelfont   = dict  (
                                                                                    size = 10,
                                                                                    color = 'white',
                                                                                    )
                                                                ), 

                                            colorbar    = dict  (
                                                                title       = symbol_z,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                )           )

        if plot_type == 'Surface':
                        plot_3D.add_trace(go.Surface  (
                                            z           = z_data,
                                            x           = x_data, 
                                            y           = y_data,
                                            colorscale  = color_palette,

                                            hovertemplate =             symbol_x + ': %{x:.2f}' +
                                                            '<br>' +    symbol_y + ': %{y:.2f}' +
                                                            '<br>' +    symbol_z + ': %{z:.2f}',   

                                            colorbar    = dict  (
                                                                title       = symbol_z,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                            )           )
        if plot_type == 'Heatmap':
                        plot_3D.add_trace(go.Heatmap  (
                                            z           = z_data,
                                            x           = x_data, 
                                            y           = y_data,
                                            colorscale  = color_palette,

                                            hovertemplate =             symbol_x + ': %{x:.2f}' +
                                                            '<br>' +    symbol_y + ': %{y:.2f}' +
                                                            '<br>' +    symbol_z + ': %{z:.2f}',   

                                            colorbar    = dict  (
                                                                title       = symbol_z,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                            )           )

        if plot_type == '3D Scatter':
            plot_3D.add_trace(go.Scatter3d  (
                                            z           = z_data,
                                            x           = x_data, 
                                            y           = y_data,
                                            mode        = 'markers',
                                            marker      = dict  (
                                                                color = z_data,
                                                                colorscale  = color_palette,
                                                                opacity = 0.7
                                                                ),

                                            hovertemplate =             symbol_x + ': %{x:.2f}' +
                                                            '</br>' +   symbol_y + ': %{y:.2f}' +
                                                            '</br>' +   symbol_z + ': %{z:.2f}',            

                                            )           )
        
        if overlay == True:
            plot_3D.add_trace	(go.Scatter (  
                            x       		= dataframe[symbol_x],
                            y       		= dataframe[symbol_y],
                            name 			= "X: "  + str(dataframe[symbol_x]) + "Y: "  + str(dataframe[symbol_y]),
                            mode            = 'markers',
                            opacity         = overlay_alpha,
                            marker          = dict  (
                                                    color   = overlay_color, 
                                                    symbol  = overlay_marker
                                                    ),
                            ),     
                )
                                
        plot_3D.update_layout	(
                                hoverlabel_align = 'right',
                                autosize    = True,
                                height      = 720,
                                width       = 1080,
                                title       = plot_type,
                                xaxis       = dict(title = symbol_x),
                                yaxis       = dict(title = symbol_y)
                                )
        
        plot_3D.update_scenes   (
                                xaxis       = dict(title = symbol_x),
                                yaxis       = dict(title = symbol_y),
                                zaxis       = dict(title = symbol_z)
                                )

        return plot_3D