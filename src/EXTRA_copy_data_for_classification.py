import os
import shutil

from src.constants import FINAL_DATA_PATH, FOR_CLASSIFICATION_DATA_PATH


def copy_pictures_and_labels_for_classification (source_path, source_images_folders, destination_path, counter=0):
    source_path = source_path
    folder = source_images_folders
    destination_path = destination_path
    labels_path = source_path + folder + '/' + 'labels/'
    images_path = source_path + folder + '/' + 'images/'

    # labels
    labels = os.listdir(labels_path)
    for file in labels:
        src = labels_path + file
        # print(f"src: {src}")
        dst = destination_path
        # print(f"dst: {dst}")
        shutil.copy(src, dst)

    # images
    image_counter = 0
    images = os.listdir(images_path)
    for file in images:
        src = images_path + file
        # print(f"src: {src}")
        dst = destination_path
        # print(f"dst: {dst}")
        shutil.copy(src, dst)
        image_counter += 1

    return image_counter

START_COUNTER = 0
counter = copy_pictures_and_labels_for_classification(source_path=FINAL_DATA_PATH,
                                                       source_images_folders='train',
                                                       destination_path=FOR_CLASSIFICATION_DATA_PATH,
                                                       counter=START_COUNTER)
print(f"Images copied: {counter}")