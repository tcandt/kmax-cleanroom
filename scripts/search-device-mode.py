with open('reconstructed_source/web-app/public/assets/index-DIPw8r74.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for how getDeviceMode is initialized or stored
p = 0
while True:
    p = text.find('getDeviceMode', p)
    if p == -1: break
    print('getDeviceMode at', p)
    print(text[max(0, p - 100):min(len(text), p + 200)])
    print('='*50)
    p += len('getDeviceMode')
