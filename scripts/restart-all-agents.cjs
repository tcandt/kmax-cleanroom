const { execSync } = require('child_process');
const path = require('path');

const devices = [
  { ip: '48', id: 'Samsung_S7_48' },
  { ip: '54', id: 'Samsung_S7_54' },
  { ip: '66', id: 'Samsung_S7_66' },
  { ip: '73', id: 'Samsung_S7_73' },
  { ip: '96', id: 'Samsung_S7_96' },
  { ip: '97', id: 'Samsung_S7_97' },
  { ip: '134', id: 'Samsung_S7_134' },
  { ip: '153', id: 'Samsung_S7_153' },
  { ip: '167', id: 'Samsung_S7' },
  { ip: '178', id: 'Samsung_S7_178' },
  { ip: '180', id: 'Samsung_S7_180' },
  { ip: '182', id: 'Samsung_S7_182' },
  { ip: '238', id: 'Samsung_S7_238' },
];

const hostIp = '192.168.1.163';
const signaling = `ws://${hostIp}:8111/register_agent`;
const runBat = path.resolve(__dirname, '../deploy_agent/run.bat');

console.log(`[Restart-All] Starting clean restart of agents on all ${devices.length} devices...`);

for (const dev of devices) {
  const serial = `192.168.1.${dev.ip}:5555`;
  console.log(`\n[*] Connecting & restarting ${dev.id} (${serial})...`);
  try {
    execSync(`adb connect ${serial}`, { stdio: 'ignore', timeout: 5000 });
    const cmd = `cmd.exe /c "${runBat} ${serial} -id ${dev.id} -signaling ${signaling}"`;
    const out = execSync(cmd, { encoding: 'utf-8', timeout: 15000 });
    const ok = out.includes('[OK] Agent started successfully');
    console.log(`[+] ${dev.id}: ${ok ? 'STARTED OK' : 'OUTPUT: ' + out.trim()}`);
  } catch (err) {
    console.error(`[-] ${dev.id} failed: ${err.message}`);
  }
}

console.log('\n[Restart-All] Finished!');
