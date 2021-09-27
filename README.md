# xPlot 📈

xPlot is a Python/Streamlit based data explorer to plot data from files for analysis.
It uses a WebUI powered by the Streamlit library, and plotting by the Plotly Library.
Data is handled and party manipulated by Pandas and Numpy.

## Installation

<br>`install.bat` is a batch file that allows the user to select from 2 installation choices.
- **Option [1]: Install Python 3.9.5, Paths, Dependancies and Launch xPlot**
<br>Using option [1] will launch a powershell script to install Python 3.9.5, all the dependencies required by xPlot and then launch the tool in a web browser
- **Option [2]: Install Dependancies and Launch xPlot**
<br>Using option [2] will bypass the python installation and just install all the dependencies (presuming it is installed and has the correct paths) required by xPlot and then launch the tool in a web browser.
<br>Once installtion is complete the tool will already be launched, and can be relaunched using `xPlot.bat`

## Running

<br>`xPlot.bat` will apply `py - 3.9 -m streamlit run xPlot.py` command to the cmd terminal which will launch a local server and open up the default web browser as the front-end.

## Plotting

Supported plots are:
### 2D
- Line
- Scatter
- Line and Scatter

![image](https://user-images.githubusercontent.com/83425701/134918166-f0dd8b45-42e0-4b04-8824-44d10c5cda7c.png)

### 3D
- Contour *
- 3D Scatter
- Surface
- Heatmap *
* Not visually 3D but use three dimensions of data.

![image](https://user-images.githubusercontent.com/83425701/134918341-34260cc6-6efc-424f-88e2-07fad63ba7f8.png)

![image](https://user-images.githubusercontent.com/83425701/134918427-f3b41999-57ad-4b95-ba90-6acb110122c0.png)
