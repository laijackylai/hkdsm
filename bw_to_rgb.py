"""
import packages
"""
import os
from PIL import Image
import numpy as np
from osgeo import gdal


IN_PATH = './tif/'
OUT_PATH = './fixed/'
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
        data = np.array(tif.ReadAsArray())

        # r = np.floor(data / 10)
        # g = np.floor((data % 10) / 0.1)
        # b = np.floor((data % 10) % 0.1 / 0.001)

        # data = np.rot90(data, 3)
        v = data + 32768
        r = np.floor(v/256)
        g = np.floor(v % 256)
        b = np.floor((v - np.floor(v)) * 256)

        rgb = np.array([r, g, b]).swapaxes(0, 1).swapaxes(1, 2)

        # * test decode
        # height = r * 10 + g * 0.1 + b * 0.001

        im = Image.fromarray(rgb.astype('uint8'), "RGB")
        im.save(TEST_PATH + name + '.png')


if __name__ == '__main__':
    main()
