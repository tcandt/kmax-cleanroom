const http = require('http');
const { execSync } = require('child_process');

function getAgentLog() {
  try {
    return execSync('adb -s 192.168.1.182:5555 shell tail -n 15 /data/local/tmp/cloudphone-agent.log', { encoding: 'utf8' }).trim();
  } catch (e) {
    return 'LOG ERROR: ' + e.message;
  }
}

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const list = JSON.parse(data);
    const target = list.find(p => p.url && p.url.includes('3111'));
    if (!target) return;
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      // Find mode button and click it to switch back to WebRTC
      const code = `
        (() => {
          const btn = Array.from(document.querySelectorAll('button.sidebar-btn')).find(b => {
            const t = b.innerText || '';
            const title = b.getAttribute('title') || '';
            return t.includes('WS') || title.includes('WebRTC') || title.includes('display');
          });
          if (btn) {
            btn.click();
            return { clicked: true, title: btn.getAttribute('title'), text: btn.innerText };
          }
          // Alternative: find any button with title mentioning 切换
          const anyBtn = Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('title') || '').includes('切换'));
          if (anyBtn) {
            anyBtn.click();
            return { clicked: true, title: anyBtn.getAttribute('title'), text: anyBtn.innerText };
          }
          return { clicked: false };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };

    let step = 0;
    ws.onmessage = (msg) => {
      const resp = JSON.parse(msg.data);
      if (resp.id === 1) {
        console.log('Switch back click:', resp.result.result.value);

        const interval = setInterval(() => {
          step++;
          const checkCode = `
            (() => {
              const video = document.querySelector('video');
              const canvas = document.querySelector('canvas.video-stream');
              return {
                mode: window.__deviceModes ? window.__deviceModes['Samsung_S7_182'] : null,
                heldWebRTC: window.__heldWebRTC ? Object.keys(window.__heldWebRTC) : [],
                video: video ? { w: video.videoWidth, h: video.videoHeight, paused: video.paused } : null,
                canvas: canvas ? { w: canvas.width, h: canvas.height } : null
              };
            })()
          `;
          ws.send(JSON.stringify({ id: 100 + step, method: 'Runtime.evaluate', params: { expression: checkCode, returnByValue: true } }));
        }, 2000);

        setTimeout(() => {
          clearInterval(interval);
          console.log('\n--- Status at 15s after switching back ---');
          console.log('Agent log:\n', getAgentLog());
          ws.close();
          process.exit(0);
        }, 15000);
      } else if (resp.id >= 100) {
        const val = resp.result.result.value;
        const elapsed = (resp.id - 100) * 2;
        console.log(`[+${elapsed}s] Mode=${val.mode} HeldWebRTC=${JSON.stringify(val.heldWebRTC)} Video=${JSON.stringify(val.video)} Canvas=${JSON.stringify(val.canvas)}`);
      }
    };
  });
});
