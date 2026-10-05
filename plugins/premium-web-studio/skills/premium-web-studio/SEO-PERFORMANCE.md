# SEO técnico e performance

## Parte 1 — SEO

### Metadados por página
- `<title>` único, 50–60 caracteres, palavra-chave principal no início, marca no fim (`Serviço — Marca`).
- `<meta name="description">` único, 140–160 caracteres, descritivo e com convite à ação.
- **Gere os metadados a partir de campos do conteúdo, nunca à mão página a página.** Cada tipo de conteúdo (página, artigo, categoria, produto) tem campos próprios de SEO (`seoTitle`, `description`, `image`) separados do título visível, com fallback para o título visível. Um título editorial longo continua no H1; o `<title>` usa a versão curta.
- **Valide limites no build ou no QA** (schema de conteúdo com `max`, ex.: Zod/Content Collections, ou o script `scripts/seo-audit.py`): título fora de 30–65 caracteres, descrição fora de 70–160, duplicados e ausentes devem aparecer antes da publicação.
- `<link rel="canonical">` absoluto em todas as páginas indexáveis.
- `<meta name="robots" content="noindex">` em páginas que não devem ser indexadas (obrigado, área logada, staging).
- `<html lang>` correto; `hreflang` (incluindo `x-default`) em sites multilíngues.
- Favicon, `apple-touch-icon` e `manifest` quando aplicável; `theme-color`.

### Compartilhamento social
- Open Graph: `og:title`, `og:description`, `og:image` (1200×630, < 300 KB, absoluta), `og:image:width`, `og:image:height`, `og:image:alt`, `og:url`, `og:type`, `og:site_name`, `og:locale`.
- `og:type` = `article` em artigos, com `article:published_time`, `article:modified_time` e `article:section`; `website` nas demais.
- `og:image` própria por artigo/produto (a imagem de destaque), com uma imagem padrão da marca como fallback.
- Twitter/X: `twitter:card` = `summary_large_image` e `twitter:image` explícito quando o site for compartilhado com frequência (os demais campos OG servem de fallback).

### Conteúdo e estrutura
- Um `h1` por página, alinhado à intenção de busca; headings descrevem o conteúdo.
- Conteúdo principal presente no HTML inicial (SSR/SSG) — não dependa de JS no cliente para conteúdo indexável.
- Textos de link descritivos (nada de "clique aqui").
- Links internos entre páginas relacionadas; breadcrumbs em sites profundos. Em artigos, links no corpo do texto para 2–5 conteúdos relacionados e um bloco de "relacionados" ao final; nenhuma página indexável órfã (sem link interno apontando para ela).
- Conteúdo em série (capítulos, partes, aulas): o H1 e o `<title>` incluem o nome da série, não só o número ("Nome da série — Capítulo 3", não "Capítulo 3"); links de anterior/próximo e de volta ao índice.
- **Autoria e credibilidade (E-E-A-T):** em conteúdo editorial ou especializado, autor identificado com página própria (biografia, formação, links), datas de publicação e de atualização visíveis, e o mesmo autor declarado nos dados estruturados.
- Imagens com `alt` e nomes de arquivo descritivos.
- Conteúdo original, útil e específico — não invente informações para "encher" página.

### URLs
- Curtas, legíveis, minúsculas, hífens, sem parâmetros desnecessários, no idioma do público.
- Política consistente de barra final e de `www`: a variante não usada responde com **redirect 301** para a canônica (só o `canonical` não basta).
- **Paginação** (`/blog/2`): `canonical` para a própria página (não para a primeira), sem `noindex`, e `<title>`/description com "Página N" para não duplicar a primeira página.
- **Páginas de taxonomia** (categoria, tag, autor): texto de introdução e description próprios, escritos para a busca. Taxonomias com pouco conteúdo (1–2 itens) recebem `noindex, follow` ou são consolidadas.
- Páginas utilitárias sem valor de busca (doação, obrigado, dados do usuário, resultados de busca interna): avalie `noindex`.
- **Redesign/migração:** mapeie URLs antigas → novas e configure redirects 301; preserve URLs que já ranqueiam sempre que possível; atualize links internos.

