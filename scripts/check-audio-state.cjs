const http = require('http');

const req = http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const list = JSON.parse(data);
      const target = list.find(p => p.url && p.url.includes('3111') && p.type === 'page');
      if (!target) {
        console.error('Target tab not found');
        return;
      }
      const ws = new WebSocket(target.webSocketDebuggerUrl);
      ws.onopen = () => {
        const code = `
          (async () => {
            const s7 = JSON.parse(window.localStorage.getItem('cloudphone_settings_Samsung_S7') || '{}');
            const pc = window.__activePeerConnection;
            let pcState = pc ? pc.connectionState : 'none';
            let iceState = pc ? pc.iceConnectionState : 'none';
            let localSdp = pc && pc.localDescription ? pc.localDescription.sdp : '';
            let remoteSdp = pc && pc.remoteDescription ? pc.remoteDescription.sdp : '';
            let offerHasAudio = remoteSdp.includes('m=audio');
            let answerHasAudio = localSdp.includes('m=audio');
            let audioTracks = pc ? pc.getReceivers().filter(r => r.track && r.track.kind === 'audio').map(r => ({
              id: r.track.id,
              enabled: r.track.enabled,
              muted: r.track.muted,
              readyState: r.track.readyState
            })) : [];
            let audioElements = Array.from(document.querySelectorAll('audio')).map(a => ({
              src: a.src,
              hasSrcObject: !!a.srcObject,
              muted: a.muted,
              volume: a.volume,
              paused: a.paused,
              readyState: a.readyState
            }));

            let remoteAudioSdp = '';
            let localAudioSdp = '';
            if (pc && pc.remoteDescription) {
              const lines = pc.remoteDescription.sdp.split('\\n');
              let inAudio = false;
              for (let i = 0; i < lines.length; i++) {
                const l = lines[i].trim();
                if (l.indexOf('m=audio') === 0) inAudio = true;
                else if (l.indexOf('m=') === 0 && inAudio) inAudio = false;
                if (inAudio) remoteAudioSdp += l + '\\n';
              }
            }
            if (pc && pc.localDescription) {
              const lines = pc.localDescription.sdp.split('\\n');
              let inAudio = false;
              for (let i = 0; i < lines.length; i++) {
                const l = lines[i].trim();
                if (l.indexOf('m=audio') === 0) inAudio = true;
                else if (l.indexOf('m=') === 0 && inAudio) inAudio = false;
                if (inAudio) localAudioSdp += l + '\\n';
              }
            }

            return {
              s7Settings: {
                audio: s7.audio,
                audioSource: s7.audioSource,
                audioGain: s7.audioGain,
                pageAudioMuted: s7.pageAudioMuted
              },
              pcState,
              iceState,
              offerHasAudio,
              answerHasAudio,
              audioTracks,
              audioElements,
              remoteAudioSdp,
              localAudioSdp
            };
          })()
        `;
        ws.send(JSON.stringify({
          id: 1,
          method: 'Runtime.evaluate',
          params: { expression: code, returnByValue: true, awaitPromise: true }
        }));
      };
      ws.onmessage = (msg) => {
        const resp = JSON.parse(msg.data);
        console.log('FULL RESP:');
        console.log(JSON.stringify(resp, null, 2));
        ws.close();
      };
      ws.onerror = (err) => console.error('WS error:', err);
    } catch (e) {
      console.error('Parse error:', e);
    }
  });
});
req.on('error', (err) => console.error('HTTP error:', err));
