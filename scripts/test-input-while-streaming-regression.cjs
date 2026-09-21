/**
 * test-input-while-streaming-regression.cjs
 * 
 * Standardized regression test for Input Control while WebSocket streaming is active.
 * 
 * Requirements:
 * 1. Timeout handling instead of infinite loops (waitForStream with timeoutMs).
 * 2. Only counts valid binary frames starting with ASCII 'PREV'.
 * 3. Verifies device_id in PREV header matches TARGET_DEVICE.
 * 4. Robust lifecycle with try/finally to always send stop_preview and cleanly close socket.
 * 5. Real oracles after each action (ADB dumpsys window, agent logs).
 */

const { execSync } = require('child_process');
const WebSocket = globalThis.WebSocket;

const SIGNALING_URL = 'ws://localhost:8111/connect_client';
const TARGET_DEVICE = 'Samsung_S7';
const DEVICE_SERIAL = '192.168.1.167:5555';

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function adbShell(cmd) {
  try {
    return execSync(`adb -s ${DEVICE_SERIAL} shell "${cmd}"`, { encoding: 'utf8', timeout: 5000 }).trim();
  } catch (err) {
    return `ERROR: ${err.message}`;
  }
}

function openSocket(ws) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('WebSocket connection timed out')), 5000);
    ws.onopen = () => {
      clearTimeout(timer);
      resolve();
    };
    ws.onerror = (err) => {
      clearTimeout(timer);
      reject(err);
    };
  });
}

function waitForStream(ws, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    let frames = 0;

    const timer = setTimeout(() => {
      reject(new Error(`Preview timeout: only ${frames} PREV frames received within ${timeoutMs}ms`));
    }, timeoutMs);

    ws.onmessage = async (e) => {
      let data = e.data;
      if (typeof Blob !== 'undefined' && data instanceof Blob) {
        data = await data.arrayBuffer();
      }
      if (!(data instanceof ArrayBuffer)) return;

      const view = new DataView(data);
      if (view.byteLength < 49) return;

      const magic = String.fromCharCode(view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3));
      if (magic !== 'PREV') return;

      const devBytes = new Uint8Array(data, 4, 32);
      let deviceId = new TextDecoder('utf-8').decode(devBytes).replace(/\0+$/, '');

      if (deviceId !== TARGET_DEVICE) {
        clearTimeout(timer);
        reject(new Error(`PREV device mismatch: expected ${TARGET_DEVICE}, got ${deviceId}`));
        return;
      }

      frames++;
      if (frames >= 5) {
        clearTimeout(timer);
        resolve(frames);
      }
    };
  });
}

async function testHome(ws) {
  console.log('  -> Action: Sending Home keycode (3)...');
  // Key Down
  ws.send(JSON.stringify({
    message_type: 'group_control_event',
    target_device_ids: [TARGET_DEVICE],
    event: { type: 'inject_keycode', action: 0, keycode: 3, repeat: 0, meta: 0 }
  }));
  await sleep(50);
  // Key Up
  ws.send(JSON.stringify({
    message_type: 'group_control_event',
    target_device_ids: [TARGET_DEVICE],
    event: { type: 'inject_keycode', action: 1, keycode: 3, repeat: 0, meta: 0 }
  }));
  await sleep(500);
}

function verifyHomeOnDevice() {
  const focus = adbShell("dumpsys window | grep mCurrentFocus");
  console.log(`     [Oracle ADB] Current focus: ${focus}`);
  if (!focus.includes('launcher')) {
    throw new Error(`Oracle check failed: expected launcher to be focused, got: ${focus}`);
  }
  console.log('     [Oracle PASS] Home button verified: launcher is focused.');
}

async function testTap(ws) {
  console.log('  -> Action: Sending Tap at (540, 960)...');
  // Touch Down
  ws.send(JSON.stringify({
    message_type: 'group_control_event',
    target_device_ids: [TARGET_DEVICE],
    event: { type: 'touch', action: 0, x: 540, y: 960, w: 1080, h: 1920, id: 0 }
  }));
  await sleep(60);
  // Touch Up
  ws.send(JSON.stringify({
    message_type: 'group_control_event',
    target_device_ids: [TARGET_DEVICE],
    event: { type: 'touch', action: 1, x: 540, y: 960, w: 1080, h: 1920, id: 0 }
  }));
  await sleep(500);
}

