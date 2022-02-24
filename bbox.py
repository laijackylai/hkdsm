import os
import numpy as np
from osgeo import gdal

IN_PATH = './tif/'
OUT_PATH = './rgb/'
TEST_PATH = './test/'


def main():
    """
    main function to endcode tif to rgb png
    """

    list = [f for f in os.listdir(
        TEST_PATH) if os.path.isfile(os.path.join(TEST_PATH, f)) and '.tif' in f]

    for tif in list:
        name = tif.split('.')[0]
        tif = gdal.Open(TEST_PATH + tif)
        # data = np.array(tif.ReadAsArray())
        print(tif.rasterSize)


if __name__ == '__main__':
    main()
