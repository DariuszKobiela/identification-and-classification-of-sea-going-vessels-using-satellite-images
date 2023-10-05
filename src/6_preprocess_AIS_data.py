# STEPS
# From list of the ASF Sentinel-1 images extract info about datetime and date of making the photo. Extract also image LAT and LON along with the image width and height in pixels.
# From list of the AIS data extract info about the date of data.
# Join both dataframes (merge them).

import pandas as pd
import os
import re
from datetime import datetime, timedelta
from osgeo import gdal
from tqdm import tqdm

from constants import RESCALED_INTENSITY_ASF_DATA_PATH, RAW_AIS_CSV_DATA_PATH, \
    RESULTS_PATH, PROCESSED_AIS_DATA_PATH, INTERPOLATED_AIS_DATA_PATH, AIS_DF_COLUMNS, RAW_AIS_CSV_DATA_PATH_BATCHTEST
from constants import USE_MEAN_DATETIME, USE_END_DATETIME, USE_START_DATETIME, TIME_WINDOW
from src.utils import calculate_lin_reg_coefficients, categorise_sign_of_time_difference

# https://stackoverflow.com/questions/66336670/returning-a-copy-versus-a-view-warning-when-using-python-pandas-dataframe
pd.options.mode.chained_assignment = None  # default='warn', in order not to show warnings

# TODO: error with change of columns name from TranscieverClass to TransceiverClass after 2021-03-30
# TODO: error if "processed_AIS_data" is empty, even no header


def list_asf_files(show_logs=False, input_path=RESCALED_INTENSITY_ASF_DATA_PATH):
    asf_files_list = os.listdir(input_path) # [input_path]
    asf_files_list = [filename for filename in asf_files_list if filename.endswith('.tif')]
    # for element in asf_files_list:
    #     if not element.endswith('.tif'):
    #         asf_files_list.remove(element)
    if show_logs:
        print(asf_files_list)

    return asf_files_list


def calculate_asf_image_features(show_logs=False, input_path=RESCALED_INTENSITY_ASF_DATA_PATH):
    # Calculate image features
    asf_images_tuples_list = list()

    for asf_file in tqdm(asf_files_list, desc="Calculating ASF image features"):
        datetime_counter = 0
        asf_file_splitted = asf_file.split('_')
        if show_logs:
            print(f"ASF file: {asf_file}")
            print(f"ASF file splitted: {asf_file_splitted}")
        datetime_pattern = re.compile("[A-Za-z0-9]+")
        for element in asf_file_splitted:
            if len(element) == 15:
                if datetime_pattern.match(element):
                    datetime_counter += 1
                    # print(element)
                    # read datetimes of making photos
                    IMAGE_DATE = element[0:4] + '-' + element[4:6] + '-' + element[6:8]
                    IMAGE_DATETIME = IMAGE_DATE + ' ' + element[9:11] + ':' + element[11:13] + ':' + element[13:15]
                    # print(IMAGE_DATETIME)
                    if datetime_counter == 1:
                        # START_DATETIME = IMAGE_DATETIME
                        START_DATETIME = pd.Timestamp(IMAGE_DATETIME)
                        # START_DATETIME = datetime.strptime(IMAGE_DATETIME, '%Y-%m-%d %H:%M:%S')
                    elif datetime_counter == 2:
                        END_DATETIME = pd.Timestamp(IMAGE_DATETIME)
                        # END_DATETIME = datetime.strptime(IMAGE_DATETIME, '%Y-%m-%d %H:%M:%S')
                        # print(f"START DATETIME: {START_DATETIME}")
                        # START DATETIME: 2021-02-04 01:58:12
                        # print(f"START DATETIME: {datetime.strptime(START_DATETIME, '%Y-%m-%d %H:%M:%S')}")
                        MEAN_DATETIME = pd.Timestamp((START_DATETIME.value + END_DATETIME.value) / 2.0)
                        if show_logs:
                            print(f"START DATETIME: {START_DATETIME}")
                            print(f"END DATETIME: {END_DATETIME}")
                            print(f"MEAN DATETIME: {MEAN_DATETIME}")
                        break  # this break is here purposedly and is necessary

        if USE_MEAN_DATETIME:
            IMAGE_DATETIME = MEAN_DATETIME
        elif USE_START_DATETIME:
            IMAGE_DATETIME = START_DATETIME
        elif USE_END_DATETIME:
            IMAGE_DATETIME = END_DATETIME

        # LAT and LON calculations
        ds = gdal.Open(input_path + '/' + asf_file)
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        minx = gt[0]
        miny = gt[3] + width * gt[4] + height * gt[5]
        maxx = gt[0] + width * gt[1] + height * gt[2]
        maxy = gt[3]
        # final tuple
        asf_images_tuples_list.append((asf_file, IMAGE_DATETIME, IMAGE_DATE, minx, miny, maxx, maxy, width, height))

    asf_df = pd.DataFrame(asf_images_tuples_list,
                          columns=['asf_file', 'image_datetime', 'date', 'minLON', 'minLAT', 'maxLON', 'maxLAT',
                                   'widthpx',
                                   'heightpx'])
    asf_df.image_datetime = pd.to_datetime(asf_df.image_datetime)
    # boundaries +/- 10 minut
    asf_df['datetime_lower'] = asf_df['image_datetime'] - timedelta(hours=0, minutes=TIME_WINDOW, seconds=0)
    asf_df['datetime_upper'] = asf_df['image_datetime'] + timedelta(hours=0, minutes=TIME_WINDOW, seconds=0)
    if show_logs:
        print(asf_df)

    return asf_df