function verifyTapEffect() {
  const agentLog = adbShell("grep -E '收到直控/群控事件: type=touch' /data/local/tmp/cloudphone-agent.log | tail -n 2");
  console.log(`     [Oracle Agent Log] Last touch events:\n${agentLog}`);
  if (!agentLog.includes('type=touch action=0') || !agentLog.includes('type=touch action=1')) {
    throw new Error('Oracle check failed: touch down/up not confirmed in agent log');
  }
  console.log('     [Oracle PASS] Tap confirmed by agent UDS injection log.');
}

async function testScroll(ws) {
  console.log('  -> Action: Sending Scroll (type="scroll", scrollV=-15)...');
  ws.send(JSON.stringify({
    message_type: 'group_control_event',
    target_device_ids: [TARGET_DEVICE],
    event: {
      type: 'scroll',
      action: 0,
      x: 540,
      y: 960,
      w: 1080,
      h: 1920,
      scrollH: 0,
      scrollV: -15
    }
  }));
  await sleep(500);
}

function verifyScrollEffect() {
  const scrollLog = adbShell("grep -E 'ScrollTrace' /data/local/tmp/cloudphone-agent.log | tail -n 1");
  console.log(`     [Oracle Agent Log] ${scrollLog}`);
  if (!scrollLog.includes('scroll=0,-15') || !scrollLog.includes('touchConn=true')) {
    throw new Error(`Oracle check failed: expected scroll trace with touchConn=true, got: ${scrollLog}`);
  }
  console.log('     [Oracle PASS] Scroll confirmed by agent ScrollTrace.');
}

async function main() {
  console.log('============================================================');
  console.log('B1: Input-While-Streaming Regression Suite (with Oracles)');
  console.log(`Target: ${TARGET_DEVICE} (${DEVICE_SERIAL}) via ${SIGNALING_URL}`);
  console.log('============================================================\n');

  // Pre-condition: Open Dialer app on phone so Home action has a distinct state change to launcher
  console.log('Setting pre-condition on Android device: launch Dialer app...');
  adbShell('am start -n com.android.dialer/.main.impl.MainActivity');
  await sleep(1000);
  const preFocus = adbShell("dumpsys window | grep mCurrentFocus");
  console.log(`Pre-condition focus: ${preFocus}\n`);

  const ws = new WebSocket(SIGNALING_URL);
  ws.binaryType = 'arraybuffer';

  try {
    await openSocket(ws);
    console.log('[1/4] WebSocket connected to signaling.');

    console.log('[2/4] Requesting start_preview...');
    ws.send(JSON.stringify({
      message_type: 'start_preview',
      type: 'start_preview',
      device_id: TARGET_DEVICE,
      fps: 30,
      max_size: 1080,
      bitrate: 4000000,
      stay_awake: false
    }));

    const initialFrames = await waitForStream(ws, 10000);
    console.log(`      Preview ready: received ${initialFrames} valid PREV frames for ${TARGET_DEVICE}.\n`);

    console.log('[3/4] Testing HOME button with OS focus oracle...');
    await testHome(ws);
    verifyHomeOnDevice();
    console.log('');

    console.log('[4/4] Testing TAP with Agent UDS oracle...');
    await testTap(ws);
    verifyTapEffect();
    console.log('');

    console.log('[5/4] Testing SCROLL with ScrollTrace touchConn oracle...');
    await testScroll(ws);
    verifyScrollEffect();
    console.log('');

    console.log('============================================================');
    console.log('ALL B1 REGRESSION TESTS & ORACLES PASSED (100%)');
    console.log('============================================================\n');
  } catch (err) {
    console.error('\n[FATAL TEST FAILURE]:', err);
    process.exit(1);
  } finally {
    console.log('Cleaning up session (finally block)...');
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        message_type: 'stop_preview',
        type: 'stop_preview',
        device_id: TARGET_DEVICE
      }));
      await sleep(200);
    }
    ws.close();
    console.log('Socket closed and preview stopped cleanly.');
  }
}

main();
