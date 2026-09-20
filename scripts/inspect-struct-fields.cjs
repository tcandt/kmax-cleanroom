const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// In Go 1.18+, type descriptors have struct field information
// Let's search for "struct { id " or "struct { type " or "struct { seq "
const patterns = ['struct { id', 'struct { seq', 'struct { type', 'struct { x', 'struct { action', '[TouchTrace]', '[ScrollTrace]'];

const str = buf.toString('latin1');
for (const p of patterns) {
  let pos = 0;
  while ((pos = str.indexOf(p, pos)) !== -1) {
    console.log(`Found "${p}" at ${pos} (0x${pos.toString(16)})`);
    console.log(str.substring(pos, pos + 300).replace(/[\x00-\x1f\x7f-\x9f]/g, '.'));
    pos += p.length + 1;
  }
}
