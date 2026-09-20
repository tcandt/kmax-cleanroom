const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// VA of strings in amd64:
// In amd64: text_off = 0x1000, text_va = 0x401000.
// rodata_va = 0x76c000, rodata_off = 0x36c000.
// str 0x78b381 => va = 0x76c000 + (0x78b381 - 0x36c000) = 0xb8b381.
// Let's verify rodata_va and rodata_off from section headers:

const e_shoff = Number(buf.readBigUInt64LE(0x28));
const e_shentsize = buf.readUInt16LE(0x3a);
const e_shnum = buf.readUInt16LE(0x3c);
const e_shstrndx = buf.readUInt16LE(0x3e);
const shstrtab_off = Number(buf.readBigUInt64LE(e_shoff + e_shstrndx * e_shentsize + 0x18));

let rodata_va = 0n, rodata_off = 0n;
let text_va = 0n, text_off = 0n, text_size = 0n;

for (let i = 0; i < e_shnum; i++) {
  const s_off = e_shoff + i * e_shentsize;
  const name_idx = buf.readUInt32LE(s_off);
  const name = buf.toString('utf8', shstrtab_off + name_idx).split('\0')[0];
  const va = buf.readBigUInt64LE(s_off + 0x10);
  const off = buf.readBigUInt64LE(s_off + 0x18);
  const size = buf.readBigUInt64LE(s_off + 0x20);
  if (name === '.rodata') { rodata_va = va; rodata_off = off; }
  if (name === '.text') { text_va = va; text_off = off; text_size = size; }
}

console.log('rodata_va:', rodata_va.toString(16), 'rodata_off:', rodata_off.toString(16));
console.log('text_va:', text_va.toString(16), 'text_off:', text_off.toString(16), 'text_size:', text_size.toString(16));

function findRefsToStr(strOffset) {
  const str_va = rodata_va + BigInt(strOffset) - rodata_off;
  console.log(`Searching references for str offset 0x${strOffset.toString(16)} (VA: 0x${str_va.toString(16)})`);
  for (let p = Number(text_off); p < Number(text_off + text_size) - 7; p++) {
    const disp = buf.readInt32LE(p + 3);
    const insn_va = text_va + BigInt(p) - text_off;
    if (insn_va + 7n + BigInt(disp) === str_va) {
      console.log(`Found RIP-relative LEA at file offset 0x${p.toString(16)} (VA: 0x${insn_va.toString(16)})`);
    }
  }
}

findRefsToStr(0x78b381);
findRefsToStr(0x78b7b8);
findRefsToStr(0x787a14);
