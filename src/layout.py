import streamlit as st
from src.utils import load_dataframe

def fixed_content():
    """
    Contains fixed content visible across different links
    :return:
    """
    # Main Page
    st.title('2D Plotter')   
    st.checkbox('Plot',value = True)
    st.checkbox('Display plotted data as table',value = False)
    st.checkbox('Display all data as table')


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

def colormap_config():
    colormap_config = dict({
        'staticPlot' : True
    })
    return colormap_config

def views(link):
    """
    Select between 2D and 3D plotter
    """
    st.sidebar.header("CSV Plot")
    st.sidebar.markdown('''<small>v0.2</small>''', unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader(label="Upload your csv or excel file here.",
                                                 accept_multiple_files=False,
                                                 type=['csv', 'xlsx'])
    
    if uploaded_file is not None:

        dataframe, columns = load_dataframe(uploaded_file=uploaded_file)

        # Create Index array, to plot against. Not all data has timestamp
        symbols = list(dataframe)
        # Use to NOT plot.
        symbols.insert(0, "Not Selected")

        trace =  dict()

        if link == '2D Plot':
            st.header("2D Plotter")

        elif link == '3D Plot':
            st.header('3D Plotter')

    else:
        st.warning("Please upload data")