
from src.constants import RESCALED_INTENSITY_ASF_DATA_PATH, RGB_PNG_ASF_DATA_PATH

import os
from osgeo import gdal
from tqdm import tqdm
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
from skimage import exposure
import numpy as np
import cv2
import numpy as np
from PIL import Image
from rasterio.profiles import DefaultGTiffProfile


sentinel_files = os.listdir(RESCALED_INTENSITY_ASF_DATA_PATH)
number_of_sentinel_files = len(sentinel_files)
print(sentinel_files)
# # TODO: delete next line:
# sentinel_files = sentinel_files[-1:]
# print(sentinel_files)
print(type(sentinel_files))

for file in tqdm(sentinel_files):
    input_filepath = RESCALED_INTENSITY_ASF_DATA_PATH + file
    print(input_filepath)
    output_filepath = RGB_PNG_ASF_DATA_PATH + file.strip('tif') + 'png'

    in_ds = gdal.Open(input_filepath)
    print(in_ds)
    # data = in_ds.ReadAsArray()
    # print(data)
    options_list = [
                '-ot Byte',
                '-of PNG',
                '-b 1',
                '-b 2',
                '-b 3',
                '-scale'
            ]
    options_string = " ".join(options_list)
    kwargs = {
        'format': 'PNG',  # JPEG, PNG, GTIFF
        'options': options_string
    }
    out_ds = gdal.Translate(destName=output_filepath,  # .tif, .png
                            srcDS=in_ds,
                            **kwargs)
    del in_ds
    del out_ds
