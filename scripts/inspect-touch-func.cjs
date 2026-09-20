const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// Look for function entry near 0x9cfada (file offset 0x5cfada)
// Scan backwards for function prologue: 49 3b 66 10 (cmp rsp, [r14+0x10])
let start = 0x5cfada;
while (start > 0x5cf000) {
  if (buf[start] === 0x49 && buf[start+1] === 0x3b && buf[start+2] === 0x66 && buf[start+3] === 0x10) {
    console.log('Function start at file offset: 0x' + start.toString(16), 'VA: 0x' + (start + 0x400000).toString(16));
    break;
  }
  start--;
}

// Let's print the bytes around 0x5cfada to see what is happening!
console.log('Bytes from 0x5cf900 to 0x5cfc00:');
console.log(buf.subarray(0x5cf900, 0x5cfc00).toString('hex'));
