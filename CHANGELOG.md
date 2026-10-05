# Changelog

Todas as mudanças relevantes do plugin Premium Web Studio são registradas aqui.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e a numeração segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/): a versão maior muda quando o fluxo ou os documentos deixam de ser compatíveis com os projetos em andamento, a menor quando algo novo é acrescentado sem quebrar o que existe, e a de correção quando só há ajustes.

## [Não lançado]

## [1.0.4] - 2026-10-05

### Adicionado

- Ciclo de correção até zerar: todo item reprovado pelas auditorias volta a corrigir → build → auditar e sobe uma escada de soluções por problema, até sair **resolvido**, por **decisão do usuário** (com opções e custo medido) ou **fora do controle do projeto** (com evidência). "Pendente" ou "aceito" sem um desses estados não conta como entrega. Relatório de QA com tabela de auditorias (degraus tentados, estado, custo, o que resolveria).
- `scripts/build-audit.py`: auditoria da pasta do build, sem rede e sem navegador. Aponta leituras de geometria na execução inicial dos scripts com `arquivo:linha:coluna` no formato do PageSpeed, o critério de compressão do PageSpeed em todos os arquivos de imagem gerados, PNG/JPG servidos, `<img>` sem `srcset`, excesso de `fetchpriority`, canonical/`og:url`/`og:image` relativos, a imagem de compartilhamento (formato, 1200×630, ≤ 300 KB), `og:image:alt`, `twitter:image`, JSON-LD `WebSite`/`Organization`, `robots.txt`, sitemap e `favicon.ico`.
- URL pública final como pré-requisito do build de entrega (domínio e subpasta), perguntada no discovery; reescritas de caminho pós-build não podem tocar em canonical, `og:*` nem JSON-LD.
- Imagem de compartilhamento tratada como peça de design (composição legível em miniatura, como gerar, como testar e limpar o cache das redes) e liberação dos robôs das redes na proteção contra bots da CDN.
- Seção sobre o Google: Search Console, nome do site (`WebSite`), ícone e logo nos resultados, `max-image-preview:large`, Google Business Profile, e o que muda quando o site fica numa subpasta.
- `perf-audit.py`: `--runs N` para repetir as rodadas e próximo passo impresso em cada grupo reprovado.
- `seo-audit.py`: prévia de compartilhamento (robôs do Facebook, WhatsApp, X e LinkedIn; `og:image` absoluta, baixável, JPG/PNG, dimensões e peso), `og:url`, `og:image:alt`, `twitter:image`, URLs relativas, `max-image-preview`, `WebSite` na home e `robots.txt`/`favicon.ico` na raiz quando o site está numa subpasta.

### Corrigido

- Reflow forçado: uma única leitura de geometria no nível superior do módulo (ex.: `let lastY = scrollY`) força o layout da página inteira na carga e o PageSpeed atribui todo esse tempo à linha; exemplo de correção e verificação em três etapas (`build-audit.py`, revisão dos handlers, `perf-audit.py --runs 3`).
- `fetchpriority` no elemento que o relatório aponta como LCP, medido em mobile e desktop, e não no que parece ser o principal (em composições com várias imagens, a maior camada em área costuma ser o LCP).
- Imagens raster passam a sair em **AVIF com fallback WebP** por padrão (`<picture>` com `<source type="image/avif">`, ou negociação pelo `Accept` no `next/image` e em CDNs), com qualidade própria para cada formato (AVIF 50–55, WebP 70–78). Medido: camada transparente de 19,5 KiB em WebP para 9,3 KiB em AVIF; foto detalhada de 126 KiB para 99 KiB, as duas passando no critério do PageSpeed. Regras por framework: no Astro, `<Picture formats={['avif']} fallbackFormat="webp">` (sem `fallbackFormat` o fallback sai em PNG) e qualidade por formato no `sharpImageService` em vez da prop `quality`; `image-set()` para imagens em CSS; `preload` com `type="image/avif"`. `build-audit.py` reprova `<img>` raster fora de `<picture>` com AVIF e trata o WebP de fallback acima do critério como aviso.
- `seo-audit.py`: `alt` sem valor (comum em HTML minificado) não é mais contado como ausente; a home servida numa subpasta não é mais cobrada por `BreadcrumbList`; variante `www` sem DNS deixa de ser tratada como erro.

## [1.0.3] - 2026-10-05

### Corrigido

- Snippet de verificação de imagens no navegador: lia `img.naturalWidth`, que em `srcset` com descritores `w` vem dividido pela densidade escolhida; em telas de alta densidade (ex.: 412 px × 1,75) acusava falsos problemas de compressão e escondia os de tamanho. Agora lê as dimensões reais do arquivo carregando `currentSrc` numa `Image` avulsa.
- WebP com transparência: o canal alfa também precisa ser lossy (`alpha_q` ~50 em vez de 80); o sharp grava o alfa sem perda por padrão e componentes de imagem de framework não expõem esse controle. Orientação para gerar fora do componente ou achatar sobre o fundo; logos em camadas raster são julgados camada a camada.
- LCP: o elemento LCP não pode entrar com `opacity: 0` ou `animation-delay` (gera "Element render delay"); no mobile ele costuma ser o parágrafo do hero. `perf-audit.py` passa a imprimir sempre o elemento LCP e suas fases, com alerta quando o atraso de renderização passa de 1 s.
- Fórmula de compressão na tabela corrigida para 0,167 byte/pixel, igual ao texto e ao snippet.

## [1.0.2] - 2026-10-05

### Corrigido

- Imagens: larguras do `srcset` derivadas da medição (inclusive os cenários do PageSpeed, 412 px × 1,75 e 1350 px × 1) em vez de listas genéricas; `sizes` igual à largura renderizada; critérios exatos do Lighthouse documentados (0,167 byte/pixel para compressão, 12 KiB de sobra com `srcset`); qualidade WebP 70–78, sem lossless por padrão; logos em SVG ou WebP lossy.
- Reflow forçado: lista das propriedades que forçam layout, o padrão do header com scroll spy proibido e uma implementação de referência com `IntersectionObserver`; busca no código como verificação obrigatória.
- Cache: passo a passo para quando a CDN reescreve o cache (Browser Cache TTL, Cache Rules/Page Rules, purge, conferência com `curl`), diagnóstico comparando a CDN ligada e desligada, caminhos atuais da Cloudflare com links diretos do painel e orientação para esperar a renovação das cópias regionais antes de mexer em configuração; o `Expires` diferente do `max-age` é inofensivo; scripts da própria CDN não são controlados pelo `.htaccess`; roteiro para quando o PageSpeed ainda acusa cache curto.
- `perf-audit.py`: mostra itens reprovados de checklists (ex.: falta de `fetchpriority`), o seletor do elemento, o trecho de código na linha/coluna do reflow e marca as URLs que pertencem à CDN.

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

[Não lançado]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.4...HEAD
[1.0.4]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/jesmarcelo/premium-web-studio/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jesmarcelo/premium-web-studio/releases/tag/v1.0.0
