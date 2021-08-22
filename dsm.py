import numpy as np
from pyproj import Transformer
from quantized_mesh_encoder import encode
from pymartini import decode_ele, Martini, rescale_positions
from imageio import imread
import mercantile

# fix rubbish np printing behaviours
np.set_printoptions(suppress=True, edgeitems=10, linewidth=180, precision=20)

testFilename = 'test.txt'
filename = '6NW24C(e819n830,e820n830).txt'

# * data structure being easting, northing, height, unknown, unknown
data = np.loadtxt(filename, delimiter=',')

transformer = Transformer.from_crs(2326, 4326)
# reference: https://github.com/shermanfcm/HK1980#python
lat, lon = transformer.transform(data[:, 1], data[:, 0])

lat = np.reshape(lat, (-1, 1))
lon = np.reshape(lon, (-1, 1))
# * new array structure: HK1980 easting, HK1980 northing, height, unknown, unknown, lat, lon
latlon = np.concatenate((data, lat, lon), axis=1)

min_lat = np.min(lat)
max_lat = np.max(lat)

min_lon = np.min(lon)
max_lon = np.max(lon)

# ! testing martini to know what quantized mesh encoder needs
# png_path = 'fuji.png'
# png = imread(png_path)
# terrain = decode_ele(png, 'mapbox')
# terrain = terrain.T
# martini = Martini(png.shape[0] + 1)
# tile = martini.create_tile(terrain)
# vertices, triangles = tile.get_mesh(10)
# bounds = mercantile.bounds(mercantile.Tile(16, 23, 6))
# rescaled = rescale_positions(
#     vertices,
#     terrain,
#     bounds=bounds,
#     flip_y=True
# )
# print('verticies', rescaled)
# print('triangles', triangles)

# TODO: generate height map in png with the data
# TODO: build quantized mesh using quantized-mesh-encoder (https://github.com/kylebarron/quantized-mesh-encoder)
# TODO: try rendering it in Deck.gl
# TODO: explore ways to simplify the generated quantized mesh

# * fixed clang problem by following this (https://github.com/andersbll/cudarray/issues/25#issuecomment-146217359)
