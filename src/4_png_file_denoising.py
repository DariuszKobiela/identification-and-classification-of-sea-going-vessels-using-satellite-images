
from src.constants import RGB_PNG_ASF_DATA_PATH, SLICED_ASF_DATA_PATH

import os
import rasterio
import cv2
from tqdm import tqdm

sentinel_files = [file for file in os.listdir(RGB_PNG_ASF_DATA_PATH) if file.endswith('.png')]
number_of_sentinel_files = len(sentinel_files)
print(sentinel_files)

for file in tqdm(sentinel_files):
    input_filepath = RGB_PNG_ASF_DATA_PATH + file
    # output_filepath1 = RGB_PNG_ASF_DATA_PATH + 'denoised_' + file
    output_filepath1 = SLICED_ASF_DATA_PATH + file

    # IMAGE DENOISING
    img = cv2.imread(input_filepath)
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    cv2.imwrite(output_filepath1, dst)