from asyncore import read
import csv
import os

RGB_PATH = os.getcwd() + "/rgb/"


def main():
    files_list = [f for f in os.listdir(RGB_PATH)
                  if os.path.isfile(os.path.join(RGB_PATH, f))
                  and '.png' in f]
    png_names = [n.split('.')[0] for n in files_list]

    with open('bbox.csv') as bbox:
        reader = csv.reader(bbox)
        for row in reader:
            name = row[0].split('.')[0]
            print(name)


if __name__ == '__main__':
    main()
