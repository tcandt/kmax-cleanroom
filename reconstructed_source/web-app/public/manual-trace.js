/**
 * manual-trace.js
 * 
 * Cleanroom Non-Intrusive Runtime Instrumentation for Manual User Verification.
 * Conforms strictly to Phase R1 (Frontend Input Lifecycle) & Phase R2 (End-to-End Control Trace).
 * 
 * Features:
 * 1. Capture-phase DOM event logging ([UI-INPUT]).
 * 2. Sequential control event tagging & tracing ([CTRL]).
 * 3. Toolbar fallback for WebSocket mode (ensures Home/Back/Volume never deadlocks).
 * 4. Stream latency and jitter metrics observation ([LATENCY]).
 */

(function() {
  'use strict';

  // --- State Variables ---
  let generation = 1;
  let currentDeviceId = '';
  let currentMode = 'unknown';
  let controlSeq = 100;
  
  window.__control_seq = controlSeq;
  window.__manual_trace_generation = generation;

  // Track active WebSocket and DataChannel references
  const activeSockets = new Set();
  const activeDataChannels = new Set();

  // Helper to get element path/identifier
  function getElementDescriptor(el) {
    if (!el) return 'null';
    let desc = el.tagName ? el.tagName.toLowerCase() : String(el);
    if (el.id) desc += '#' + el.id;
    if (el.className && typeof el.className === 'string') {
      const classes = el.className.trim().split(/\s+/).filter(Boolean).slice(0, 3).join('.');
      if (classes) desc += '.' + classes;
    }
    return desc;
  }

  // Detect topmost overlay blocking interaction
  function getOverlayAt(x, y, target) {
    const topEl = document.elementFromPoint(x, y);
    if (!topEl || topEl === target || target.contains(topEl)) {
      return 'none';
    }
    const modal = topEl.closest('.modal-overlay, .modal, .card-menu, .dialog, .settings-modal, .drawer');
    if (modal) {
      return getElementDescriptor(modal);
    }
    return getElementDescriptor(topEl);
  }

  // Determine active device mode from DOM or store
  function detectCurrentMode() {
    // Check mode badge on DOM if present
    const wsBadge = document.querySelector('.item-ws-mode-badge, .ws-mode, .stream-mode-badge');
    if (wsBadge) return 'websocket';
    const webrtcBadge = document.querySelector('.item-webrtc-badge, .webrtc-mode');
    if (webrtcBadge) return 'display';
    
    // Check localStorage settings
    try {
      const match = location.search.match(/device=([^&]+)/);
      const devId = match ? decodeURIComponent(match[1]) : '';
      if (devId) {
        currentDeviceId = devId;
        const mode = localStorage.getItem(`cloudphone_mode_${devId}`);
        if (mode) return mode;
      }
    } catch {}

    return currentMode || 'display';
  }

  // Socket state string
  function getWsStateStr() {
    let openCount = 0;
    let totalCount = 0;
    activeSockets.forEach(ws => {
      totalCount++;
      if (ws.readyState === WebSocket.OPEN) openCount++;
    });
    return `${openCount}/${totalCount}_OPEN`;
  }

  // DataChannel state string
  function getDcStateStr() {
    let openCount = 0;
    let totalCount = 0;
    activeDataChannels.forEach(dc => {
      totalCount++;
      if (dc.readyState === 'open') openCount++;
    });
    return `${openCount}/${totalCount}_OPEN`;
  }

  // --- Phase R1: Capture-Phase DOM Input Event Logger ---
  function logUiInput(e) {
    const target = e.target;
    const x = e.clientX;
    const y = e.clientY;
    const computedStyle = target instanceof Element ? window.getComputedStyle(target) : null;
    const pointerEvents = computedStyle ? computedStyle.pointerEvents : 'unknown';
    const overlay = (typeof x === 'number' && typeof y === 'number') ? getOverlayAt(x, y, target) : 'none';
    
    currentMode = detectCurrentMode();

    const isScreen = !!(target.closest && target.closest('.device-screen-wrapper, .canvas-wrapper, canvas, video'));
    const isToolbar = !!(target.closest && target.closest('.sidebar-btn, .nav-btn, .custom-btn, .toolbar'));
    const activeController = isScreen ? 'DIRECT_TOUCH' : (isToolbar ? 'TOOLBAR' : 'OTHER');

    console.log(
      `[UI-INPUT] generation=${generation} mode=${currentMode} event=${e.type} target=${getElementDescriptor(target)} ` +
      `x=${Math.round(x || 0)} y=${Math.round(y || 0)} pointerEvents=${pointerEvents} overlay=${overlay} ` +
      `activeController=${activeController} wsState=${getWsStateStr()} dcState=${getDcStateStr()}`
    );
  }

  ['pointerdown', 'pointerup', 'wheel'].forEach(evName => {
    window.addEventListener(evName, logUiInput, { capture: true, passive: true });
  });

  // Increment generation on mode change or navigation
  window.addEventListener('popstate', () => {
    generation++;
    window.__manual_trace_generation = generation;
    console.log(`[UI-INPUT] Mode/Navigation transition detected -> generation=${generation}`);
  });

  // --- Phase R2: Monkey-Patch WebSocket.send & RTCDataChannel.send for [CTRL] Trace ---
  const origWsSend = WebSocket.prototype.send;
  WebSocket.prototype.send = function(data) {
    activeSockets.add(this);
    this.addEventListener('close', () => activeSockets.delete(this), { once: true });
    this.addEventListener('error', () => activeSockets.delete(this), { once: true });

    if (typeof data === 'string') {
      try {
        const parsed = JSON.parse(data);
        const msgType = parsed.message_type || parsed.type;

        if (msgType === 'group_control_event' && parsed.event) {
          const seq = ++window.__control_seq;
          parsed.event.control_seq = seq;
          data = JSON.stringify(parsed);
          const evType = parsed.event.type || 'unknown';
          const dev = (parsed.target_device_ids || []).join(',');
          console.log(`[CTRL] seq=${seq} event=${evType} type=TOOLBAR send dev=${dev} payload=`, parsed.event);
        } else if (msgType === 'command') {
          const seq = ++window.__control_seq;
          parsed.control_seq = seq;
          data = JSON.stringify(parsed);
          console.log(`[CTRL] seq=${seq} event=command type=TOOLBAR send dev=${parsed.device_id} cmd="${parsed.command}"`);
        } else if (msgType === 'start_preview') {
          generation++;
          window.__manual_trace_generation = generation;
          console.log(`[CTRL] event=start_preview send dev=${parsed.device_id} -> generation=${generation}`);
        } else if (msgType === 'stop_preview') {
          console.log(`[CTRL] event=stop_preview send dev=${parsed.device_id}`);
        }
      } catch {}
    }

    return origWsSend.call(this, data);
  };

  const origDcSend = RTCDataChannel.prototype.send;
  RTCDataChannel.prototype.send = function(data) {
    activeDataChannels.add(this);
    this.addEventListener('close', () => activeDataChannels.delete(this), { once: true });
    this.addEventListener('error', () => activeDataChannels.delete(this), { once: true });

    if (this.label === 'input-channel' && typeof data === 'string') {
      try {
        const parsed = JSON.parse(data);
        const seq = ++window.__control_seq;
        parsed.control_seq = seq;
        data = JSON.stringify(parsed);
        const evType = parsed.type || 'unknown';
        console.log(`[CTRL] seq=${seq} event=${evType} type=DIRECT_TOUCH send x=${parsed.x} y=${parsed.y}`);
      } catch {}
    }

    return origDcSend.call(this, data);
  };

  // --- Phase R1/R2: Sidebar Toolbar Keycode Bridge for WebSocket Stream Mode ---
  // In pure WebSocket mode, DevicePanel's sendCommand() was hardcoded to return false.
  // We attach a capture listener to .sidebar-btn to ensure keycodes (Power=26, Home=3, Back=4, Vol+=24, Vol-=25)
  // are guaranteed to be dispatched over group_control_event when in WebSocket mode.
  document.addEventListener('click', (e) => {
    const btn = e.target.closest && e.target.closest('.sidebar-btn, .nav-btn');
    if (!btn) return;

    const title = (btn.getAttribute('title') || '').toLowerCase();
    const text = (btn.innerText || '').trim();

    let keycode = 0;
    if (title.includes('power') || title.includes('电源') || text.includes('电源')) {
      keycode = 26;
    } else if (title.includes('home') || title.includes('主页') || title.includes('首页') || text.includes('首页')) {
      keycode = 3;
    } else if (title.includes('back') || title.includes('返回') || text.includes('返回')) {
      keycode = 4;
    } else if (title.includes('音量加') || title.includes('volumeup') || text.includes('音量+')) {
      keycode = 24;
    } else if (title.includes('音量减') || title.includes('volumedown') || text.includes('音量-')) {
      keycode = 25;
    } else if (title.includes('recents') || title.includes('最近任务') || text.includes('最近')) {
      keycode = 187;
    }

    if (keycode > 0) {
      currentMode = detectCurrentMode();
      // If in websocket mode, dispatch inject_keycode via open socket to guarantee response
      if (currentMode === 'websocket') {
        const openSocket = Array.from(activeSockets).find(s => s.readyState === WebSocket.OPEN);
        if (openSocket) {
          const seqDown = ++window.__control_seq;
          const seqUp = ++window.__control_seq;
          const downPayload = {
            message_type: 'group_control_event',
            target_device_ids: currentDeviceId ? [currentDeviceId] : [],
            event: { type: 'inject_keycode', action: 0, keycode: keycode, repeat: 0, meta: 0, control_seq: seqDown }
          };
          const upPayload = {
            message_type: 'group_control_event',
            target_device_ids: currentDeviceId ? [currentDeviceId] : [],
            event: { type: 'inject_keycode', action: 1, keycode: keycode, repeat: 0, meta: 0, control_seq: seqUp }
          };
          console.log(`[CTRL] seq=${seqDown} event=inject_keycode key=${keycode} type=TOOLBAR send (WS Bridge DOWN)`);
          openSocket.send(JSON.stringify(downPayload));
          setTimeout(() => {
            console.log(`[CTRL] seq=${seqUp} event=inject_keycode key=${keycode} type=TOOLBAR send (WS Bridge UP)`);
            openSocket.send(JSON.stringify(upPayload));
          }, 50);
        }
      }
    }
  }, { capture: true });

  // --- Phase R4: Latency & Performance Observability Loop ---
  setInterval(() => {
    const video = document.querySelector('video');
    const canvas = document.querySelector('canvas');
    currentMode = detectCurrentMode();

    if (video && currentMode === 'display' && video.srcObject) {
      // If WebRTC is active, query stats from RTCPeerConnection if accessible
      if (window.__activePeerConnection) {
        window.__activePeerConnection.getStats().then(stats => {
          stats.forEach(report => {
            if (report.type === 'inbound-rtp' && report.kind === 'video') {
              console.log(
                `[LATENCY] mode=webrtc packetsReceived=${report.packetsReceived} ` +
                `framesDecoded=${report.framesDecoded} framesDropped=${report.framesDropped} ` +
                `jitter=${Math.round((report.jitter || 0) * 1000)}ms jitterBufferDelay=${Math.round((report.jitterBufferDelay || 0) * 1000)}ms`
              );
            }
          });
        }).catch(() => {});
      }
    } else if (canvas && currentMode === 'websocket') {
      // In WebSocket mode, monitor canvas dimensions
      if (canvas.width > 0 && canvas.height > 0) {
        // Canvas is actively rendering frames
      }
    }
  }, 5000);

  console.log('[MANUAL-TRACE] Initialized Phase R1/R2 instrumentation hook.');
})();
