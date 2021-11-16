from osgeo import gdal
import glob


def main():
    list = glob.glob('./tif/*.tif')

    vrt = gdal.BuildVRT("./all/all.vrt", list)
    gdal.Translate("./all/all.tif", vrt)
    vrt = None


if __name__ == '__main__':
    main()
