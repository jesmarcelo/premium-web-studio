# QA e revisão visual

Regra central: **marque um item como aprovado apenas se ele foi realmente verificado.** Para cada item, registre um destes estados em `docs/website/qa-report.md`:

- ✅ verificado e aprovado (com a ferramenta/método usado);
- ❌ verificado com problema (e se foi corrigido);
- ⚠️ verificado parcialmente (explique);
- ⏭️ não verificado (explique por quê — ex.: ferramenta indisponível).

Um ❌ só pode ficar no relatório final com um destes estados: **decisão do usuário** (opções e custos apresentados, escolha registrada com data), **fora do controle do projeto** (com evidência) ou **a verificar após publicar** (com o comando). Qualquer outro ❌ volta ao [ciclo de correção](WORKFLOW.md#ciclo-de-correção-até-zerar-fases-8-a-10).

Rode tudo contra o **build de produção** sempre que possível.

---

## 1. Build e código

- [ ] Instalação limpa funciona com o gerenciador de pacotes do projeto.
- [ ] `build` sem erros.
- [ ] `typecheck` sem erros (quando aplicável).
- [ ] `lint` sem erros; avisos novos justificados ou corrigidos.
- [ ] Testes existentes passando; testes novos para lógica não trivial (formulários, utilitários, integrações).
- [ ] Console do navegador sem erros nem avisos relevantes (hidratação, chaves, 404 de assets).
- [ ] Sem código morto, `console.log` de depuração, imports não usados ou TODOs não registrados.
- [ ] Nenhum secret no código, no bundle do cliente ou em arquivos versionados.
- [ ] Dependências novas listadas e justificadas.

## 2. Funcionalidade

- [ ] Todos os links internos funcionam; externos abrem corretamente (com `rel="noopener"` quando `target="_blank"`).
- [ ] Navegação principal, mobile e rodapé funcionam.
- [ ] Formulários: envio válido, validação de erros, mensagens de sucesso/erro, estado de carregamento, proteção contra envio duplo, anti-spam, destino real dos dados testado (ou registrado como pendente).
- [ ] Estados de loading, vazio, erro e sucesso implementados em tudo que é assíncrono.
- [ ] Página 404 (e 500, quando aplicável) projetada e com status correto.
- [ ] Integrações (analytics, CMS, pagamentos, mapas) funcionando ou claramente documentadas como pendentes.

## 3. Responsividade

Verifique em: **320/375 px** (mobile), **768 px** (tablet), **1024 px** (notebook pequeno), **1440 px** (desktop), **1920 px+** (tela grande).

- [ ] Sem rolagem horizontal em nenhuma largura (inclusive 320 px).
- [ ] Sem textos cortados, sobrepostos ou com quebras ruins (palavras longas, títulos com uma palavra órfã).
- [ ] Imagens com proporção e enquadramento corretos em cada breakpoint.
- [ ] Navegação utilizável em mobile; alvos de toque adequados.
- [ ] Tabelas, código e conteúdo largo tratados (rolagem própria, reorganização).
- [ ] Em telas grandes, o conteúdo não fica esticado nem perdido (largura máxima).
- [ ] Orientação paisagem em mobile não quebra o layout.
- [ ] Alturas de tela em mobile usam `dvh`/`svh` e não ficam escondidas sob a barra do navegador.

## 4. Acessibilidade

Detalhes em [ACCESSIBILITY.md](ACCESSIBILITY.md).

- [ ] axe/Lighthouse sem violações críticas ou sérias.
- [ ] Navegação completa por teclado com foco visível.
- [ ] Link "pular para o conteúdo".
- [ ] Headings em ordem lógica; um `h1` por página; landmarks corretos.
- [ ] Contraste AA em todos os pares de cor usados.
- [ ] Imagens com `alt` adequado.
- [ ] Formulários com labels, erros acessíveis e `autocomplete`.
- [ ] `prefers-reduced-motion` respeitado (testado com emulação).
- [ ] Zoom 200% e reflow em 320 px sem perda de conteúdo.

## 5. SEO

Detalhes em [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md).

- [ ] `scripts/build-audit.py <pasta do build> --site <url final>` saindo com código 0 (ou cada reprovação com estado final).
- [ ] `scripts/seo-audit.py` rodado contra o build de produção (ou o site publicado), sem pendências não justificadas.
- [ ] URL pública final (domínio e subpasta, se houver) configurada no build; canonical, `og:url`, `og:image` e URLs do JSON-LD absolutos, e nenhuma reescrita de caminho pós-build tocando neles.
- [ ] `title` (30–65) e `description` (70–160) únicos por página, gerados a partir de campos do conteúdo.
- [ ] Canonical, `lang`, Open Graph (com imagem, dimensões e `alt`) e Twitter/X card com `twitter:image`; `og:type` = `article` em artigos.
- [ ] Imagem de compartilhamento desenhada para a marca (legível em miniatura), JPG/PNG 1200×630 até 300 KB; robôs do Facebook, WhatsApp, X e LinkedIn recebem 200 (`seo-audit.py`); prévia conferida no Sharing Debugger/Post Inspector depois de publicar, ou registrada como a verificar.
- [ ] Google: `WebSite` com `name` na home, `Organization.logo` absoluto (≥ 112×112), favicon quadrado múltiplo de 48 px, `max-image-preview:large`; Search Console verificado e sitemap enviado (ou listado nas pendências com o passo a passo para o usuário).
- [ ] Paginação com "Página N" no título e canonical próprio; taxonomias com texto próprio ou `noindex`.
- [ ] `sitemap.xml` (com `lastmod` real) e `robots.txt` corretos; `/favicon.ico` responde 200; variante `www`/não-`www` com redirect 301. Em subpasta, o que depende da raiz do domínio registrado conforme [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#site-servido-numa-subpasta).
- [ ] Dados estruturados válidos e condizentes com o conteúdo visível: grafo Organization/WebSite (e Person, se houver), `BreadcrumbList` abaixo da home, `BlogPosting` completo em artigos.
- [ ] Conteúdo principal presente no HTML inicial.
- [ ] Redirects 301 para URLs alteradas (em redesign).
- [ ] Páginas que não devem ser indexadas com `noindex`.

## 6. Performance

- [ ] Lighthouse mobile no build de produção (registre os números).
- [ ] `scripts/perf-audit.py --runs 3` rodado (mobile e desktop) contra o build de produção e, depois da publicação, contra o site publicado; cada item listado resolvido ou com estado final da [escada de soluções](SEO-PERFORMANCE.md#escada-de-soluções).
- [ ] Imagem LCP priorizada; demais imagens com lazy loading e dimensões.
- [ ] Imagens raster em AVIF com fallback WebP (`<picture>` com `<source type="image/avif">` ou negociação pelo `Accept`), redimensionadas para o tamanho exibido medido (1× e 2×), sem originais PNG/JPG servidos (exceto `og:image` e favicons); o `<img>` de fallback aponta para WebP.
- [ ] Toda imagem com `srcset` de larguras derivadas da medição (vizinhas a no máximo ~20%) e `sizes` igual à largura renderizada; snippet de verificação de [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#pipeline-obrigatório-de-imagens-raster) sem linhas nos cenários 412 px × 1,75 e 1350 px × 1.
- [ ] Nenhuma imagem acima de 0,167 byte/pixel com mais de 4 KiB de sobra (critério de compressão do PageSpeed), conferido em todos os arquivos do build com `build-audit.py`; o critério vale para o AVIF entregue (o WebP de fallback reprovado vira aviso); logos em SVG ou AVIF + WebP com alfa lossy, sem duas versões baixadas quando só uma aparece.
- [ ] Fontes otimizadas (WOFF2, subset, `font-display`, preload apenas da crítica); poucos arquivos de fonte na home.
- [ ] Sem reflow forçado causado pelo código do projeto: `build-audit.py` sem linhas no grupo `reflow` (nenhuma leitura de geometria no nível superior dos scripts, como `let y = scrollY`), revisão dos handlers no código-fonte e `perf-audit.py --runs 3` sem "Forced reflow" do projeto; os vindos de terceiros registrados.
- [ ] `fetchpriority="high"` no elemento que o `perf-audit.py` imprime como LCP, em mobile e desktop (não no que se supõe ser o principal), sem `loading="lazy"` e descoberto no HTML; o grupo LCP sem itens reprovados.
- [ ] Elemento LCP (o que o `perf-audit.py` imprime, muitas vezes um texto do hero no mobile) visível desde o primeiro paint: sem `opacity: 0` nem `animation-delay` na entrada; "Element render delay" abaixo de 1 s.
- [ ] Árvore de dependência de rede revisada: sem `@import` encadeado, sem scripts/beacons desnecessários no caminho crítico.
- [ ] JS do cliente mínimo; componentes pesados carregados sob demanda.
- [ ] Scripts de terceiros adiados ou com fachada.
- [ ] CLS sem deslocamentos visíveis no carregamento.
- [ ] HTML, CSS e JS minificados no build de produção.
- [ ] Configuração de servidor gerada para a hospedagem ([references/server-config.md](references/server-config.md)) e **presente na pasta do build** (ex.: `dist/.htaccess`).
- [ ] Brotli/gzip ativos e `Cache-Control` ≥ 30 dias verificados com `curl -I` no ambiente publicado em uma URL real de **cada extensão** servida (`webp`, `avif`, `woff2`, `css`, `js`, `svg`), ou registrados como pendência. Com CDN como proxy, Browser Cache TTL em "Respect Existing Headers".

## 7. Conteúdo

- [ ] Sem lorem ipsum.
- [ ] Ortografia e acentuação revisadas.
- [ ] Nenhuma informação inventada (números, clientes, depoimentos, prêmios).
- [ ] Placeholders explicitamente identificados e listados nas pendências.
- [ ] Microcopy específica (botões descrevem a ação: "Solicitar orçamento", não "Enviar").
- [ ] Informações legais exigidas no país e no setor (política de privacidade, termos, identificação legal da empresa, aviso de cookies, avisos regulatórios).

---

## 8. Revisão visual (fase 9)

### Ferramentas, em ordem de preferência
1. **Playwright MCP** ou **Claude in Chrome** (se conectados): navegar, redimensionar, capturar screenshots e inspecionar.
2. **Playwright CLI** (com aprovação para baixar via `npx`):
   ```bash
   npx playwright screenshot --viewport-size=375,812 --full-page http://localhost:4321 tmp/screens/home-375.png
   npx playwright screenshot --viewport-size=1440,900 --full-page http://localhost:4321 tmp/screens/home-1440.png
   ```
   (ajuste porta e rota; screenshots em `tmp/screens/`). Depois leia as imagens para inspecioná-las.
3. **Firecrawl** com formato `screenshot` apenas para URLs públicas (nunca para localhost nem staging privado).
4. Nenhuma disponível: diga isso claramente e peça ao usuário screenshots ou conduza uma revisão guiada com perguntas objetivas.

Capture, no mínimo, home e páginas-chave em 375, 768, 1440 e 1920 px, e estados de hover/foco/erro relevantes.

### Cuidados com a captura
- **Elementos fixos, sticky, canvas ou vídeo** costumam sair duplicados, deslocados ou em branco com `--full-page`. Nesses casos, capture por viewport, rolando a página, e confira cada captura com o que aparece no navegador. Falha de captura não é defeito do site: refaça a captura antes de registrar o problema.
- **Animações e scroll-linked** não aparecem numa tela parada: percorra a rolagem com capturas sequenciais ou gere uma tira de frames ([VISUAL-REVIEW.md](VISUAL-REVIEW.md#3-evidências)).
- **Comparação com a referência** só vale entre larguras e estados equivalentes.

### O que procurar (olhar de diretor de arte)

Este checklist é a **autoverificação** antes do ciclo de críticos: serve para eliminar os defeitos óbvios. Ele não substitui o julgamento independente de [VISUAL-REVIEW.md](VISUAL-REVIEW.md).

- [ ] **Alinhamento:** elementos compartilham eixos; nada desalinhado por poucos pixels.
- [ ] **Espaçamento:** ritmo consistente com a escala de tokens; seções nem apertadas nem soltas demais.
- [ ] **Hierarquia:** o foco de cada tela é óbvio em 3 segundos; CTA primário inconfundível.
- [ ] **Tipografia:** escala com contraste suficiente, comprimento de linha confortável, sem viúvas/órfãs feias em títulos.
- [ ] **Quebras:** nada sobreposto, cortado ou transbordando.
- [ ] **Mobile:** hierarquia mantida, nada espremido, imagens com bom recorte, CTA alcançável.
- [ ] **Componentes fracos:** cards, formulários, botões e rodapé com acabamento equivalente ao hero.
- [ ] **Aparência genérica:** compare com a lista de anti-padrões de [DESIGN.md](DESIGN.md#anti-padrões-de-site-gerado-por-ia). Se a página pudesse ser de qualquer empresa, refine.
- [ ] **Contraste:** textos sobre imagens e cores de destaque legíveis.
- [ ] **Coerência:** todas as páginas parecem do mesmo produto; estados (hover, foco, ativo, desabilitado) consistentes.
- [ ] **Fidelidade à direção aprovada:** o resultado corresponde ao `design-direction.md`.
- [ ] **Originalidade:** o resultado não é reconhecível como cópia de nenhuma referência.

### Registro
Liste os problemas encontrados por prioridade (bloqueador, alto, médio, polimento), com página, viewport e descrição. Corrija na fase 10 e recapture para confirmar. Depois, siga para o ciclo de críticos independentes ([VISUAL-REVIEW.md](VISUAL-REVIEW.md)) e registre os vereditos na seção "Ciclo visual" do `qa-report.md`.
