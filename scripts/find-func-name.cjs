const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// Parse Go pclntab
// Find pclntab magic: \xfb\xff\xff\xff\x00\x00 (Go 1.18+) or \xfa\xff\xff\xff\x00\x00 (Go 1.16/1.17)
const magic118 = Buffer.from([0xfb, 0xff, 0xff, 0xff, 0x00, 0x00]);
const magic120 = Buffer.from([0xf1, 0xff, 0xff, 0xff, 0x00, 0x00]);
const magic116 = Buffer.from([0xfa, 0xff, 0xff, 0xff, 0x00, 0x00]);

let pTabOff = buf.indexOf(magic118);
if (pTabOff === -1) pTabOff = buf.indexOf(magic120);
if (pTabOff === -1) pTabOff = buf.indexOf(magic116);

console.log('pclntab offset:', pTabOff, '0x' + pTabOff.toString(16));

// In Go 1.18+:
// [0..5] magic
// [6] ptrsize
// [7] quantum
// [8..15] nfunc (uintptr)
// [16..23] nfiles
// [24..31] funcnameOffset
// [32..39] cuOffset
// [40..47] filetabOffset
// [48..55] pctabOffset
// [56..63] pclnOffset
// [64..71] funcdataOffset

const ptrsize = buf[pTabOff + 6];
const quantum = buf[pTabOff + 7];
const nfunc = Number(buf.readBigUInt64LE(pTabOff + 8));
const funcnameOffset = Number(buf.readBigUInt64LE(pTabOff + 24));
const pclnOffset = Number(buf.readBigUInt64LE(pTabOff + 56));

console.log('ptrsize:', ptrsize, 'nfunc:', nfunc);

// Search through func array
// In Go 1.18+, pclnOffset has array of func entries:
// Each entry has: entryOff (uint32), funcOff (uint32)
// Or entry is uintptr (8 bytes) + funcOff (uint32)...
// Let's check format:
// Entry 0 is at pTabOff + pclnOffset
const targetVA = 0x9cfada;
const text_va = 0x401000;

for (let i = 0; i < nfunc; i++) {
  const fOff = pTabOff + pclnOffset + i * 8; // 2 uint32s or uint64?
  if (fOff + 16 > buf.length) break;
  // Let's check entry VA
  const entryOff = buf.readUInt32LE(fOff);
  const funcOff = buf.readUInt32LE(fOff + 4);
  const entryVA = text_va + entryOff;
  
  if (i < 10) {
    console.log(`Func ${i}: entryVA=0x${entryVA.toString(16)} funcOff=0x${funcOff.toString(16)}`);
  }
}
