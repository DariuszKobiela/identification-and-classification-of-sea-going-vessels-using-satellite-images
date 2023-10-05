import os
import shutil

from src.constants import SLICED_ASF_DATA_PATH, RGB_PNG_ASF_DATA_PATH

# sliced_ASF_files = [file for file in os.listdir(SLICED_ASF_DATA_PATH) if file.endswith('.png')]
sliced_ASF_files = [file for file in os.listdir(RGB_PNG_ASF_DATA_PATH) if file.endswith('.xml')]
number_of_sentinel_files = len(sliced_ASF_files)
print(sliced_ASF_files)

source_path = RGB_PNG_ASF_DATA_PATH
destination_path = SLICED_ASF_DATA_PATH

for file in sliced_ASF_files:
    src = source_path + '/' + file
    # print(f"src: {src}")
    dst = destination_path + '/' + file
    # print(f"dst: {dst}")
    shutil.copy(src, dst)
    # dirs_exist_ok = True parameter will overwrite the already existing data of the same name without raising error.