### Arquivos técnicos
- `sitemap.xml` gerado automaticamente, apenas com URLs canônicas e indexáveis; referenciado no `robots.txt`; `lastmod` com a data real de atualização do conteúdo (não a data do build). Sitemap index quando houver várias seções ou muitas URLs.
- Feed RSS/Atom em sites com blog, anunciado com `<link rel="alternate" type="application/rss+xml">`.
- `/favicon.ico` respondendo 200 na raiz (alguns buscadores e navegadores o pedem direto, mesmo com outro ícone declarado), além do ícone declarado no `<head>`.
- Firewall/CDN (bot protection) não pode bloquear `robots.txt`, sitemaps nem buscadores legítimos; teste com o user agent do Googlebot.
- `robots.txt` que não bloqueie CSS/JS nem páginas importantes; staging bloqueado (preferencialmente por autenticação, não só robots).
- Página 404 útil com status HTTP 404 real.

### Dados estruturados (JSON-LD)
Use apenas tipos que correspondam ao conteúdo visível da página. Monte um **grafo** (`@graph`) com `@id` estáveis: `Organization` (ou `LocalBusiness`), `WebSite` e, quando houver uma pessoa à frente da marca, `Person`, presentes em todas as páginas e referenciados por `@id` (`publisher`, `author`) nos tipos específicos de cada página.

Tipos comuns:
- `Organization` / `LocalBusiness` (e subtipos como `LegalService`, `Dentist`, `Restaurant`) com nome, logo, contato, endereço, `sameAs`.
- `WebSite` (com `SearchAction` se houver busca interna).
- `BreadcrumbList` em todas as páginas abaixo da home (Início › Seção › Página).
- `BlogPosting`/`Article` completo: `headline`, `description`, `image`, `datePublished`, `dateModified`, `author` (Person com `url`), `publisher`, `mainEntityOfPage`, `inLanguage`, `articleSection`.
- `Course` (com `provider` e `offers`/`hasCourseInstance`) para cursos; `Product` + `Offer` para e-commerce; `Service` para serviços; `Event` para eventos; `Book`/`CollectionPage` para coleções e obras.
- `FAQPage` somente quando o conteúdo de perguntas e respostas for de fato visível na página.
- Valide no Rich Results Test e no Schema Markup Validator.
- Nunca inclua avaliações, preços ou dados que não existam de fato.

### SEO local (quando aplicável)
- NAP (nome, endereço, telefone) consistente no site e no Google Business Profile.
- Página por unidade/localidade com conteúdo próprio; mapa incorporado com carregamento tardio.

### Analytics e consentimento
- Analytics apenas se pedido; prefira soluções leves (Plausible, Umami, Fathom) ou GA4/GTM com carregamento após consentimento quando exigido pela lei de privacidade aplicável (ex.: GDPR, LGPD, CCPA).
- Banner de consentimento acessível, sem bloquear o conteúdo inteiro sem necessidade.

---

## Parte 2 — Performance

### Metas (Core Web Vitals, percentil 75, mobile)
| Métrica | Bom |
|---|---|
| LCP (Largest Contentful Paint) | ≤ 2,5 s |
| INP (Interaction to Next Paint) | ≤ 200 ms |
| CLS (Cumulative Layout Shift) | ≤ 0,1 |

Metas de laboratório adicionais (orientativas): Lighthouse Performance ≥ 90 em mobile para sites de conteúdo; JS inicial < 150 KB comprimido em sites institucionais.

### Imagens
- Formatos AVIF/WebP com fallback quando necessário; SVG para logos e ícones.
- `srcset`/`sizes` responsivos; nunca sirva imagem 2× maior que o necessário.
- `width`/`height` ou `aspect-ratio` sempre (evita CLS).
- Imagem LCP: **sem** lazy loading, com `fetchpriority="high"` (ou o recurso equivalente do framework, como `priority` no `next/image`) e, se descoberta tardiamente, `preload`.
- **O elemento LCP nunca entra com animação atrasada.** O LCP só é registrado quando o elemento fica visível; um texto ou imagem que começa com `opacity: 0` (ou `visibility: hidden`, `clip-path`, blur total) e só aparece depois de um `animation-delay` empurra o LCP pelo tempo do atraso mais a animação (o Lighthouse mostra isso como "Element render delay"). No mobile o LCP costuma ser o parágrafo de abertura do hero, não o título nem a imagem: confirme qual é no relatório (`perf-audit.py` imprime o elemento) e deixe esse elemento visível desde o primeiro paint. A coreografia de entrada pode continuar nos outros elementos; se o LCP também precisar de movimento, anime só `transform`, partindo de opacidade 1, sem atraso.
- `loading="lazy"` e `decoding="async"` abaixo da dobra.
- Use o componente de imagem do framework quando existir.
- Toda imagem raster (fornecida pelo cliente, gerada ou de banco) passa pelo pipeline abaixo antes de entrar no site.

