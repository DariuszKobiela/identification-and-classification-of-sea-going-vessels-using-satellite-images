import math
import os

from tqdm import tqdm
from PIL import Image
from PIL import ImageDraw
import pandas as pd
import gdal
import math
import numpy as np
import matplotlib.pyplot as plt

from src.constants import SLICED_AND_ANNOTATED_ASF_DATA_PATH, INTERPOLATED_AIS_DATA_PATH, AIS_DF_COLUMNS, \
    FILES_FORMAT_TO_PROCESS, LOGS_PATH, SHIP_WIDTH_PX, SHIP_HEIGHT_PX, SLICED_ASF_DATA_PATH
from src.utils import delete_contents_of_the_given_folders_by_extension, get_full_data_df, calculate_px_from_lon2, \
    calculate_px_from_lat2


def create_auxiliary_data_df(path, df, asf_file_name, picture_name, area_number):
    df.to_csv(path + asf_file_name + '_' + picture_name + '_' + str(area_number) + '.csv')


def calculate_px_from_Length(row, meters_in_one_pixel):
    if math.isnan(row['Length']):
        return math.nan
    return row['Length'] / meters_in_one_pixel


def calculate_px_from_Width(row, meters_in_one_pixel):
    if math.isnan(row['Width']):
        return math.nan
    return row['Width'] / meters_in_one_pixel


def calculate_Length_ratio(row, image_height):
    if math.isnan(row['Length_px']) or row['Length_px'] == 0:
        return math.nan
    return image_height / row['Length_px']


def calculate_Width_ratio(row, image_width):
    if math.isnan(row['Width_px']) or row['Width_px'] == 0:
        return math.nan
    return image_width / row['Width_px']

delete_contents_of_the_given_folders_by_extension(path=SLICED_AND_ANNOTATED_ASF_DATA_PATH, recursive=True, extension='.txt')
full_data_df = get_full_data_df(newest=True, show_logs=False)
input_ais_path = INTERPOLATED_AIS_DATA_PATH
input_asf_path = SLICED_ASF_DATA_PATH

