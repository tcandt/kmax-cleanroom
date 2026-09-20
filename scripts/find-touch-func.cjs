const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-arm64');
const str = buf.toString('utf8');

// Find all occurrences of "[ScrollTrace]" in pclntab / code
const p1 = buf.indexOf(Buffer.from('[ScrollTrace] recv'));
const p2 = buf.indexOf(Buffer.from('[TouchTrace] recv'));

console.log('p1 ([ScrollTrace] recv):', p1, 'p2 ([TouchTrace] recv):', p2);

// Look around p2 in the binary to see what symbols or functions are nearby
// Let's search pclntab for function names containing "Touch" or "Scroll" or "Input" or "DataChannel"
let idx = 0;
const funcs = [];
while ((idx = str.indexOf('Touch', idx)) !== -1) {
  funcs.push(str.substring(Math.max(0, idx - 30), idx + 30));
  idx += 5;
}
console.log('Touch occurrences in strings:', funcs.length);
funcs.slice(0, 15).forEach(f => console.log(JSON.stringify(f)));
