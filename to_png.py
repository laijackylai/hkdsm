import time
import os
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

inpath = os.getcwd() + "/tif/"
outpath = os.getcwd() + "/png/"

os.chdir(inpath)
files = [f for f in os.listdir(
    inpath) if os.path.isfile(os.path.join(inpath, f))]

for f in files:
    print(f)
    lu = gdal.Open(inpath + f)
    raw_data = lu.ReadAsArray()
    print(np.shape(raw_data))
    exit()

    lue = lu.GetGeoTransform()
    Proj = lu.GetProjection()

    band = lu.GetRasterBand(1)
    array = band.ReadAsArray()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    img = ax.imshow(array)
    img.set_cmap('jet')
    fig.colorbar(img)
    # plt.plot(xlonx,ylatx,'md')
    name = f.split('.')[0]
    fig.savefig(outpath + name + ".png")