def create_ais_df(show_logs=False, input_path=RAW_AIS_CSV_DATA_PATH):
    ais_files_list = os.listdir(input_path)
    ais_files_list = [filename for filename in ais_files_list if filename.endswith('.csv')]
    # for element in ais_files_list:
    #     if not element.endswith('.csv'):
    #         ais_files_list.remove(element)
    if show_logs:
        print(ais_files_list)

    ais_images_tuples_list = list()

    for ais_file in tqdm(ais_files_list, desc="Creating AIS dataframes"):
        # print(ais_file)
        ais_file_splitted = ais_file.split('_')
        # print(ais_file_splitted)
        AIS_FILE_DATE = ais_file_splitted[1] + '-' + ais_file_splitted[2] + '-' + ais_file_splitted[3].split('.')[0]
        # print(AIS_FILE_DATE)
        ais_images_tuples_list.append((ais_file, AIS_FILE_DATE))

    ais_df = pd.DataFrame(ais_images_tuples_list, columns=['ais_file', 'date'])
    if show_logs:
        print(ais_df)

    return ais_df

def create_full_data_df(asf_df, ais_df, save=True, show_logs=False):
    full_data_df = asf_df.merge(ais_df, on='date')
    if show_logs:
        print(full_data_df)
    if save:
        # save your work
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # print(current_datetime)
        full_data_df.to_csv(RESULTS_PATH + current_datetime + '_full_data_df.csv')

    return full_data_df

def restrict_data_by_given_conditions(full_data_df, save=True, show_logs=False, input_path=RAW_AIS_CSV_DATA_PATH, output_path=PROCESSED_AIS_DATA_PATH):
    # WORK ON THE PREPARED DATAFRAME
    # Restrict data by the given conditions
    # newest_results_file = "2023-01-13_00-58-29_full_data_df.csv"
    # full_data_df = pd.read_csv(results_directory + newest_results_file, index_col=0)
    # full_data_df
    for index, row in tqdm(full_data_df.iterrows(), total=full_data_df.shape[0], desc="Restricting AIS data by given conditions"):
        # TODO: if AIS file already in '4_processed_AIS_data" folder, then ommit loading and saving again
        if show_logs:
            print(row['ais_file'])
        file_path = input_path + '/' + str(row['ais_file'])
        ais_full_data = pd.read_csv(file_path)
        ais_full_data.columns = AIS_DF_COLUMNS
        # print(ais_full_data.head(10))
        # condition for latitude: between 19.193 and 21.1203
        condition1 = (ais_full_data.LAT > row['minLAT']) & (ais_full_data.LAT < row['maxLAT'])
        # condition for latitude: between -157.0894 and -154.4233
        condition2 = (ais_full_data.LON > row['minLON']) & (ais_full_data.LON < row['maxLON'])
        # final dataframe
        target_area = ais_full_data[condition1 & condition2]
        # display(target_area)
        # target area contains 5542 rows × 17 columns
        target_area.reset_index(drop=True, inplace=True)
        target_area.BaseDateTime = pd.to_datetime(target_area.BaseDateTime)
        # target_area.loc['BaseDateTime'] = pd.to_datetime(target_area.loc['BaseDateTime'])
        # display(target_area)
        # filter by date: from 2021-01-05 00:00:00 to 2021-01-05 23:59:59
        DATE1 = row['datetime_lower']
        DATE2 = row['datetime_upper']
        target_area_and_time = target_area[(target_area.BaseDateTime >= DATE1) & (target_area.BaseDateTime <= DATE2)]
        target_area_and_time.reset_index(drop=True, inplace=True)
        target_area_and_time.sort_values(by='BaseDateTime',
                                         axis=0,
                                         ascending=True,
                                         inplace=True,
                                         kind='quicksort',
                                         na_position='last',
                                         ignore_index=True)
        # display(target_area_and_time)

        if save:
            saving_name = 'processed_' + row['ais_file']
            target_area_and_time.to_csv(output_path + '/' + saving_name)
        # all data is from 4th January 2021

    # display(target_area_and_time.head(10))

    # Use algorithm to predict the best value from the TIME_WINDOW.
    #full_data_df = pd.read_csv(results_directory + "2022-10-15_16-37-28_full_data_df.csv", index_col=0)
    full_data_df['processed_ais_file'] = 'processed_' + full_data_df['ais_file']
    if show_logs:
        print(full_data_df)

    return full_data_df


