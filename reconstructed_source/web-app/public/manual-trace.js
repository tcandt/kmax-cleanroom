/**
 * manual-trace.js
 * 
 * Phase R5 — Direct Input Hot-Path Recovery & Passive Observability.
 * 
 * Strict Guarantees:
 * 1. ZERO monkey-patching on WebSocket.prototype.send or RTCDataChannel.prototype.send.
 * 2. ZERO packet modification or synthetic injection on high-frequency streams.
 * 3. NO global DOM toolbar event bridge (control routing belongs to stream controllers).
 * 4. In-memory circular ring buffer (200 events max) to prevent DevTools console overhead.
 * 5. Console output restricted to DOWN, UP, errors/drops, and 1-in-30 MOVEs.
 * 6. Interactive diagnostic helpers: window.__dumpControlTrace(), window.__dumpCoordDiag(), window.__dumpStreamStats().
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
        gen: e.ctrlGen ?? e.dcGen ?? '-',
        result: e.result ?? e.reason ?? '-',
        coords: (e.x !== undefined && e.y !== undefined) ? `${e.x},${e.y}` : '-',
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

  // --- R5.3: Direct Touch Observability Hooks ---
  window.__recordTouchSent = function(info) {
    pushTrace({
      category: 'TOUCH',
      action: info.action,
      seq: info.seq,
      result: 'SENT',
      ctrlGen: info.ctrlGen,
      dcGen: info.dcGen,
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

    const isDown = info.action === 'DOWN' || info.action === 0;
    const isUp = info.action === 'UP' || info.action === 1;
    const isMove = info.action === 'MOVE' || info.action === 2;

    if (isDown || isUp) {
      console.log(
        `[TOUCH] seq=${info.seq} action=${isDown ? 'DOWN' : 'UP'} result=SENT ` +
        `dcState=${info.dcState} dcId=${info.dcId ?? '-'} pcState=${info.pcState ?? '-'} ` +
        `buf=${info.bufferedAmount ?? 0} x=${info.x} y=${info.y} w=${info.w} h=${info.h} ` +
        `activeGen=${info.ctrlGen ?? '-'} dcGen=${info.dcGen ?? '-'}`
      );
    } else if (isMove) {
      moveLogCounter++;
      if (moveLogCounter % 30 === 0) {
        console.log(
          `[TOUCH] seq=${info.seq} action=MOVE (#${moveLogCounter}) result=SENT ` +
          `dcState=${info.dcState} x=${info.x} y=${info.y} activeGen=${info.ctrlGen ?? '-'} dcGen=${info.dcGen ?? '-'}`
        );
      }
    }
  };

  window.__recordTouchDrop = function(reason, details) {
    pushTrace({
      category: 'TOUCH-DROP',
      reason: reason,
      result: 'DROPPED',
      details: details,
      dcState: details ? details.dcState : 'none'
    });

    console.warn(`[TOUCH-DROP] reason=${reason} dcState=${details && details.dcState ? details.dcState : 'none'}`, details);
  };

  // --- R5.4: Controller & DataChannel Lifecycle Hooks ---
  window.__recordDcLife = function(event, gen, details) {
    pushTrace({
      category: 'DC-LIFE',
      event: event,
      dcGen: gen,
      details: details
    });
    console.log(`[DC-LIFE] gen=${gen} ${event}`, details || '');
  };

  window.__recordCtrlLife = function(event, gen, details) {
    pushTrace({
      category: 'CTRL-LIFE',
      event: event,
      ctrlGen: gen,
      details: details
    });
    console.log(`[CTRL-LIFE] activeGen=${gen} ${event}`, details || '');
  };

  // --- R5.5: Pointer Event Observability Hook ---
  window.__recordPointer = function(info) {
    pushTrace({
      category: 'POINTER',
      event: info.event,
      pointerId: info.pointerId,
      buttons: info.buttons,
      target: info.target,
      insideVideo: info.insideVideo,
      ctrlGen: info.controllerGen
    });

    if (info.event === 'down' || info.event === 'up' || info.event === 'cancel') {
      console.log(
        `[POINTER] event=${info.event} pointerId=${info.pointerId ?? '-'} ` +
        `buttons=${info.buttons ?? 0} target=${info.target} insideVideo=${info.insideVideo} ` +
        `controllerGen=${info.controllerGen ?? '-'}`
      );
    }
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

  // --- R5.8: Low-Overhead Periodic Stream Metrics Collector ---
  setInterval(() => {
    const video = document.querySelector('video');
    const canvas = document.querySelector('canvas');

    if (video && video.srcObject && window.__activePeerConnection) {
      window.__activePeerConnection.getStats().then(stats => {
        stats.forEach(report => {
          if (report.type === 'inbound-rtp' && report.kind === 'video') {
            window.__streamStats = {
              timestamp: Date.now(),
              mode: 'webrtc',
              packetsReceived: report.packetsReceived,
              framesReceived: report.framesReceived,
              framesDecoded: report.framesDecoded,
              framesDropped: report.framesDropped,
              jitter: report.jitter ? Math.round(report.jitter * 1000) : 0,
              jitterBufferDelay: report.jitterBufferDelay ? Math.round(report.jitterBufferDelay * 1000) : 0,
              totalDecodeTime: report.totalDecodeTime ? Math.round(report.totalDecodeTime * 1000) : 0,
              framesPerSecond: report.framesPerSecond || 0,
              videoCurrentTime: video.currentTime
            };
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

  console.log('[MANUAL-TRACE] Phase R5 Direct Input Hot-Path Recovery initialized (zero send-interception, ring-buffer observability active).');
})();
