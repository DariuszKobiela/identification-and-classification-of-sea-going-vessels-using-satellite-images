from datetime import datetime

import pandas as pd
from osgeo import gdal
import math
import os
import glob
from PIL import Image  # PIL library supports only TIF format but not newer TIFF
import numpy as np
import shutil
from tqdm import tqdm

from src.constants import SLICED_AND_ANNOTATED_ASF_DATA_PATH, FINAL_DATA_PATH, FORMAT_TO_COPY, FINAL_TEST_DATA_PATH, \
    FINAL_TRAIN_DATA_PATH, FINAL_VAL_DATA_PATH, DESIRED_COLUMNS_WIDTH, LOGS_PATH
from src.utils import create_train_test_file_splits, delete_contents_of_the_given_folders

pd.set_option('display.width', DESIRED_COLUMNS_WIDTH)
pd.set_option('display.max_columns', 20)
# np.set_printoption(linewidth=desired_width)


def copy_pictures_and_labels(source_path, source_images_folders, destination_path_images, destination_path_labels,
                             destination_format, counter=0, dataset_description='some'):
    source_path = source_path
    source_images_folders = source_images_folders
    destination_path_images = destination_path_images
    destination_path_labels = destination_path_labels
    destination_format = destination_format
    image_counter = counter
    labels_counter = counter
    print(destination_path_labels)

    for folder in tqdm(source_images_folders, desc=f"Creating {dataset_description} sets"):
        # print()
        # print(folder)
        # choose only files with txt annotations
        # print(os.listdir(source_path + folder))
        # print()
        labels = list()
        images = list()
        for file in os.listdir(source_path + folder):
            if file.endswith(".txt") and not file.endswith("original_picture.txt"):
                labels.append(file)
                image_file = file.replace(".txt", ".png")
                images.append(image_file)
        # print(f"images: {images}")
        # print(f"labels: {labels}")
        # labels
        for file in labels:
            src = source_path + '/' + folder + '/' + file
            # print(f"src: {src}")
            dst = destination_path_labels + str(labels_counter) + '.txt'  # folder + file
            # print(f"dst: {dst}")
            shutil.copy(src, dst)
            labels_counter += 1
        # pictures
        counter = counter
        for file in images:
            src = source_path + '/' + folder + '/' + file
            # print(f"src: {src}")
            dst = destination_path_images + str(image_counter) + '.' + destination_format  # folder + file
            # print(f"dst: {dst}")
            shutil.copy(src, dst)
            image_counter += 1

    return image_counter


def count_number_of_annotations(dataset='train', path=FINAL_TRAIN_DATA_PATH):
    annotation_files = os.listdir(path + 'labels')
    total_counter = 0
    for file in annotation_files:
        with open(path + 'labels/' + file, 'r') as fp:
            for count, line in enumerate(fp):
                pass
        total_counter += count + 1
    print(f'Total number of {dataset} annotated ships: {total_counter}')

    return total_counter

train_folders, val_folders, test_folders, total_number_of_folders, nr_train_folders, nr_val_folders, nr_test_folders = create_train_test_file_splits()

# clear file structure
delete_contents_of_the_given_folders(FINAL_DATA_PATH)

# start counting
START_COUNTER = 0

# TEST PICTURES
dataset_description = 'TEST'
test_counter = copy_pictures_and_labels(source_path=SLICED_AND_ANNOTATED_ASF_DATA_PATH,
                                        source_images_folders=test_folders,
                                        destination_path_images=FINAL_TEST_DATA_PATH + 'images/',
                                        destination_path_labels=FINAL_TEST_DATA_PATH + 'labels/',
                                        destination_format=FORMAT_TO_COPY,
                                        counter=START_COUNTER,
                                        dataset_description=dataset_description)
print(f"{dataset_description} images counter: {test_counter}")

# TRAIN PICTURES
dataset_description = 'TRAIN'
train_counter = copy_pictures_and_labels(source_path=SLICED_AND_ANNOTATED_ASF_DATA_PATH,
                                         source_images_folders=train_folders,
                                         destination_path_images=FINAL_TRAIN_DATA_PATH + 'images/',
                                         destination_path_labels=FINAL_TRAIN_DATA_PATH + 'labels/',
                                         destination_format=FORMAT_TO_COPY,
                                         counter=START_COUNTER,
                                         dataset_description=dataset_description)
print(f"{dataset_description} images counter: {train_counter}")

# VALIDATION PICTURES
dataset_description = 'VAL'
val_counter = copy_pictures_and_labels(source_path=SLICED_AND_ANNOTATED_ASF_DATA_PATH,
                                       source_images_folders=val_folders,
                                       destination_path_images=FINAL_VAL_DATA_PATH + 'images/',
                                       destination_path_labels=FINAL_VAL_DATA_PATH + 'labels/',
                                       destination_format=FORMAT_TO_COPY,
                                       counter=START_COUNTER,
                                       dataset_description=dataset_description)
print(f"{dataset_description} images counter: {val_counter}")

total_images_counter = train_counter + test_counter
print(f"TOTAL images counter: {total_images_counter}")

train_annot = count_number_of_annotations(dataset='train', path=FINAL_TRAIN_DATA_PATH)
val_annot = count_number_of_annotations(dataset='val', path=FINAL_VAL_DATA_PATH)
test_annot = count_number_of_annotations(dataset='test', path=FINAL_TEST_DATA_PATH)
total_annot = train_annot + test_annot
print(f'Total number of annotated ships: {total_annot}')

datasets_dict = {
    'total_folders': [total_number_of_folders],
    'train_folders': [nr_train_folders],
    'val_folders': [nr_val_folders],
    'test_folders': [nr_test_folders],
    'total_pictures': [total_images_counter],
    'train_pictures': [train_counter],
    'val_pictures': [val_counter],
    'test_pictures': [test_counter],
    'total_ships': [total_annot],
    'train_ships': [train_annot],
    'val_ships': [val_annot],
    'test_ships': [test_annot]

}
df = pd.DataFrame.from_dict(datasets_dict)
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
df.to_csv(LOGS_PATH + current_datetime + '_train_val_test_splits.csv')
print(df)
