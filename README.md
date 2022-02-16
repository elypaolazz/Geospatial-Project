# **<i>Discovering Dolomiti peaks</i>**
<h3>Geeospatial Analysis and Representation for Data Science course final project</h3>

<br>
<h2><b>Description</b></h2>

The project aims to explore the Dolomites area through the methodologies discussed in the Geospatial Analysis and Representation for Data Science course. Through the various analyses performed, we then attempt to apply the lectures' arguments and other related insights in order to find useful findings about the area, for which geospatial data are not often investigated.

<br>
<h2><b>Prerequisites</b></h2>

In order to run this project's Python notebook, it is recommended to preferably use Python 3.9 version and the following version of the libraries:
- `geopandas==0.10.1`,
- `contextly==1.1.0`,
- `pandas==1.3.4`,
- `matplotlib==3.4.3`,
- `folium==0.12.1`,
- `pyrosm==0.6.1`,
- `osmnx==1.1.1`,
- `rasterio==1.2.10`,
- `OWSLib==0.25.0`,
- `Shapely==1.7.1`,
- `pyproj==3.3.0`.

In order to be able to run the R nortebook, the following libraries are required: 
- `rgdal`,
- `spdep`,
- `boot`.

<br>
<h2><b>Installation</b></h2>

Clone this repository in a local directory typing `git clone https://github.com/elypaolazz/Geospatial-Project.git` in the command line.

It is strongly recommended to create a virtual environment in which to install the correct versions of the required Python libraries:
- if you create the environment via virtualenv, you can type `pip install -r requirements.txt` to install all the libraries used;
- if you prefer to work with Anaconda's evironment, you can simply type `conda env create --file environment.yaml` to create the environment containing all the libraries in the appropriate versions.

For the R libraries installation, it will only be required to run the first chunk of the `5_spatial_statistics_analysis.Rmd` notebook.

<br>
<h2><b>Code structure</b></h2>

The project is composed by five main scripts:
- `1_dolomiti_intro.ipynb`, which contains an introduction to the topic and initial exploration and visualisation;
- `2_dolomiti_reg_prov_mun_analysis.ipynb`, which analyses and ranks the regions, provinces and municipalities of the Dolomiti;
- `3_dolomiti_alto_adige_ski.ipynb`, which deals with the analysis of province of Bolzano Dolomiti's ski areas and other related aspects;
- `4_dolomiti_alto_adige_raster.ipynb`, which deals with the analysis of raster data of the province of Bolzano Dolomiti's area;
- `5_spatial_statistics_analysis.Rmd`, R notebook aimed at analysing ski passes prices in the area and their possible spatial relationship.

There are also some important forlders such as `data`, containing all the data and resources used, and `notebooks_html`, which contains the notebooks in html format so that they can be easily accessed without running the code. In addition to this, files such as `function.py` and `ski_area_cost.ipynb` represent support scripts for the analyses performed in the main files.


Code tree:

```
├── data
│  	├── area_dolomiti_BZ
│  	├── Castelrotto_raster
│  	├── Limiti01012021_g
│  	├── Raster_alpine_region
│  	├── Ski_lift_data
│  	├── Ski_slopes_data
│  	├── altoadige.pbf
│  	└── I_nove_Sistemi_delle_Dolomiti_UNESCO.kml
│  
├── notebooks_html
│
├── notebooks_images
│ 
├── 1_dolomiti_intro.ipynb
│ 
├── 2_dolomiti_reg_prov_mun_analysis.ipynb
│
├── 3_dolomiti_alto_adige_ski.ipynb
│
├── 4_dolomiti_alto_adige_raster.ipynb
│
├── 5_spatial_statistics_analysis.Rmd
│
├── environment.yml.Rmd
│
├── function.py
│
├── README.md
│
├── requirements.txt
│
└── skipass_price_data_building
```

<br>
<h2><b>Report and script exploration</b></h2>

A more in-depth explanation of the project can be found in the file `project_report.pdf`. You can also view the executed scripts (without cloning the repository locally) at this <a href="https://elypaolazz.github.io/geosp_pages/index.html">address </a>.
