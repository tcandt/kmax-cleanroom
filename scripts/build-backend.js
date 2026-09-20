import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const backendDir = path.resolve(__dirname, '../reconstructed_source/webrtc-signaling');

console.log('[Runner] Building Go Backend (http-server.exe)...');
const child = spawn('go', ['build', '-o', 'bin/http-server.exe', './cmd/http-server'], {
  cwd: backendDir,
  stdio: 'inherit',
});

child.on('error', (err) => {
  console.error('[Runner] Failed to build backend:', err);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
