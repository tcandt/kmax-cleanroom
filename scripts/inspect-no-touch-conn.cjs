const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// VA 0x9cfada is file offset 0x5cfada
// Let's examine instructions between 0x5cf900 and 0x5d0150
console.log('Examining 0x5cf900 - 0x5d0150:');

const start = 0x5cf900;
const end = 0x5d0150;

// Let's print disassembled assembly or instructions around 0x5cfada
// In x86_64:
// Let's check what leads up to 0x5cfada (which logs result=no-touch-conn)
// and what leads up to 0x5d00d0 (which logs write=%s err=%v)
console.log(buf.subarray(0x5cfada - 64, 0x5cfada + 64).toString('hex'));
