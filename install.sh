#!/bin/bash
# Use: source ./install.sh  (para o venv ficar ativo no terminal)

# Detecta o diretório do script tanto com source quanto com ./
if [ -n "$BASH_SOURCE" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE")" && pwd)"
else
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✔]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✘]${NC} $1"; }

echo ''
echo '================================'
echo '  mark-cli — Setup do ambiente  '
echo '================================'
echo ''

# ── 1. Verificar Python ──────────────────────────────────────────────

if ! command -v python3 &>/dev/null; then
  error 'Python 3 não encontrado. Instale com: brew install python3'
  return 1 2>/dev/null || exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
info "Python encontrado: $PYTHON_VERSION"

# ── 2. Criar/atualizar virtual environment ────────────────────────────

VENV_DIR="$SCRIPT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
  info 'Virtual environment já existe (.venv)'
else
  warn 'Criando virtual environment em .venv ...'
  python3 -m venv "$VENV_DIR"
  info 'Virtual environment criado'
fi

# Ativar venv
source "$VENV_DIR/bin/activate"
info "venv ativado: $(which python)"

# ── 3. Instalar dependências ──────────────────────────────────────────

warn 'Instalando dependências do requirements.txt ...'
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
info 'Dependências instaladas'

# ── 4. Criar .env se não existir ──────────────────────────────────────

ENV_FILE="$SCRIPT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
  info 'Arquivo .env já existe'
else
  warn 'Criando arquivo .env vazio ...'
  touch "$ENV_FILE"
  info 'Arquivo .env criado'
fi

# ── 5. Configurar CLI mark ────────────────────────────────────────────

chmod +x "$SCRIPT_DIR/mark.sh" 2>/dev/null

MARK_SOURCE_LINE="source $SCRIPT_DIR/mark.sh --setup-completion"
ZSHRC="$HOME/.zshrc"

if [ -f "$ZSHRC" ] && grep -qF "$MARK_SOURCE_LINE" "$ZSHRC"; then
  info 'CLI mark já configurado no .zshrc'
else
  warn 'Adicionando CLI mark ao .zshrc ...'
  echo '' >> "$ZSHRC"
  echo '# mark - Personal CLI' >> "$ZSHRC"
  echo "$MARK_SOURCE_LINE" >> "$ZSHRC"
  info 'CLI mark adicionado ao .zshrc'
fi

# Ativa mark na sessão atual se estiver em zsh
if [ -n "$ZSH_VERSION" ]; then
  source "$SCRIPT_DIR/mark.sh" --setup-completion
  info 'CLI mark ativo nesta sessão (use mark help para listar scripts)'
else
  warn 'Abra um novo terminal zsh para usar o comando mark'
fi

# ── 6. Resumo ─────────────────────────────────────────────────────────

echo ''
echo '================================'
echo '  Setup concluído! venv ativo.  '
echo '================================'
echo ''
echo '  Scripts:  mark help'
echo ''
