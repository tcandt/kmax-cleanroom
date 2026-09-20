const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-arm64');
const str = buf.toString('utf8');

function printAround(term, len = 200) {
  let pos = 0;
  while ((pos = str.indexOf(term, pos)) !== -1) {
    console.log(`=== Found "${term}" at ${pos} ===`);
    console.log(str.substring(Math.max(0, pos - 50), pos + len));
    pos += term.length;
  }
}

printAround('json:"action"');
