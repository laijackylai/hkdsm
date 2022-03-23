// reference: https://www.sohamkamani.com/nodejs/http2/#making-client-side-requests

const http2 = require('http2');
const fs = require('fs');

const client = http2.connect('https://localhost:8443', {
  // we don't have to do this if our certificate is signed by
  // a recognized certificate authority, like LetsEncrypt
  ca: fs.readFileSync('./keys/cert.pem')
})

const req = client.request({ ':path': '/ping' })

req.setTimeout(3000, () => {
  console.info('request timed out')
  req.close()
})

req.end()

req.on('response', (headers) => {
  // we can log each response header here
  const keys = Object.keys(headers)
  keys.forEach(k => console.log(`${k}: ${headers[k]}`))
})

// To fetch the response body, we set the encoding
// we want and initialize an empty data string
req.setEncoding('utf8')
let data = ''

// append response data to the data string every time
// we receive new data chunks in the response
req.on('data', (chunk) => { data += chunk })

// Once the response is finished, log the entire data
// that we received
req.on('end', () => {
  console.log(`\n${data}`)
  // In this case, we don't want to make any more
  // requests, so we can close the session
  client.close()
})