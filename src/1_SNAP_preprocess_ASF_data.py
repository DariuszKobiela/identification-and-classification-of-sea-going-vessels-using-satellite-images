# Import Libraries
import sys
sys.path.append('C:/Python34/virtenv/Lib/snappy')  # NECESSARY FOR SNAPPY

import os
os.system('color')  # to get the ANSI codes working on windows

import snappy
from snappy import ProductIO, Product, ProductData, ProductUtils, String, jpy
from snappy import HashMap, GPF, WKTReader, ProgressMonitor
from src.constants import LOS_ANGELES_WKT, RAW_ASF_DATA_PATH_BATCHTEST, \
    RAW_ASF_DATA_PATH_BATCH0, RAW_ASF_DATA_PATH_BATCH1, RAW_ASF_DATA_PATH_BATCH2, RAW_ASF_DATA_PATH_BATCH3, \
    SNAP_ASF_DATA_AFTER_SUBSETTING, SNAP_ASF_DATA_AFTER_LANDSEAMASK, SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH, \
    SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH


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


def ImageSubset(input_file, wkt, save=False, file_saving_location=SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH, file_saving_format='BEAM-DIMAP'):
    print('\tSubsetting...')
    parameters = HashMap()
    geom = WKTReader().read(wkt)
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geom)
    output_file = GPF.createProduct('Subset', parameters, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


def LandSeaMask(input_file, save=False, file_saving_location=SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH, file_saving_format='BEAM-DIMAP'):
    print('\tLand/Sea Masking...')
    params = HashMap()
    params.put('useSRTM', True)
    params.put('landMask', True)
    params.put('shorelineExtension', '40')
    params.put('sourceBands', 'Intensity_VV, Intensity_VH')
    output_file = GPF.createProduct('Land-Sea-Mask', params, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


def GeometricTerrainCorrection(input_file, save=True, file_saving_location=SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH, file_saving_format='GeoTIFF'):
    print('\tRadar Geometric Terrain correction...')
    # https://forum.step.esa.int/t/s1a-product-terrain-correction/27599/10
    # DETAILED DOCUMENTATION
    # print(subprocess.Popen(['gpt', '-h', 'Terrain-Correction'], stdout=subprocess.PIPE,
    #                        universal_newlines=True).communicate()[0])
    parameters = HashMap()
    #parameters.put('sourceBandNames', 'Intensity_VV, Intensity_VH')
    parameters.put('sourceBands', 'Intensity_VV, Intensity_VH')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('demName', 'Copernicus 30m Global DEM')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('saveSelectedSourceBand', True)
    parameters.put('mapProjection', 'WGS84(DD)')
    parameters.put('nodataValueAtSea', False)
    parameters.put('maskOutAreaWithoutElevation', False)
    output_file = GPF.createProduct("Terrain-Correction", parameters, input_file)

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


def AddNewBand(input_file, save=True, file_saving_location=SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH, file_saving_format='GeoTIFF'):
    # product = ProductIO.readProduct(input_file)
    product = input_file
    width = product.getSceneRasterWidth()
    height = product.getSceneRasterHeight()
    name = product.getName()
    description = product.getDescription()
    band_names = list(product.getBandNames())
    print("Product: %s, %d x %d pixels, %s" % (name, width, height, description))
    print("\tInput bands: " + str(band_names))

    band1 = input_file.getBand('Intensity_VV')
    band2 = input_file.getBand('Intensity_VH')
    print("\tBand1: " + str(band1) + ", Band2: " + str(band2))

    BandDescriptor = jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')

    targetBand = BandDescriptor()
    targetBand.name = 'Divided_intensity'
    targetBand.type = 'float32' # 'float32'
    targetBand.expression = 'Intensity_VV / Intensity_VH'

    targetBand2 = BandDescriptor()
    targetBand2.name = 'Intensity_VV'
    targetBand2.type = 'float32'  # 'float32'
    targetBand2.expression = 'Intensity_VV'

    targetBand3 = BandDescriptor()
    targetBand3.name = 'Intensity_VH'
    targetBand3.type = 'float32'  # 'float32'
    targetBand3.expression = 'Intensity_VH'

    # targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
    targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 3)  # number at the end is the size of the array
    # print(targetBands)
    targetBands[0] = targetBand2
    targetBands[1] = targetBand3
    targetBands[2] = targetBand
    # print(targetBands)

    parameters = HashMap()
    parameters.put('targetBands', targetBands)
    output_file = GPF.createProduct('BandMaths', parameters, input_file)
    output_bands = list(output_file.getBandNames())
    print("\tOutput bands: " + str(output_bands))
    band1 = output_file.getBand('Intensity_VV')
    band2 = output_file.getBand('Intensity_VH')
    band3 = output_file.getBand('Divided_intensity')
    print("\tBand1: " + str(band1) + ", Band2: " + str(band2) + ", Band3: " + str(band3))

    if save:
        print('\tSaving to file...')
        ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)

    return output_file


