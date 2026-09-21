const fs = require('fs');
const orig = fs.readFileSync('cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/index-DIPw8r74.js', 'utf8');

let idx = 0;
while ((idx = orig.indexOf('/connect_client', idx)) !== -1) {
  console.log('connect_client at', idx, ':', orig.substring(idx - 100, idx + 300));
  idx += 15;
}
