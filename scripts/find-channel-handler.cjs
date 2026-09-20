const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-arm64');

// Search for the string "input-channel" in rodata
const inputChStr = Buffer.from('input-channel');
const idx = buf.indexOf(inputChStr);
console.log('Found "input-channel" at offset:', idx, '(0x' + idx.toString(16) + ')');

// In ELF AMD64 / ARM64, find references to this offset or virtual address
// Let's inspect pclntab to find functions in the agent
const strings = buf.toString('utf8');
const lines = [];
let i = 0;
while (true) {
  const p = strings.indexOf('[TouchTrace]', i);
  if (p === -1) break;
  lines.push(`TouchTrace at ${p}: ` + strings.substring(p, p + 100));
  i = p + 1;
}
console.log(lines);
