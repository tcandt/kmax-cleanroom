with open('reconstructed_source/web-app/public/assets/index-DIPw8r74.js', 'r', encoding='utf-8') as f:
    text = f.read()

def dump_around(pos, length=400):
    start = max(0, pos - 150)
    end = min(len(text), pos + length)
    print("=" * 60)
    print(text[start:end])

print("--- SNIPPETS FOR input-channel ---")
p = 0
while True:
    p = text.find('input-channel', p)
    if p == -1: break
    dump_around(p)
    p += len('input-channel')

print("--- SNIPPET FOR FIRST sendTouch DEFINITION ---")
p = text.find('function sendTouch')
if p == -1:
    p = text.find('sendTouch(')
dump_around(p, 800)
