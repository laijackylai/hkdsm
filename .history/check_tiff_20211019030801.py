import time
import os
from numpy.lib.type_check import imag
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from PIL import Image
import rasterio as rio

# inpath = os.getcwd() + "/tif/"
# outpath = os.getcwd() + "/png/"

# os.chdir(inpath)
# files = [f for f in os.listdir(
#     inpath) if os.path.isfile(os.path.join(inpath, f)) and '.tif' in f]

# for f in files:
# print(f)

path = '.tif/2NE19A\(e827n843:e827n844\).tif'

with rio.open(path) as src:
    print(src.bounds)

    # lu = gdal.Open(inpath + f)
    # raw_data = lu.ReadAsArray()

    # image = Image.fromarray(raw_data).convert('LA')
    # name = str(f.split('.')[0])
    # image.save(outpath + name + '.png')

    # lue = lu.GetGeoTransform()
    # Proj = lu.GetProjection()

    # band = lu.GetRasterBand(1)
    # array = band.ReadAsArray()
    # print(np.shape(array))
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # img = ax.imshow(array)
    # img.set_cmap('jet')
    # fig.colorbar(img)
    # # plt.plot(xlonx,ylatx,'md')
    # name = f.split('.')[0]
    # fig.savefig(outpath + name + ".png")
