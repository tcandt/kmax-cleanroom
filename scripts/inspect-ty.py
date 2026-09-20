import sys
with open('reconstructed_source/web-app/public/assets/index-DIPw8r74.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Ty starts around char 147500
p = text.find('function Ty(')
print('Ty at:', p)
sys.stdout.buffer.write(text[p:p+1000].encode('utf-8'))
