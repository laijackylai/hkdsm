###################################################################################################
### This python file is used to translate all the xyz TXT file into Geotiff.                    ###
###################################################################################################
# import the needed package
import time
import os
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# set paths
inpath = os.getcwd() + "/input_txt/"
outpath = os.getcwd() + "/tif/"

start_time = time.time()

# make file list
os.chdir(inpath)
files = [f for f in os.listdir(
    inpath) if os.path.isfile(os.path.join(inpath, f))]


for f in files:
    # open .xyz file as csv file
    start_time2 = time.time()
    print(f)
    df = pd.read_csv(inpath + f, sep=",")
    df = df.dropna(axis=1)
    df = pd.DataFrame(np.vstack([df.columns, df]))
    for i in [0, 1, 2, 3]:
        df.iloc[0][i] = float(df.iloc[0][i])
    df.columns = ["Lon", "Lat", "Ele", "Na", "Na2"]
    name = f.split('.')[0]
    df = df.drop(columns={'Na', 'Na2'})
    df["Ele"] = df["Ele"] + 0.146

    df.to_csv(outpath + name + ".csv", index=False)

    # create .vrt file for raster format conversion (from csv to Geotiff(gdal))
    os.chdir(outpath)
    fn = name + ".csv"
    vrt_fn = fn.replace(".csv", ".vrt")
    lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tif')

    with open(outpath + vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % lyr_name)
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write(
            '\t\t<GeometryField encoding="PointFromColumns" x="Lon" y="Lat" z="Ele"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')

    gdal.Grid(outpath + out_tif, outpath + vrt_fn)

    os.remove(outpath + fn)  # remove the csv file
    os.remove(outpath + vrt_fn)  # remove the vrt file
    print("--- %s seconds ---" % (time.time() - start_time2))

print("--- %s seconds ---" % (time.time() - start_time))
print("--- CSV to GTiff convertion DONE ---")


start_time1 = time.time()

# find the Tiff file to loop for
tif_files = [f for f in os.listdir(
    outpath) if os.path.isfile(os.path.join(outpath, f))]

# set the coordinate system
dst_crs = 'EPSG:2326'
# change the coordinate system in each file
for tfn in tif_files:
    print(tfn)
    with rio.open(outpath + tfn) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({'crs': dst_crs, 'transform': transform,
                      'width': width, 'height': height})
        with rio.open(outpath + tfn, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(source=rio.band(src, i),
                          destination=rio.band(dst, i),
                          src_transform=src.transform,
                          src_crs=src.crs,
                          dst_transform=transform,
                          dst_crs=dst_crs,
                          resampling=Resampling.nearest)
print("--- %s seconds ---" % (time.time() - start_time1))
print("--- GTiff UPDATE coordinate system DONE ---")

print("--- Total: %s seconds ---" % (time.time() - start_time))
