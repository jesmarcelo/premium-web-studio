#!/usr/bin/env bash
# Verifica e aplica atualizações da Skill a partir do GitHub.
# Uso (a partir da raiz do projeto do usuário):
#   bash update.sh check   -> compara a versão instalada com a do GitHub (padrão)
#   bash update.sh apply   -> substitui os arquivos da Skill pela versão do GitHub
# Arquivos temporários e backup ficam em ./tmp/ do projeto atual.
set -euo pipefail

REPO="jesmarcelo/premium-web-studio"
BRANCH="main"
SKILL_SUBDIR="plugins/premium-web-studio/skills/premium-web-studio"
MODE="${1:-check}"

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${PWD}/tmp/premium-web-studio-update"

command -v curl >/dev/null || { echo "ERRO: curl não encontrado."; exit 1; }
command -v tar  >/dev/null || { echo "ERRO: tar não encontrado."; exit 1; }

# Tipo de instalação
INSTALL="manual"
case "$SKILL_DIR" in
  */.claude/plugins/*) INSTALL="plugin" ;;
esac
# Clone do próprio repositório: a Skill está exatamente em <raiz do clone>/SKILL_SUBDIR
GIT_ROOT="$(git -C "$SKILL_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$GIT_ROOT" ] && [ "$(cd "$GIT_ROOT" && pwd)/$SKILL_SUBDIR" = "$SKILL_DIR" ]; then
  INSTALL="git"
fi

LOCAL_VERSION="$(cat "$SKILL_DIR/VERSION" 2>/dev/null || echo "desconhecida")"

rm -rf "$WORK"
mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT
if ! curl -fsSL "https://codeload.github.com/${REPO}/tar.gz/refs/heads/${BRANCH}" | tar -xz -C "$WORK"; then
  echo "ERRO: não foi possível baixar ${REPO}@${BRANCH}. Verifique a conexão."
  exit 1
fi
REMOTE_DIR="$(find "$WORK" -mindepth 1 -maxdepth 1 -type d | head -1)/${SKILL_SUBDIR}"
[ -f "$REMOTE_DIR/SKILL.md" ] || { echo "ERRO: estrutura inesperada no repositório remoto."; exit 1; }
REMOTE_VERSION="$(cat "$REMOTE_DIR/VERSION" 2>/dev/null || echo "desconhecida")"

echo "Instalação:     $INSTALL ($SKILL_DIR)"
echo "Versão local:   $LOCAL_VERSION"
echo "Versão remota:  $REMOTE_VERSION"

CHANGES="$(diff -rq "$SKILL_DIR" "$REMOTE_DIR" 2>/dev/null | grep -v '\.DS_Store' || true)"
if [ -z "$CHANGES" ]; then
  echo "STATUS: atualizado"
  exit 0
fi

echo "STATUS: atualização disponível"
echo "Arquivos diferentes:"
echo "$CHANGES" | sed -e "s|$SKILL_DIR|local|g" -e "s|$REMOTE_DIR|remoto|g" -e 's/^/  /'

[ "$MODE" = "apply" ] || exit 0

case "$INSTALL" in
  git)
    echo "A Skill está num clone git do repositório. Atualize com: git -C \"$SKILL_DIR\" pull"
    exit 2 ;;
  plugin)
    echo "A Skill foi instalada como plugin. Atualize com:"
    echo "  claude plugin marketplace update premium-web-studio"
    echo "  claude plugin update premium-web-studio@premium-web-studio"
    exit 2 ;;
esac

BACKUP="${PWD}/tmp/premium-web-studio-backup-$(date +%Y%m%d-%H%M%S)"
cp -R "$SKILL_DIR" "$BACKUP"
find "$SKILL_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -R "$REMOTE_DIR/." "$SKILL_DIR/"
chmod +x "$SKILL_DIR"/scripts/*.sh 2>/dev/null || true

echo "ATUALIZADO: $LOCAL_VERSION -> $REMOTE_VERSION"
echo "Backup da versão anterior: $BACKUP"
echo "Abra uma nova sessão do Claude Code para carregar a versão nova."
