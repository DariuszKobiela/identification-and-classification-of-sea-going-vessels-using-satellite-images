import pandas as pd
import os
import glob

from src.constants import RESULTS_PATH, SLICED_AND_ANNOTATED_ASF_DATA_PATH, STOPFILES, TEST_RATIO, VALIDATION_RATIO


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
# ANSI escape sequences. Python code from the Blender build scripts:
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def calculate_lin_reg_coefficients(x1, y1, x2, y2):
    """
    x is LON (longitude)
    y is LAT (latitude)
    """
    # y = ax + b
    # y1 = a*x1 + b
    # b = y1 - a*x1
    # y2 = a*x2 + y1 - a*x1
    # y2 - y1 = a*x2 - a*x1
    # y2 - y1 = a*(x2-x1)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    return a, b


def categorise_sign_of_time_difference(row):
    if row['time_difference'].days < 0:
        return 0
    return 1


def get_full_data_df(newest=True, given_idx=0, show_logs=False):
    """
    In case when newest=False you have to pass the index
     of the dataframe in the given_idx parameter

    """
    results_list = sorted(os.listdir(RESULTS_PATH), reverse=True)
    idx = 0
    if not newest:
        idx = given_idx
    newest_results_file = results_list[idx]
    full_data_df = pd.read_csv(RESULTS_PATH + newest_results_file, index_col=0)
    if show_logs:
        print(full_data_df)

    return full_data_df


def calculate_px_from_lon2(row, xOrigin, pixelWidth):
    return round((row['LON'] - xOrigin) / pixelWidth)


def calculate_px_from_lat2(row, yOrigin, pixelHeight):
    return round((yOrigin - row['LAT']) / pixelHeight)


def create_train_test_file_splits():
    pictures=list()

    for file in os.listdir(SLICED_AND_ANNOTATED_ASF_DATA_PATH):
        if not file in STOPFILES:
            pictures.append(file)

    print(pictures)
    print()
    total_number_of_pictures = len(pictures)
    print(f"total number_of_folder_pictures: {total_number_of_pictures}")
    print()
    nr_test_pictures = round(TEST_RATIO*total_number_of_pictures)
    print(f"number_of_test_folder_pictures: {nr_test_pictures}")
    nr_train_pictures = total_number_of_pictures - nr_test_pictures
    print(f"number_of_train_folder_pictures: {nr_train_pictures}")
    nr_val_pictures = round(VALIDATION_RATIO*nr_train_pictures)
    print(f"number_of_val_folder_pictures: {nr_val_pictures}")
    print()

    test_folders = pictures[0:nr_test_pictures]
    print(f"test_folders: {test_folders}")
    train_folders = pictures[nr_test_pictures:]
    print(f"train_folders: {train_folders}")
    val_folders = pictures[nr_test_pictures:nr_test_pictures+nr_val_pictures]
    print(f"val_folders: {val_folders}")
    print()

    return train_folders, val_folders, test_folders, total_number_of_pictures, nr_train_pictures, nr_val_pictures, nr_test_pictures


def delete_contents_of_the_given_folders(path, recursive=True):
    # https://pynative.com/python-delete-files-and-directories/
    # recursive=True if also delete the content of the subdirectories
    given_path = path  # FINAL_DATA_PATH
    pattern = given_path + "**/*.*"  # in order to delete all file types - *
    files = glob.glob(pattern, recursive=recursive)  # recursive=True if also delete the content of the subdirectories

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def delete_contents_of_the_given_folders_by_extension(path, recursive=True, extension='.txt'):
    given_path = path  # SLICED_AND_ANNOTATED_ASF_DATA_PATH
    pattern = given_path + "**/*.*"  # in order to delete all file types - *
    files = glob.glob(pattern, recursive=recursive)  # recursive=True if also delete the content of the subdirectories

    for f in files:
        if f.endswith(extension):
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
