# Changelog

Todas as mudanças relevantes do plugin Premium Web Studio são registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e a numeração segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/): a versão maior muda quando o fluxo ou os documentos deixam de ser compatíveis com os projetos em andamento, a menor quando algo novo é acrescentado sem quebrar o que existe, e a de correção quando só há ajustes.

## [Não lançado]

## [1.0.1] - 2026-10-04

### Adicionado

- `scripts/perf-audit.py`: roda o Lighthouse em mobile e desktop e lista só as falhas de cache, imagens, reflow forçado, árvore de dependência de rede, LCP, CLS, fontes e bloqueio de renderização, com as URLs afetadas.
- Regras e verificação de reflow forçado (layout thrashing) no JS do projeto.
- Orientação sobre a árvore de dependência de rede: menos arquivos de fonte, `unicode-range`, beacons de CDN fora do caminho crítico.
- Seção sobre CDN como proxy (ex.: Cloudflare): Browser Cache TTL em "Respect Existing Headers", purge após mudar o cache e desativação do beacon de RUM.

### Corrigido

- `.htaccess` gerado por padrão quando a hospedagem é desconhecida, criado na pasta que o build copia (ex.: `public/`) e conferido na saída do build; verificação de cache com `curl` em cada extensão servida (`webp`, `woff2` etc.).
- Componentes de imagem do framework obrigatoriamente com `srcset`/`sizes` (ou `layout` responsivo no Astro): `width` sozinho gerava um único arquivo maior que o exibido. Inclui snippet que compara o arquivo entregue com o tamanho exibido × `devicePixelRatio`.

## [1.0.0] - 2026-10-02

Primeira versão pública.

### Adicionado

- Ciclo completo em 11 fases: discovery, auditoria do repositório, pesquisa, análise de referências, direção visual, arquitetura, implementação, QA, revisão visual, refinamento e entrega, com critérios de saída e pontos de aprovação do usuário.
- Pesquisa de 5 a 10 referências reais com Firecrawl, nota em todos os aspectos e top 3 com URL para o usuário escolher a referência principal; dispensa do Firecrawl quando o usuário já fornece os sites de referência.
- Direção visual original e contextual, com lista explícita de anti-padrões de "site com cara de IA" e regras de não cópia.
- Funciona para qualquer nicho, mercado, idioma e stack, com método para derivar o perfil do nicho e opções de stack com trade-offs.
- Pipeline obrigatório de imagens: medição do tamanho exibido, redimensionamento (1× e 2×) e conversão para WebP.
- Configuração de compressão (Brotli/gzip) e cache de navegador por hospedagem: `.htaccess`, Nginx, Netlify/Cloudflare Pages e Vercel.
- SEO técnico e on-page: metadados gerados a partir do conteúdo, paginação, taxonomias, grafo de dados estruturados, `BreadcrumbList`, `BlogPosting` completo e autoria (E-E-A-T).
- Acessibilidade WCAG 2.2 AA, Core Web Vitals, checklist de QA e revisão visual em vários breakpoints.
- Regras de segurança: secrets fora do chat e do código, conteúdo pesquisado tratado como dado não confiável (prompt injection).
- Scripts de diagnóstico do Firecrawl, panorama de repositório existente e auditoria de SEO a partir do sitemap (`seo-audit.py`).
- Comando `/premium-web-studio update` para verificar e aplicar atualizações a partir do GitHub.
- Instalação pelo marketplace do Claude Code ou manualmente como Skill.

[Não lançado]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jesmarcelo/premium-web-studio/releases/tag/v1.0.0
