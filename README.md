# DATA PREPROCESSING INSTRUCTION

## ASF DATA DOWNLOAD
1. Download data from webpage: https://search.asf.alaska.edu/#/.

	A. Use Filters: 
	- Search Type: Geographic Search
	- Dataset: Sentinel-1
	- Start Date: date of interest (eg. 2021-JAN-05 or 2021-FEB-04 or 2021-MAR-06). 
	- End Date: same as Start Date. 

	B. Then mark Area of Interest using "Draw a Box". Use "Update". 

	C. Choose the correct area (eg. Los Angeles port). 

	D. Download L1 Detected High-Res Dual-Pol (GRD-HD). 

	E. No operations should be performed on the photo: no DEM, no speckle filter.

2. Put the downloaded data in the ZIP format in the "1_raw_ASF_data" folder. 

3. It is good practice to choose the same area and only change the dates. 

## AIS DATA DOWNLOAD
1. Download data from webpage: https://marinecadastre.gov/ais/. 
- chooose the year (eg. 2021)
- choose the day and month (eg. AIS_2021_01_05 and AIS_2021_02_04 and AIS_2021_03_06). 
- chosen days should correspond to the chosen dates in the ASF DATA. 

2. AIS data will be downloaded in .zip format. 
Unpack the data (should be in CSV format) to the folder "2_raw_AIS_csv_data". 
ZIP file should be put in the "0_raw_AIS_zip_data" folder. 


## ASF Data preprocessing
1. Use tool: SNAP ->  https://step.esa.int/main/download/snap-download/
https://step.esa.int/main/toolboxes/snap/

2. Load ZIP file of the chosen area (drag-and-drop). 
Click on the loaded file/Bands/Amplitude_VH and wait till the image load. 

3. OPTION FOR AUTOMATION: 
- Draw rectangle (Rectangle drawing tool). 
- Selection tool (mouse) and select the rectangle.
- Right mouse click/WKT from Geometry (Well Known Text). 
- Copy the text. Should be in the format:

	POLYGON ((-118.37846494072772 33.483346787956265, -118.04017792681735 33.53066498906752, 
	   -118.0972044694882 33.81569238337598, -118.43743144365283 33.768348681301156, 
	   -118.37846494072772 33.483346787956265))
	   
	POLYGON ((-118.36808413797584 33.32752540890519, -118.00903444292464 33.377912812694035, 
   -118.1006294874334 33.83557113460484, -118.46367122511965 33.78504216157723, 
   -118.36808413797584 33.32752540890519))
   
   POLYGON ((-118.34902506811939 33.28125919889688, -117.99967688614623 33.330331658045004, 
   -118.09509484870476 33.80720768223687, -118.44821001610778 33.75803227611276, 
   -118.34902506811939 33.28125919889688))

- Run script "". 
- For this use conda env "geoenv" ("conda activate geoenv") from "conda env list". 

4. MANUAL OPTION: 
- Click on the panel: Raster/Subset. 
- If necessary, click Use Preview. 
- Cut to the needed area of interest. 
- Click OK. 
Subset exists in the program memory. 

You can click on the subset file/Bands/Amplitude_VH and wait till the image load to see the results. 

5. Choose subset. On the panel choose:
- Radar/Geometric/Terrain correction/Range-Doppler Terrain correction. 

The window comes. In the second tab "Processing parameters" choose:
- Source Bands as intensity_VV and intensity_VH. 
- Digital Elevation Model: Copernicus 30m Global DEM (Auto Download). 
- DEM and Image resampling: default (BILINEAR_INTERPOLATION). 
- Map projection: default (WGS84(DD)). 
- IMPORTANT!!! Disable checkbox "Mask out areas without elevation". 
- In the tab "I/O parameters" change "Save as": GeoTIFF. 
- CHANGE SAVING DIRECTORY to "3_processed_ASF_data". 
Run. Wait a few minutes (pictures has big sizes - even 900 MB). 

6. Check if the processed picture is in the folder "3_processed_ASF_data" in the TIF format. 

## AIS Data preprocessing
1. Run python/jupyter script: "1_AIS_data_preprocessing.py". 
2. Prepared AIS data should appear in the folder "4_processed_AIS_data". 

## Check the work
1. Go to QGIS. 
2. Load the prepared AIS data as Layer/Add Layer/Add Delimeted Text Layer. 
Check if in Point coordinates X field is LON and Y field is LAT. 
3. Load the prepared AIS data as Layer/Add Layer/Add Raster Layer. 
4. Loaded image has 2 bands: VV and VH. Create third band = VV/VH:
- Raster/Raster calculator/???


## Useful links.
1. https://drr.ikcest.org/tutorial/k8022 - GDAL tutorial
2. https://step.esa.int/main/download/snap-download/ - SNAP download
3. https://github.com/senbox-org/ - SNAP
4. https://snap-contrib.github.io/snapista/ - SNAPISTA, python snappy language
5. https://snap.stanford.edu/snappy/ - SNAP.py - SNAP for python
6. https://snap.stanford.edu/snappy/doc/tutorial/tutorial.html - SNAPPY tutorial



