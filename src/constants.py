# constants for packages
DESIRED_COLUMNS_WIDTH = 320

# constant paths
DATA_PATH = '../data/'
RAW_AIS_ZIP_DATA_PATH = DATA_PATH + '1_raw_AIS_zip_data/'
RAW_AIS_CSV_DATA_PATH = DATA_PATH + '2_raw_AIS_csv_data/'
RAW_AIS_CSV_DATA_PATH_BATCHTEST = DATA_PATH + '2_raw_AIS_csv_data_batchtest/'
RAW_ASF_DATA_PATH_BATCH0 = DATA_PATH + '3_raw_ASF_data_batch0/'
RAW_ASF_DATA_PATH_BATCH1 = DATA_PATH + '3_raw_ASF_data_batch1/'
RAW_ASF_DATA_PATH_BATCH2 = DATA_PATH + '3_raw_ASF_data_batch2/'
RAW_ASF_DATA_PATH_BATCH3 = DATA_PATH + '3_raw_ASF_data_batch3/'
RAW_ASF_DATA_PATH_BATCHTEST = DATA_PATH + '3_raw_ASF_data_batchtest/'
SNAP_ASF_DATA_AFTER_SUBSETTING = DATA_PATH + '4_SNAP_ASF_data_after_subsetting/'
SNAP_ASF_DATA_AFTER_LANDSEAMASK = DATA_PATH + '4_SNAP_ASF_data_after_LandSeaMask/'
SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH = DATA_PATH + '4_SNAP_preprocessed_ASF_data_2_channels/'
SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH = DATA_PATH + '5_SNAP_preprocessed_ASF_data_3_channels/'
NANS_TO_ZEROS_ASF_DATA_PATH = DATA_PATH + '6_nans_to_zeros_ASF_data/'
RESCALED_INTENSITY_ASF_DATA_PATH = DATA_PATH + '7_rescaled_intensity_ASF_data/'
RGB_PNG_ASF_DATA_PATH = DATA_PATH + '8_rgb_png_ASF_data/'
SLICED_ASF_DATA_PATH = DATA_PATH + '9_sliced_ASF_data/'
PROCESSED_AIS_DATA_PATH = DATA_PATH + '10_processed_AIS_data/'
INTERPOLATED_AIS_DATA_PATH = DATA_PATH + '11_interpolated_AIS_data/'
SLICED_AND_ANNOTATED_ASF_DATA_PATH = DATA_PATH + '12_sliced_and_annotated_ASF_data/'
FINAL_DATA_PATH = DATA_PATH + '13_final_data/'
FINAL_TEST_DATA_PATH = FINAL_DATA_PATH + 'test/'
FINAL_TRAIN_DATA_PATH = FINAL_DATA_PATH + 'train/'
FINAL_VAL_DATA_PATH = FINAL_DATA_PATH + 'val/'

RESULTS_PATH = '../results/'
PLOTS_PATH = '../plots/'
LOGS_PATH = '../logs/'
MAIN_PICTURES_AREAS_PATH = '../main_pictures_areas/'

# constants for AIS data
TIME_WINDOW = 10  # in minutes, +/- how much time to take into consideration between datetime of making the photo
# Use either START, END or MEAN datetime for calculations. MEAN is the preferred option.
USE_END_DATETIME = False
USE_START_DATETIME = False
USE_MEAN_DATETIME = True
AIS_DF_COLUMNS = ['MMSI', 'BaseDateTime', 'LAT', 'LON', 'SOG', 'COG', 'Heading', 'VesselName', 'IMO', 'CallSign',
                  'VesselType', 'Status', 'Length', 'Width', 'Draft', 'Cargo', 'TranscieverClass'
                  ]

# constants for ASF data
CHOSEN_PICTURE_SIZE = 320  # in px # 208 # pictures of example size 1000x1000 will be cutted # USE 320x320 or 416x416
# on each image should be at most 20 ships (best option is to have 10-20 ships on each image)
SHIP_WIDTH_PX = 50  # 50
SHIP_HEIGHT_PX = 50  # 50
OBJECT_CLASS = 0

# constants for train and test sets creation
TEST_RATIO = 0.3
VALIDATION_RATIO = 0
FORMAT_TO_COPY = 'png'
FILES_FORMAT_TO_PROCESS = '.png'
STOPFILES = ['.gitkeep', '.ipynb_checkpoints', 'original_picture.txt', 'original_picture.png.aux.xml',
             'original_picture.png']

# WKT for geometry (well-known-text - WKT) coordinates (can be obtained from SNAP by drawing a polygon)
# Los Angeles coordinates

# port and surroundings - more computationally heavy, but will bring more ships
# LOS_ANGELES_WKT = "POLYGON ((-118.43171789361054 32.405169794041434, -117.06829448255402 32.61853107011102, " \
#                   "-117.3858042991724 34.118662483068455, -118.77733562488359 33.90537103736663, -118.43171789361054 " \
#                   "32.405169794041434))"

# LOS_ANGELES_WKT = "POLYGON ((-117.11507823585683 32.602753306673264, -118.47370300811659 32.39549296144899," \
#                   "-118.81829293218819 33.92546385467516, -118.40461950081445 33.987786188616006,-117.6931648358746 " \
#                   "33.5170868914202, -117.39898762259354 33.29753175138585,-117.24267220094382 32.98967740315516, " \
#                   "-117.23488700738707 32.9615256861061,-117.23488700738707 32.9615256861061, -117.11507823585683 " \
#                   "32.602753306673264))"

# IMAGECS - most proper polygon
# POLYGON ((-1025.142822265625 19071.22857142857, 4416 19071.22857142857,
#    12175.54296875 10349.628962053572, 12964.1142578125 4924.257380022322,
#    -1876.800048828125 5302.771540178572, -2034.5142822265625 14923.342829241072,
#    -2018.7427978515625 14986.428766741072, -2018.7427978515625 14986.428766741072,
#    -1025.142822265625 19071.22857142857))

# just the port - LOS_ANGELES_SMALL_WKT
LOS_ANGELES_WKT = "POLYGON ((-118.3519496977353 33.49095484819047, -117.8921279805309 33.56247074493937, -117.95121096828032 " \
                  "33.83355450820764, -118.41396202220257 33.76185206832226, -118.3519496977353 33.49095484819047))"
