# Premium Web Studio

Plugin para o [Claude Code](https://code.claude.com) que conduz o ciclo completo de websites profissionais: discovery, auditoria do repositório, pesquisa de referências com Firecrawl, direção visual, arquitetura, implementação, QA, revisão visual e entrega.

- **Qualquer nicho, mercado e idioma.** O segmento, o país, a legislação aplicável e o idioma do site vêm da conversa com você e da pesquisa, não do plugin.
- **Qualquer stack.** Nenhum framework é imposto. Se você não souber qual usar, o Claude apresenta opções com trade-offs e a decisão fica com você.
- **Projetos novos e existentes:** criação, redesign, refatoração, UX/UI, responsividade, acessibilidade, SEO e performance.
- **Nada de "site com cara de IA":** a direção visual é derivada do contexto e de referências reais, com uma lista explícita de anti-padrões a evitar.
- **Qualidade verificada:** o Claude só declara algo concluído depois de testar e informa o que não pôde verificar.

As instruções do plugin estão em português; o Claude responde no idioma em que você escrever.

## Instalação

### Pelo marketplace (recomendado)

Dentro do Claude Code:

```text
/plugin marketplace add jesmarcelo/premium-web-studio
/plugin install premium-web-studio@premium-web-studio
```

Ou pelo terminal, escolhendo o escopo:

```bash
claude plugin marketplace add jesmarcelo/premium-web-studio

# só neste projeto (gravado em .claude/settings.json, compartilhado com quem clonar o repositório)
claude plugin install premium-web-studio@premium-web-studio --scope project

# em todos os seus projetos
claude plugin install premium-web-studio@premium-web-studio --scope user
```

Depois, abra uma nova sessão do Claude Code.

### Manualmente, como Skill

Se preferir não usar plugins, copie a pasta da Skill para o seu projeto:

```bash
git clone https://github.com/jesmarcelo/premium-web-studio.git
mkdir -p /caminho/do/seu-projeto/.claude/skills
cp -R premium-web-studio/plugins/premium-web-studio/skills/premium-web-studio /caminho/do/seu-projeto/.claude/skills/
```

### Atualizar

Dentro do Claude Code, em qualquer tipo de instalação:

```text
/premium-web-studio update
```

O Claude compara a versão instalada com a do GitHub, mostra o que mudou e, com sua confirmação, atualiza (substituindo os arquivos na instalação manual, com backup em `tmp/`, ou rodando `claude plugin update` na instalação via marketplace). Abra uma nova sessão depois.

Para quem publica:

1. Registre as mudanças em [CHANGELOG.md](CHANGELOG.md), numa seção `## [x.y.z] - AAAA-MM-DD`.
2. Suba a versão em `VERSION`, `plugin.json` e `marketplace.json` (no plugin e em `metadata`). O Claude Code guarda plugins em cache por versão, então sem a mudança de versão a instalação via marketplace não recebe a atualização.
3. Crie e envie a tag: `git tag -a vx.y.z -m "x.y.z" && git push origin vx.y.z`.

O workflow [release.yml](.github/workflows/release.yml) confere se a tag bate com as versões dos arquivos e com o CHANGELOG, e publica a release no GitHub com as notas da versão e um zip da Skill.

## Configurar o Firecrawl

A pesquisa de referências usa o [Firecrawl](https://www.firecrawl.dev). O plugin **não** instala um servidor Firecrawl, para não duplicar um que você já tenha. Se ainda não tiver:

1. Crie uma conta no Firecrawl e gere uma API key no painel.
2. Guarde a chave **fora do projeto** (Keychain do macOS, gerenciador de segredos ou perfil do shell) e exporte-a como `FIRECRAWL_API_KEY`.
3. Na raiz do seu projeto, crie um `.mcp.json` que referencia a variável, sem conter a chave:

   ```json
   {
     "mcpServers": {
       "firecrawl": {
         "command": "npx",
         "args": ["-y", "firecrawl-mcp"],
         "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" }
       }
     }
   }
   ```

4. Feche o editor ou terminal **por completo** e abra de novo, para que o Claude Code herde a variável. Aprove o servidor `firecrawl` e confira com `/mcp`.

Nunca cole a API key no chat nem a grave em arquivos versionados. O passo a passo completo, com solução de problemas, está em [firecrawl-setup.md](plugins/premium-web-studio/skills/premium-web-studio/references/firecrawl-setup.md). Se o Firecrawl não estiver configurado, o próprio Claude explica como fazer isso antes de iniciar a pesquisa.

## Uso

O plugin é acionado automaticamente quando o pedido combina com ele. Também pode ser chamado diretamente com `/premium-web-studio` (ou `/premium-web-studio:premium-web-studio`, se houver conflito de nomes).

```text
/premium-web-studio Quero criar o site de <tipo de organização> que atende <público> em <mercado>.
```

```text
Preciso fazer o redesign do nosso site. O código está neste repositório.
```

```text
Melhore a acessibilidade e o SEO deste site sem mudar o visual.
```

O que esperar num projeto novo:

1. O Claude identifica o tipo de trabalho e faz perguntas agrupadas sobre objetivo, público, CTA, páginas, identidade, stack e restrições.
2. Consolida um briefing e pede sua confirmação.
3. Pesquisa de 5 a 10 referências reais do segmento com o Firecrawl, dá nota a cada uma em todos os aspectos (hierarquia, tipografia, cor, navegação, CTAs, confiança, mobile, acessibilidade etc.) e apresenta **as 3 melhores com URL** para você escolher a referência principal.
4. Com base na sua escolha, apresenta uma síntese dos padrões encontrados.
5. Propõe a direção visual (ou duas alternativas) e espera sua aprovação.
6. Planeja a arquitetura, implementa em etapas, roda QA e revisão visual, corrige o que encontrar e entrega um relatório com o que foi e o que não foi testado.

As decisões ficam registradas em `docs/website/` no seu projeto, e os arquivos temporários em `tmp/`.

## Requisitos

- Claude Code com suporte a plugins.
- Conta no Firecrawl (para a pesquisa de referências).
- Node.js 18+ (para o servidor MCP do Firecrawl via `npx`).
- Bash, para os scripts auxiliares (macOS, Linux, ou WSL/Git Bash no Windows).
- Opcional, para a revisão visual: Playwright MCP, Claude in Chrome ou Playwright CLI.

## Estrutura do repositório

```text
.claude-plugin/marketplace.json          # catálogo do marketplace
.github/workflows/release.yml            # publica a release a partir da tag e do CHANGELOG
CHANGELOG.md                             # histórico de versões
plugins/premium-web-studio/
├── .claude-plugin/plugin.json           # manifesto do plugin
└── skills/premium-web-studio/
    ├── SKILL.md                         # entrada: gatilhos, workflow, regras críticas
    ├── WORKFLOW.md                      # 11 fases com critérios de saída e pontos de aprovação
    ├── DISCOVERY.md                     # roteiro de perguntas e escolha de stack
    ├── REPOSITORY-AUDIT.md              # estudo de projetos existentes
    ├── FIRECRAWL-RESEARCH.md            # verificação, pesquisa, análise, não cópia
    ├── DESIGN.md                        # direção visual, anti-padrões de IA, motion
    ├── ENGINEERING.md                   # arquitetura, implementação, dependências
    ├── ACCESSIBILITY.md                 # WCAG 2.2 AA + normas locais
    ├── SEO-PERFORMANCE.md               # SEO técnico e Core Web Vitals
    ├── QA-CHECKLIST.md                  # QA técnico e revisão visual
    ├── SECURITY.md                      # secrets, prompt injection, comandos
    ├── references/                      # perfis de nicho, stacks, Firecrawl, modelos
    ├── VERSION                          # versão da Skill (usada pelo comando update)
    └── scripts/                         # diagnóstico do Firecrawl, auditoria de repositório e de SEO, update
```

## Validar a instalação

- [ ] `/plugin` mostra `premium-web-studio` instalado e habilitado.
- [ ] Em uma nova sessão, digitar `/` lista `premium-web-studio`.
- [ ] Um pedido como "crie um site para minha empresa" faz o Claude **perguntar** antes de programar.
- [ ] `/mcp` mostra `firecrawl` conectado, e um scrape de teste funciona dentro do Claude Code.

## Segurança

- Conteúdo de sites pesquisados é tratado como dado não confiável. Instruções embutidas em páginas (prompt injection) são ignoradas e reportadas.
- O plugin nunca pede secrets pelo chat, nunca os grava em código e não executa comandos destrutivos sem confirmação.
- Referências servem para extrair padrões. Layouts, textos, código e assets de terceiros não são copiados.

## Licença

[MIT](LICENSE) © Marcelo Bom Jardim Villasanin