#### Pipeline obrigatório de imagens raster
1. **Meça o tamanho exibido.** Com a página rodando, descubra a maior largura CSS que a imagem ocupa em cada breakpoint (375, 768, 1440, 1920 px). No navegador: `getBoundingClientRect().width` do elemento; sem navegador, calcule pelo layout (largura do container, colunas, `max-width`). Registre também a proporção do recorte (`object-fit`/`aspect-ratio`).
2. **Redimensione para larguras derivadas da medição, não para uma lista genérica.** Para cada breakpoint, gere a largura medida × 1 e × 2, mais as duas do PageSpeed (largura exibida no viewport de 412 px × 1,75 e no de 1350 px × 1), nunca maiores que o original. Entre dois candidatos vizinhos, no máximo ~15–20% de diferença: com candidatos esparsos (ex.: 400w e 720w para uma imagem exibida a 531 px), o navegador baixa o próximo acima e o PageSpeed acusa. Recorte na proporção exibida quando ela for fixa.
3. **Converta para WebP com compressão real.** Nunca converta PNG para JPG nem entregue o arquivo original. Qualidade de partida: ~70–78 para fotos e ilustrações (com `-sharp_yuv` no `cwebp` quando houver texto ou bordas finas). Lossless e qualidade ≥ 90 quase sempre reprovam no critério de compressão abaixo; use só se o arquivo ainda passar nele. WebP com transparência também deve ser lossy **inclusive no canal alfa**: o sharp e vários encoders gravam o alfa sem perda por padrão (`alphaQuality: 100`), e em arte fina com transparência (traços de logo, filetes, ornamentos) o alfa pesa mais que a cor. Parta de `-q 70 -alpha_q 50` no `cwebp` (sharp: `{ quality: 70, alphaQuality: 50, effort: 6 }`) e suba o `alpha_q` só se as bordas serrilharem. Componentes de imagem de framework costumam expor só `quality`, sem controle do alfa; se a imagem transparente reprovar, gere os arquivos fora do componente (script com sharp/`cwebp` e `srcset` manual) ou, quando o fundo atrás dela for sempre o mesmo, achate a imagem sobre essa cor e elimine o alfa. AVIF pode ser oferecido adicionalmente via `<picture>`.
4. **Declare no markup.** `srcset` com as larguras geradas, `sizes` com a largura **medida** em cada breakpoint (um `sizes` de 500px para uma imagem que renderiza com 531 px faz o navegador pular para o candidato seguinte), `width`/`height` da versão 1×.
5. **Confira o resultado** com o snippet de verificação abaixo e inspecione visualmente (artefatos, banding, texto borrado). Referência: imagem de conteúdo < 200 KB, hero < 300 KB na versão 1×.

**Como o PageSpeed julga cada imagem** (critérios do código do Lighthouse, "Improve image delivery"):

| Aviso | Quando aparece | Como passar |
|---|---|---|
| "Aumentar o fator de compactação" | arquivo com mais de **0,167 byte por pixel do arquivo** (largura × altura do arquivo, não da tela) e economia estimada acima de 4 KiB | qualidade ~70–78, sem lossless, alfa lossy em imagens transparentes; `bytes ≤ largura × altura × 0,167 + 4096` |
| "Maior do que precisa ser" (com `srcset`) | pixels do arquivo além dos exibidos × densidade, valendo mais de **12 KiB** | candidatos próximos (passo 2) e `sizes` medido |
| "Maior do que precisa ser" (sem `srcset`) | qualquer sobra acima de 4 KiB | sempre `srcset` |

