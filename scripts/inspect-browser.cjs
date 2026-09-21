const http = require('http');

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const list = JSON.parse(data);
    const target = list.find(p => p.url && p.url.includes('3111'));
    if (!target) {
      console.log('No tab found');
      return;
    }
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      const code = `
        (() => {
          const errorBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('重试'));
          const stateTexts = Array.from(document.querySelectorAll('.state-text')).map(s => s.innerText);
          return {
            hasRetryBtn: !!errorBtn,
            stateTexts,
            devStates: window.__deviceConnectionStates || {},
            devEpochs: window.__deviceEpochs || {}
          };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };
    ws.onmessage = (msg) => {
      console.log(msg.data);
      ws.close();
    };
  });
});
