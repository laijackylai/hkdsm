from PIL import Image, ImageOps
import os

IN_PATH = './png/'
OUT_PATH = './fixed/'
TEST_PATH = './test/'


def main():
    list = [f for f in os.listdir(
        IN_PATH) if os.path.isfile(os.path.join(IN_PATH, f)) and '.png' in f]

    for im in list:
        name = im
        im = Image.open(IN_PATH + im)
        im_flip = ImageOps.flip(im)
        im_rot = im_flip.rotate(90, expand=True)
        im_rot.save(OUT_PATH + name)


if __name__ == '__main__':
    main()
