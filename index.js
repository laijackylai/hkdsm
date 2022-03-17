const { exec } = require('child_process');

exec('http-server . --cors --gzip', (err, stdout, stderr) => {
  if (err) {
    console.error(err)
    return;
  }
  console.log(`stdout: ${stdout}`);
  console.log(`stderr: ${stderr}`);
})