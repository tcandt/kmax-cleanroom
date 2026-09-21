const fs = require('fs');
const orig = fs.readFileSync('cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/index-DIPw8r74.js', 'utf8');

let idx = 0;
while ((idx = orig.indexOf('sendInjectKeycode', idx)) !== -1) {
  console.log('sendInjectKeycode at', idx, ':', orig.substring(idx - 50, idx + 150));
  idx += 17;
}
