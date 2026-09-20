const fs = require('fs');
const buf = fs.readFileSync('deploy_agent/cloudphone-agent-amd64');
const str = buf.toString('latin1');
const re = /json:"([^"]+)"/g;
let m;
const tags = new Set();
while ((m = re.exec(str)) !== null) {
  tags.add(m[1]);
}
console.log('All JSON tags found in agent:');
console.log(Array.from(tags).sort().join(', '));
