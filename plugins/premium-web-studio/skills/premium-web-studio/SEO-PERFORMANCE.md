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
- `loading="lazy"` e `decoding="async"` abaixo da dobra.
- Use o componente de imagem do framework quando existir.
- Toda imagem raster (fornecida pelo cliente, gerada ou de banco) passa pelo pipeline abaixo antes de entrar no site.

#### Pipeline obrigatório de imagens raster
1. **Meça o tamanho exibido.** Com a página rodando, descubra a maior largura CSS que a imagem ocupa em cada breakpoint (375, 768, 1440, 1920 px). No navegador: `getBoundingClientRect().width` do elemento; sem navegador, calcule pelo layout (largura do container, colunas, `max-width`). Registre também a proporção do recorte (`object-fit`/`aspect-ratio`).
2. **Redimensione para o necessário.** Gere a versão 1× (maior largura exibida) e a 2× (para telas retina), nunca maiores que o original. Se a imagem aparece com tamanhos muito diferentes entre mobile e desktop, gere as larguras intermediárias para o `srcset`. Recorte na proporção exibida quando ela for fixa.
3. **Converta para WebP.** Nunca converta PNG para JPG nem entregue o arquivo original. Qualidade de partida: ~75–82 para fotos, `-lossless` ou qualidade alta para ilustrações, capturas de tela e imagens com texto. WebP preserva transparência, então PNG com alfa também vira WebP. AVIF pode ser oferecido adicionalmente via `<picture>`.
4. **Declare no markup.** `srcset` com as larguras geradas, `sizes` coerente com o layout medido, `width`/`height` da versão 1×.
5. **Confira o resultado.** Compare o peso antes/depois e inspecione visualmente (artefatos, banding, texto borrado). Referência: imagem de conteúdo < 200 KB, hero < 300 KB na versão 1×.

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

- **Astro (`<Image>`/`<Picture>`):** use `layout="constrained"` (ou `full-width` para imagens de largura total), que gera `srcset` e `sizes` automaticamente (Astro 5.10+; em versões anteriores, `experimental.responsiveImages`); ou passe `widths={[...]}` **e** `sizes` explícitos. `width` sozinho não basta. Defina `quality` (~75–80) em vez de depender do padrão.
- **Next (`next/image`):** `sizes` é obrigatório sempre que a imagem não tem largura fixa (com `fill` ou largura responsiva); sem ele, o navegador assume `100vw` e baixa a maior versão. Ajuste `quality` (~75).
- **Nuxt (`<NuxtImg>`):** use `sizes` (ex.: `sizes="sm:100vw md:50vw lg:600px"`) e `densities="x1 x2"`.
- **Qualquer framework:** o passo 1 continua obrigatório: o `sizes` precisa refletir a largura medida em cada breakpoint, não um chute. Confirme que o formato de saída inclui WebP/AVIF.

**Verificação no navegador.** Com o build de produção aberto, rode no console (ou via Playwright `page.evaluate`) em 375 e 1440 px e corrija toda linha que aparecer:

```js
[...document.images].filter(i => i.currentSrc && i.getBoundingClientRect().width > 0).map(i => {
  const need = Math.ceil(i.getBoundingClientRect().width * devicePixelRatio);
  return { src: i.currentSrc.split('/').pop(), arquivo: i.naturalWidth, exibido: Math.round(i.getBoundingClientRect().width), necessario: need, sobra: (i.naturalWidth / need).toFixed(2) };
}).filter(r => r.arquivo > r.necessario * 1.15)
```

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

### Reflow forçado (layout thrashing)
Acontece quando o JS lê uma propriedade de geometria logo depois de alterar estilo ou DOM, obrigando o navegador a recalcular o layout na hora. O PageSpeed lista em "Reflow forçado" com o arquivo e a linha. Regras para todo JS escrito no projeto:

- **Leia tudo, depois escreva tudo.** Nunca alterne em loop `el.style.x = ...` com leituras de `offsetWidth/Height/Top`, `clientWidth/Height`, `scrollTop/Height`, `getBoundingClientRect()`, `getComputedStyle()`, `innerWidth`. Junte as leituras antes e aplique as escritas depois, de preferência dentro de `requestAnimationFrame`.
- **Observers no lugar de medições em evento.** `IntersectionObserver` para revelar ao rolar, lazy load, header que muda e contadores; `ResizeObserver` para reagir a tamanho; `matchMedia` para breakpoints. Nada de `getBoundingClientRect()` dentro de `scroll`/`resize`.
- **Animação em `transform`/`opacity`**, não em `top`, `left`, `width`, `height` ou `margin`.
- **Medição inicial fora do caminho crítico:** cálculo de altura (acordeão, menu, marquee) só quando o componente é usado, ou com CSS (`grid-template-rows: 0fr → 1fr`, `interpolate-size`, `details`) para dispensar a medição.
- **Bibliotecas de animação/scroll** (GSAP ScrollTrigger, Lenis, AOS, carrosséis) inicializadas depois do primeiro paint e só nas páginas que as usam.
- Se o reflow vier de script de terceiro (analytics, chat, beacon da CDN), registre a origem e avalie adiar ou remover; não é corrigível no código do projeto.

**Verificação:** Lighthouse ("Forced reflow"/"Reflow forçado" vazio, também listado por `scripts/perf-audit.py`) e, para detalhe, DevTools → Performance: blocos roxos "Layout" com aviso "Forced reflow" apontam a linha do código.
- Analise o bundle (`vite-bundle-visualizer`, `@next/bundle-analyzer`, `rollup-plugin-visualizer`).

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
