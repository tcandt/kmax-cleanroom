import sys
with open('reconstructed_source/web-app/public/assets/index-DIPw8r74.js', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('sh=!0,n.focusDevice(a.value),Te.sendTouch(0')
# Search backwards for "const Te =" or "let Te ="
p_te = text.rfind('Te=', 0, p)
print('p_te:', p_te)
start = max(0, p_te - 100)
end = min(len(text), p_te + 200)
sys.stdout.buffer.write(text[start:end].encode('utf-8'))
