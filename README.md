<p align="center">
  <img src="https://user-images.githubusercontent.com/83425701/137222206-7953099b-2a39-4ac3-98a8-5bfd3a910c0e.png" /img>
</p>

xPlot is a Python/Streamlit based data explorer to plot data from files for analysis.
<br>It uses a WebUI powered by the Streamlit library, and plotting by the Plotly Library.
<br>Data is handled and partly manipulated by Pandas and Numpy.

## Installation

<br>`install.ink` is a shortcut to a batch file that allows the user to select from 2 installation choices.
- **Option [1]: Install Python 3.7.4, Paths, Dependancies and Launch xPlot**
<br>Using option [1] will launch a powershell script to install Python 3.7.4, all the dependencies required by xPlot and then launch the tool in a web browser
- **Option [2]: Install Dependancies and Launch xPlot**
<br>Using option [2] will bypass the python installation and just install all the dependencies (presuming it is installed and has the correct paths) required by xPlot and then launch the tool in a web browser.
<br>Once installtion is complete the tool will already be launched, and can be relaunched using `xPlot.bat`

## Running

<br>`xPlot.bat` will apply `py - 3.7 -m streamlit run xPlot.py` command to the cmd terminal which will launch a local server and open up the default web browser as the front-end.

## Plotting

Supported plots are:
### 2D
- Line
- Scatter
- Line and Scatter

![image](https://user-images.githubusercontent.com/83425701/137307577-3c0ef09c-49a9-4738-8cf1-4484f90de77f.png)
![image](https://user-images.githubusercontent.com/83425701/137308794-2bda73dd-d12e-4096-934c-5b3a9df1dd25.png)
![image](https://user-images.githubusercontent.com/83425701/137308847-7d6041a5-8617-457b-a7d5-203cc6ece13e.png)


### 3D
- Contour *
- 3D Scatter
- Surface
- Heatmap *
* Not visually 3D but use three dimensions of data.
![image](https://user-images.githubusercontent.com/83425701/137308065-8a3dd4cb-417d-453a-9481-04cc3cc7adaf.png)
![image](https://user-images.githubusercontent.com/83425701/137308427-a93921fe-9136-4c63-8a32-03d9d4078420.png)
![image](https://user-images.githubusercontent.com/83425701/137308578-1c503083-d586-4eec-a993-4289b6535493.png)


