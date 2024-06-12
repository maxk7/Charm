const https = require('https');
const fs = require('fs');
const path = require('path');

const filesToCheck = [
  {
    url: 'https://unpkg.com/hydra-synth@1.3.29/dist/hydra-synth.js',
    localPath: path.join(__dirname, 'js', 'hydra-synth.js')
  },
  {
    url: 'https://cdn.socket.io/4.0.0/socket.io.min.js',
    localPath: path.join(__dirname, 'js', 'socket.io.min.js')
  }
];

function downloadFile(url, localPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(localPath);
    https.get(url, function(response) {
      response.pipe(file);
      file.on('finish', function() {
        file.close();
        console.log(`Downloaded: ${localPath}`);
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(localPath); // Delete the file async. (But we don't check the result)
      reject(err);
    });
  });
}

function checkForUpdates() {
  return Promise.all(filesToCheck.map(file => {
    const { url, localPath } = file;

    return new Promise((resolve, reject) => {
      https.get(url, function(response) {
        const newLastModified = response.headers['last-modified'];
        fs.stat(localPath, (err, stats) => {
          if (err || !stats.mtime || new Date(newLastModified) > stats.mtime) {
            console.log(`Updating ${localPath}...`);
            downloadFile(url, localPath).then(resolve).catch(reject);
          } else {
            console.log(`${localPath} is up to date.`);
            resolve();
          }
        });
      }).on('error', reject);
    });
  }));
}

module.exports = { checkForUpdates };
