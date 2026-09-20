const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// Scan backwards from 0x5cf1d5
let p = 0x5cf1d5;
while (p > 0x5c0000) {
  // Go function prologue typically starts with:
  // 49 3b 66 10 (cmp rsp, [r14+0x10])
  // or 4c 8d a4 24 ... 4d 3b 66 10
  if (buf[p] === 0x49 && buf[p+1] === 0x3b && buf[p+2] === 0x66 && buf[p+3] === 0x10) {
    console.log(`Prologue 49 3b 66 10 at 0x${p.toString(16)} (VA: 0x${(p + 0x400000).toString(16)})`);
    break;
  }
  if (buf[p] === 0x4d && buf[p+1] === 0x3b && buf[p+2] === 0x66 && buf[p+3] === 0x10) {
    // Check backwards a few bytes for 4c 8d a4 24
    let start = p - 7;
    console.log(`Prologue 4d 3b 66 10 at 0x${p.toString(16)}, func start ~0x${start.toString(16)} (VA: 0x${(start + 0x400000).toString(16)})`);
    break;
  }
  p--;
}

// Also find who calls or creates this function / goroutine!
