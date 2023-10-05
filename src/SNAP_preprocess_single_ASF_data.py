# Import Libraries
import sys

# sys.path.append('C:/Users/user/anaconda3/envs/snap/Lib/snappy')  # or sys.path.insert(1, '<snappy-dir>')
sys.path.append('C:/Python34/virtenv/Lib/snappy')

import os
# import numpy as np
# import matplotlib.pyplot as plt
import snappy
from snappy import ProductIO, Product, ProductData, ProductUtils, String
from snappy import HashMap, GPF, Product, ProductIO, ProductUtils, WKTReader

# Los Angeles coordinates
wkt = "POLYGON ((-118.3519496977353 33.49095484819047, -117.8921279805309 33.56247074493937, -117.95121096828032 33.83355450820764, -118.41396202220257 33.76185206832226, -118.3519496977353 33.49095484819047))"
## well-known-text (WKT) file for subsetting (can be obtained from SNAP by drawing a polygon)
# WKT from geometry

# DO_SUBSET WORKS
def do_subset(source, wkt):
    print('\tSubsetting...')
    parameters = HashMap()
    geom = WKTReader().read(wkt)
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geom)
    output = GPF.createProduct('Subset', parameters, source)
    return output

#LAND/SEA MASK WORKS
def LandSeaMask(inpt, outpt):
    print('\tLand/Sea Masking...')
    # source = ProductIO.readProduct(inpt)
    source = inpt
    print(source)

    params = HashMap()
    params.put('useSRTM', True)
    params.put('landMask', True)
    params.put('shorelineExtension', '40')
    #params.put('sourceBands', 'Intensity_VV')
    params.put('sourceBands', 'Intensity_VV, Intensity_VH')
    target = GPF.createProduct('Land-Sea-Mask', params, source)

    # print('\tSaving to file...')
    # ProductIO.writeProduct(target, outpt, 'BEAM-DIMAP')

    return target


def terrain_correction(source_file, saving_destination):
    print('\tTerrain correction...')
    # https://forum.step.esa.int/t/s1a-product-terrain-correction/27599/10
    # DETAILED DOCUMENTTATION
    # print(subprocess.Popen(['gpt', '-h', 'Terrain-Correction'], stdout=subprocess.PIPE,
    #                        universal_newlines=True).communicate()[0])
    parameters = HashMap()
    parameters.put('sourceBandNames', 'Intensity_VV, Intensity_VH')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('demName', 'Copernicus 30m Global DEM')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('saveSelectedSourceBand', True)
    parameters.put('mapProjection', 'WGS84(DD)')
    parameters.put('nodataValueAtSea', False)
    parameters.put('maskOutAreaWithoutElevation', False)

    output_file = GPF.createProduct("Terrain-Correction", parameters, source_file)

    print('\tSaving to file...')
    ProductIO.writeProduct(output_file, saving_destination, 'GeoTIFF')

    return output_file


# Set Path to Input Satellite Data
# miniconda users
path = r'C:\Users\user\PycharmProjects\identification-and-classification-of-sea-going-vessels-using-satellite-images\data\3_raw_ASF_data'
initial_filename = 'S1A_IW_GRDH_1SDV_20210106T015004_20210106T015033_036011_04381A_71E9.zip'
subset_filename = 'S1A_IW_GRDH_1SDV_20210106T015004_20210106T015033_036011_04381A_71E9.dim'
final_filename = 'S1A_IW_GRDH_1SDV_20210106T015004_20210106T015033_036011_04381A_71E9'
# .dim is BEAM-DIMAP format, native to snap
# our final destination format is 'GeoTIFF'

#sentinel_1 = ProductIO.readProduct(path + "\" + folder + "\\manifest.safe")
sentinel_1 = ProductIO.readProduct(path + "\\" + initial_filename)
print(sentinel_1)

bands = list(sentinel_1.getBandNames())
print(bands)

subset_sentinel1 = do_subset(sentinel_1, wkt)
print(subset_sentinel1)

target_location = path + '\\' + subset_filename
masked_sentinel1 = LandSeaMask(subset_sentinel1, target_location)
print(masked_sentinel1)

final_location = path + '\\' + final_filename
terrain_corrected_sentinel1 = terrain_correction(masked_sentinel1, final_location)
print(terrain_corrected_sentinel1)

print("\tExecution ended")
# SAVE PARTIAL WORK TO FILE
#ProductIO.writeProduct(subset_sentinel1, target_location, 'BEAM-DIMAP')
#ProductIO.writeProduct(out_product, output_file, 'GeoTIFF')



