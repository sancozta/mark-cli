# mark-cli

CLI pessoal para automações via scripts Python.

## Setup

```bash
source ./install.sh   # cria venv, instala deps, registra `mark` no .zshrc
source .venv/bin/activate  # reativar em terminais novos
```

## Uso

```bash
mark <script> [args...]
mark help    # lista todos os scripts disponíveis
```

## Estrutura

- `python/` — scripts executáveis + módulos utilitários (`util_*.py`)
- `mark.sh` — wrapper CLI (autocomplete, descoberta de scripts, ativa venv)
- `install.sh` — setup inicial (venv, deps, registra mark no .zshrc)
- `requirements.txt` — dependências Python

## Convenções de scripts

- Qualquer `.py` em `python/` é automaticamente descoberto pelo `mark help`
- Adicione `# desc: Descrição curta` na primeira linha para aparecer na listagem
- Scripts com prefixo `_` são privados (chamados sem o `_`): `_meu.py` → `mark meu`
- Módulos com prefixo `util_` não aparecem na listagem (uso como import)

## Scripts base

| Script | Uso |
|---|---|
| `decode_basic` | `mark decode_basic <base64>` |
| `decode_jwt` | `mark decode_jwt <jwt>` |
| `encode_basic` | `mark encode_basic <texto>` |
| `get_screen` | `mark get_screen <url>` |
