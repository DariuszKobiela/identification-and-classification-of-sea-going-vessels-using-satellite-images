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
Unpack the data (should be in CSV format) to the folder "2_raw_AIS_csv_data" using TOTAL COMMANDER program (it is very fast and helpful to unzip multiple files at once). 
ZIP file should be put in the "0_raw_AIS_zip_data" folder. 


## ASF Data preprocessing
1. Use tool: SNAP ->  https://step.esa.int/main/download/snap-download/ (Sentinel Toolboxes, Main download)
https://step.esa.int/main/toolboxes/snap/

### SNAPPY python
2. Open SNAP Command Line in Start (Windows). 

	* PYTHON interpreter: C:\Users\user\AppData\Local\Programs\Python\Python36

3. Configuration (only first time): 
	> cd C:\Program Files\snap\bin
	> snappy-conf C:\Users\user\anaconda3\envs\snap\python.exe C:\Users\user\anaconda3\envs\snap\Lib\
	> snappy-conf C:\Python34\python.exe C:\Python34\python.exe\Lib

> Configuring SNAP-Python interface...
> Done. The SNAP-Python interface is located in 'C:\Users\user\anaconda3\envs\snap_python3_5\Lib\snappy'
> When using SNAP from Python, either do: sys.path.append('C:\\Users\\user\\anaconda3\\envs\\snap_python3_5\\Lib') 
> or copy the 'snappy' module into your Python's 'site-packages' directory.

HOW TO CONFIGURE virtualenv with python 3.4 for snappy ESA SNAP:
https://senbox.atlassian.net/wiki/spaces/SNAP/pages/50855941/Configure+Python+to+use+the+SNAP-Python+snappy+interface
1. Install python 3.4 from https://www.python.org/downloads/release/python-340/.
2. Open PowerShell as Admin. Allow scripts execution by command "Set-ExecutionPolicy RemoteSigned". In order to get back to the previous state in the future, type "Set-ExecutionPolicy Restricted". 
3. Real about virtualenv at https://realpython.com/python-virtual-environments-a-primer/. 
   - https://docs.python.org/3/library/venv.html
4. Open PowerShell in standard mode. Go to C:\Python34\virtenv\Scripts>. 
	> PS C:\Python34\virtenv> Scripts\activate                         
	> (virtenv) PS C:\Python34\virtenv> python 
	> Python 3.4.0 (v3.4.0:04f714765c13, Mar 16 2014, 19:25:23) [MSC v.1600 64 bit (AMD64)] on win32 
	> Type "help", "copyright", "credits" or "license" for more information.       
	> >>> import GPT                      
   > Traceback (most recent call last):                
   > File "<stdin>", line 1, in <module>                  
   > ImportError: No module named 'GPT'              
   > >>> from snappy import GPF                   
   > INFO: org.esa.snap.core.gpf.operators.tooladapter.ToolAdapterIO: Initializing external tool adapters     
   > INFO: org.esa.s2tbx.dataio.gdal.GDALVersion: GDAL not found on system. Internal GDAL 3.2.1 from distribution will be used. (f0)  
   > INFO: org.esa.s2tbx.dataio.gdal.GDALVersion: Internal GDAL 3.2.1 set to be used by SNAP. 
   > Native library load failed.                                                         
   > java.lang.UnsatisfiedLinkError: C:\Users\user\.snap\auxdata\gdal\gdal-3-2-1\gdalalljni.dll: Can't find dependent libraries  
   > SEVERE: org.esa.s2tbx.dataio.gdal.GDALLoader: Failed to initialize GDAL native drivers. GDAL readers and writers were disabled.java.lang.reflect.InvocationTargetException             
   > INFO: org.esa.snap.core.util.EngineVersionCheckActivator: Please check regularly for new updates for the best SNAP experience.     
          
5. In order to install extra packages in the virtualenv: 
   > (virtenv) PS C:\Python34\virtenv> python -m pip3 install numpy 

6. Additional extra command: 
   - PS C:\Users\user> where.exe 
   
7. Learn about making scripts in ESA snappy SNAP python:
   - https://forum.step.esa.int/t/snappy-gpf-createproduct-object-discrimination-no-output-mask/35729
   - https://github.com/wajuqi/Sentinel-1-preprocessing-using-Snappy/blob/master/s1_preprocessing.py
   - https://forum.step.esa.int/t/using-subset-in-snappy-and-snap-why-different-result/34175
   - https://forum.step.esa.int/t/write-a-georeferenced-tiff-with-snappy/16751
   - https://forum.step.esa.int/t/exporting-rgb-image-as-geotiff-error/13353/2
   - https://senbox.atlassian.net/wiki/spaces/SNAP/pages/19300362/How+to+use+the+SNAP+API+from+Python
   - https://github.com/senbox-org/snap-engine/blob/master/snap-python/src/main/resources/snappy/examples/snappy_write_image.py
   - https://www.youtube.com/watch?v=PiU68g3WRIY
   - https://forum.step.esa.int/t/snappy-where-to-start/1463/4
   - https://www.youtube.com/watch?v=iEEMn7h35nU
   - https://forum.step.esa.int/t/s1a-product-terrain-correction/27599/10

