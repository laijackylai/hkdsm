# HKDSM
read, transform and serve hk dsm data

## Usage
An Express.js webserver has been written and and provides an endpoint for the tilesets.  
It is being wrapped in PM2 in cluster mode, with 3 instances currently.  
To start:
```
yarn start
```

## Done
Custom tiled 3D terrain are generated and are stored in the tiles/ folder

## Steps
- Transform the raw text data to VRT -> GeoTiff -> height map -> render in Deck.gl

## TODO
- Explore [GeoTiff](https://www.ogc.org/standards/geotiff) standard
- Explore [Martini](https://github.com/mapbox/martini) with this [blog](https://observablehq.com/@mourner/martin-real-time-rtin-terrain-mesh), [Delatin](https://github.com/mapbox/delatin) and [Quantized Mesh Encoder](https://github.com/kylebarron/quantized-mesh-encoder)
- Explore the [layer](https://deck.gl/docs/api-reference/core/layer) rendering structure used by Deck.gl
- Explore the [SimpleMeshLayer](https://deck.gl/docs/api-reference/mesh-layers/simple-mesh-layer), [MVTLayer](https://deck.gl/docs/api-reference/geo-layers/mvt-layer) and the [TerrainLayer](https://deck.gl/docs/api-reference/geo-layers/terrain-layer)
- Explore the possibility of writing a [custom layer](https://deck.gl/docs/developer-guide/custom-layers) for this use case

## Done