for index, row in tqdm(full_data_df.iterrows(), total=full_data_df.shape[0], desc="Tagging ASF pictures"):
    asf_file_name = row['asf_file'].strip(".tif") + '.png'
    ais_file_name = 'interpolated_processed_' + row['ais_file']
    ais_file_df = pd.read_csv(input_ais_path + ais_file_name, index_col=0)
    if ais_file_df.empty:
        print('DataFrame is empty!')
        ais_file_df = ais_file_df.join(pd.DataFrame(columns=AIS_DF_COLUMNS))
    else:
        ais_file_df.columns = AIS_DF_COLUMNS  # solution for improper columns names
    print(ais_file_df.head(3))
    print(ais_file_df.columns)
    directory = input_asf_path + asf_file_name
    print(f"File: {index}")
    print(f"ASF file name: {asf_file_name}")
    print(f"AIS file name: {ais_file_name}")
    print(f'directory: {directory}')

    output_filepath = SLICED_AND_ANNOTATED_ASF_DATA_PATH + asf_file_name.strip('png')
    output_dir = output_filepath + '/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    im_data = ais_file_df
    print(im_data.head())

    print(directory)
    im = Image.open(directory)
    # im.show()

    in_ds = gdal.Open(directory)
    image_width = in_ds.RasterXSize
    image_height = in_ds.RasterYSize
    geo_transform = in_ds.GetGeoTransform()
    xOrigin = geo_transform[0]  # NEEDED
    yOrigin = geo_transform[3]  # NEEDED
    pixelWidth = geo_transform[1]  # NEEDED
    pixelHeight = -geo_transform[5]  # NEEDED
    print(image_width, image_height, xOrigin, yOrigin, pixelWidth, pixelHeight)

    minx = geo_transform[0]  # minLON
    miny = geo_transform[3] + image_width * geo_transform[4] + image_height * geo_transform[5]  # minLAT
    maxx = geo_transform[0] + image_width * geo_transform[1] + image_height * geo_transform[2]  # maxLON
    maxy = geo_transform[3]  # maxLAT

    condition1 = (im_data.LAT > miny) & (im_data.LAT < maxy)
    # condition for latitude: between -157.0894 and -154.4233
    condition2 = (im_data.LON > minx) & (im_data.LON < maxx)
    # final dataframe
    target_area = im_data[condition1 & condition2].copy().reset_index(drop=True)

    im_data = target_area

    # 1 pixel is about 11.5 meters
    METERS_IN_ONE_PIXEL = 11.5
    for _, row in im_data.iterrows():
        im_data['LONpx_X2'] = im_data.apply(
            lambda row: calculate_px_from_lon2(row, xOrigin, pixelWidth), axis=1)
        im_data['LATpx_Y2'] = im_data.apply(
            lambda row: calculate_px_from_lat2(row, yOrigin, pixelHeight), axis=1)
        im_data['Length_px'] = im_data.apply(
            lambda row: calculate_px_from_Length(row, METERS_IN_ONE_PIXEL), axis=1)
        im_data['Width_px'] = im_data.apply(
            lambda row: calculate_px_from_Width(row, METERS_IN_ONE_PIXEL), axis=1)
    #     im_data['Length_px_ratio'] = im_data.apply(
    #         lambda row: calculate_Length_ratio(row, image_height), axis=1)
    #     im_data['Width_px_ratio'] = im_data.apply(
    #         lambda row: calculate_Width_ratio(row, image_width), axis=1)

    try:
        CHOSEN_SLICING_SIZE_PX = 60
        NEW_IMAGE_LENGTH_RATIO_SCALER = np.longdouble(image_height / (2 * CHOSEN_SLICING_SIZE_PX))
        NEW_IMAGE_WIDTH_RATIO_SCALER = np.longdouble(image_width / (2 * CHOSEN_SLICING_SIZE_PX))
        # print(image_width, image_height)
        # print(NEW_IMAGE_LENGTH_RATIO_SCALER, NEW_IMAGE_WIDTH_RATIO_SCALER)
        # print()
        CROP_MARGIN_PX = 0  # -20
        FINAL_RECTANGLE_MARGIN_PX = 2
        subset_number = 0
        for index, row in im_data.iterrows():
            subset_number += 1
            # print("---------------------")
            # print("NEW PICTURE")
            lon_x_px = row['LONpx_X2']
            lat_y_px = row['LATpx_Y2']
            # print(f"Ship center current coordinates: {lon_x_px, lat_y_px}")
            left, upper = lon_x_px - CHOSEN_SLICING_SIZE_PX, lat_y_px - CHOSEN_SLICING_SIZE_PX
            right, lower = lon_x_px + CHOSEN_SLICING_SIZE_PX, lat_y_px + CHOSEN_SLICING_SIZE_PX
            # print(f"Ship left upper corner current coordinates: {left, upper}")
            # print(f"Ship right lower current coordinates: {right, lower}")
            im_cropped = im.crop((left, upper, right, lower))
            # print(f"Cropped image size: {im_cropped.size}")
            # im_cropped.show()

            #####################################
            # CHANGE BLACK PIXELS INTO MEAN PIXEL VALUE FROM THE PICTURE
            #####################################
            # Threshold just for pixels change
            threshold_level = 1  # black is 0,0,0
            im_gray = im_cropped.convert('L')
            im_gray = im_gray.point(lambda p: 255 if p > threshold_level else 0)
            im_gray = im_gray.convert('1')
            # display(im_gray)
            array = np.array(im_gray).astype(int)
            # print(array)
            coords_black = np.column_stack(np.where(array < threshold_level))
            # print(f"black pixels cordinates: {coords_black}")
            # print(f"array shape: {coords_black.shape}")

            pixels = list(im_cropped.getdata())
            filtered_pixels = filter(lambda pixel: pixel != (0, 0, 0), pixels)
            no_black_pixels_df = pd.DataFrame(filtered_pixels, columns=['R', 'G', 'B']).astype(
                {'R': int, 'G': int, 'B': int})
            # display(no_black_pixels_df)
            if no_black_pixels_df.empty:
                mean_r, mean_g, mean_b = 0, 0, 0
            else:
                mean_r = no_black_pixels_df['R'].mean()
                mean_g = no_black_pixels_df['G'].mean()
                mean_b = no_black_pixels_df['B'].mean()
                mean_r, mean_g, mean_b = round(mean_r), round(mean_g), round(mean_b)
            mean_pixel_value_from_image = [mean_r, mean_g, mean_b]
            # print(f"mean_pixel_value_from_image: {mean_pixel_value_from_image}")

            for a in range(coords_black.shape[0]):
                x = coords_black[a][0]
                y = coords_black[a][1]
                im_cropped.putpixel((y, x), (mean_r, mean_g, mean_b))
            # print()
            #####################################
            # GETTING IMAGE CENTER
            #####################################
            center_x = (right - left) / 2
            center_y = (lower - upper) / 2
            # print(f"Ship center current coordinates: {center_x, center_y}")
            r, g, b = im_cropped.getpixel((center_x, center_y))
            # print(f"RGB = {r, g, b}")
            if (r, g, b) == (0, 0, 0):
                print("Black mask - not tagging")
                print()
                continue
            elif math.isnan(row['Length']):  # or math.isnan(row['Width'])
                print("Missing data about Length - not tagging")  # or Width
                print()
                continue
            elif row['Length'] < 20:
                print(f"Ship is too small to be seen ({row['Length']} m) - not tagging")
                print()
                continue
            # print(f"Ship Length: ({row['Length']} m), Width: ({row['Width']} m)")

            crop_size_x, crop_size_y = 50, 50
            # print(crop_size_x, crop_size_y)

            left, upper = center_x - (crop_size_x / 2) + CROP_MARGIN_PX, center_y - (crop_size_y / 2) + CROP_MARGIN_PX
            right, lower = center_x + (crop_size_x / 2) + CROP_MARGIN_PX, center_y + (crop_size_y / 2) + CROP_MARGIN_PX
            # ADDITIONAL DRAW
            # dr = ImageDraw.Draw(im_cropped)
            # dr.rectangle(((left, upper), (right, lower)), outline="black")
            # display(im_cropped)
            ############################
            #### TURN TO GRAYSCALE
            ############################
            threshold = 200  # 200 is the best
            im_gray = im_cropped.convert('L')
            # Threshold
            im_gray = im_gray.point(lambda p: 255 if p > threshold else 0)
            # To mono
            im_gray = im_gray.convert('1')
            array = np.array(im_gray).astype(int)
            # print(array)

            width_series = pd.Series(np.sum(array, axis=0))
            width_max = width_series.max()
            # print(f"Maximum x-axis pixel: {width_max}")
            LENGTH_SUM_THRESHOLD = 5
            if width_max < LENGTH_SUM_THRESHOLD:
                print(f"Cumulated axis=0 sum px < THRESHOLD ({width_max} < {LENGTH_SUM_THRESHOLD}) - not tagging")
                print()
                continue
            # print(f"Maximum y-axis sum: {width_max}")
            width_max_pixel = width_series[width_series == width_max].index[0]
            width_max_pixel_first = width_series[width_series > 0].index[0]
            width_max_pixel_last = width_series[width_series > 0].index[-1]
            width_center_pixel = round((width_max_pixel_first + width_max_pixel_last) / 2)
            # print(f"Maximum x-axis pixel: from {width_max_pixel_first} to {width_max_pixel_last}")
            # print(f"Maximum x-axis pixel: {width_max_pixel}")
            # print(f"Center x-axis pixel: {width_center_pixel}")
            # print(f"Maximum y-axis pixel: {width_max_pixel}")

            length_series = pd.Series(np.sum(array, axis=1))
            length_max = length_series.max()
            # print(f"Maximum y-axis pixel: {length_max}")
            if length_max < LENGTH_SUM_THRESHOLD:
                print(f"Cumulated axis=1 sum px < THRESHOLD ({length_max} < {LENGTH_SUM_THRESHOLD}) - not tagging")
                print()
                continue
            width_series.plot(label='axis=0')
            length_series.plot(label='axis=1', xlabel='pixel value', ylabel='cumulated sum')
            # print(f"Maximum x-axis sum: {length_max}")
            length_max_pixel = length_series[length_series == length_max].index[0]
            length_max_pixel_first = length_series[length_series > 0].index[0]
            length_max_pixel_last = length_series[length_series > 0].index[-1]
            length_center_pixel = round((length_max_pixel_first + length_max_pixel_last) / 2)
            # print(f"Maximum x-axis pixel: from {length_max_pixel_first} to {length_max_pixel_last}")
            # print(f"Maximum x-axis pixel: {length_max_pixel}")
            # print(f"Center x-axis pixel: {length_center_pixel}")
            plt.legend()

            # print(f"Ship center current coordinates: {length_center_pixel, width_center_pixel}")
            left, upper = width_center_pixel - (crop_size_x / 2) + CROP_MARGIN_PX, length_center_pixel - (
                        crop_size_y / 2) + CROP_MARGIN_PX
            right, lower = width_center_pixel + (crop_size_x / 2) + CROP_MARGIN_PX, length_center_pixel + (
                        crop_size_y / 2) + CROP_MARGIN_PX
            # ADDITIONAL DRAW
            # dr = ImageDraw.Draw(im_cropped)
            # dr.rectangle(((left, upper), (right, lower)), outline="blue")

            # print(f"Ship center current coordinates: {width_center_pixel, length_center_pixel}")
            tagging_length = length_max_pixel_last - length_max_pixel_first
            tagging_width = width_max_pixel_last - width_max_pixel_first
            # print(f"tagging_length = {tagging_width}, tagging_width = {tagging_length}")
            # IF THERE IS MORE THAN 1 SHIP IN THE PICTURE
            if tagging_length > SHIP_HEIGHT_PX or tagging_width > SHIP_WIDTH_PX:
                print(f"More than 1 ship on the picture - TEMPORARILY not tagging")
                print()
                # TODO later: find a way to tag more than 1 ship
                #         tagging_length = SHIP_HEIGHT_PX
                #         tagging_width = SHIP_WIDTH_PX
                continue
            # print(f"tagging_length = {tagging_width}, tagging_width = {tagging_length}")
            left, upper = width_center_pixel - (tagging_width / 2) - FINAL_RECTANGLE_MARGIN_PX, length_center_pixel - (
                        tagging_length / 2) - FINAL_RECTANGLE_MARGIN_PX
            right, lower = width_center_pixel + (tagging_width / 2) + FINAL_RECTANGLE_MARGIN_PX, length_center_pixel + (
                        tagging_length / 2) + FINAL_RECTANGLE_MARGIN_PX
            # print(f"x0,y0 = {left, upper}, x1,y1 = {right, lower}")
            # ADDITIONAL DRAW
            # dr = ImageDraw.Draw(im_cropped)
            # dr.rectangle(((left, upper), (right, lower)), outline="purple")
            # im_cropped.show()
            # SAVE IMAGE
            im_cropped.save(output_dir + f'subset{subset_number}.png')

            # TAGGING
            object_class = 0
            # ONLY 2 classes makes sense
            # # CLASSES CUTS = [135m]
            # if row['Length'] < 135:
            #     object_class = 0  # small ship
            # else:
            #     object_class = 1  # big ship

            # # CLASSES CUTS = [110m, 265m]
            # if row['Length'] < 111:
            #     object_class = 0  # small ship
            # elif row['Length'] < 266:
            #     object_class = 1  # medium ship
            # else:
            #     object_class = 2  # big ship

            # CLASSES CUTS = [12m, 17m, 26m, 230m]
            # CLASSES NEW CUTS = [50m, 150m, 250m, 310m]
            # CLASSES NEWEST CUTS = [135m, 220m, 275m, 325m]
            if row['Length'] < 135:
                object_class = 0
            elif row['Length'] < 220:
                object_class = 1
            elif row['Length'] < 275:
                object_class = 2
            elif row['Length'] < 325:
                object_class = 3
            else:
                object_class = 4

            tagging_file = output_dir + f'subset{subset_number}.txt'
            file_object = open(tagging_file, 'a')
            image_width, image_height = im_cropped.size
            # OBJECT_CLASS, SHIP_WIDTH_PX, SHIP_HEIGHT_PX
            # print("before normalization")
            # print("LONpx_X2", row['LONpx_X2'])
            # print("LATpx_Y2", row['LATpx_Y2'])
            # TODO: check if width and length are in proper order
            X_CENTER_AXIS_VALUE = width_center_pixel  # row['LONpx_X2']
            Y_CENTER_AXIS_VALUE = length_center_pixel  # row['LATpx_Y2']
            # print(OBJECT_CLASS, X_CENTER_AXIS_VALUE, Y_CENTER_AXIS_VALUE, SHIP_WIDTH_PX, SHIP_HEIGHT_PX)
            # print("after normalization")
            # X_CENTER_AXIS_VALUE = (X_CENTER_AXIS_VALUE + SHIP_WIDTH_PX/2) / image_width
            # Y_CENTER_AXIS_VALUE = (Y_CENTER_AXIS_VALUE + SHIP_HEIGHT_PX/2) / image_height
            X_CENTER_AXIS_VALUE = X_CENTER_AXIS_VALUE / image_width
            Y_CENTER_AXIS_VALUE = Y_CENTER_AXIS_VALUE / image_height
            SHIP_WIDTH_normalized = tagging_width / image_width
            SHIP_HEIGHT_normalized = tagging_length / image_height
            # print(OBJECT_CLASS, X_CENTER_AXIS_VALUE, Y_CENTER_AXIS_VALUE, SHIP_WIDTH_normalized, SHIP_HEIGHT_normalized)
            string_to_write = f"{object_class} {X_CENTER_AXIS_VALUE} {Y_CENTER_AXIS_VALUE} {SHIP_WIDTH_normalized} {SHIP_HEIGHT_normalized}\n"
            file_object.write(string_to_write)
            # Close the file
            file_object.close()

            # plt.show()
            # TODO: TODELETE
            # if index > 1:
            #     break
    except:
        print("IndexError: image index out of range")
        continue
