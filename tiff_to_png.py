"""
import modules
"""
from osgeo import gdal


def main():
    """
    translate tiff to png
    """
    in_path = './all/all.tif'
    out_path = './all/all.png'
    options_list = [
        '-ot Byte',
        '-of PNG',
        '-b 1',
        '-scale',
        '-a_srs EPSG:4326'
    ]
    options_string = " ".join(options_list)
    gdal.Translate(
        out_path,
        in_path,
        options=options_string
    )


if __name__ == '__main__':
    main()
