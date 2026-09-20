const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// Function at 0x5cf780 in file (VA 0x9cf780)
// Let's inspect the code from 0x5cf780 to 0x5cfb00
// We can use a simple x86 disassembler or print instructions
// Let's see what is at 0x5cf780:
console.log('Bytes at 0x5cf780:');
console.log(buf.subarray(0x5cf780, 0x5cf900).toString('hex'));

// Let's search for references to 0x9cf780 in .text
const targetVA = 0x9cf780n;
const text_va = 0x401000n;
const text_off = 0x1000;
const text_size = 0x5f0b91;

console.log('Searching for references to 0x9cf780...');
for (let p = text_off; p < text_off + text_size - 7; p++) {
  // Direct pointer in code/rodata?
  const val = buf.readBigUInt64LE(p);
  if (val === targetVA) {
    console.log(`Direct pointer to 0x9cf780 at 0x${p.toString(16)}`);
  }
  // Call / Jmp rel32 (E8 rel32 or E9 rel32)
  if (buf[p] === 0xe8 || buf[p] === 0xe9) {
    const rel = buf.readInt32LE(p + 1);
    const insn_va = text_va + BigInt(p - text_off);
    if (insn_va + 5n + BigInt(rel) === targetVA) {
      console.log(`Call/Jmp to 0x9cf780 at 0x${p.toString(16)} (VA: 0x${insn_va.toString(16)})`);
    }
  }
  // LEA rel32 (48 8d reg disp32)
  if (buf[p] === 0x48 && buf[p+1] === 0x8d) {
    const rel = buf.readInt32LE(p + 3);
    const insn_va = text_va + BigInt(p - text_off);
    if (insn_va + 7n + BigInt(rel) === targetVA) {
      console.log(`LEA to 0x9cf780 at 0x${p.toString(16)} (VA: 0x${insn_va.toString(16)})`);
    }
  }
}
