"""
import packages
"""
import os
from PIL import Image
import numpy as np


IN_PATH = './tif/'
OUT_PATH = './fixed/'
TEST_PATH = './test/'


def main():
    """
    main function to endcode tif to rgb png
    """

    list = [f for f in os.listdir(
        TEST_PATH) if os.path.isfile(os.path.join(TEST_PATH, f)) and '.png' in f]

    for png in list:
        name = png.split('.')[0]
        print(name)
        png = Image.open(TEST_PATH + png)
        data = np.array(png)
        height = np.shape(data)[0]
        width = np.shape(data)[1]
        for i in range(height):
            for j in range(width):
                rgb = data[i, j, :]
                print(rgb)


if __name__ == '__main__':
    main()
