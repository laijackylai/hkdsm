###################################################################################################
### This python file is used to translate all the xyz TXT file into Geotiff.                    ###
###################################################################################################
# import the needed package
import math
import time
import os
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import Transformer


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


# set paths
inpath = os.getcwd() + "/input_txt/"
outpath = os.getcwd() + "/tif/"

start_time = time.time()

# make file list
os.chdir(inpath)

files = [f for f in os.listdir(
    inpath) if os.path.isfile(os.path.join(inpath, f)) and 'test' not in f and 'DS_Store' not in f]

for f in files:
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
    df = df.drop(columns={'Na', 'Na2'})
    df["Ele"] = df["Ele"] + 0.146

    #! Northing -> Longitude, Easting -> Latitude
    transformer = Transformer.from_crs(2326, 4326)
    # reference: https://github.com/shermanfcm/HK1980#python
    lat, lon = transformer.transform(df['Northing'], df['Easting'])

    df.insert(0, 'Lon', lon.tolist())
    df.insert(0, 'Lat', lat.tolist())

    df.to_csv(outpath + name + ".csv", index=False)
    print('Translated to CSV - ', time.time() - start_time)

    minLat = lat.min()
    maxLat = lat.max()
    minLon = lon.min()
    maxLon = lon.max()

    lat_cover = haversine(minLon, minLat, minLon, maxLat)
    lon_cover = haversine(minLon, minLat, maxLon, minLat)

    img_width = lat_cover / 2
    img_height = lon_cover / 2

    # create .vrt file for raster format conversion (from csv to Geotiff(gdal))
    os.chdir(outpath)
    fn = name + ".csv"
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')

    with open(outpath + vrt_fn, 'w+') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write(
            '\t\t<GeometryField encoding="PointFromColumns" x="Lat" y="Lon" z="Ele"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

    print('created VRT - ', time.time() - start_time)

    gridOptions = {
        'destName': outpath + out_tif,
        'srcDS': outpath + vrt_fn,
        'width': img_width,
        'height': img_height
    }

    gdal.Grid(**gridOptions)

    # os.remove(outpath + fn)  # remove the csv file
    # os.remove(outpath + vrt_fn)  # remove the vrt file
    print('created GeoTiff - ', time.time() - start_time)

# # find the Tiff file to loop for
# tif_files = [f for f in os.listdir(
#     outpath) if os.path.isfile(os.path.join(outpath, f)) and 'test' not in f and 'DS_Store' not in f]

# # set the coordinate system
# dst_crs = 'EPSG:2326'
# # change the coordinate system in each file
# for tfn in tif_files:
#     print(tfn)
#     with rio.open(outpath + tfn) as src:
#         # print(src.crs, dst_crs, src.width, src.height, *src.bounds)
#         transform, width, height = calculate_default_transform(
#             src.crs, dst_crs, src.width, src.height, *src.bounds)
#         kwargs = src.meta.copy()
#         kwargs.update({'crs': dst_crs, 'transform': transform,
#                       'width': width, 'height': height})
#         print(kwargs)
#         with rio.open(outpath + tfn, 'w', **kwargs) as dst:
#             for i in range(1, src.count + 1):
#                 reproject(source=rio.band(src, i),
#                           destination=rio.band(dst, i),
#                           src_transform=src.transform,
#                           src_crs=src.crs,
#                           dst_transform=transform,
#                           dst_crs=dst_crs,
#                           resampling=Resampling.nearest)

# print('updated GeoTiff coordinate system')
