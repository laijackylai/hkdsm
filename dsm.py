import numpy as np
from pyproj import Transformer 

np.set_printoptions(suppress=True, edgeitems=10,linewidth=180) # fix rubbish np printing behaviours

filename = 'test.txt'

# * data structure being easting, northing, height, unknown, unknown
data = np.loadtxt(filename, dtype=np.float, delimiter=',')

sorted = np.sort(data, axis=0) # sort by easting

transformer = Transformer.from_crs(2326, 4326)
lat, lon = transformer.transform(sorted[:, 1], sorted[:, 0]) # reference: https://github.com/shermanfcm/HK1980#python

lat = np.reshape(lat, (-1, 1))
lon = np.reshape(lon, (-1, 1))
# * new array structure: HK1980 easting, HK1980 northing, height, unknown, unknown, lat, lon
sorted = np.concatenate((sorted, lat, lon), axis=1) 

print(sorted)