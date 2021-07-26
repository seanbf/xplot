import streamlit as st
from palettable.cartocolors.qualitative import Pastel_10,   Antique_10, Bold_10,        Prism_10,   Safe_10,        Vivid_10
from palettable.colorbrewer.qualitative import Accent_8,    Paired_12,  Pastel2_8,      Set3_12,    Set2_8,         Set1_9,         Pastel2_8,      Pastel1_9
from palettable.tableau                 import BlueRed_6,   BlueRed_12, ColorBlind_10,  Gray_5,     GreenOrange_6,  GreenOrange_12, PurpleGray_6,   PurpleGray_12,  Tableau_10, Tableau_20, TableauLight_10,    TableauMedium_10,   TrafficLight_9
from palettable.cartocolors.diverging   import ArmyRose_7,  Earth_7,    Fall_7,         Geyser_7,   TealRose_7,     Temps_7,        Tropic_7
from palettable.colorbrewer.diverging   import BrBG_11,     PRGn_11,    PiYG_11,        PuOr_11,    RdBu_11,        RdGy_11,        RdYlBu_11,      RdYlGn_11,      Spectral_11
from palettable.scientific.diverging    import Berlin_20,   Broc_20,    Cork_20,        Lisbon_20,  Roma_20,        Tofino_20,      Vik_20
from palettable.matplotlib              import Inferno_20,  Magma_20,   Plasma_20,      Viridis_20
from palettable.colorbrewer.sequential  import Blues_9,     BuGn_9,     BuPu_9,         GnBu_9,     Greens_9,       Greys_9,        OrRd_9,         Oranges_9,      PuBu_9,     PuBuGn_9,   PuRd_9,             Purples_9,           RdPu_9, Reds_9,YlGn_9,YlGnBu_9,YlOrBr_9
import plotly.graph_objects as go


@st.cache
def qualitive_color_dict():
    """Qualitive Color Dictionary
    """
    color_dict    =      dict({
                        'Tableau'           :Tableau_10.hex_colors, 
                        'Tableau Paired'    :Tableau_20.hex_colors, 
                        'Tableau Light'     :TableauLight_10.hex_colors, 
                        'Tableau Medium'    :TableauMedium_10.hex_colors, 
                        'Pastel'            :Pastel_10.hex_colors,
                        'Antique'           :Antique_10.hex_colors, 
                        'Bold'              :Bold_10.hex_colors, 
                        'Prism'             :Prism_10.hex_colors, 
                        'Safe'              :Safe_10.hex_colors, 
                        'Vivid'             :Vivid_10.hex_colors,
                        'Accent'            :Accent_8.hex_colors, 
                        'Paired'            :Paired_12.hex_colors, 
                        'Pastel 2'          :Pastel2_8.hex_colors, 
                        'Set 3'             :Set3_12.hex_colors, 
                        'Set 2'             :Set2_8.hex_colors,
                        'Set 1'             :Set1_9.hex_colors, 
                        'Pastel 2'          :Pastel2_8.hex_colors, 
                        'Pastel 1'          :Pastel1_9.hex_colors,
                        'Blue Red 6'        :BlueRed_6.hex_colors, 
                        'Blue Red 12'       :BlueRed_12.hex_colors, 
                        'Color Blind'       :ColorBlind_10.hex_colors, 
                        'Gray'              :Gray_5.hex_colors, 
                        'Green Orange 6'    :GreenOrange_6.hex_colors, 
                        'Green Orange 12'   :GreenOrange_12.hex_colors, 
                        'Purple Gray 6'     :PurpleGray_6.hex_colors, 
                        'Purple Gray 12'    :PurpleGray_12.hex_colors,
                        'Traffic Light'     :TrafficLight_9.hex_colors
                        })       
    return color_dict

