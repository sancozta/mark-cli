# desc: Lista dependências desatualizadas (pip/npm)
import subprocess
import json

print('  === pip ===\n')
try:
    result = subprocess.run(
        ['pip', 'list', '--outdated', '--format=json'],
        capture_output=True, text=True, timeout=30
    )
    packages = json.loads(result.stdout) if result.stdout else []
    if packages:
        print(f'  {"Pacote":<30} {"Atual":<15} {"Última":<15}')
        print(f'  {"-"*30} {"-"*15} {"-"*15}')
        for p in packages:
            print(f'  {p["name"]:<30} {p["version"]:<15} {p["latest_version"]:<15}')
    else:
        print('  Tudo atualizado ✔')
except FileNotFoundError:
    print('  pip não encontrado')
except Exception as e:
    print(f'  Erro: {e}')

print('\n  === npm ===\n')
try:
    result = subprocess.run(
        ['npm', 'outdated', '--json'],
        capture_output=True, text=True, timeout=30
    )
    packages = json.loads(result.stdout) if result.stdout else {}
    if packages:
        print(f'  {"Pacote":<30} {"Atual":<15} {"Última":<15}')
        print(f'  {"-"*30} {"-"*15} {"-"*15}')
        for name, info in packages.items():
            current = info.get('current', '?')
            latest = info.get('latest', '?')
            print(f'  {name:<30} {current:<15} {latest:<15}')
    else:
        print('  Tudo atualizado ✔ (ou sem package.json)')
except FileNotFoundError:
    print('  npm não encontrado')
except Exception as e:
    print(f'  Erro: {e}')
