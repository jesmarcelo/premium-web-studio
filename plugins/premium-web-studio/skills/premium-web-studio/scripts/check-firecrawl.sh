#!/usr/bin/env bash
# Diagnóstico da integração Firecrawl para o Claude Code.
# Somente leitura. Nunca imprime o valor da API key.
# Uso: bash <SKILL_DIR>/scripts/check-firecrawl.sh [raiz-do-projeto]
# Rode em um terminal interativo: variáveis definidas no perfil do shell
# (~/.zshrc, ~/.bashrc) podem não existir em shells não interativos.

set -u

ROOT="${1:-$(pwd)}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ok=0

echo "== Firecrawl: diagnóstico =="
echo "Projeto: $ROOT"
echo

# 1. Variável de ambiente: existência, prefixo e validade na API
if [ -n "${FIRECRAWL_API_KEY:-}" ]; then
  case "$FIRECRAWL_API_KEY" in
    fc-*) echo "[ok]    FIRECRAWL_API_KEY definida neste shell (prefixo fc- reconhecido)" ;;
    *)    echo "[aviso] FIRECRAWL_API_KEY definida, mas sem o prefixo fc- esperado" ;;
  esac
  if command -v curl >/dev/null 2>&1; then
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 \
      -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
      https://api.firecrawl.dev/v2/team/credit-usage)
    case "$code" in
      200) echo "[ok]    A API do Firecrawl aceitou a chave (HTTP 200)" ;;
      401|403) echo "[falha] A API do Firecrawl recusou a chave (HTTP $code). Gere uma nova no painel."; ok=1 ;;
      000) echo "[aviso] Não foi possível contatar a API do Firecrawl (rede/proxy)" ;;
      *)   echo "[aviso] Resposta inesperada da API do Firecrawl (HTTP $code)" ;;
    esac
  fi
else
  echo "[falta] FIRECRAWL_API_KEY não está definida neste shell"
  echo "        (se ela está no perfil do shell, abra um terminal novo e rode o script nele)"
  ok=1
fi

# 2. Configuração MCP no projeto
MCP_FILE="$ROOT/.mcp.json"
if [ -f "$MCP_FILE" ]; then
  if grep -q '"firecrawl' "$MCP_FILE"; then
    echo "[ok]    .mcp.json do projeto contém um servidor firecrawl"
    if grep -Eq 'fc-[A-Za-z0-9]{8,}' "$MCP_FILE"; then
      echo "[RISCO] .mcp.json parece conter uma API key literal. Substitua por \${FIRECRAWL_API_KEY} e revogue a chave exposta."
      ok=1
    fi
  else
    echo "[info]  .mcp.json existe, mas não registra o firecrawl"
  fi
else
  echo "[info]  .mcp.json não encontrado na raiz do projeto (o firecrawl pode estar em outro escopo)"
fi

# 3. Configuração do usuário (somente presença, sem exibir conteúdo)
if [ -f "$HOME/.claude.json" ] && grep -q '"firecrawl' "$HOME/.claude.json" 2>/dev/null; then
  echo "[info]  Há uma entrada firecrawl em ~/.claude.json (escopo local/usuário)"
  if grep -Eq 'fc-[A-Za-z0-9]{8,}' "$HOME/.claude.json" 2>/dev/null; then
    echo "[aviso] ~/.claude.json parece conter uma API key literal (texto puro). Prefira referenciar a variável de ambiente."
  fi
fi

# 4. Node/npx para rodar o servidor MCP oficial
if command -v npx >/dev/null 2>&1; then
  echo "[ok]    npx disponível ($(node --version 2>/dev/null || echo 'node ?'))"
else
  echo "[falta] npx não encontrado. Instale Node.js 18+"
  ok=1
fi

# 5. Estado dos servidores MCP segundo o Claude Code
if command -v claude >/dev/null 2>&1; then
  echo
  echo "-- claude mcp list (apenas linhas do firecrawl, chaves mascaradas) --"
  (cd "$ROOT" && claude mcp list 2>/dev/null | grep -i -A1 firecrawl | sed -E 's/fc-[A-Za-z0-9]+/fc-***/g') \
    || echo "(firecrawl não listado)"
fi

echo
if [ "$ok" -eq 0 ]; then
  echo "Resultado: configuração aparente OK."
  echo "Se o Claude Code ainda retornar 'Unauthorized/Invalid token', ele foi aberto antes de a variável existir:"
  echo "feche o editor/terminal por completo, abra de novo e reconecte o servidor com /mcp."
else
  echo "Resultado: configuração incompleta. Veja $SKILL_DIR/references/firecrawl-setup.md"
fi
exit "$ok"
