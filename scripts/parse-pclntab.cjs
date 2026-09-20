const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

const pTabOff = 0x870ac0;
console.log('Magic bytes at pTabOff:', buf.subarray(pTabOff, pTabOff + 8).toString('hex'));

const ptrsize = buf[pTabOff + 7];
const nfunc = Number(buf.readBigUInt64LE(pTabOff + 8));
const nfiles = Number(buf.readBigUInt64LE(pTabOff + 16));
const funcnameOffset = Number(buf.readBigUInt64LE(pTabOff + 24));
const cuOffset = Number(buf.readBigUInt64LE(pTabOff + 32));
const filetabOffset = Number(buf.readBigUInt64LE(pTabOff + 40));
const pctabOffset = Number(buf.readBigUInt64LE(pTabOff + 48));
const pclnOffset = Number(buf.readBigUInt64LE(pTabOff + 56));

console.log({ ptrsize, nfunc, funcnameOffset, pclnOffset });

const text_va = 0x401000;
const targetVA = 0x9cfada;

function getCString(off) {
  let end = off;
  while (buf[end] !== 0) end++;
  return buf.toString('utf8', off, end);
}

// In Go 1.18+:
// pclnOffset points to array of:
// [entryOff (uint32), funcOff (uint32)]
// If Go 1.20: entry is uint32 (offset from text_va)
let matchFunc = null;
let prevEntry = 0, prevName = '';

for (let i = 0; i < nfunc; i++) {
  const off = pTabOff + pclnOffset + i * 8;
  const entryOff = buf.readUInt32LE(off);
  const funcOff = buf.readUInt32LE(off + 4);
  const entryVA = text_va + entryOff;
  
  const funcDataOff = pTabOff + funcOff;
  const nameOff = buf.readUInt32LE(funcDataOff + 4); // name offset in funcname table
  const funcName = getCString(pTabOff + funcnameOffset + nameOff);
  
  if (entryVA <= targetVA) {
    prevEntry = entryVA;
    prevName = funcName;
  } else {
    console.log(`Target VA 0x${targetVA.toString(16)} is in function:`);
    console.log(`  Entry: 0x${prevEntry.toString(16)} Name: ${prevName}`);
    console.log(`  Next func entry: 0x${entryVA.toString(16)} Name: ${funcName}`);
    break;
  }
}
