// reference: https://www.sohamkamani.com/nodejs/http2/#making-client-side-requests

const http2 = require('http2')
const fs = require('fs')
const router = require('./router')

// create a new server instance
const server = http2.createSecureServer({
  // we can read the certificate and private key from
  // our project directory
  key: fs.readFileSync('server/keys/key.pem'),
  cert: fs.readFileSync('server/keys/cert.pem')
})
// log any error that occurs when running the server
server.on('error', (err) => console.error(err))

// the 'stream' callback is called when a new
// stream is created. Or in other words, every time a
// new request is received
server.on('stream', router)

// start the server
server.listen(8443)