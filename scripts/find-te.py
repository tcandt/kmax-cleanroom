import sys
with open('reconstructed_source/web-app/public/assets/index-DIPw8r74.js', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('sh=!0,n.focusDevice(a.value),Te.sendTouch(0')
start = max(0, p - 3000)
snippet = text[start:p]
# replace non-ascii
sys.stdout.buffer.write(snippet.encode('utf-8'))
