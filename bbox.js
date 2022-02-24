const gdal = require('gdal');
const fs = require('fs');
const ObjectsToCsv = require('objects-to-csv')

const PATH = './tif/'

let data = []
fs.readdirSync(PATH).forEach(file => {
  if (file.includes('tif')) {
    const ds = gdal.open(PATH + file)
    var driver = ds.driver;
    var driver_metadata = driver.getMetadata();
    if (driver_metadata['DCAP_RASTER'] !== 'YES') {
      console.error('Source file is not a raster');
      process.exit(1);
    }

    // raster dimensions
    var size = ds.rasterSize;
    // console.log('Size is ' + size.x + ', ' + size.y);

    // geotransform
    var geotransform = ds.geoTransform;

    // corners
    var corners = {
      'Upper Left  ': { x: 0, y: 0 },
      'Upper Right ': { x: size.x, y: 0 },
      'Bottom Right': { x: size.x, y: size.y },
      'Bottom Left ': { x: 0, y: size.y },
      'Center      ': { x: size.x / 2, y: size.y / 2 }
    };

    var wgs84 = gdal.SpatialReference.fromEPSG(4326);
    var coord_transform = new gdal.CoordinateTransformation(ds.srs, wgs84);

    var corner_names = Object.keys(corners);
    let minLat = 91
    let maxLat = -91
    let minLon = 181
    let maxLon = -181;
    corner_names.forEach(function (corner_name) {
      // convert pixel x,y to the coordinate system of the raster
      // then transform it to WGS84
      var corner = corners[corner_name];

      // ul, ur, br, bl, c
      var pt_orig = {
        x: geotransform[0] + corner.x * geotransform[1] + corner.y * geotransform[2],
        y: geotransform[3] + corner.x * geotransform[4] + corner.y * geotransform[5]
      };
      if (pt_orig.x < minLat) {
        minLat = pt_orig.x
      }
      if (pt_orig.x > maxLat) {
        maxLat = pt_orig.x
      }
      if (pt_orig.y < minLon) {
        minLon = pt_orig.y
      }
      if (pt_orig.y > maxLon) {
        maxLon = pt_orig.y
      }
    });
    data.push(
      { "name": file, "minLon": minLon, "minLat": minLat, "maxLon": maxLon, "maxLat": maxLat }
    )
    console.log(file, minLon, minLat, maxLon, maxLat)
  }
});

// If you use "await", code must be inside an asynchronous function:
(async () => {
  const csv = new ObjectsToCsv(data);
  // Save to file:
  await csv.toDisk('./bbox.csv');
})();