def interpolate_ais_data(full_data_df, save=True, show_logs=False, input_path=PROCESSED_AIS_DATA_PATH, output_path=INTERPOLATED_AIS_DATA_PATH):
    # The way of choosing ships (+/- time)
    for index, row in tqdm(full_data_df.iterrows(), total=full_data_df.shape[0], desc="Interpolating AIS data"):
        image_datetime = pd.to_datetime(row['image_datetime'])
        if show_logs:
            print("file: ", index)
            print(row['processed_ais_file'])
            print('image_datetime:', image_datetime)
        file_path = input_path + '/' + str(row['processed_ais_file'])
        processed_ais_full_data = pd.read_csv(file_path, index_col=0)
        processed_ais_full_data.BaseDateTime = pd.to_datetime(processed_ais_full_data.BaseDateTime)
        # display(processed_ais_full_data)

        # for every ship
        list_of_unique_ships = processed_ais_full_data.MMSI.unique()
        # display(list_of_unique_ships)

        list_of_df_dicts_after_lin_reg = list()
        for ship in list_of_unique_ships:
            if show_logs:
                print('ship: ', ship)
            working_df = processed_ais_full_data[processed_ais_full_data.MMSI == ship]
            working_df.reset_index(drop=True, inplace=True)
            # display(working_df)
            time_difference = image_datetime - working_df['BaseDateTime']
            if show_logs:
                print("time difference: ", time_difference)
            working_df['time_difference'] = time_difference
            working_df['abs_time_difference'] = abs(time_difference)
            working_df['sign_time_difference'] = working_df.apply(lambda row: categorise_sign_of_time_difference(row),
                                                                  axis=1)
            # SORT TABLE ASCENDINGLY
            working_df.sort_values(by='abs_time_difference',
                                   axis=0,
                                   ascending=True,
                                   inplace=True,
                                   kind='quicksort',
                                   na_position='last',
                                   ignore_index=True)
            #         print("working_df, first sorting: ")
            #         display(working_df)

            if working_df.shape[0] > 1:  # number of rows has to be greater than 1
                # transform datetime to integer - first 2 rows of sorted dataframe by time_difference
                time1 = working_df['BaseDateTime'][0]
                time1 = int(time1.strftime("%H%M%S"))
                LON1 = working_df['LON'][0]
                LAT1 = working_df['LAT'][0]

                first_row_sign = working_df['sign_time_difference'][0]
                if first_row_sign == 0:
                    looking_for_sign = 1
                else:
                    looking_for_sign = 0

                second_working_df = working_df[working_df['sign_time_difference'] == looking_for_sign]
                if len(second_working_df) == 0:  # check if dataframe is empty
                    time2 = working_df['BaseDateTime'][1]
                    time2 = int(time2.strftime("%H%M%S"))
                    LON2 = working_df['LON'][1]
                    LAT2 = working_df['LAT'][1]
                else:
                    second_working_df.sort_values(by='abs_time_difference',
                                                  axis=0,
                                                  ascending=True,
                                                  inplace=True,
                                                  kind='quicksort',
                                                  na_position='last',
                                                  ignore_index=True)

                    time2 = second_working_df['BaseDateTime'][0]
                    time2 = int(time2.strftime("%H%M%S"))
                    LON2 = second_working_df['LON'][0]
                    LAT2 = second_working_df['LAT'][0]
                #                 print("working_df, second sorting: ")
                #                 display(second_working_df)
                # print(f"time before conversion: {time1}, {time2}")

                # 1 opcja konwersji to zamiana całości daty i czasu na int (kosztowne obliczeniowo):
                # 2021-02-04 01:57:13 -> 20210204015713
                # time1 = int(time1.strftime("%Y%m%d%H%M%S"))
                # time2 = int(time2.strftime("%Y%m%d%H%M%S"))

                # 2 opcja konwersji to zamiana tylko czasu na int (lepsze obliczeniowo):
                # 2021-02-04 01:57:13 -> 15713
                #             time1 = int(time1.strftime("%H%M%S"))
                #             time2 = int(time2.strftime("%H%M%S"))
                # print(f"time after conversion: {time1}, {time2}")

                # calculate coefficient a1, b1 for LON (x)
                #             LON1 = working_df['LON'][0]
                #             LON2 = working_df['LON'][1]
                #             LAT1 = working_df['LAT'][0]
                #             LAT2 = working_df['LAT'][1]

                a1, b1 = calculate_lin_reg_coefficients(x1=time1, y1=LON1, x2=time2, y2=LON2)
                # print(f"LON equation: y = {a1}*x + {b1}")

                a2, b2 = calculate_lin_reg_coefficients(x1=time1, y1=LAT1, x2=time2, y2=LAT2)
                # print(f"LAT equation: y = {a2}*x + {b2}")

                time3 = int(image_datetime.strftime("%H%M%S"))
                # print(f"Image time after conversion: {time3}")

                image_LON = a1 * time3 + b1
                image_LAT = a2 * time3 + b2
                # print(f"Image LON: {image_LON}, LAT: {image_LAT}")
            else:
                image_LON = working_df['LON'][0]
                image_LAT = working_df['LAT'][0]

            # prepare row for new dataframe
            # I take data from the first row (closest) from the two which I have used for calculations
            new_df_dict = {'MMSI': working_df['MMSI'][0],
                           'BaseDateTime': image_datetime,
                           'LAT': image_LAT,
                           'LON': image_LON,
                           'SOG': working_df['SOG'][0],
                           'COG': working_df['COG'][0],
                           'Heading': working_df['Heading'][0],
                           'VesselName': working_df['VesselName'][0],
                           'IMO': working_df['IMO'][0],
                           'CallSign': working_df['CallSign'][0],
                           'VesselType': working_df['VesselType'][0],
                           'Status': working_df['Status'][0],
                           'Length': working_df['Length'][0],
                           'Width': working_df['Width'][0],
                           'Draft': working_df['Draft'][0],
                           'Cargo': working_df['Cargo'][0],
                           'TranscieverClass': working_df['TranscieverClass'][0]}

            list_of_df_dicts_after_lin_reg.append(new_df_dict)
            # print(list_of_df_dicts_after_lin_reg)

        # print(list_of_df_dicts_after_lin_reg[0])
        # print(list_of_df_dicts_after_lin_reg[0].keys)
        # df_after_lin_reg = pd.DataFrame.from_dict(list_of_df_dicts_after_lin_reg, columns=list_of_df_dicts_after_lin_reg[0].keys)
        df_after_lin_reg = pd.DataFrame.from_dict(list_of_df_dicts_after_lin_reg)
        print(df_after_lin_reg.head(10))

        if save:
            saving_name = 'interpolated_' + row['processed_ais_file']
            df_after_lin_reg.to_csv(output_path + '/' + saving_name)

    if show_logs:
        print(df_after_lin_reg)

    return df_after_lin_reg


asf_files_list = list_asf_files(show_logs=False, input_path=RESCALED_INTENSITY_ASF_DATA_PATH)
asf_df = calculate_asf_image_features(show_logs=False, input_path=RESCALED_INTENSITY_ASF_DATA_PATH)
# TODO: change RAW_AIS_CSV_DATA_PATH_BATCHTEST to RAW_AIS_CSV_DATA_PATH
ais_df = create_ais_df(show_logs=False, input_path=RAW_AIS_CSV_DATA_PATH_BATCHTEST)
full_data_df = create_full_data_df(asf_df, ais_df, save=True, show_logs=False)
# TODO: change RAW_AIS_CSV_DATA_PATH_BATCHTEST to RAW_AIS_CSV_DATA_PATH
full_data_df = restrict_data_by_given_conditions(full_data_df, show_logs=False, input_path=RAW_AIS_CSV_DATA_PATH_BATCHTEST, output_path=PROCESSED_AIS_DATA_PATH)
df_after_lin_reg = interpolate_ais_data(full_data_df, save=True, show_logs=False, input_path=PROCESSED_AIS_DATA_PATH, output_path=INTERPOLATED_AIS_DATA_PATH)
print(df_after_lin_reg)


