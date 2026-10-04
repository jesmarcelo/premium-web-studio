# QA e revisão visual

Regra central: **marque um item como aprovado apenas se ele foi realmente verificado.** Para cada item, registre um destes estados em `docs/website/qa-report.md`:

- ✅ verificado e aprovado (com a ferramenta/método usado);
- ❌ verificado com problema (e se foi corrigido);
- ⚠️ verificado parcialmente (explique);
- ⏭️ não verificado (explique por quê — ex.: ferramenta indisponível).

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

- [ ] `scripts/seo-audit.py` rodado contra o build de produção (ou o site publicado), sem pendências não justificadas.
- [ ] `title` (30–65) e `description` (70–160) únicos por página, gerados a partir de campos do conteúdo.
- [ ] Canonical, `lang`, Open Graph (com imagem, dimensões e `alt`) e Twitter/X card; `og:type` = `article` em artigos.
- [ ] Paginação com "Página N" no título e canonical próprio; taxonomias com texto próprio ou `noindex`.
- [ ] `sitemap.xml` (com `lastmod` real) e `robots.txt` corretos; `/favicon.ico` responde 200; variante `www`/não-`www` com redirect 301.
- [ ] Dados estruturados válidos e condizentes com o conteúdo visível: grafo Organization/WebSite (e Person, se houver), `BreadcrumbList` abaixo da home, `BlogPosting` completo em artigos.
- [ ] Conteúdo principal presente no HTML inicial.
- [ ] Redirects 301 para URLs alteradas (em redesign).
- [ ] Páginas que não devem ser indexadas com `noindex`.

## 6. Performance

- [ ] Lighthouse mobile no build de produção (registre os números).
- [ ] `scripts/perf-audit.py` rodado (mobile e desktop) contra o build de produção e, depois da publicação, contra o site publicado; cada item listado corrigido ou justificado.
- [ ] Imagem LCP priorizada; demais imagens com lazy loading e dimensões.
- [ ] Imagens raster em WebP, redimensionadas para o tamanho exibido medido (1× e 2×), sem originais PNG/JPG servidos (exceto `og:image` e favicons).
- [ ] Toda imagem com `srcset` + `sizes` (ou `layout` responsivo do framework); nenhum arquivo entregue maior que exibido × `devicePixelRatio` (snippet de verificação em [SEO-PERFORMANCE.md](SEO-PERFORMANCE.md#pipeline-obrigatório-de-imagens-raster), em 375 e 1440 px).
- [ ] Fontes otimizadas (WOFF2, subset, `font-display`, preload apenas da crítica); poucos arquivos de fonte na home.
- [ ] Sem reflow forçado causado pelo código do projeto (Lighthouse "Forced reflow" e DevTools → Performance); os vindos de terceiros registrados.
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

### O que procurar (olhar de diretor de arte)
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
Liste os problemas encontrados por prioridade (bloqueador, alto, médio, polimento), com página, viewport e descrição. Corrija na fase 10 e recapture para confirmar.
