const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

// Find string "[TouchTrace] recv"
const touchStr = Buffer.from('[TouchTrace] recv');
const strIdx = buf.indexOf(touchStr);
console.log('touchStr offset in amd64:', strIdx, '0x' + strIdx.toString(16));

// Find references to this string or its VA
// In Go 1.20+, rodata VA can be estimated from section headers or pclntab
// Let's find ELF section headers
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
  if (name === '.rodata') {
    rodata_va = va;
    rodata_off = off;
  }
  if (name === '.text') {
    text_va = va;
    text_off = off;
    text_size = size;
  }
}

console.log('rodata VA:', '0x' + rodata_va.toString(16), 'off:', '0x' + rodata_off.toString(16));
const str_va = rodata_va + BigInt(strIdx) - rodata_off;
console.log('string VA:', '0x' + str_va.toString(16));

// Find references to str_va in .text
const vaBytes = Buffer.alloc(8);
vaBytes.writeBigUInt64LE(str_va);
console.log('Looking for LE64 pointer:', vaBytes.toString('hex'));

let ref = buf.indexOf(vaBytes, Number(text_off));
console.log('Direct pointer reference at:', ref);

// Also look for LE32 low part (for RIP-relative LEA)
// In x86_64, lea reg, [rip + disp32] => disp32 = target_va - (insn_va + 7)
for (let p = Number(text_off); p < Number(text_off + text_size) - 7; p++) {
  const disp = buf.readInt32LE(p + 3);
  const insn_va = text_va + BigInt(p) - text_off;
  if (insn_va + 7n + BigInt(disp) === str_va) {
    console.log('Found RIP-relative LEA at file offset 0x' + p.toString(16), 'VA: 0x' + insn_va.toString(16));
  }
}
