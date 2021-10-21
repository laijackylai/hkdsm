###################################################################################################
### This python file is used to translate all the xyz TXT file into Geotiff.                    ###
###################################################################################################
# import the needed package
import math
import time
import os
import shutil
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import Transformer
from multiprocessing import Pool
import multiprocessing
import csv
import dask.dataframe as dd
# import glob

# TODO: add concurrancy for processing the txt files in parallel
# TODO: save the matching png files and its bounding box in a csv for later use in rendering the front end

# set paths and start time
home = os.getcwd()
# inpath = os.getcwd() + "/input_txt/"
# inpath = '/mnt/c/Users/laija/Downloads/D6.ASCII_DTM/'
inpath = '/home/rsmcvis/D6.ASCII_DTM/'
tifpath = os.getcwd() + "/test/"
pngpath = os.getcwd() + "/png/"
start_time = time.time()


def __init():
    # os.chdir(inpath)
    print('starting program')
    # clean_folder(tifpath)
    # clean_folder(pngpath)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 6371
    return c * r * 1000  # in meters


def clean_folder(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print('cleaned ', str(path))
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_files_to_be_processed():
    """
    get txt files that needs to be processed
    """
    pngfiles = [f for f in os.listdir(
        home + '/png/') if os.path.isfile(os.path.join(home + '/png/', f)) and '.png']
    pngfiles = [f.replace('.png', '.txt') for f in pngfiles]
    pngfiles = [f.replace(':', ',') for f in pngfiles]
    files = [f for f in os.listdir(
        inpath) if os.path.isfile(os.path.join(inpath, f)) and '.txt' in f and 'DS_Store' not in f and 'test' not in f]
    files = list(set(files) - set(pngfiles))
    return files


def process_single_file(f):
    """
    process one single txt file -> csv -> create vrt -> create geotiff -> generate height map
    """
    # open .xyz file as csv file
    print('processing ' + f)
    df = pd.read_csv(inpath + f, sep=",")

    df = df.dropna(axis=1)
    df = pd.DataFrame(np.vstack([df.columns, df]))
    for i in [0, 1, 2, 3]:
        df.iloc[0][i] = float(df.iloc[0][i])
    # should be Easting, Northing
    df.columns = ["Easting", "Northing", "Ele", "Na", "Na2"]
    name = f.split('.')[0]
    name = name.replace(',', ':')
    df = df.drop(columns={'Na', 'Na2'})
    df["Ele"] = df["Ele"] + 0.146

    #! Northing -> Latitude -> x, Easting -> Longitude -> y
    transformer = Transformer.from_crs(2326, 3857)
    # reference: https://github.com/shermanfcm/HK1980#python
    lat, lon = transformer.transform(df['Easting'], df['Northing'])

    df.insert(0, 'Lon', lon.tolist())
    df.insert(0, 'Lat', lat.tolist())

    df.to_csv(tifpath + name + ".csv", index=False)
    print('1/4 -', str(time.time() - start_time), 's - Translated to CSV')

    ##############################################################

    min_lat = lat.min()
    max_lat = lat.max()
    min_lon = lon.min()
    max_lon = lon.max()
    print('bounding box: ' + str(min_lon) + ',' +
          str(min_lat)+',' + str(max_lon) + ',' + str(max_lat))

    # store data in csv
    os.chdir(home)
    with open('metadata.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        metadata = [name, min_lon, min_lat, max_lon, max_lat]
        writer.writerow(metadata)

    lat_cover = haversine(min_lon, min_lat, min_lon, max_lat)
    lon_cover = haversine(min_lon, min_lat, max_lon, min_lat)

    img_width = lat_cover / 2
    img_height = lon_cover / 2

    # create .vrt file for raster format conversion (from csv to Geotiff(gdal))
    os.chdir(tifpath)
    fn = name + ".csv"
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')

    with open(tifpath + vrt_fn, 'w+') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write(
            '\t\t<GeometryField encoding="PointFromColumns" x="Lat" y="Lon" z="Ele"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

    print('2/4 -', str(time.time() - start_time), 's - Created VRT')

    ##############################################################

    grid_options = {
        'destName': tifpath + out_tif,
        'srcDS': tifpath + vrt_fn,
        'width': img_width,
        'height': img_height
    }
    gdal.Grid(**grid_options)
    os.remove(tifpath + fn)  # remove the csv file
    os.remove(tifpath + vrt_fn)  # remove the vrt file
    print('3/4 -', str(time.time() - start_time), 's - Created GeoTiff')

    ##############################################################

    # set the coordinate system
    dst_crs = 'EPSG:4326'
    with rio.open(tifpath + out_tif) as src:
        # print(src.crs, dst_crs, src.width, src.height, *src.bounds)
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({'crs': dst_crs, 'transform': transform,
                       'width': width, 'height': height})
        print(kwargs)
        with rio.open(tifpath + out_tif, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(source=rio.band(src, i),
                          destination=rio.band(dst, i),
                          src_transform=src.transform,
                          src_crs=src.crs,
                          dst_transform=transform,
                          dst_crs=dst_crs,
                          resampling=Resampling.nearest)
    print(time.time() - start_time, 's - Updated GeoTiff coordinate system')

    ##############################################################

    options_list = [
        '-ot Byte',
        '-of PNG',
        '-b 1',
        '-scale',
        '-a_srs EPSG:4326'
    ]
    options_string = " ".join(options_list)
    gdal.Translate(
        pngpath + name + '.png',
        tifpath + out_tif,
        options=options_string
    )
    print('4/4 -', str(time.time() - start_time), 's - Exported to PNG')


def dask_read_all_csv():
    """
    parallel read all csv using dask
    """
    df = dd.read_csv(inpath + '*')
    df = df.compute()
    return df


def read_all_csv(listToBeProcessed):
    """
    read all csv sequentially
    """
    df_from_each_file = (pd.read_csv(inpath + f) for f in listToBeProcessed)
    df = pd.concat(df_from_each_file, ignore_index=True)
    print(df)


def test(file):
    """
    test function for pool
    """
    print(file)


if __name__ == "__main__":
    __init()
    listToBeProcessed = get_files_to_be_processed()
    print(listToBeProcessed)
    exit()
    # df = dask_read_all_csv()
    # process_single_file(df)
    # read_all_csv(listToBeProcessed)
    # replace test with process_single_file to do the real transition
    with Pool(multiprocessing.cpu_count() // 2) as p:
        p.map(process_single_file, listToBeProcessed)
