/**
 * manual-trace.js
 * 
 * Phase R5.1b — Direct Input Hot-Path Recovery & Passive Observability.
 * 
 * Strict Guarantees:
 * 1. ZERO monkey-patching on WebSocket.prototype.send or RTCDataChannel.prototype.send.
 * 2. ZERO packet modification or synthetic injection on high-frequency streams.
 * 3. NO global DOM toolbar event bridge (control routing belongs to stream controllers).
 * 4. In-memory circular ring buffer (200 events max) to prevent DevTools console overhead.
 * 5. Console output restricted to DOWN, UP, errors/drops, and 1-in-30 MOVEs.
 * 6. Interactive diagnostic helpers: window.__dumpControlTrace(), window.__dumpCoordDiag(), window.__dumpStreamStats().
 * 7. Unified Controller Session ID tracking across DevicePanel, PeerConnection, and DataChannel.
 * 8. Delta-based WebRTC stream metrics (actualFps, avgJitterBufferMs, avgDecodeMs, bitrateKbps).
 */

(function() {
  'use strict';

  // --- In-Memory Ring Buffer (Max 200 Entries) ---
  const MAX_BUFFER = 200;
  const traceBuffer = [];
  let moveLogCounter = 0;

  function pushTrace(entry) {
    entry.timestamp = Date.now();
    entry.timeStr = new Date(entry.timestamp).toISOString().substring(11, 23);
    traceBuffer.push(entry);
    if (traceBuffer.length > MAX_BUFFER) {
      traceBuffer.shift();
    }
  }

  // --- Global Session State ---
  window.__globalSessionSeq = window.__globalSessionSeq || 0;
  window.__activeSessionId = window.__activeSessionId || 0;
  window.__lastTouchTs = 0;

  // --- Diagnostic Dump API ---
  window.__dumpControlTrace = function(count = 100) {
    const slice = traceBuffer.slice(-Math.min(count, traceBuffer.length));
    console.group(`[CONTROL TRACE DUMP] Last ${slice.length} events:`);
    if (console.table) {
      console.table(slice.map(e => ({
        time: e.timeStr,
        cat: e.category,
        action: e.action || e.event || '',
        seq: e.seq ?? '-',
        sess: e.session ?? '-',
        dcSess: e.dcSession ?? '-',
        result: e.result ?? e.reason ?? '-',
        coords: (e.x !== undefined && e.y !== undefined) ? `${e.x},${e.y}` : (e.clientX !== undefined ? `${e.clientX},${e.clientY}` : '-'),
        details: typeof e.details === 'object' ? JSON.stringify(e.details) : (e.details || '')
      })));
    } else {
      slice.forEach(e => console.log(e.timeStr, e));
    }
    console.groupEnd();
    return slice;
  };

  window.__lastCoordDiag = null;
  window.__dumpCoordDiag = function() {
    console.group('[COORDINATE MAPPING DIAGNOSTIC]');
    if (window.__lastCoordDiag) {
      console.log(window.__lastCoordDiag);
    } else {
      console.log('No coordinate diagnostic recorded yet. Touch the screen to record.');
    }
    console.groupEnd();
    return window.__lastCoordDiag;
  };

  window.__streamStats = null;
  window.__dumpStreamStats = function() {
    console.group('[STREAM METRICS]');
    if (window.__streamStats) {
      console.log(window.__streamStats);
    } else {
      console.log('No stream stats collected yet.');
    }
    console.groupEnd();
    return window.__streamStats;
  };

  // --- R5.1b: Native DOM Input Observability Hook ---
  window.__recordInput = function(info) {
    const sess = info.session ?? window.__activeSessionId ?? '-';
    pushTrace({
      category: 'INPUT',
      session: sess,
      event: info.event,
      clientX: info.clientX,
      clientY: info.clientY,
      target: info.target
    });
    console.log(`[INPUT] session=${sess} event=${info.event} clientX=${info.clientX} clientY=${info.clientY}`);
  };

  // --- R5.1b: Direct Touch Observability Hook ---
  window.__recordTouchSent = function(info) {
    const panelSession = info.session ?? window.__activeSessionId;
    const dcSession = info.dcSession ?? info.dcId;
    const isStale = (info.dcSession !== undefined && info.dcSession !== null && info.dcSession !== 'ws' && info.dcSession !== panelSession);

    pushTrace({
      category: 'TOUCH',
      session: panelSession,
      dcSession: dcSession,
      pcSession: info.pcSession,
      isStale: isStale,
      action: info.action,
      seq: info.seq,
      result: 'SENT',
      dcState: info.dcState,
      dcId: info.dcId,
      pcState: info.pcState,
      bufferedAmount: info.bufferedAmount,
      x: info.x,
      y: info.y,
      w: info.w,
      h: info.h,
      overheadMs: info.overheadMs
    });

    if (isStale) {
      console.warn(
        `[STALE_CONTROLLER] panelSession=${panelSession} controllerSession=${panelSession} pcSession=${info.pcSession ?? '-'} dcSession=${dcSession}`
      );
    }

    const isDown = info.action === 'DOWN' || info.action === 0;
    const isUp = info.action === 'UP' || info.action === 1;
    const isMove = info.action === 'MOVE' || info.action === 2;

    if (isDown || isUp) {
      console.log(
        `[TOUCH] session=${panelSession} dcSession=${dcSession ?? '-'} seq=${info.seq} action=${isDown ? 'DOWN' : 'UP'} result=SENT ` +
        `dcState=${info.dcState} bufferedAmount=${info.bufferedAmount ?? 0} finalX=${info.x} finalY=${info.y} w=${info.w} h=${info.h}`
      );
    } else if (isMove) {
      moveLogCounter++;
      if (moveLogCounter % 30 === 0) {
        console.log(
          `[TOUCH] session=${panelSession} dcSession=${dcSession ?? '-'} seq=${info.seq} action=MOVE (#${moveLogCounter}) result=SENT ` +
          `dcState=${info.dcState} bufferedAmount=${info.bufferedAmount ?? 0} finalX=${info.x} finalY=${info.y}`
        );
      }
    }
  };

  window.__recordTouchDrop = function(reason, details) {
    pushTrace({
      category: 'TOUCH-DROP',
      session: window.__activeSessionId,
      reason: reason,
      result: 'DROPPED',
      details: details,
      dcState: details ? details.dcState : 'none'
    });

    console.warn(`[TOUCH-DROP] reason=${reason} dcState=${details && details.dcState ? details.dcState : 'none'}`, details);
  };

  // --- R5.1b: Controller & DataChannel Lifecycle Hooks ---
  window.__recordDcLife = function(event, session, details) {
    pushTrace({
      category: 'DC-LIFE',
      event: event,
      dcSession: session,
      details: details
    });
    console.log(`[DC-LIFE] dcSession=${session} ${event}`, details || '');
  };

  window.__recordCtrlLife = function(event, session, details) {
    pushTrace({
      category: 'CTRL-LIFE',
      event: event,
      session: session,
      details: details
    });
    console.log(`[CTRL-LIFE] panelSession=${session} ${event}`, details || '');
  };

  // --- R5.6: Coordinate Mapping Diagnostic Hook ---
  window.__recordCoordDiag = function(diag) {
    window.__lastCoordDiag = {
      timestamp: Date.now(),
      elementRect: diag.elementRect,
      videoWidth: diag.videoWidth,
      videoHeight: diag.videoHeight,
      actualW: diag.actualW,
      actualH: diag.actualH,
      offsetX: diag.offsetX,
      offsetY: diag.offsetY,
      relativeX: diag.relativeX,
      relativeY: diag.relativeY,
      finalX: diag.finalX,
      finalY: diag.finalY,
      deviceTargetW: diag.targetW,
      deviceTargetH: diag.targetH,
      rotationState: diag.isRotated ? 'rotated' : 'standard'
    };
  };

  // --- R5.1b: Low-Overhead Periodic Stream Metrics Collector with Delta Calculations ---
  let prevInboundStats = null;
  let prevInboundTime = null;

  setInterval(() => {
    const video = document.querySelector('video');
    const canvas = document.querySelector('canvas');

    if (video && video.srcObject && window.__activePeerConnection) {
      window.__activePeerConnection.getStats().then(stats => {
        stats.forEach(report => {
          if (report.type === 'inbound-rtp' && report.kind === 'video') {
            const now = Date.now();
            if (prevInboundStats && prevInboundTime) {
              const deltaTimeSec = (now - prevInboundTime) / 1000;
              if (deltaTimeSec > 0) {
                const deltaDecoded = (report.framesDecoded || 0) - (prevInboundStats.framesDecoded || 0);
                const deltaReceived = (report.framesReceived || 0) - (prevInboundStats.framesReceived || 0);
                const deltaDropped = (report.framesDropped || 0) - (prevInboundStats.framesDropped || 0);
                const deltaPackets = (report.packetsReceived || 0) - (prevInboundStats.packetsReceived || 0);
                const deltaPacketsLost = (report.packetsLost || 0) - (prevInboundStats.packetsLost || 0);
                const deltaBytes = (report.bytesReceived || 0) - (prevInboundStats.bytesReceived || 0);
                const deltaJitterDelay = (report.jitterBufferDelay || 0) - (prevInboundStats.jitterBufferDelay || 0);
                const deltaJitterEmitted = (report.jitterBufferEmittedCount || 0) - (prevInboundStats.jitterBufferEmittedCount || 0);
                const deltaDecodeTime = (report.totalDecodeTime || 0) - (prevInboundStats.totalDecodeTime || 0);

                const actualFps = Math.round((deltaDecoded / deltaTimeSec) * 10) / 10;
                const avgJitterBufferMs = deltaJitterEmitted > 0 ? Math.round((deltaJitterDelay / deltaJitterEmitted) * 1000) : 0;
                const avgDecodeMs = deltaDecoded > 0 ? Math.round((deltaDecodeTime / deltaDecoded) * 1000 * 10) / 10 : 0;
                const bitrateKbps = Math.round(((deltaBytes * 8) / deltaTimeSec) / 1000);

                window.__streamStats = {
                  timestamp: now,
                  mode: 'webrtc',
                  actualFps: actualFps,
                  avgJitterBufferMs: avgJitterBufferMs,
                  avgDecodeMs: avgDecodeMs,
                  packetLossDelta: Math.max(0, deltaPacketsLost),
                  frameDropDelta: Math.max(0, deltaDropped),
                  bitrateKbps: bitrateKbps,
                  // Raw cumulative counters for reference
                  packetsReceived: report.packetsReceived,
                  framesReceived: report.framesReceived,
                  framesDecoded: report.framesDecoded,
                  framesDropped: report.framesDropped,
                  jitter: report.jitter ? Math.round(report.jitter * 1000) : 0,
                  videoCurrentTime: video.currentTime
                };
              }
            }
            prevInboundStats = {
              framesDecoded: report.framesDecoded || 0,
              framesReceived: report.framesReceived || 0,
              framesDropped: report.framesDropped || 0,
              packetsReceived: report.packetsReceived || 0,
              packetsLost: report.packetsLost || 0,
              bytesReceived: report.bytesReceived || 0,
              jitterBufferDelay: report.jitterBufferDelay || 0,
              jitterBufferEmittedCount: report.jitterBufferEmittedCount || 0,
              totalDecodeTime: report.totalDecodeTime || 0
            };
            prevInboundTime = now;
          }
        });
      }).catch(() => {});
    } else if (canvas && canvas.width > 0 && canvas.height > 0) {
      window.__streamStats = {
        timestamp: Date.now(),
        mode: 'websocket',
        canvasWidth: canvas.width,
        canvasHeight: canvas.height
      };
    }
  }, 5000);

  console.log('[MANUAL-TRACE] Phase R5.1b Direct Input Hot-Path Recovery initialized (unified session tracking, delta metrics, native event path).');
})();