O PageSpeed emula mobile com viewport de 412 px a densidade 1,75 e desktop com 1350 px a densidade 1; teste nesses dois cenários.

**Logos e marcas:** SVG sempre que existir ou puder ser vetorizado (peça o vetor ao cliente). Logo raster com transparência, mesmo pequeno, costuma passar de 0,8 byte/pixel em lossless e é reprovado. Se for inevitável, WebP lossy com `-alpha_q 50` (ver passo 3), no tamanho exibido × 2; logo de arte fina pequeno pode reprovar mesmo assim (medido: 220 × 95 px com `-q 75 -alpha_q 80` fica em ~0,6 byte/pixel), e aí a saída é vetorizar ou achatar sobre o fundo. Isso vale também para logos montados em camadas raster para animação: cada camada é uma imagem julgada separadamente. Não baixe duas versões do mesmo logo (positivo/negativo) quando só uma aparece: use `<picture>` com `media`, CSS ou um SVG com `currentColor`.

Ferramentas, conforme o disponível no projeto (verifique antes; peça aprovação para instalar):
```bash
# cwebp (libwebp): redimensiona e converte
cwebp -q 80 -resize 1440 0 origem.png -o public/img/hero-1440.webp
# ImageMagick
magick origem.png -resize 1440x -quality 80 public/img/hero-1440.webp
# sharp-cli (via npx)
npx sharp-cli -i origem.png -o public/img/hero-1440.webp resize 1440 -- webp --quality 80
```
Mantenha o original fora da pasta pública (ex.: `assets-src/` ou `tmp/`) para poder regerar.

**Original guardado, entrega recortada.** O arquivo original (em alta resolução) pode e deve ficar no projeto como fonte; o que nunca pode acontecer é o navegador baixar um arquivo maior que o exibido. O PageSpeed acusa "imagem maior do que precisa ser" quando o arquivo entregue passa do tamanho exibido × densidade de pixels do dispositivo, mesmo que seja só 1,5×.

**Componentes de imagem do framework** (`next/image`, `astro:assets`, `@nuxt/image` etc.) já redimensionam e convertem, **mas só geram `srcset` quando configurados para isso**. Uma única `width` gera um único arquivo e nenhum `srcset`: todo dispositivo baixa a mesma imagem. Regras:

- **Astro (`<Image>`/`<Picture>`):** passe `widths={[...]}` com as larguras do passo 2 **e** `sizes` medido, além de `quality={75}` (ou o padrão global em `image.service.config`). `width` sozinho gera um único arquivo. `layout="constrained"` (Astro 5.10+) gera `srcset` automaticamente, mas com breakpoints genéricos e espaçados (640, 750, 828, 1080…) e um `sizes` que presume uma coluna; em layouts com colunas, sobrescreva `widths` e `sizes`.
- **Next (`next/image`):** `sizes` é obrigatório sempre que a imagem não tem largura fixa (com `fill` ou largura responsiva); sem ele, o navegador assume `100vw` e baixa a maior versão. Ajuste `quality` (~75).
- **Nuxt (`<NuxtImg>`):** use `sizes` (ex.: `sizes="sm:100vw md:50vw lg:600px"`) e `densities="x1 x2"`.
- **Qualquer framework:** o passo 1 continua obrigatório: o `sizes` precisa refletir a largura medida em cada breakpoint, não um chute. Confirme que o formato de saída inclui WebP/AVIF.

**Verificação no navegador.** Com o build de produção aberto, role a página até o fim (para carregar as imagens lazy) e rode no console (ou via Playwright `page.evaluate`) nos dois cenários do PageSpeed: 412 px com densidade 1,75 e 1350 px com densidade 1 (no DevTools, modo dispositivo com "Device pixel ratio"). Corrija toda linha que aparecer:

