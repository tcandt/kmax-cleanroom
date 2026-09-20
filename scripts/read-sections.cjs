const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

const e_shoff = Number(buf.readBigUInt64LE(0x28));
const e_shentsize = buf.readUInt16LE(0x3a);
const e_shnum = buf.readUInt16LE(0x3c);
const e_shstrndx = buf.readUInt16LE(0x3e);
const shstrtab_off = Number(buf.readBigUInt64LE(e_shoff + e_shstrndx * e_shentsize + 0x18));

for (let i = 0; i < e_shnum; i++) {
  const s_off = e_shoff + i * e_shentsize;
  const name_idx = buf.readUInt32LE(s_off);
  const name = buf.toString('utf8', shstrtab_off + name_idx).split('\0')[0];
  const va = buf.readBigUInt64LE(s_off + 0x10);
  const off = buf.readBigUInt64LE(s_off + 0x18);
  const size = buf.readBigUInt64LE(s_off + 0x20);
  if (name.includes('pclntab') || name.includes('symtab') || name.includes('text')) {
    console.log(`Section: ${name}, VA: 0x${va.toString(16)}, Offset: 0x${off.toString(16)}, Size: 0x${size.toString(16)}`);
  }
}
