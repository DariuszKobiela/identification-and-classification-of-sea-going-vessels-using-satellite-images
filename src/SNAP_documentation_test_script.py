# Import Libraries
import sys
import subprocess
# sys.path.append('C:/Users/user/anaconda3/envs/snap/Lib/snappy')  # or sys.path.insert(1, '<snappy-dir>')
sys.path.append('C:/Python34/virtenv/Lib/snappy')

import os
# import numpy as np
# import matplotlib.pyplot as plt
import snappy

# try:
#     from snappy import ProductIO, Product, ProductData, ProductUtils, String
# except RuntimeError:
#     print('trying second time')

from snappy import ProductIO, Product, ProductData, ProductUtils, String
# import snappy
# from snappy import ProductIO

# Set Path to Input Satellite Data
# miniconda users
path = r'C:\Python34\virtenv\Lib\snappy\testdata'
filename = 'MER_FRS_L1B_SUBSET.dim'
# Read File
df = ProductIO.readProduct(os.path.join(path, filename))
# Get the list of Band Names
print(list(df.getBandNames()))
# Using "radiance_3" band as an example
band = df.getBand('radiance_3')  # Assign Band to a variable
w = df.getSceneRasterWidth()  # Get Band Width
h = df.getSceneRasterHeight()  # Get Band Height
print(w)
print(h)
# # Create an empty array
# band_data = np.zeros(w * h, np.float32)
# # Populate array with pixel value
# band.readPixels(0, 0, w, h, band_data)
# # Reshape
# band_data.shape = h, w
# # Plot the band
# plt.figure(figsize=(18, 10))
# plt.imshow(band_data, cmap=plt.cm.binary)
# plt.show()

## DOCUMENTATION
# print(subprocess.Popen(['gpt', '-h', 'Subset'], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

# GENERAL
# print(subprocess.Popen(['gpt', '-h'], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

# TOCHECK:
# RangeFilter
# LinearToFromdB
# Calibration
# AdaptiveThresholding

# DETAILED
# print(subprocess.Popen(['gpt', '-h', 'Terrain-Correction'], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])
print(subprocess.Popen(['gpt', '-h', 'LinearToFromdB'], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])


