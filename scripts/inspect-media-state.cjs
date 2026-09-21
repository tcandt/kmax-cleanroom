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
        (() => {
          const allCanvas = Array.from(document.querySelectorAll('canvas')).map(c => ({
            w: c.width,
            h: c.height,
            cls: c.className,
            id: c.id
          }));
          const allVideos = Array.from(document.querySelectorAll('video')).map(v => ({
            w: v.videoWidth,
            h: v.videoHeight,
            paused: v.paused,
            src: v.src,
            srcObject: !!v.srcObject,
            cls: v.className,
            id: v.id
          }));
          const errorMsg = document.querySelector('.error-msg') || document.querySelector('.ant-alert');
          const devContainer = document.querySelector('.device-screen') || document.querySelector('.screen-container') || document.querySelector('.player-container');
          return {
            mode: window.__deviceModes ? window.__deviceModes['Samsung_S7_182'] : null,
            canvas: allCanvas,
            videos: allVideos,
            error: errorMsg ? errorMsg.innerText : null,
            containerHtml: devContainer ? devContainer.outerHTML.slice(0, 300) : null
          };
        })()
      `;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: code, returnByValue: true } }));
    };
    ws.onmessage = (msg) => {
      console.log('Media State:', JSON.stringify(JSON.parse(msg.data).result.result.value, null, 2));
      ws.close();
    };
  });
});
