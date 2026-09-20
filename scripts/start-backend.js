import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const backendDir = path.resolve(__dirname, '../reconstructed_source/webrtc-signaling');

console.log('[Runner] Starting Go Backend Server on port 8111...');
const child = spawn('go', ['run', './cmd/http-server', '-port', '8111', '-data', './data', '-noAuth', '-debug'], {
  cwd: backendDir,
  stdio: 'inherit',
});

child.on('error', (err) => {
  console.error('[Runner] Failed to start backend:', err);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
