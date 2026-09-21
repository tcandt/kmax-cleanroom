/**
 * patch-webapp-mode-switch.cjs
 * 
 * Forensic patch for DevicePanel mode switch reactivity in cloudphone-web.
 * 
 * Problem:
 * In upstream index-DIPw8r74.js, the mode switch handler Vt() toggles the deviceMode
 * in the Pinia store, but does NOT reinitialize Se.value (shallowRef pointing to useWebRTC/useWebSocketPreview).
 * As a result, when WebRTC fails and user switches to WebSocket preview, canvas clicks/touch/keys
 * still attempt to dispatch over the closed WebRTC DataChannel.
 * 
 * Solution:
 * Extends Vt() to invoke Te.disconnect(), re-evaluate Se.value = Ue(deviceId, options),
 * re-register in store, and run yo() (connecting stream and binding event listeners).
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const BASELINE_SHA256 = '30f9494bd783a6b133ac63c3c5ad3bdb793c3cf257fb6395e78c869d755366cb';
const PATCHED_SHA256 = '0da8adfd22e40e014ed25442163c0fff9b737be5ce64b624e074fe503945af60';

const TARGET_SNIPPET = 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}';
const REPLACEMENT_SNIPPET = 'function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X);a.value&&(Te.disconnect(),Se.value=Ue(a.value,T.value),n.registerWebRTC(a.value,Te),yo())}';

const TARGET_FILES = [
  path.resolve(__dirname, '../../reconstructed_source/web-app/public/assets/index-DIPw8r74.js'),
  path.resolve(__dirname, '../../reconstructed_source/web-app/dist/assets/index-DIPw8r74.js')
];

function computeSha256(filePath) {
  const data = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

function applyPatch(filePath, isRevert = false) {
  if (!fs.existsSync(filePath)) {
    console.warn(`[WARN] File not found, skipping: ${filePath}`);
    return;
  }

  const currentHash = computeSha256(filePath);
  console.log(`Checking ${path.relative(process.cwd(), filePath)} (sha256: ${currentHash})`);

  let content = fs.readFileSync(filePath, 'utf8');

  if (isRevert) {
    if (currentHash === BASELINE_SHA256) {
      console.log('  -> Already at clean baseline. Nothing to revert.');
      return;
    }
    if (!content.includes(REPLACEMENT_SNIPPET)) {
      throw new Error(`Cannot revert: patched snippet not found in ${filePath}`);
    }
    content = content.replace(REPLACEMENT_SNIPPET, TARGET_SNIPPET);
    fs.writeFileSync(filePath, content, 'utf8');
    const newHash = computeSha256(filePath);
    if (newHash !== BASELINE_SHA256) {
      throw new Error(`Revert hash mismatch! Expected ${BASELINE_SHA256}, got ${newHash}`);
    }
    console.log(`  -> Successfully reverted to baseline (sha256: ${newHash})`);
  } else {
    if (currentHash === PATCHED_SHA256) {
      console.log('  -> Already patched with valid checksum. Skipping.');
      return;
    }
    if (currentHash !== BASELINE_SHA256) {
      console.warn(`  -> [NOTICE] File sha256 (${currentHash}) does not match exact baseline (${BASELINE_SHA256}). Checking snippet presence...`);
    }
    if (!content.includes(TARGET_SNIPPET)) {
      if (content.includes(REPLACEMENT_SNIPPET)) {
        console.log('  -> Patched snippet already present.');
        return;
      }
      throw new Error(`Target snippet for Vt() not found in ${filePath}! Bundle may have changed.`);
    }
    content = content.replace(TARGET_SNIPPET, REPLACEMENT_SNIPPET);
    fs.writeFileSync(filePath, content, 'utf8');
    const newHash = computeSha256(filePath);
    console.log(`  -> Successfully applied patch (sha256: ${newHash})`);
  }
}

const isRevert = process.argv.includes('--revert');
console.log(`=== WebApp Mode-Switch Patch Tool (${isRevert ? 'REVERT' : 'APPLY'}) ===`);
for (const file of TARGET_FILES) {
  applyPatch(file, isRevert);
}
console.log('=== Done ===\n');
