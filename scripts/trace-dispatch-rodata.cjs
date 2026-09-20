const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

const func_start = 0x5cef41;
const func_end = 0x5d0500;
const text_va = 0x401000n;
const text_off = 0x1000;
const rodata_va = 0x9f2000n;
const rodata_off = 0x5f2000;

console.log(`Analyzing function from 0x${func_start.toString(16)} to 0x${func_end.toString(16)}...`);

for (let p = func_start; p < func_end; p++) {
  const insn_va = text_va + BigInt(p - text_off);
  
  // Check RIP-relative LEA (48 8d reg disp32 or 4c 8d reg disp32)
  if ((buf[p] === 0x48 || buf[p] === 0x4c) && (buf[p+1] === 0x8d || buf[p+1] === 0x8b)) {
    const modrm = buf[p+2];
    if ((modrm & 0xc7) === 0x05) { // [rip + disp32]
      const disp = buf.readInt32LE(p + 3);
      const target_va = insn_va + 7n + BigInt(disp);
      // Check if target is in rodata
      if (target_va >= rodata_va && target_va < rodata_va + 0x400000n) {
        const str_off = Number(target_va - rodata_va) + rodata_off;
        // Print snippet of string or data
        let s = buf.subarray(str_off, str_off + 60).toString('latin1').replace(/[\x00-\x1f\x7f-\x9f]/g, '.');
        console.log(`[0x${insn_va.toString(16)}] LEA/MOV [rip+0x${disp.toString(16)}] => VA 0x${target_va.toString(16)}: "${s}"`);
      }
    }
  }
}
