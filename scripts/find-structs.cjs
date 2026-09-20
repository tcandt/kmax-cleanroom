const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');
const str = buf.toString('latin1');

// Find all struct definitions with these tags
function findStructsWithTag(tag) {
  let pos = 0;
  while ((pos = str.indexOf(`json:"${tag}"`, pos)) !== -1) {
    // print 200 bytes backwards and forwards
    console.log(`=== Struct around json:"${tag}" at offset ${pos} (0x${pos.toString(16)}) ===`);
    console.log(str.substring(Math.max(0, pos - 200), pos + 200).replace(/[\x00-\x1f\x7f-\x9f]/g, '.'));
    pos += tag.length + 7;
  }
}

console.log('--- Structs with json:"client_ts_ms" ---');
findStructsWithTag('client_ts_ms');

console.log('--- Structs with json:"scroll_h" ---');
findStructsWithTag('scroll_h');

console.log('--- Structs with json:"event" ---');
findStructsWithTag('event');
