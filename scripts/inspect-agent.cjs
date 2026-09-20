const fs = require('fs');

const buf = fs.readFileSync('deploy_agent/cloudphone-agent-arm64');
const str = buf.toString('utf8');

// Find all matches for "type" in json tags or strings
const matches = [];
let pos = 0;
while ((pos = str.indexOf('json:"type"', pos)) !== -1) {
  matches.push(str.substring(Math.max(0, pos - 100), pos + 100));
  pos += 11;
}

console.log('Matches for json:"type":', matches.length);
matches.slice(0, 10).forEach((m, i) => console.log(`[${i}] ${JSON.stringify(m)}`));