```js
(async () => {
  const imgs = [...document.images].filter(i => i.currentSrc && i.getBoundingClientRect().width > 0 && !i.currentSrc.endsWith('.svg'));
  const linhas = await Promise.all(imgs.map(async i => {
    // Dimensões reais do arquivo: em <img srcset> com descritores "w", naturalWidth vem dividido pela densidade escolhida.
    const f = new Image(); f.src = i.currentSrc; await f.decode().catch(() => {});
    const w = f.naturalWidth, h = f.naturalHeight, px = w * h, r = i.getBoundingClientRect();
    const bytes = performance.getEntriesByName(i.currentSrc)[0]?.decodedBodySize || 0;
    const sobraPx = 1 - (r.width * r.height * devicePixelRatio ** 2) / px;
    return { src: i.currentSrc.split('/').pop(), arquivo: `${w}x${h}`, exibido: `${Math.round(r.width)}x${Math.round(r.height)}`,
      kib: +(bytes / 1024).toFixed(1), bytesPorPixel: +(bytes / px).toFixed(3),
      compressao: bytes - px * 0.167 > 4096 ? 'REPROVA' : 'ok', tamanho: sobraPx > 0 && sobraPx * bytes > 12288 ? 'REPROVA' : 'ok' };
  }));
  const reprovadas = linhas.filter(x => x.compressao !== 'ok' || x.tamanho !== 'ok');
  console.table(reprovadas);
  return reprovadas;
})()
```

Não use `img.naturalWidth` direto para essa conta: quando a imagem vem de um `srcset` com descritores `w`, o navegador divide as dimensões do arquivo pela densidade que escolheu (arquivo de 720 px num slot de 412 px a 1,75× aparece como 412). Em telas de alta densidade isso subestima os pixels, gera falsos "REPROVA" de compressão e esconde os de tamanho. O snippet acima carrega `currentSrc` numa `Image` avulsa, sem `srcset`, para ler as dimensões reais (vem do cache, sem novo download).

`scripts/perf-audit.py` faz a mesma checagem a partir do Lighthouse, em mobile e desktop.

**Exceções:** logos e ícones em SVG; `og:image` em JPG ou PNG (nem todo scraper de redes sociais lê WebP); favicons nos formatos próprios (ICO/PNG/SVG).

- Vídeos de fundo: comprimidos, `muted`, `playsinline`, com `poster`, desativados com reduced motion e em conexões lentas quando possível; prefira não usá-los no hero mobile.

### Fontes
- Self-host (ou o otimizador de fontes do framework) em WOFF2.
- Subset conforme os idiomas do site (ex.: latin + latin-ext para idiomas com acentos; cyrillic, greek, vietnamese etc. quando necessário) e apenas os pesos usados; prefira fontes variáveis quando substituem vários arquivos.
- `font-display: swap` (ou `optional` para fontes não essenciais).
- `preload` apenas da fonte usada acima da dobra — no máximo 1–2 arquivos. Pré-carregar todas as variações compete com a imagem LCP pela banda e piora o LCP.
- Métricas de fallback ajustadas (`size-adjust`, `ascent-override`) para reduzir CLS — `next/font` e Fontsource fazem isso.
- **Poucos arquivos de fonte na primeira visita.** Cada arquivo é um nó na árvore de dependência de rede. Some os `.woff2` baixados na home: acima de 3–4, reduza (fonte variável no lugar de vários pesos, um peso a menos, itálico só se usado acima da dobra). Fontes de escrita secundária (outro alfabeto, uso pontual) levam `unicode-range` para só baixarem quando os caracteres aparecem.