# def SaveAsRGB(input_file, save=True, file_saving_location=RGB_ASF_DATA_PATH, file_saving_format='png'):
#     # IT IS NOT POSSIBLE TO SAVE RGB IMAGES IN SNAP
#     # https://forum.step.esa.int/t/create-and-save-rgb-images-from-3-bands/2860
#     jpy = snappy.jpy
#     # p = ProductIO.readProduct(file)
#     b2 = input_file.getBand('Intensity_VV')
#     b3 = input_file.getBand('Intensity_VH')
#     b4 = input_file.getBand('Divided_intensity')
#     info = ProductUtils.createImageInfo([b4,b3,b2], True, ProgressMonitor.NULL)
#     print(info)
#     image = ProductUtils.createRgbImage([b4,b3,b2], info, ProgressMonitor.NULL)
#     print(image)
#     # image_bands = list(image.getBandNames())
#     # File = jpy.get_type('java.io.File')
#     # savefile = File(‘C:\Users\Antonio\test_image_RGB.png’)
#     # looks = jpy.get_type('org.esa.snap.core.datamodel.quicklooks.QuicklookGenerator')
#     # print(looks)
#
#     if save:
#         print('\tSaving to file...')
#         # ProductIO.writeProduct(image, file_saving_location, file_saving_format)
#         #looks.writeImage(image, file_saving_location)

#################################################################################################################
# CHOOSE DATA BATCH
raw_asf_data_path = RAW_ASF_DATA_PATH_BATCHTEST
# raw_asf_data_path = RAW_ASF_DATA_PATH_BATCH3
################################################################################################################

# SNAP SCRIPTS
# https://github.com/kedziorm/mySNAPscripts/blob/4c5438b2da84201653f4a944685be2132b42d01b/myScripts.py#L891

# Set Path to Input Satellite Data
# input_path = r'C:\Users\user\PycharmProjects\identification-and-classification-of-sea-going-vessels-using-satellite-images\data\3_raw_ASF_data'
# input_path = r'../data/3_raw_ASF_data'
# .dim is BEAM-DIMAP format, native to snap
# our final destination format is 'GeoTIFF'

sentinel_files = os.listdir(raw_asf_data_path)
number_of_sentinel_files = len(sentinel_files)
print(sentinel_files)