OTHER USEFUL LINKS: 
- https://stackoverflow.com/questions/4037939/powershell-says-execution-of-scripts-is-disabled-on-this-system
- https://www.roelpeters.be/virtualenv-venv-choose-python-version/
- https://step.esa.int/docs/tutorials/Importing%20data%20into%20SNAP.pdf
- https://realpython.com/python-virtual-environments-a-primer/#the-virtualenv-project
- http://step.esa.int/main/doc/tutorials/
- https://rus-copernicus.eu/portal/wp-content/uploads/library/education/training/PY01_Sentinel1Processing_snappy.pdf


### Manual options
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

5. MASK for harbour and terrain
W SNAPie:
Ładujesz zdjęcie na etapie przetwarzania
Raster / Mask / "Land/Sea Mask"
Kanały Intensity_VV i Intensity_VH (oba)
Opcja Extent shoreline: daj nawet 30 pikseli (metrów)
EDIT: TRZEBA BRAĆ po 40 m (inaczej nie zakrywa całości nabrzeża)
Zaznacz "Mask out the Land"
Zapisujemy w natywnym formacie SNAPa

6. Choose subset. On the panel choose:
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

7. Check if the processed picture is in the folder "5_processed_ASF_data" in the TIF format. 

## AIS Data preprocessing
1. Run python/jupyter script: "1_AIS_data_preprocessing.py". 
2. Semi-processed data will be saved to the folder "4_processed_AIS_data".
3. Prepared AIS data should appear in the folder "5_interpolated_AIS_data". 

## Check the work
1. Go to QGIS. 
2. Load the prepared AIS data as Layer/Add Layer/Add Delimeted Text Layer. 
Check if in Point coordinates X field is LON and Y field is LAT. 
3. Load the prepared AIS data as Layer/Add Layer/Add Raster Layer. 
4. Loaded image has 2 bands: VV and VH. Create third band = VV/VH:
- Raster/Raster calculator/???
5. Load AIS data into QGIS. Layer/Add Layer/Add Delimited Text Layer. 
Make sure that "X_field" is "LON" and "Y_field" is "LAT". 

## ASF Data labelling
1. https://github.com/heartexlabs/label-studio
2. https://labelstud.io/guide/install.html#System-requirements
3. https://www.tensorflow.org/hub/tutorials/object_detection
4. https://www.geeksforgeeks.org/detect-an-object-with-opencv-python/
5. https://pypi.org/project/labelImg/#labelimg
6. https://www.youtube.com/watch?v=p0nR2YsCY_U
7. https://github.com/heartexlabs/label-studio
8. https://labelstud.io/guide/label_studio_compare.html
9. https://www.youtube.com/watch?v=e1yJZUp0590
10. https://labelstud.io/tags/image.html
11. https://cornelliusyudhawijaya.medium.com/innovative-data-labeling-projects-with-label-studio-and-dagshub-99c327f357e5

## Useful links.
1. https://drr.ikcest.org/tutorial/k8022 - GDAL tutorial
2. https://step.esa.int/main/download/snap-download/ - SNAP download
3. https://github.com/senbox-org/ - SNAP
4. https://snap-contrib.github.io/snapista/ - SNAPISTA, python snappy language
5. https://snap.stanford.edu/snappy/ - SNAP.py - SNAP for python
6. https://snap.stanford.edu/snappy/doc/tutorial/tutorial.html - SNAPPY tutorial
7. https://blog.paperspace.com/train-yolov5-custom-data/ - YOLO network
8. https://learnxinyminutes.com/docs/rst/ - restructured text (RST) for github (results presentation)

## Links for YOLO
1. https://github.com/shahkaran76/yolo_v3-tensorflow-ipynb/blob/master/ReadMe.pdf
2. https://github.com/shahkaran76/yolo_v3-tensorflow-ipynb/blob/master/YOLO%20Tensorflow.ipynb
3. https://blog.paperspace.com/train-yolov5-custom-data/
4. https://github.com/OlafenwaMoses/ImageAI/blob/master/imageai/Detection/Custom/CUSTOMDETECTIONTRAINING.md
5. https://medium.com/@shahkaran76/yolo-object-detection-algorithm-in-tensorflow-e080a58fa79b
6. https://medium.com/geekculture/journey-putting-yolo-v7-model-into-tensorflow-lite-object-detection-api-model-running-on-android-e3f746a02fc4
7. https://github.com/WongKinYiu/yolov7/blob/main/models/yolo.py
8. https://github.com/WongKinYiu/yolov7
9. https://inside-machinelearning.com/en/use-yolov7/
10. https://inside-machinelearning.com/en/use-yolov6/
11. https://learnopencv.com/fine-tuning-yolov7-on-custom-dataset/
12. https://www.kaggle.com/code/aruchomu/yolo-v3-object-detection-in-tensorflow
13. https://wellsr.com/python/object-detection-from-images-with-yolo/
14. https://towardsdatascience.com/step-by-step-yolo-model-deployment-in-localhost-using-python-8537e93a1784

## Links for COCO dataset
1. https://github.com/cocodataset/cocoapi/tree/master/PythonAPI
2. https://cocodataset.org/#home
3. https://cocodataset.org/#download
4. https://cocodataset.org/#detection-2020
5. https://cocodataset.org/#format-data
6. https://paperswithcode.com/dataset/coco
7. https://voxel51.com/docs/fiftyone/user_guide/dataset_zoo/index.html
8. https://paperswithcode.com/paper/microsoft-coco-common-objects-in-context