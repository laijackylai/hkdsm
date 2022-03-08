"""
import packages
"""
from multiprocessing import Pool
import multiprocessing
import os
from time import sleep
from PIL import Image
import numpy as np
from osgeo import gdal
import math
import cv2 as cv


IN_PATH = './tiles/'
OUT_PATH = './tiles/png/'
TEST_PATH = './test/'
ALL_PATH = './all/'


def main(tif):
    """
    main function to endcode tif to rgb png
    """

    # list = [f for f in os.listdir(
    #     IN_PATH) if os.path.isfile(os.path.join(IN_PATH, f)) and '.tif' in f]
    # list = Path(IN_PATH).glob('**/*.tif')

    # for tif in list:
    name = tif.split('.')[1].split('/')[4]
    zoom = name.split('-')[2]

    tif = gdal.Open(tif)
    data = np.array(tif.ReadAsArray())

    # print('shape: ', np.shape(data))
    # print('min: ', data.min(), 'm')
    # print('max: ', data.max(), 'm')

    # return if all data are zeros
    if(not np.any(data)):
        print('all zeros')
        return

    # r = np.floor(data / 10)
    # g = np.floor((data % 10) / 0.1)
    # b = np.floor((data % 10) % 0.1 / 0.001)

    data = np.rot90(data, 3)
    v = data + 32768
    r = np.floor(v/256)
    g = np.floor(v % 256)
    b = np.floor((v - np.floor(v)) * 256)

    r = cv.resize(r, (512, 512), interpolation=cv.INTER_NEAREST)
    g = cv.resize(g, (512, 512), interpolation=cv.INTER_NEAREST)
    b = cv.resize(b, (512, 512), interpolation=cv.INTER_NEAREST)

    rgb = np.array([r, g, b]).swapaxes(0, 1).swapaxes(1, 2)

    # * test decode
    # height = r * 10 + g * 0.1 + b * 0.001

    im = Image.fromarray(rgb.astype('uint8'), "RGB")
    im = im.transpose(Image.FLIP_TOP_BOTTOM)

    # im.show()
    # exit()
    # im.save(TEST_PATH + name + '.png')

    x = im.size[0]
    y = im.size[1]

    next_x = pow(2, round(math.log(x)/math.log(2)))
    next_y = pow(2, round(math.log(y)/math.log(2)))

    out = OUT_PATH + zoom + '/'

    # if next_x > next_y:
    # im = im.resize((512, 512), resample=Image.BILINEAR)
    im.save(out + name + '.png')
    # else:
    #     im = im.resize((next_y, next_y))
    #     im.save(out + name + '.png')

    print(out + name + '.png')


if __name__ == '__main__':
    list = []
    for subdir, dirs, files in os.walk(IN_PATH):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".tiff"):
                list.append(filepath)

    # main(list[0])

    # * multiprocessing
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(main, list)
