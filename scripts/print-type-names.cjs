const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');

const rodata_va = 0x9f2000n;
const rodata_off = 0x5f2000;

function printGoType(va) {
  const off = Number(va - rodata_va) + rodata_off;
  if (off < 0 || off + 48 > buf.length) {
    console.log(`VA 0x${va.toString(16)} out of range`);
    return;
  }
  // In Go 1.18+, type struct:
  // size uintptr (8 bytes)
  // ptrdata uintptr (8 bytes)
  // hash uint32 (4 bytes)
  // tflag uint8 (1 byte)
  // align uint8 (1 byte)
  // fieldAlign uint8 (1 byte)
  // kind uint8 (1 byte)
  // equal func
  // gcdata *byte
  // str int32 (offset to name)
  // ptrToThis int32
  const size = buf.readBigUInt64LE(off);
  const kind = buf[off + 23] & 0x1f;
  const strOff = buf.readInt32LE(off + 40);
  // name is at rodata_off + (va + 40 + strOff - rodata_va)
  const name_va = va + 40n + BigInt(strOff);
  const name_off = Number(name_va - rodata_va) + rodata_off;
  let name = '(cannot read)';
  if (name_off >= 0 && name_off < buf.length) {
    // In Go, type name prefix has 1-2 bytes length
    const len = buf[name_off + 1];
    name = buf.subarray(name_off + 2, name_off + 2 + len).toString('utf8');
  }
  console.log(`Type at VA 0x${va.toString(16)}: size=${size} kind=${kind} name="${name}"`);
}

const vas = [0xa4ddc0n, 0xa4de40n, 0xa4dd40n, 0xa4e000n, 0xa4dc80n, 0xa4dcc0n, 0xa4de00n, 0xb0c7e0n];
vas.forEach(printGoType);