### JavaScript
- Envie o mínimo de JS: renderize no servidor/estático, hidrate apenas o interativo (ilhas, Server Components).
- Code splitting por rota; `import()` dinâmico para componentes pesados abaixo da dobra (mapas, players, gráficos, carrosséis).
- Evite bibliotecas pesadas para tarefas simples (ver [ENGINEERING.md](ENGINEERING.md#dependências)).
- Quebre tarefas longas (> 50 ms) em interações; evite handlers síncronos pesados (INP).
- Analise o bundle (`vite-bundle-visualizer`, `@next/bundle-analyzer`, `rollup-plugin-visualizer`).

### Reflow forçado (layout thrashing)
Acontece quando o JS lê uma propriedade de geometria depois de alterar estilo ou DOM no mesmo quadro, obrigando o navegador a recalcular o layout na hora. O PageSpeed lista em "Reflow forçado" com arquivo, linha e coluna (`/pagina/:6:538` = script inline na linha 6 do HTML). O resultado varia entre execuções, porque depende do que roda durante a carga: um teste limpo não prova ausência; a prevenção está no código.

**Propriedades que forçam layout quando lidas:** `offsetTop/Left/Width/Height`, `clientWidth/Height`, `scrollTop/Height`, `scrollX/scrollY`, `innerWidth/innerHeight`, `getBoundingClientRect()`, `getComputedStyle()`, `focus()`, `scrollIntoView()`.

**O padrão que mais causa o problema** é o header "inteligente" com scroll spy: no handler de rolagem, troca uma classe (`is-compact`) e logo em seguida lê `getBoundingClientRect()`/`offsetHeight` do próprio header e de todas as seções para descobrir a seção ativa e a cor do menu. E ainda chama essa função de forma síncrona na carga. Ele é proibido. Use observers, que entregam a geometria sem forçar layout e já disparam com o estado inicial:

```js
// Header compacto: um sentinela no topo da página, sem ler scrollY.
const nav = document.querySelector('[data-nav]');
const sentinel = document.querySelector('[data-nav-sentinel]'); // elemento vazio no topo, com altura (ex.: 40vh)
new IntersectionObserver(([e]) => nav.classList.toggle('is-compact', !e.isIntersecting)).observe(sentinel);

// Scroll spy: seção que cruza a linha a 45% da altura da tela.
const links = new Map([...document.querySelectorAll('[data-spy]')].map(a => [a.hash.slice(1), a]));
const spy = new IntersectionObserver(entries => {
  for (const e of entries) if (e.isIntersecting) links.forEach((a, id) => id === e.target.id ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current'));
}, { rootMargin: '-45% 0px -55% 0px' });
document.querySelectorAll('main section[id]').forEach(s => spy.observe(s));

// Cor do menu conforme a seção sob ele: faixa fina na altura do header.
const theme = new IntersectionObserver(entries => {
  for (const e of entries) if (e.isIntersecting) nav.classList.toggle('is-light', e.target.dataset.nav === 'light');
}, { rootMargin: '-40px 0px -95% 0px' });
document.querySelectorAll('main section[data-nav]').forEach(s => theme.observe(s));
```

Regras para todo JS do projeto:

- **Observers no lugar de medições em evento.** `IntersectionObserver` para header que muda, scroll spy, revelar ao rolar, lazy load e contadores; `ResizeObserver` para reagir a tamanho; `matchMedia` para breakpoints. Nenhuma propriedade da lista acima dentro de `scroll`, `resize`, `pointermove` ou de um loop.
- **Se medir for inevitável: leia tudo, depois escreva tudo**, dentro de `requestAnimationFrame`, com as leituras no início do callback e nenhuma escrita antes delas. Guarde valores que mudam pouco (`innerHeight`, alturas) e atualize-os só num `ResizeObserver`.
- **Nada de medição síncrona na carga do script.** Não chame `atualizar()` no fim do módulo para "acertar o estado inicial": os observers já fazem isso no primeiro callback. Se precisar, agende com `requestAnimationFrame`.
- **Animação em `transform`/`opacity`**, não em `top`, `left`, `width`, `height` ou `margin`.
- **Altura de acordeão, menu e marquee com CSS** (`grid-template-rows: 0fr → 1fr`, `interpolate-size: allow-keywords`, `<details>`), sem medir `scrollHeight`.
- **Bibliotecas de animação/scroll** (GSAP ScrollTrigger, Lenis, AOS, carrosséis) inicializadas depois do primeiro paint e só nas páginas que as usam.
- Se o reflow vier de script de terceiro (analytics, chat, beacon ou desafio anti-bot da CDN), registre a origem e avalie adiar ou remover; não é corrigível no código do projeto.

**Verificação:** antes de entregar, procure no código-fonte as propriedades da lista acima (`grep -rnE "getBoundingClientRect|offset(Top|Height|Width)|scrollY|innerHeight|getComputedStyle" src/`) e confira que nenhuma ocorrência está em handler de rolagem/redimensionamento, depois de uma escrita no mesmo quadro ou na execução inicial do script. Depois, Lighthouse/`scripts/perf-audit.py` (que mostra o trecho do código na linha e coluna apontadas) rodado mais de uma vez, e DevTools → Performance: blocos roxos "Layout" com aviso "Forced reflow" apontam a linha.

### Scripts de terceiros
- Inventarie todos (analytics, chat, pixels, mapas, vídeos incorporados).
- Carregue de forma adiada/após interação ou consentimento; use fachadas (facade) para YouTube, mapas e chats.
- Cada script de terceiro precisa justificar seu custo.

### CSS e renderização
- CSS crítico inline quando o framework suportar; remova CSS não usado (Tailwind já faz purge).
- Evite layout shifts: reserve espaço para banners, embeds, anúncios e conteúdo dinâmico.
- `content-visibility: auto` para seções longas abaixo da dobra quando seguro.
- Animações apenas em `transform`/`opacity`.

### Rede e cache
- HTTP/2 ou HTTP/3, CDN quando possível.
- **Obrigatório em toda entrega:** HTML, CSS e JS minificados no build; compressão Brotli com fallback gzip; cache de navegador de no mínimo 30 dias para imagens, fontes, CSS e JS (1 ano `immutable` para assets com hash); HTML com `no-cache`. Gere o arquivo de configuração da hospedagem real (`.htaccess` em Apache/LiteSpeed, `_headers`, `vercel.json`, Nginx) conforme [references/server-config.md](references/server-config.md).
- `preconnect` apenas para origens críticas de terceiros (máximo 2–3). Se tudo vem da mesma origem, não há o que pré-conectar.

### Árvore de dependência de rede (cadeias críticas)
Cada recurso que só é descoberto depois de outro (HTML → CSS → fonte; HTML → script → requisição) soma latência ao caminho crítico. Para encurtar:

- **Fontes:** preload apenas da 1–2 usadas no texto LCP/acima da dobra (com `crossorigin`), menos arquivos (ver Fontes) e `unicode-range` nas secundárias. Preload de todas piora o LCP.
- **CSS:** inline o crítico ou mantenha um único arquivo pequeno; nada de `@import` encadeado.
- **Imagem LCP** descoberta no HTML (não via CSS `background-image` nem JS), com `fetchpriority="high"`.
- **Scripts de terceiros e beacons** fora do caminho crítico (adiados ou removidos). Beacons injetados pela CDN (RUM/Web Analytics) são desativados no painel dela, ver [references/server-config.md](references/server-config.md#proxy-de-cdn-na-frente-do-servidor-ex-cloudflare-com-nuvem-laranja).

Esse diagnóstico não entra na nota do PageSpeed; use-o para orientar as melhorias acima, sem perseguir uma árvore "vazia": o próprio HTML e as fontes essenciais sempre aparecem.

### Como medir
- **Auditoria de SEO on-page:** `python3 "${CLAUDE_SKILL_DIR}/scripts/seo-audit.py" <url-base>` percorre o sitemap e aponta títulos/descrições fora do limite ou duplicados, canonical errado, H1 ausente ou múltiplo, imagens sem `alt`, páginas com pouco texto, JSON-LD ausente ou inválido, `www`/HTTP sem redirect, favicon e `robots.txt`. Funciona em produção ou no `preview` local (passe `--sitemap` se a URL do sitemap for outra).
- **Laboratório:** Lighthouse (`npx lighthouse <url> --view` ou DevTools) em modo mobile, contra o **build de produção** (`build` + `preview`/`start`), nunca contra o servidor de desenvolvimento.
- **Auditoria de performance focada:** `python3 "${CLAUDE_SKILL_DIR}/scripts/perf-audit.py" <url>` roda o Lighthouse em mobile e desktop e lista só o que falhou em cache, imagens (tamanho, compressão, formato), reflow forçado, árvore de rede, LCP, CLS, fontes e bloqueio de renderização, com as URLs afetadas. Aceita `--report arquivo.json` para analisar um relatório já salvo. O item de cache só é válido contra o site publicado (o servidor de `preview` local não usa o `.htaccess`).
- **Campo:** PageSpeed Insights / CrUX para sites já publicados com tráfego.
- Registre os números reais obtidos, o ambiente de medição e as limitações (medição local não equivale a dados de campo).
