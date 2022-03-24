const express = require('express')
const http2Express = require('http2-express-bridge')
const http2 = require('http2')
const cors = require('cors')
const fs = require('fs')
const { promisify } = require('util')

const readFile = promisify(fs.readFile)

const app = http2Express(express)
app.use(cors())

app.get('/tiles/:z-:x-:y.png', async (req, res) => {
  const { z, x, y } = req.params
  const imgPath = `tiles/png/${z}/${x}-${y}-${z}.png`

  console.info(req.headers['user-agent'], ': ', req.headers[':method'], imgPath)

  if (fs.existsSync(imgPath)) {
    const img = await readFile(imgPath)
    res.send(img)
  }
  else {
    res.send('file not found')
  }
})

const options = {
  key: fs.readFileSync('server/keys/key.pem'),
  cert: fs.readFileSync('server/keys/cert.pem'),
  allowHTTP1: true
}

const server = http2.createSecureServer(options, app)
server.listen(3001, () => console.info(`server listening on 3001`))