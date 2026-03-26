# desc: Top 10 maiores arquivos/pastas no diretório
import os
import sys

target = sys.argv[1] if len(sys.argv) > 1 else '.'

def fmt_size(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024:
            return f'{b:.1f} {unit}'
        b /= 1024
    return f'{b:.1f} TB'

def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total

items = []
for name in os.listdir(target):
    path = os.path.join(target, name)
    if name.startswith('.'):
        continue
    if os.path.isfile(path):
        items.append((os.path.getsize(path), name))
    elif os.path.isdir(path):
        items.append((dir_size(path), name + '/'))

items.sort(reverse=True)

print(f'  Top 10 em: {os.path.abspath(target)}\n')
for size, name in items[:10]:
    print(f'  {fmt_size(size):>10}  {name}')
