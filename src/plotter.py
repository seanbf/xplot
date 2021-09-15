import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from src.functions import y_functions_dict
from src.plot_setup import get_y_axis, get_hovertip, get_name, get_subplot, get_y_axis_config

@st.cache
def plot_2D(dataframe, plot_config, symbol_0):
    plotted_data = pd.DataFrame()       
    with st.spinner('Generating Interactive Plot'):
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
                temp_col = dataframe[plot_config["Symbol"][row]]
                for j in range(0, len(plot_config["Function"][row])):
                    if plot_config["Value"][row][j] == "None":
                        temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col)
                    else:
                        temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col, plot_config["Value"][row][j] )

                dataframe[Name] = temp_col
                y_axis_symbol = dataframe[Name]
                plotted_data[Name] = y_axis_symbol
            else:
                y_axis_symbol = dataframe[plot_config["Symbol"][row]]
                plotted_data[Name] = y_axis_symbol

            # Plot type

            if plot_config["Chart_Type"][row] == 'lines':
                
                plot.add_trace	(go.Scattergl (  
                                            x       		= dataframe[symbol_0],
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
                plot.add_trace	(go.Scattergl (  
                                            x       		= dataframe[symbol_0],
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
                plot.add_trace	(go.Scattergl (  
                                            x       		= dataframe[symbol_0],
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
                                hovermode	= 'x',  
                                autosize    = True,
                                height      = plotheight
                                )    

    return plot

@st.cache
def plot_3D(x, y, z, dataframe, plot_config, color_palette, overlay, overlay_alpha, overlay_marker, overlay_color):

    with st.spinner("Generating 3D Plot"):

        plot_3D = go.Figure()

        if plot_config["Chart_Type"][0] == 'Contour':
            plot_3D.add_trace(go.Contour    (
                                            z           = z,
                                            x           = x, 
                                            y           = y,
                                            colorscale  = color_palette,
                                            hovertemplate = str(plot_config["Symbol"][0]) + ': %{x:.2f}' + 
                                                            '<br>' + str(plot_config["Symbol"][1])+ ': %{y:.2f}</br>' +
                                                            str(plot_config["Symbol"][2]) + ': %{z:.2f}',

                                            contours    = dict  (
                                                                coloring    ='heatmap',
                                                                showlabels  = True,
                                                                labelfont   = dict  (
                                                                                    size = 10,
                                                                                    color = 'white',
                                                                                    )
                                                                ), 

                                            colorbar    = dict  (
                                                                title       = str(plot_config["Symbol"][2]),
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                    )       )

        if plot_config["Chart_Type"][0] == 'Surface':
                        plot_3D.add_trace(go.Surface  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,

                                            contours =  {
                                                        "x": {"show": True},
                                                        "z": {"show": True}
                                                        },

                                            colorscale  = color_palette,
<<<<<<< HEAD
                                        
=======
                                     
>>>>>>> 038394f1fb2cc6cb6e7d98c3301def72256ae320
                            
                                            hovertemplate = str(plot_config["Symbol"][0]) + ': %{x:.2f}' + 
                                                            '<br>' + str(plot_config["Symbol"][1])+ ': %{y:.2f}</br>' +
                                                            str(plot_config["Symbol"][2]) + ': %{z:.2f}',              
                                            colorbar    = dict  (
                                                                title       = str(plot_config["Symbol"][2]),
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                )
                                            )           )
        if plot_config["Chart_Type"][0] == 'Heatmap':
                        plot_3D.add_trace(go.Heatmap  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,

                                            colorscale  = color_palette,

                                            hovertemplate = str(plot_config["Symbol"][0]) + ': %{x:.2f}' + 
                                                            '<br>' + str(plot_config["Symbol"][1])+ ': %{y:.2f}</br>' +
                                                            str(plot_config["Symbol"][2]) + ': %{z:.2f}',

                                            colorbar    = dict  (
                                                                title       = str(plot_config["Symbol"][2]),
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

                                            hovertemplate = str(plot_config["Symbol"][0]) + ': %{x:.2f}' + 
                                                            '<br>' + str(plot_config["Symbol"][1])+ ': %{y:.2f}</br>' +
                                                            str(plot_config["Symbol"][2]) + ': %{z:.2f}',             

                                            )           )
        
        if overlay == True:
            plot_3D.add_trace	(go.Scatter (  
                            x       		= dataframe[plot_config["Symbol"][0]],
                            y       		= dataframe[plot_config["Symbol"][1]],
                            name 			= "X: "  + str(dataframe[plot_config["Symbol"][0]]) + "Y: "  + str(dataframe[plot_config["Symbol"][1]]),
                            mode            = 'markers',
                            opacity         = overlay_alpha,
                            marker          = dict  (
                                                    color   = overlay_color, 
                                                    symbol  = overlay_marker
                                                    ),
                            ),     
                )
                                
        plot_3D.update_layout	(
                    autosize    = True,
                    height      = 720,
                    width       = 1080,
                    title       = plot_config["Chart_Type"][0] ,
                    xaxis       = dict(title=str(plot_config["Symbol"][0])),
                    yaxis       = dict(title=str(plot_config["Symbol"][1]))
                    
                    )

        return plot_3D
