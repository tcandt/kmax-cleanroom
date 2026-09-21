const http = require('http');

http.get('http://127.0.0.1:9222/json', (res) => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const list = JSON.parse(data);
    const target = list.find(p => p.url && p.url.includes('3111'));
    if (!target) {
      console.log('No 3111 target found');
      return;
    }
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    ws.onopen = () => {
      const code = `
        (() => {
          const btns = Array.from(document.querySelectorAll('*')).filter(el => {
            const t = el.innerText || '';
            const title = el.getAttribute('title') || '';
            const isSidebarBtn = el.classList && el.classList.contains('sidebar-btn');
            const matchesTextOrTitle = /WebSocket|WebRTC|投屏|切换|Switch/.test(t + ' ' + title);
            return (isSidebarBtn && matchesTextOrTitle) || /WebSocket|投屏/.test(t + ' ' + title);
          }).map(el => ({
            tag: el.tagName,
            cls: el.className,
            title: el.getAttribute('title'),
            text: el.innerText ? el.innerText.trim().slice(0, 50) : ''
          }));
          return {
            modes: window.__deviceModes,
            activeIds: window.__activeDeviceIds,
            btns
          };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };
    ws.onmessage = (msg) => {
      console.log(JSON.stringify(JSON.parse(msg.data).result.result.value, null, 2));
      ws.close();
    };
  });
});
