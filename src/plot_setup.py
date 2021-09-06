import streamlit as st
from plotly.validators.scatter.marker import SymbolValidator

def trace_dict(toggle):
    '''
    Determine trace dictionary depending on 2d or 3d graph
    '''

    trace =  dict()

    if toggle == "2D Plot":
        trace["Symbol"]         = []
        trace["Name"]           = []
        trace["Hex_rep"]        = []
        trace["Bin_rep"]        = []
        trace["Plot_row"]       = []
        trace["Axis"]           = []
        trace["Color"]          = []
        trace["Size"]           = []
        trace["Style"]          = []
        trace["Chart_Type"]     = []
        trace["Function"]       = []
        trace["Value"]          = []
        trace["Extra_Signals"]  = 0

    elif toggle == "3D Plot":
        trace["Symbol"]         = []
        trace["Name"]           = []
        trace["Chart_Type"]     = []
        trace["Fill_Value"]     = []
        trace["Interp_Method"]  = []
        trace["Grid_Res"]       = []
    
    return trace

@st.cache
def get_markers():
    raw_symbols = SymbolValidator().values
    namestems = []

    for symbols in range(0,len(raw_symbols),3):
        name = raw_symbols[symbols+2]
        namestems.append(name)

    marker_names = namestems
    return marker_names

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

    return y_axis_plot 


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
    
    ## Subplot 2 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 2']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass

    ## Subplot 2 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 3']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass

        ## Subplot 2 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 4']

    if len(secondary_y["Axis"].unique()) == 1:
        y_axis_config.append([{'secondary_y': False}])

    elif len(secondary_y["Axis"].unique()) == 2:
        y_axis_config.append([{'secondary_y': True}])
    else:
        pass

        ## Subplot 2 Secondary Y's
    secondary_y =  plot_config.loc[plot_config['Plot_row'] == 'Subplot 5']

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
        plotheight = 1100
    elif Subplot =="Subplot 3":
        subplot = 4
        plotheight = 1300
    elif Subplot =="Subplot 4":
        subplot = 4
        plotheight = 1400
    elif Subplot =="Subplot 5":
        subplot = 4
        plotheight = 1600
    else:
        subplot = 1
        plotheight = 900
    
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
#            temp_col = dataframe[plot_config["Symbol"][row]]
#            for j in range(0, len(plot_config["Function"][row])):
#                if plot_config["Value"][row][j] == "None":
#                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col)
#                else:
#                    temp_col = np.vectorize(y_functions_dict[plot_config["Function"][row][j]])(temp_col, plot_config["Value"][row][j] )
#
#            dataframe[Name] = temp_col
#            y_axis_symbol = dataframe[Name]
#            plotted_data[Name] = y_axis_symbol
#        else:
#            y_axis_symbol = dataframe[plot_config["Symbol"][row]]
#            plotted_data[Name] = y_axis_symbol