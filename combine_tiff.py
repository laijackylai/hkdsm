###################################################################################################
### This python file is used to concat the hk map mosaic.                                       ###
###################################################################################################
"""
import needed packages
"""
import time
import os
import affine
import rasterio as rio
from rasterio.merge import merge
import numpy as np

STATION = 'hks'
DATATYPE = 'DTM'

# set paths
IN_PATH = './tif/'
NEW_PATH = './all/'

start_time = time.time()


def main():
    '''
    main function
    '''
    # making mosaic file array
    src_files_to_mosaic = []

    files = [f for f in os.listdir(IN_PATH)
             if os.path.isfile(os.path.join(IN_PATH, f))
             and '.DS_Store' not in f
             and 'all' not in f
             and '.xml' not in f]

    for f in files:
        src = rio.open(IN_PATH + f)
        src_files_to_mosaic.append(src)

    print(src.meta.copy()['transform'])
    exit()

    # merge the function, returns a single mosaic array and transformation info
    mosaic, out_trans = merge(src_files_to_mosaic, res=[src.meta.copy()[
        'transform'][0], src.meta.copy()['transform'][0]])

    # copy the metadata
    out_meta = src.meta.copy()

    arr = np.array(out_trans)
    new_trans = np.concatenate(
        (np.concatenate((arr[3:6], arr[0:3])), arr[6:9]))
    new_trans = affine.Affine(new_trans[0], new_trans[1], new_trans[2], new_trans[3],
                              new_trans[4], new_trans[5])

    # update the metadata
    out_meta.update({
        'driver': 'GTiff',
        'height': mosaic.shape[2],
        'width': mosaic.shape[1],
        'transform': new_trans
    })

    print(mosaic)
    print(out_trans)
    print(out_meta)

    # write the mosaic raster to disk
    with rio.open(f'{NEW_PATH}all.tif', 'w', **out_meta) as dest:
        dest.write(mosaic)

    print(str(time.time() - start_time), 's - combined GeoTiffs')

    # options_list = [
    #     '-ot Byte',
    #     '-of PNG',
    #     '-b 1',
    #     '-scale',
    #     '-a_srs EPSG:4326'
    # ]
    # options_string = " ".join(options_list)
    # gdal.Translate(
    #     './all/all.png',
    #     './all/all.tif',
    #     options=options_string
    # )

    # print(str(time.time() - start_time), 's - Exported to PNG')


if __name__ == "__main__":
    main()
