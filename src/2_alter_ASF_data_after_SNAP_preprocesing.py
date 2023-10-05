from skimage.exposure import equalize_hist

from src.constants import SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH, NANS_TO_ZEROS_ASF_DATA_PATH, \
    RESCALED_INTENSITY_ASF_DATA_PATH

import os
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
from skimage import exposure
import numpy as np
import cv2
import numpy as np
from PIL import Image
from rasterio.profiles import DefaultGTiffProfile

sentinel_files = os.listdir(SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH)
number_of_sentinel_files = len(sentinel_files)
print(sentinel_files)

for file in sentinel_files:
    input_filepath = SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH + file
    output_filepath1 = NANS_TO_ZEROS_ASF_DATA_PATH + file
    output_filepath2 = RESCALED_INTENSITY_ASF_DATA_PATH + file
    # output_filepath3 = output_filepath2 + '_denoised'

    with rasterio.open(input_filepath) as src_dataset:
    #dataset = rasterio.open(input_filepath)
        print(src_dataset)
        print(src_dataset.meta)
        width, height = src_dataset.width, src_dataset.height

        # image = dataset.read()
        # print(image)
        band1 = src_dataset.read(1)
        band2 = src_dataset.read(2)
        band3 = src_dataset.read(3)
        # change nans to zeros
        band3 = np.nan_to_num(band3, np.nan)
        print(band3.shape)
        # print(np.count(band3))
        print(f"Number of nans: {np.count_nonzero(np.isnan(band3))}")
        print(f"Number of numbers: {np.count_nonzero(~np.isnan(band3))}")
        print(f"Number of zeros: {np.count_nonzero(band3==0)}")

        # band3_geo = band3.profile
        # band3_geo.update({"count": 3})
        dataset_geo = src_dataset.profile
        dataset_geo.update({"count": 3})

        with rasterio.open(output_filepath1, 'w', **dataset_geo) as dst_dataset:
            # I rearanged the band order writting to 2→3→4 instead of 4→3→2
            # dest.write(band1.read(1), 1)
            dst_dataset.write(band1, 1)
            dst_dataset.write(band2, 2)
            dst_dataset.write(band3, 3)

        # dataset.close()
        # print(dataset.closed)

    # Rescale the image (divide by 10000 to convert to [0:1] reflectance
    # img = rasterio.open(output_filepath)
    # image = np.array([img.read(1), img.read(2), img.read(3)])#.transpose(1, 2, 0)
    # p2, p98 = np.percentile(image, (2, 98))
    # image = exposure.rescale_intensity(image, in_range=(p2, p98)) / 100000

    # RESCALING INTENSITY
    with rasterio.open(output_filepath1) as src_dataset:
        # Get a copy of the source dataset's profile. Thus our
        # destination dataset will have the same dimensions,
        # number of bands, data type, and georeferencing as the
        # source dataset.
        kwds = src_dataset.profile

        with rasterio.open(output_filepath2, 'w', **kwds) as dst_dataset:
            # Write data to the destination dataset.
            # Rescale the image (divide by 10000 to convert to [0:1] reflectance
            image = np.array([src_dataset.read(1), src_dataset.read(2), src_dataset.read(3)])
            p2, p98 = np.percentile(image, (2, 98))
            image = exposure.rescale_intensity(image, in_range=(p2, p98)) # * 255  # / 100000
            # image = equalize_hist(image, nbins=256, mask=None) # no sense - just black pixels
            image = image * 255
            dst_dataset.write(image)

    print("works")