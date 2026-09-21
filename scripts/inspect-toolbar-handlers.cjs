const fs = require('fs');
const orig = fs.readFileSync('cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/index-DIPw8r74.js', 'utf8');

// Let's find keycode handlers around line 364000
let idx = orig.indexOf('sendInjectKeycode', 350000);
console.log('sendInjectKeycode at', idx, ':', orig.substring(idx - 100, idx + 200));

let idx2 = orig.indexOf('sendCommand', 350000);
console.log('sendCommand at', idx2, ':', orig.substring(idx2 - 100, idx2 + 200));
