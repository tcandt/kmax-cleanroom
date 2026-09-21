const fs = require('fs');
const orig = fs.readFileSync('cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/index-DIPw8r74.js', 'utf8');
let idx = orig.indexOf('openDevice:');
console.log('openDevice at', idx, ':', orig.substring(idx - 100, idx + 100));

// Let's find definition of the function assigned to openDevice
// It was: openDevice:$
idx = orig.indexOf('function $(', 120000);
if (idx === -1) idx = orig.indexOf('const $=', 120000);
if (idx === -1) {
  // search for '$(' in range 120000..125000
  let r = orig.substring(120000, 125000);
  console.log('range 120000..125000 snippet:', r.substring(0, 500));
} else {
  console.log('$ at', idx, ':', orig.substring(idx - 50, idx + 300));
}