for count, sentinel_file in enumerate(sentinel_files):
    processed_files_percentage = round((count/number_of_sentinel_files) * 100)
    print()
    print(BColors.WARNING + "\tFILES PROCESSING STATUS: " + str(processed_files_percentage) + "% (" + str(count) + "/" + str(number_of_sentinel_files) + ")" + BColors.ENDC)
    print()
    snap_asf_data_after_subsetting_location = SNAP_ASF_DATA_AFTER_SUBSETTING + "\\" + sentinel_file.strip(".zip")
    snap_asf_data_after_landseamask_location = SNAP_ASF_DATA_AFTER_LANDSEAMASK + "\\" + sentinel_file.strip(".zip")
    file_saving_location = SNAP_PREPROCESSED_ASF_DATA_2_CHANNELS_PATH + "\\" + sentinel_file.strip(".zip")
    sentinel_1 = ProductIO.readProduct(raw_asf_data_path + "\\" + sentinel_file)

    bands = list(sentinel_1.getBandNames())
    print("\tProcessing " + str(sentinel_1) + ", initial bands " + str(bands))

    subset_sentinel1 = ImageSubset(sentinel_1, LOS_ANGELES_WKT, save=True, file_saving_location=snap_asf_data_after_subsetting_location, file_saving_format='BEAM-DIMAP')
    masked_sentinel1 = LandSeaMask(subset_sentinel1, save=True, file_saving_location=snap_asf_data_after_landseamask_location, file_saving_format='BEAM-DIMAP')
    # terrain_corrected_sentinel1 = GeometricTerrainCorrection(masked_sentinel1, save=True, file_saving_location=file_saving_location, file_saving_format='GeoTIFF')
    # print("\tFile " + str(terrain_corrected_sentinel1) + " saved into " + str(file_saving_location))
    #
    # file_saving_location2 = SNAP_PREPROCESSED_ASF_DATA_3_CHANNELS_PATH + sentinel_file.strip(".zip")
    # added_band_sentinel1 = AddNewBand(terrain_corrected_sentinel1, save=True, file_saving_location=file_saving_location2, file_saving_format='GeoTIFF')
    # print("\tFile " + str(added_band_sentinel1) + " saved into " + str(file_saving_location2))
    ##################################################################################################################################################
    #########################################                         END OF SCRIPT                    ###############################################
    ##################################################################################################################################################

    # file_saving_location3 = RGB_ASF_DATA_PATH + sentinel_file.strip(".zip")
    # rgb_sentinel1 = SaveAsRGB(added_band_sentinel1, save=True, file_saving_location=file_saving_location3, file_saving_format='png')
    # print("\tFile " + str(rgb_sentinel1) + " saved into " + str(file_saving_location3))

    # IT IS NOT POSSIBLE TO PERFORM HISTOGRAM EQUALIZATION IN SNAP
    # https://forum.step.esa.int/t/equalization-slc-and-grd-images-with-snap/4851/15
    # INSTEAD THERE CAN BE DONE:
    # calibration to sigma0 and convert to db
    # what has similar effect to the histogram

print("\tALL ASF data processed via ESA SNAPPY")




# # get subset:
# SubsetOp = jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
# op = SubsetOp()
# op.setSourceProduct(source_product)
# op.setRegion(snappy.Rectangle(range[0], range[2], range[1] - range[0], range[3] - range[2]))
# sub_product = op.getTargetProduct()
# writer = snappy.ProductIO.getProductWriter('BEAM-DIMAP')
# sub_product.setProductWriter(writer)

# width = input_file.getBandAt(0).getRasterWidth()
# height = input_file.getBandAt(0).getRasterHeight()
#
# data_array = intensityvv/ intensityvh
# # for y in range(height):
# #     print("processing line ", y, " of ", height)
# #     r7 = b7.readPixels(0, y, width, 1, r7)
# #     r10 = b10.readPixels(0, y, width, 1, r10)
# #     ndvi = (r10 - r7) / (r10 + r7)
# #     ndviBand.writePixels(0, y, width, 1, ndvi)
# #     ndviLow = ndvi < 0.0
# #     ndviHigh = ndvi > 1.0
# #     ndviFlags = numpy.array(ndviLow + 2 * ndviHigh, dtype=numpy.int32)
# #     ndviFlagsBand.writePixels(0, y, width, 1, ndviFlags)
#
#
# output_file = input_file.addBand('intensity_divided_VV_VH', ProductData.TYPE_UINT8)
# output_file.writePixels(0, 0, width, height, data_array)
#
# targetBand1 = BandDescriptor()
# targetBand1.name = 'Difference'
# targetBand1.type = 'float32'
#
# ##  index is zero-based, so index 1 refers to the second product
# targetBand1.expression = band + ' - $sourceProduct.1.' + band
#
# targetBands = jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
# targetBands[0] = targetBand1
#
# parameters = HashMap()
# parameters.put('targetBands', targetBands)
#
# ## More at http://forum.step.esa.int/t/calculate-the-difference-or-division-between-bands-in-two-different-products
# result = GPF.createProduct('BandMaths', parameters, input_file)
#
# # print("Write results")
# # ProductIO.writeProduct(result, 'difference_output.dim', 'BEAM-DIMAP')
#
# if save:
#     print('\tSaving to file...')
#     ProductIO.writeProduct(output_file, file_saving_location, file_saving_format)
#
# return output_file



