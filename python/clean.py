# desc: Limpa caches comuns (pip, brew, npm, .DS_Store)
import os
import subprocess
import shutil

HOME = os.path.expanduser('~')

tasks = [
    ('pip cache',       ['pip', 'cache', 'purge']),
    ('brew cleanup',    ['brew', 'cleanup', '--prune=all', '-s']),
    ('npm cache',       ['npm', 'cache', 'clean', '--force']),
]

total = 0

for name, cmd in tasks:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f'  ✔ {name}')
        else:
            print(f'  ⏭ {name} (não disponível)')
    except FileNotFoundError:
        print(f'  ⏭ {name} (não instalado)')
    except Exception as e:
        print(f'  ✘ {name}: {e}')

# Remove .DS_Store do diretório atual recursivamente
count = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        if f == '.DS_Store':
            os.remove(os.path.join(root, f))
            count += 1

if count:
    print(f'  ✔ {count} .DS_Store removidos')
else:
    print(f'  ⏭ nenhum .DS_Store encontrado')

# __pycache__
count = 0
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))
            count += 1

if count:
    print(f'  ✔ {count} __pycache__ removidos')
else:
    print(f'  ⏭ nenhum __pycache__ encontrado')
