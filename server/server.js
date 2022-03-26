const express = require('express')
const http2Express = require('http2-express-bridge')
const http2 = require('http2')
const cors = require('cors')
const fs = require('fs')
const request = require('request')
const { promisify } = require('util')

const readFile = promisify(fs.readFile)

const app = http2Express(express)
app.use(cors())

app.get('/tiles/:z-:x-:y.png', async (req, res) => {
  const { z, x, y } = req.params
  const imgPath = `tiles/png/${z}/${x}-${y}-${z}.png`

  // console.info(req.headers['user-agent'], ': ', req.headers[':method'], imgPath)

  if (fs.existsSync(imgPath)) {
    const img = await readFile(imgPath)
    res.send(img)
    console.info('sent hkdsm', img, '\n')
  } else {
    const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoibGFpamFja3lsYWkiLCJhIjoiY2tjZWZucjAzMDd1eDJzcGJvN2tiZHduOSJ9.vWThniHwg9V1wEO3O6xn_g';
    const mapboxRGBUrl = `https://api.mapbox.com/v4/mapbox.terrain-rgb/${z}/${x}/${y}.pngraw?access_token=${MAPBOX_ACCESS_TOKEN}`

    const options = {
      url: mapboxRGBUrl,
      method: "get",
      encoding: null
    };

    request(options, (error, response, body) => {
      if (error) {
        return
      }
      res.send(body)
      console.info('sent mapbox terrain', body, '\n')
    })
  }
})

const options = {
  key: fs.readFileSync('server/keys/key.pem'),
  cert: fs.readFileSync('server/keys/cert.pem'),
  allowHTTP1: true
}

const server = http2.createSecureServer(options, app)
server.listen(3001, () => console.info(`server listening on 3001`))