const express = require('express')
const http2Express = require('http2-express-bridge')
const http2 = require('http2')
const cors = require('cors')
const fs = require('fs')
const path = require('path')
// const compression = require('compression') // ! compression does not support http2
const request = require('request')
const { promisify } = require('util')

const readFile = promisify(fs.readFile)

const app = http2Express(express)
app.use(cors())
// app.use(compression())

app.get('/tiles/:z-:x-:y.png', async (req, res) => {
  const { z, x, y } = req.params
  const imgPath = `tiles/png/${z}/${x}-${y}-${z}.png`

  // console.info(req.headers['user-agent'], ': ', req.headers[':method'], imgPath)

  if (fs.existsSync(imgPath)) {
    const img = await readFile(imgPath)
    res.send(img)
    console.info(`sent hkdsm: ${imgPath}`)
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
      console.info(`sent mapbox terrain: ${imgPath}`)
    })
  }
})

app.get('/coastline.pbf', (req, res) => {
  // const dataPath = '/Users/laijackylai/Documents/hkdsm/coastline/coastline.pbf'
  const dataPath = '/home/rsmcvis/hkdsm/coastline/coastline.pbf'
  res.sendFile(dataPath)
})

app.get('/test/data.ply', async (req, res) => {
  // const dataPath = '/Users/laijackylai/Documents/hkdsm/test/test.json.lzma'
  const dataPath = '/Users/laijackylai/Documents/hkradar/test/data.ply'
  // const dataPath = '/Users/laijackylai/Documents/hkradar/test/tet.ply'
  res.sendFile(dataPath)
})

app.get('/radarData/:date/:fileName', async (req, res) => {
  const { date, fileName } = req.params
  // const basePath = '/Users/laijackylai/Documents/hkradar/'
  const basePath = '/home/rsmcvis/hkradar/'
  const filePath = basePath.concat(date).concat('/', fileName)
  res.sendFile(filePath)
})

app.get('/availableTimeslots/:radarType/:date/:dataset', async (req, res) => {
  const { radarType, date, dataset } = req.params
  if (!dataset || !date || !radarType) {
    res.send(400)
  }
  let data = ''
  if (dataset === 'radar') {
    data = 'hkradar/'
  }
  const directoryPath = path.join('/home/rsmcvis/', data, date, '/')
  const list = []
  fs.readdirSync(directoryPath).forEach(file => {
    if (file.toString().includes('.ply') && !file.toString().includes('ascii') && file.toString().includes(radarType)) {
      list.push(file.toString());
    }
  });
  const returnList = []
  for (let i = 0; i < list.length; i += 1) {
    const e = list[i]
    const s = { label: e.split('.')[0].split('_')[2].replace(date, ''), value: e }
    returnList.push(s)
  }
  returnList.sort((a, b) => parseInt(a.label, 10) - parseInt(b.label, 10))
  res.send(returnList)

  // * send data format
  // const options = [
  //   { value: 'chocolate', label: 'Chocolate' },
  //   { value: 'strawberry', label: 'Strawberry' },
  //   { value: 'vanilla', label: 'Vanilla' }
  // ];
})

const options = {
  key: fs.readFileSync('server/keys/key.pem'),
  cert: fs.readFileSync('server/keys/cert.pem'),
  allowHTTP1: true
}

const server = http2.createSecureServer(options, app)
server.listen(8001, () => console.info(`server listening on 8001`))

