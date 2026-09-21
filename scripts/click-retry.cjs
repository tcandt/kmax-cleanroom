const http = require('http');

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const list = JSON.parse(data);
    const target = list.find(p => p.url && p.url.includes('3111'));
    if (!target) return;
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      const code = `
          const btn =
            document.querySelector('button.retry-btn') ||
            Array.from(document.querySelectorAll('button')).find(
              b => ['Retry', '重试'].includes((b.textContent || '').trim())
            );
          if (btn) {
            btn.click();
            return 'clicked';
          }
          return 'btn not found';
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };
    ws.onmessage = (msg) => {
      console.log('Result:', JSON.parse(msg.data).result.result.value);
      ws.close();
    };
  });
});
