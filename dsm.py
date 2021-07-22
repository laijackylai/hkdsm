import numpy as np
from pyproj import Transformer 
from quantized_mesh_encoder import encode
from pymartini import decode_ele, Martini, rescale_positions
from imageio import imread
import mercantile

np.set_printoptions(suppress=True, edgeitems=10,linewidth=180) # fix rubbish np printing behaviours

testFilename = 'test.txt'
filename = '6NW24C(e819n830,e820n830).txt'

# * data structure being easting, northing, height, unknown, unknown
data = np.loadtxt(testFilename, delimiter=',')

sorted = np.sort(data, axis=0) # sort by easting

transformer = Transformer.from_crs(2326, 4326)
lat, lon = transformer.transform(sorted[:, 1], sorted[:, 0]) # reference: https://github.com/shermanfcm/HK1980#python

lat = np.reshape(lat, (-1, 1))
lon = np.reshape(lon, (-1, 1))
# * new array structure: HK1980 easting, HK1980 northing, height, unknown, unknown, lat, lon
sorted = np.concatenate((sorted, lat, lon), axis=1) 

# ! testing martini to know what quantized mesh encoder needs
png_path = 'fuji.png'
png = imread(png_path)
terrain = decode_ele(png, 'mapbox')
terrain = terrain.T
martini = Martini(png.shape[0] + 1)
tile = martini.create_tile(terrain)
vertices, triangles = tile.get_mesh(10)
bounds = mercantile.bounds(mercantile.Tile(16, 23, 6))
rescaled = rescale_positions(
    vertices,
    terrain,
    bounds=bounds,
    flip_y=True
)
print('verticies', rescaled)
print('triangles', triangles)

# TODO: build quantized mesh using quantized-mesh-encoder (https://github.com/kylebarron/quantized-mesh-encoder)
# TODO: try rendering it in Deck.gl
# TODO: explore ways to simplify the generated quantized mesh