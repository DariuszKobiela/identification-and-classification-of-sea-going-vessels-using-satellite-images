from constants import FOR_CLASSIFICATION_DATA_PATH, CUTTED_FOR_CLASSIFICATION_DATA_PATH

import os
import pandas as pd

source_path = FOR_CLASSIFICATION_DATA_PATH
columns = ['class_id', 'x', 'y', 'width', 'height']

images_and_labels = os.listdir(source_path)
print(images_and_labels)

images_list = []
for item in images_and_labels:
    if item.endswith(".png"):
        images_list.append(item)
print(images_list)

# after having the list of all pictures
for image in images_list:
    image_id = image.strip(".png")
    image_label = image_id + ".txt"
    print(image_label)
    tags_df = pd.read_csv(source_path + image_label, sep=" ", names=columns)
    print(tags_df)
    for index, row in tags_df.iterrows():
        print(row)

    break
