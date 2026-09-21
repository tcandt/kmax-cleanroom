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
      console.log('Sending touch / click to canvas...');
      const code = `
        (() => {
          const canvas = document.querySelector('canvas.video-stream');
          if (!canvas) return { error: 'No canvas.video-stream' };
          const rect = canvas.getBoundingClientRect();
          const x = rect.left + rect.width / 2;
          const y = rect.top + rect.height / 2;

          // Dispatch mousedown, mousemove, mouseup
          const down = new MouseEvent('mousedown', { clientX: x, clientY: y, bubbles: true });
          const up = new MouseEvent('mouseup', { clientX: x, clientY: y, bubbles: true });
          canvas.dispatchEvent(down);
          setTimeout(() => {
            canvas.dispatchEvent(up);
          }, 100);
          return { dispatched: true, x, y };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };
    ws.onmessage = (msg) => {
      console.log('Dispatch result:', JSON.parse(msg.data).result.result.value);
      setTimeout(() => {
        console.log('Agent log after touch:\n', getAgentLog());
        ws.close();
      }, 1000);
    };
  });
});
