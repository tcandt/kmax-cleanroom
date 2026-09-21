const http = require('http');
const { execSync } = require('child_process');

function getPs() {
  try {
    return execSync('adb -s 192.168.1.182:5555 shell ps | grep app_process', { encoding: 'utf8' }).trim();
  } catch (e) {
    return 'NOT RUNNING';
  }
}

function getAgentLog() {
  try {
    return execSync('adb -s 192.168.1.182:5555 shell tail -n 10 /data/local/tmp/cloudphone-agent.log', { encoding: 'utf8' }).trim();
  } catch (e) {
    return 'LOG ERROR';
  }
}

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const list = JSON.parse(data);
    const target = list.find(p => p.url && p.url.includes('3111'));
    if (!target) {
      console.log('No target');
      return;
    }
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      console.log('--- Before Switch ---');
      console.log('CoreService ps:', getPs());

      // Click the switch button
      const clickCode = `
        (() => {
          const btn = document.querySelector('button.sidebar-btn[title*="WebSocket"]');
          if (btn) {
            btn.click();
            return { clicked: true, title: btn.getAttribute('title') };
          }
          return { clicked: false };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: clickCode, returnByValue: true } }));
    };

    let step = 0;
    ws.onmessage = (msg) => {
      const resp = JSON.parse(msg.data);
      if (resp.id === 1) {
        console.log('Click result:', resp.result.result.value);

        // Now poll every 2s for 20s
        const interval = setInterval(() => {
          step++;
          const checkCode = `
            (() => {
              const canvas = document.querySelector('canvas');
              const video = document.querySelector('video');
              const btn = document.querySelector('button.sidebar-btn');
              const fpsBadge = document.querySelector('.fps-badge') || document.querySelector('.stream-meta') || document.querySelector('.header-meta');
              return {
                mode: window.__deviceModes ? window.__deviceModes['Samsung_S7_182'] : null,
                heldWebRTC: window.__heldWebRTC ? Object.keys(window.__heldWebRTC) : [],
                canvas: canvas ? { width: canvas.width, height: canvas.height } : null,
                video: video ? { width: video.videoWidth, height: video.videoHeight, paused: video.paused } : null,
                btnText: btn ? btn.innerText.trim() : null,
                btnTitle: btn ? btn.getAttribute('title') : null,
                fpsText: fpsBadge ? fpsBadge.innerText.trim() : null
              };
            })()
          `;
          ws.send(JSON.stringify({ id: 100 + step, method: 'Runtime.evaluate', params: { expression: checkCode, returnByValue: true } }));
        }, 2000);

        setTimeout(() => {
          clearInterval(interval);
          console.log('\n--- Final Inspection at 22 seconds ---');
          console.log('CoreService ps:', getPs());
          console.log('Recent agent log:\n', getAgentLog());
          ws.close();
          process.exit(0);
        }, 22000);
      } else if (resp.id >= 100) {
        const val = resp.result.result.value;
        const elapsed = (resp.id - 100) * 2;
        console.log(`[+${elapsed}s] Mode=${val.mode} HeldWebRTC=${JSON.stringify(val.heldWebRTC)} Canvas=${JSON.stringify(val.canvas)} Video=${JSON.stringify(val.video)} Btn=${val.btnText} CoreService=${getPs() ? 'ALIVE' : 'DEAD'}`);
      }
    };
  });
});