@st.cache
def diverging_color_dict():
    """Diverging Color Dictionary
    """
    color_dict    =      dict({
                        'Berlin'            :Berlin_20.hex_colors, 
                        'Broc'              :Broc_20.hex_colors, 
                        'Cork'              :Cork_20.hex_colors, 
                        'Lisbon'            :Lisbon_20.hex_colors, 
                        'Roma'              :Roma_20.hex_colors, 
                        'Torfino'           :Tofino_20.hex_colors, 
                        'Vik'               :Vik_20.hex_colors,
                        'ArmyRose'          :ArmyRose_7.hex_colors,
                        'Earth'             :Earth_7.hex_colors, 
                        'Fall'              :Fall_7.hex_colors, 
                        'Geyser'            :Geyser_7.hex_colors, 
                        'TealRose'          :TealRose_7.hex_colors, 
                        'Temps'             :Temps_7.hex_colors,
                        'Tropic'            :Tropic_7.hex_colors, 
                        'Brown Blue-Green'  :BrBG_11.hex_colors, 
                        'Purple Green'      :PRGn_11.hex_colors, 
                        'Pink Green'        :PiYG_11.hex_colors, 
                        'Orange Purple'     :PuOr_11.hex_colors,
                        'Red Blue'          :RdBu_11.hex_colors, 
                        'Red Grey'          :RdGy_11.hex_colors, 
                        'Red Yellow Blue'   :RdYlBu_11.hex_colors,
                        'Red Yellow Green'  :RdYlGn_11.hex_colors, 
                        'Spectral'          :Spectral_11.hex_colors 
                        })                   
    return color_dict

@st.cache
def sequential_color_dict():
    """Sequential_color_set Color Dictionary
    """
    color_dict    =      dict({
                        'Viridis'               :Viridis_20.hex_colors, 
                        'Inferno'               :Inferno_20.hex_colors, 
                        'Magma'                 :Magma_20.hex_colors, 
                        'Plasma'                :Plasma_20.hex_colors,  
                        'Greens'                :Greens_9.hex_colors, 
                        'Blues'                 :Blues_9.hex_colors, 
                        'Reds'                  :Reds_9.hex_colors, 
                        'Purples'               :Purples_9.hex_colors, 
                        'Oranges'               :Oranges_9.hex_colors, 
                        'Greys'                 :Greys_9.hex_colors, 
                        'Blue Green'            :BuGn_9.hex_colors,
                        'Blue Purple'           :BuPu_9.hex_colors,
                        'Green Blue'            :GnBu_9.hex_colors, 
                        'Orange Red'            :OrRd_9.hex_colors, 
                        'Purple Blue'           :PuBu_9.hex_colors, 
                        'Purple Red'            :PuRd_9.hex_colors, 
                        'Red Purple'            :RdPu_9.hex_colors,
                        'Yellow Green'          :YlGn_9.hex_colors, 
                        'Yellow Green Blue'     :YlGnBu_9.hex_colors, 
                        'Yellow Orange Brown'   :YlOrBr_9.hex_colors, 
                        'Purple Blue Green'     :PuBuGn_9.hex_colors, 
                        })          
    return color_dict

@st.cache
def plot_color_set(color_palaette, color_set, is_three_d):
    """Plot color pallete as Bar chart for previewing.
    """
    if is_three_d == True:
        width           = 575
    else:
        width           = 340

    n = len(color_palaette)
    fig = go.Figure (
                    data =  [go.Bar     (
                                        orientation = "v",
                                        x           = [color_palaette] * n,
                                        y           = [1] * n,
                                        customdata  = [(x + 1) / n for x in range(n)],
                                        marker      = dict(color=list(range(n)), colorscale=color_palaette, line_width=0),
                                        name        = color_set,
                                        )
                            ],
                    layout = dict   (
                                    xaxis           = dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                                    yaxis           = dict(showticklabels=False, showgrid=False, fixedrange = True, visible=False),
                                    height          = 85,
                                    width           = width,
                                    margin          = dict(l=0,r=0,b=0,t=25),
                                    paper_bgcolor   = 'rgba(0,0,0,0)',
                                    plot_bgcolor    = 'rgba(0,0,0,0)'
                                    ),
                    )
    return fig