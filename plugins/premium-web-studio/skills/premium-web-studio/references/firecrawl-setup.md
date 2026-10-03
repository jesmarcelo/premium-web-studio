# Configuração segura do Firecrawl no Claude Code

Guia para apresentar ao usuário quando o Firecrawl não estiver disponível. A integração preferida é o **servidor MCP oficial** (`firecrawl-mcp`, mantido pela Firecrawl), em escopo de projeto.

> **Nunca cole a API key no chat do Claude Code.** Ela fica no histórico da conversa. Se isso acontecer, revogue a chave no painel do Firecrawl e gere outra.

## 1. Criar a conta e a chave

1. Acesse https://www.firecrawl.dev e crie uma conta (há plano gratuito com créditos limitados).
2. No painel (dashboard), em **API Keys**, gere uma chave (começa com `fc-`).
3. Copie a chave diretamente para o gerenciador de segredos do passo 2 — não para arquivos do projeto.

## 2. Guardar a chave fora do projeto

Escolha uma opção.

### Opção A — Keychain do macOS (recomendada no Mac)

```bash
# Pede a chave de forma interativa (não fica no histórico do shell)
security add-generic-password -a "$USER" -s FIRECRAWL_API_KEY -w
```

Depois, adicione ao `~/.zshrc`:

```bash
export FIRECRAWL_API_KEY="$(security find-generic-password -a "$USER" -s FIRECRAWL_API_KEY -w 2>/dev/null)"
```

### Opção B — Gerenciador de segredos (1Password CLI, Doppler, Bitwarden, Vault)

Exemplo com 1Password CLI no `~/.zshrc`:

```bash
export FIRECRAWL_API_KEY="$(op read 'op://Private/Firecrawl/credential' 2>/dev/null)"
```

### Opção C — Variável de ambiente simples (Linux/Windows/WSL)

Adicione ao perfil do shell (`~/.bashrc`, `~/.zshrc`) ou às variáveis de ambiente do usuário no Windows. É menos seguro que as opções A e B (texto puro no disco), mas fica fora do projeto.

Após qualquer opção: **abra um novo terminal** (ou reinicie completamente o VS Code) para que a variável seja carregada.

Verifique sem exibir a chave:

```bash
[ -n "$FIRECRAWL_API_KEY" ] && echo "FIRECRAWL_API_KEY definida" || echo "FIRECRAWL_API_KEY ausente"
```

## 3. Registrar o servidor MCP no projeto

Crie (ou complemente) o arquivo `.mcp.json` na **raiz do projeto**. O Claude Code expande `${FIRECRAWL_API_KEY}` a partir do ambiente, então o arquivo **não contém a chave** e pode ser versionado com segurança:

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

Requisito: Node.js 18+ (para `npx`).

Alternativa por linha de comando (cria a mesma entrada no `.mcp.json` com escopo de projeto). As aspas simples impedem que o shell expanda a variável, então o arquivo guarda a referência, não o valor:

```bash
claude mcp add firecrawl --scope project -e 'FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}' -- npx -y firecrawl-mcp
```

Confira depois que o `.mcp.json` contém literalmente `${FIRECRAWL_API_KEY}` e não a chave.

### Por que não as outras formas
- `claude mcp add … -e FIRECRAWL_API_KEY=fc-xxxx` grava a chave em texto puro na configuração.
- O endpoint remoto do Firecrawl com a chave na URL também expõe a chave em texto puro na configuração e em logs. Use somente se o usuário preferir conscientemente.

## 4. Ativar e verificar

1. Reinicie o Claude Code (ou use `/mcp` para reconectar).
2. Na primeira vez, o Claude Code pede aprovação para servidores definidos no `.mcp.json` do projeto — aprove `firecrawl`.
3. Rode `claude mcp list` (ou `/mcp`): `firecrawl` deve aparecer como conectado.
4. Rode o diagnóstico da Skill:
   ```bash
   bash <SKILL_DIR>/scripts/check-firecrawl.sh
   ```
5. Teste pedindo ao Claude Code: "Use o Firecrawl para fazer scrape de https://example.com e me diga o título da página." Se as ferramentas aparecerem mas o teste retornar `Unauthorized`, veja a tabela abaixo.

## 5. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `firecrawl` aparece com falha ou pendente em `/mcp` | Variável não carregada no processo do Claude Code, ou servidor ainda não aprovado | Abra novo terminal / feche o editor por completo (no macOS, Cmd+Q) e reabra; aprove o servidor em `/mcp` |
| Ferramentas aparecem, mas retornam `Unauthorized: Invalid token`, e o script mostra a chave aceita (HTTP 200) | O servidor MCP subiu antes de a variável existir e recebeu valor vazio | Feche o editor/terminal por completo e reabra; ou reconecte o servidor em `/mcp` a partir de uma sessão iniciada depois de definir a variável |
| Erro 401 / Unauthorized e o script também mostra recusa | Chave inválida ou revogada | Gere nova chave no painel e atualize o gerenciador de segredos |
| Erro 402 / créditos | Créditos do plano esgotados | Verifique o uso no painel do Firecrawl |
| `npx: command not found` | Node.js ausente | Instale Node.js 18+ |
| Servidor não aparece | `.mcp.json` fora da raiz ou JSON inválido | Valide o JSON e a localização do arquivo |

## 6. Custos

Cada scrape, busca ou página de crawl consome créditos. A Skill limita a pesquisa a 5–10 referências e poucas páginas por referência; o usuário pode pedir uma pesquisa mais enxuta ou mais ampla.
