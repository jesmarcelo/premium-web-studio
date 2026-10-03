# Auditoria de repositório existente

Execute antes de editar qualquer arquivo de um projeto existente. O objetivo é entender o projeto o suficiente para trabalhar **dentro** das convenções dele.

## Panorama rápido

Rode o script auxiliar a partir da raiz do projeto:

```bash
bash <SKILL_DIR>/scripts/audit-repo.sh
```

Ele é somente leitura: lista estrutura, manifestos, configs, scripts e indícios de framework. Use o resultado como ponto de partida, não como conclusão.

## Checklist de auditoria

1. **Estrutura** — árvore de diretórios (ignorando `node_modules`, `dist`, `.next`, `vendor`, `build`). Onde ficam páginas, componentes, estilos, assets, conteúdo.
2. **Framework e versões** — leia `package.json`, `composer.json`, `Gemfile`, `pyproject.toml`, `go.mod` ou equivalentes. Anote versões exatas de framework, React/Vue/Svelte, Tailwind, TypeScript. Versões mudam APIs: consulte a documentação da versão instalada, não da mais recente.
3. **Gerenciador de pacotes** — pelo lockfile (`package-lock.json` → npm, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb`/`bun.lock` → bun). Use sempre o mesmo.
4. **Scripts** — `dev`, `build`, `lint`, `test`, `typecheck`, `format`. Descubra como rodar e validar.
5. **Convenções** — nomenclatura de arquivos e componentes, export default vs. nomeado, organização por feature ou por tipo, padrão de imports/aliases, idioma dos comentários, estilo de CSS (Tailwind, CSS Modules, styled-components, Sass, BEM).
6. **Componentes reutilizáveis** — botões, inputs, cards, layout, modais. Reutilize antes de criar.
7. **Design system** — tokens (cores, tipografia, espaçamento, raios, sombras), tema (`tailwind.config`, `@theme`, variáveis CSS, `theme.ts`), biblioteca de UI (shadcn/ui, Radix, MUI, Chakra).
8. **Estilos globais** — reset, fontes carregadas, variáveis, dark mode.
9. **Dependências** — o que já está instalado para animação, ícones, formulários, validação, datas, gráficos. Sinalize dependências abandonadas, duplicadas ou pesadas.
10. **Rotas** — mapa de páginas e layouts, rotas dinâmicas, middleware, redirects.
11. **Configurações** — build, lint, TypeScript (`strict`?), Prettier, env vars esperadas (pelos nomes em `.env.example`, nunca leia nem exiba valores de `.env` reais), deploy (`vercel.json`, `netlify.toml`, Dockerfile, CI).
12. **Padrão arquitetural** — SSR/SSG/SPA, data fetching, gerenciamento de estado, camada de API, CMS.
13. **Estado de saúde** — rode `build`, `lint` e `typecheck` (se existirem) e registre o resultado **antes** de mudar algo, para separar problemas preexistentes dos que você introduzir.
14. **Git** — `git status` e branch atual. Se houver alterações não commitadas do usuário, não as sobrescreva; avise antes de editar arquivos com mudanças pendentes.
15. **Site publicado** — se houver URL de produção, use Firecrawl para scrape e, se possível, Lighthouse para uma linha de base.

## Saída da auditoria

Apresente ao usuário:

```markdown
## Auditoria do repositório
- Stack: <framework@versão>, <linguagem>, <estilização>, <gerenciador de pacotes>
- Como rodar: <comando dev> / build: <comando> / lint: <comando>
- Estado atual: build ✅/❌, lint ✅/❌ (N avisos), typecheck ✅/❌
- Design system existente: <tokens/biblioteca ou "inexistente">
- Componentes reutilizáveis relevantes: <lista>
- Pontos fortes a preservar: <lista>
- Problemas encontrados: <lista priorizada>
- Riscos/decisões que precisam de aprovação: <lista>
```

## Regras

- Preserve padrões bons existentes, mesmo que você preferisse outros.
- Não troque framework, biblioteca de estilos, gerenciador de pacotes ou estrutura de pastas sem aprovação.
- Não rode `npm audit fix --force`, upgrades major, codemods ou formatação em massa sem aprovação — geram diffs enormes e quebras.
- Mudanças fora do escopo pedido viram **sugestões** no relatório, não edições.
