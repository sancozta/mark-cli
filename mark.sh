#!/bin/zsh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_DIR="$SCRIPT_DIR/python"
VENV_DIR="$SCRIPT_DIR/.venv"

# Autocomplete: ao rodar "source mark.sh --setup-completion", registra a function e completion no shell
if [[ "$1" == "--setup-completion" ]]; then
  _MARK_DIR="$SCRIPT_DIR"
  _MARK_PYTHON_DIR="$PYTHON_DIR"

  mark() {
    "$_MARK_DIR/mark.sh" "$@"
  }

  _mark_complete() {
    local scripts=()
    for f in "$_MARK_PYTHON_DIR"/*.py; do
      local name=$(basename "$f" .py)
      [[ "$name" == util_* ]] && continue
      [[ "$name" == __* ]] && continue
      # Scripts pessoais (_prefixo): expor sem o _
      [[ "$name" == _* ]] && name="${name#_}"
      scripts+=("$name")
    done
    compadd -X "Scripts disponíveis:" $scripts
  }

  compdef _mark_complete mark
  return 0 2>/dev/null || exit 0
fi

typeset -A DESCRIPTIONS

# Descrições de scripts pessoais (prefixo _ no arquivo, chamados sem _)
# Adicione '# desc: Minha descrição' na primeira ou segunda linha do script.

_get_personal_desc() {
  local file="$1"
  local desc=$(grep -m1 '^# desc:' "$file" 2>/dev/null | sed 's/^# desc: *//')
  echo "${desc:-Sem descrição disponível}"
}

GRAY='\033[90m'
CYAN='\033[36m'
NC='\033[0m'

show_help() {
  echo "Uso: mark <script> [args...]"
  echo ""

  local has_private=false
  for f in "$PYTHON_DIR"/_*.py(N); do
    has_private=true
    break
  done

  printf "  %-28s | %s\n" "Script" "Descrição"
  printf "  %-28s-+-%s\n" "----------------------------" "--------------------------------------------------"
  for f in "$PYTHON_DIR"/*.py; do
    name=$(basename "$f" .py)
    [[ "$name" == util_* ]] && continue
    [[ "$name" == __* ]] && continue
    [[ "$name" == _* ]] && continue
    # Lê descrição do comentário '# desc:' no script, senão usa DESCRIPTIONS
    desc=$(grep -m1 '^# desc:' "$f" 2>/dev/null | sed 's/^# desc: *//')
    desc="${desc:-${DESCRIPTIONS[$name]:-Sem descrição disponível}}"
    printf "  %-28s | %s\n" "$name" "$desc"
  done

  if $has_private; then
    echo ""
    printf "  %-28s | %s\n" "Script Privado" "Descrição"
    printf "  %-28s-+-%s\n" "----------------------------" "--------------------------------------------------"
    for f in "$PYTHON_DIR"/_*.py(N); do
      name=$(basename "$f" .py)
      display_name="${name#_}"
      desc=$(_get_personal_desc "$f")
      printf "  %-28s | %s\n" "$display_name" "$desc"
    done
  fi
}

if [[ -z "$1" || "$1" == "help" || "$1" == "--help" || "$1" == "-h" ]]; then
  show_help
  exit 0
fi

SCRIPT_NAME="$1"
shift

SCRIPT_PATH="$PYTHON_DIR/${SCRIPT_NAME}.py"

# Fallback: tentar script pessoal com prefixo _
if [ ! -f "$SCRIPT_PATH" ]; then
  SCRIPT_PATH="$PYTHON_DIR/_${SCRIPT_NAME}.py"
fi

if [ ! -f "$SCRIPT_PATH" ]; then
  echo "Erro: script '$SCRIPT_NAME' não encontrado em $PYTHON_DIR"
  echo "Use 'mark help' para listar os scripts disponíveis."
  exit 1
fi

if [ -d "$VENV_DIR" ]; then
  source "$VENV_DIR/bin/activate"
fi

python "$SCRIPT_PATH" "$@"
