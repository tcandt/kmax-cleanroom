const fs = require('fs');
const orig = fs.readFileSync('cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/index-DIPw8r74.js', 'utf8');

// Let's find where DevicePanel is referenced in template
// Let's search for "DevicePanel" or references to the component
let matches = [];
let idx = 0;
while ((idx = orig.indexOf('activeDeviceIds', idx)) !== -1) {
  matches.push({ idx, snippet: orig.substring(idx - 50, idx + 150) });
  idx += 15;
}
console.log('Matches for activeDeviceIds:', JSON.stringify(matches, null, 2));
