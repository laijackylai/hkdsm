import mercantile
from PIL import Image
import subprocess

MIN_LAT = 22.1537640910980613
MIN_LON = 113.8349922853287239
MAX_LAT = 22.5620254686685620
MAX_LON = 114.4420072690531640

Image.MAX_IMAGE_PIXELS = 933120000


def main():
    all_png = Image.open('./all/all.png')

    width = all_png.size[0]
    height = all_png.size[1]

    lon_per_pixel = (MAX_LON - MIN_LON) / width
    lat_per_pixel = (MAX_LAT - MIN_LAT) / height

    # z = 14
    for z in range(10, 16):

        ll_tile = mercantile.tile(MIN_LON, MIN_LAT, z)  # lower left tile
        ur_tile = mercantile.tile(MAX_LON, MAX_LAT, z)  # upper right tile

        # lower left tile bounding box
        ll_tile_bbox = mercantile.bounds(ll_tile)
        # upper right tile bounding box
        ur_tile_bbox = mercantile.bounds(ur_tile)

        # loop through the tiles
        for i in range(ll_tile.x, ur_tile.x + 1):
            for j in range(ur_tile.y, ll_tile.y + 1):
                name = f"{i}-{j}-{z}"
                tile_bounds = mercantile.bounds(i, j, z)
                subprocess.call(["gdalbuildvrt", "-te", str(tile_bounds.south), str(tile_bounds.west),
                                str(tile_bounds.north), str(tile_bounds.east), "-tr", "512", "512", f"./tiles/vrt/{z}/{name}.vrt", "./all/all.tif"])
                subprocess.call(
                    ["gdal_translate", f"./tiles/vrt/{z}/{name}.vrt", f"./tiles/tif/{z}/{name}.tiff"])
                print(z, i, j)


if __name__ == "__main__":
    main()
