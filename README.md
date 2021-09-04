# hkdsm
read and transform hk dsm data

## Steps
- Transform the raw data to GeoTiff -> height map -> render in Deck.gl

## TODO
- Explore [GeoTiff](https://www.ogc.org/standards/geotiff) standard
- Explore [Martini](https://github.com/mapbox/martini) with this [blog](https://observablehq.com/@mourner/martin-real-time-rtin-terrain-mesh), [Delatin](https://github.com/mapbox/delatin) and [Quantized Mesh Encoder](https://github.com/kylebarron/quantized-mesh-encoder)
- Explore the [layer](https://deck.gl/docs/api-reference/core/layer) rendering structure used by Deck.gl
- Explore the [SimpleMeshLayer](https://deck.gl/docs/api-reference/mesh-layers/simple-mesh-layer), [MVTLayer](https://deck.gl/docs/api-reference/geo-layers/mvt-layer) and the [TerrainLayer](https://deck.gl/docs/api-reference/geo-layers/terrain-layer)
- Explore the possibility of writing a [custom layer](https://deck.gl/docs/developer-guide/custom-layers) for this use case