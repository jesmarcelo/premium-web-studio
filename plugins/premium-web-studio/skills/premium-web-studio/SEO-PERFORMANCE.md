# SEO técnico e performance

## Parte 1 — SEO

### URL pública final (pré-requisito)
Canonical, `og:url`, `og:image`, sitemap e as URLs do JSON-LD precisam ser **absolutos**, e só podem ser gerados com a URL pública final do site: domínio **e** subpasta, se o site for servido em uma (`https://host.com/projeto/`). Sem ela, o build sai sem canonical e com `og:image` relativo, e a prévia ao compartilhar no WhatsApp, Facebook, LinkedIn e X sai **sem imagem** (os scrapers não resolvem caminho relativo).

- Pergunte a URL final no discovery. Se o domínio definitivo ainda não existe, use a URL onde o site vai ficar no ar agora (inclusive temporária) e troque quando o domínio sair; nunca publique sem nenhuma.
- Configure-a no framework (`site` + `base` no Astro, `metadataBase` no Next, `site.url` no Nuxt, `baseURL` no Hugo etc.) ou por variável de ambiente no build, e confira a saída com `scripts/build-audit.py dist --site <url>`.
- **Reescritas de caminho depois do build** (ex.: trocar `/_astro/` por `./_astro/` para o site rodar em qualquer pasta) não podem tocar em `canonical`, `og:*`, `twitter:*`, `link rel=alternate` nem no JSON-LD: esses ficam absolutos.
- Se o usuário decidir publicar sem URL definida, isso é uma **decisão registrada** com a consequência explícita (sem canonical e prévia de compartilhamento sem imagem), não uma pendência esquecida.

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
- Open Graph: `og:title`, `og:description`, `og:image` (absoluta com `https`), `og:image:width`, `og:image:height`, `og:image:alt`, `og:url`, `og:type`, `og:site_name`, `og:locale`.
- `og:type` = `article` em artigos, com `article:published_time`, `article:modified_time` e `article:section`; `website` nas demais.
- `og:image` própria por artigo/produto (a imagem de destaque), com uma imagem padrão da marca como fallback.
- Twitter/X: `twitter:card` = `summary_large_image`, `twitter:image` e `twitter:image:alt` explícitos (o X nem sempre cai no `og:image`).

**A imagem de compartilhamento é uma peça de design, não um recorte qualquer.** É o primeiro contato de quem recebe o link.
- **Arquivo:** 1200×630 px, JPG (ou PNG se tiver texto fino e ainda ficar leve), **até 300 KB**: o WhatsApp descarta prévias pesadas. Nada de WebP/AVIF aqui.
- **Composição:** marca e mensagem legíveis em miniatura (a prévia aparece com ~400 px de largura no celular e recortada em quadrado em alguns apps): logo, nome e uma frase curta dentro da área central segura (~630×630), com contraste alto, fundo e tipografia da direção visual. Nada de texto pequeno nem de print da página inteira.
- **Como gerar:** um template HTML de 1200×630 com os tokens do site, capturado por screenshot (Playwright) ou composto com sharp/ImageMagick; no framework, gere por página (rotas de imagem OG do Next/Astro/Nuxt, ou um script no build) quando houver artigos ou produtos. Confira o arquivo lendo a imagem antes de entregar.
- **Verificação:** `scripts/build-audit.py` (antes de publicar) e `scripts/seo-audit.py` (publicado) conferem URL absoluta, formato, dimensões, peso e se os robôs das redes conseguem baixar a página. Depois de publicar, confirme no Facebook Sharing Debugger, no LinkedIn Post Inspector e numa conversa de teste do WhatsApp. As redes guardam a prévia em cache: depois de corrigir, use "Scrape again" no Facebook e, no WhatsApp, teste com um parâmetro novo (`?v=2`).
- **Proteção contra bots da CDN/firewall** (bot fight mode, desafio JS, WAF) pode devolver 403 para `facebookexternalhit`, `WhatsApp`, `Twitterbot` e `LinkedInBot`, e a prévia some. Libere esses agentes ou desative o desafio nas páginas públicas; se o painel não for do usuário, registre como fora do controle do projeto.

### Google: Search Console, nome do site, ícone e logo
- **Search Console:** verifique a propriedade (de domínio por DNS ou, sem acesso ao DNS, de prefixo de URL com a meta `google-site-verification` vinda de variável de ambiente), envie o sitemap e use a Inspeção de URL na home e em uma página interna. Não invente o código de verificação: peça ao usuário ou deixe a variável vazia e liste nas pendências. Equivalentes em outros buscadores (Bing Webmaster Tools, que também alimenta outros buscadores; IndexNow) são opcionais.
- **Nome do site nos resultados:** JSON-LD `WebSite` na home com `name` (e `alternateName`, se houver sigla ou nome alternativo) e `url` da home; o nome igual ao do `og:site_name` e do `<title>` da home.
- **Ícone nos resultados:** favicon quadrado, em múltiplo de 48 px (ou SVG), numa URL estável e rastreável, declarado com `<link rel="icon">` na home, além de `/favicon.ico` na raiz e `apple-touch-icon` de 180×180.
- **Logo da organização:** `Organization.logo` com URL absoluta de uma imagem de pelo menos 112×112 px, legível sobre fundo branco.
- **Imagens grandes na busca e no Discover:** `<meta name="robots" content="max-image-preview:large">` nas páginas indexáveis.
- **Negócio com endereço ou área de atendimento:** perfil no Google Business Profile com o mesmo NAP do site (ver SEO local), link do perfil em `sameAs`.

### Site servido numa subpasta
Quando o site fica em `https://host.com/projeto/`, `robots.txt` e `/favicon.ico` só têm efeito na raiz do domínio, que pode não ser do usuário. Gere o sitemap com as URLs completas da subpasta, envie-o no Search Console (propriedade de prefixo de URL) e peça ao responsável pelo domínio para declará-lo no `robots.txt` da raiz. O que não puder ser feito entra no relatório como fora do controle do projeto, com o motivo.

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
- **Toda imagem raster sai em AVIF com fallback WebP**, via `<picture>` (o navegador que aceita AVIF baixa o AVIF; os outros, o WebP) ou via negociação pelo cabeçalho `Accept` quando o framework ou a CDN faz isso. SVG para logos e ícones.
- `srcset`/`sizes` responsivos; nunca sirva imagem 2× maior que o necessário.
- `width`/`height` ou `aspect-ratio` sempre (evita CLS).
- Imagem LCP: **sem** lazy loading, com `fetchpriority="high"` (ou o recurso equivalente do framework, como `priority` no `next/image`) e, se descoberta tardiamente, `preload`.
- **O `fetchpriority` vai no elemento que o relatório aponta como LCP, não no que parece ser o principal.** O LCP é o maior elemento pintado na viewport, e muda entre mobile e desktop. Em composições com várias imagens (logo em camadas, colagem, hero com recortes), a maior camada em área, muitas vezes um ornamento, ganha de um texto ou da camada "mais importante". Rode `perf-audit.py`, leia o seletor de "Elemento LCP" nos dois formatos e coloque `fetchpriority="high"` nele (no máximo 1–2 imagens no total). Rode de novo e confirme que o item "fetchpriority=high precisa ser aplicada" sumiu do grupo LCP.
- **O elemento LCP nunca entra com animação atrasada.** O LCP só é registrado quando o elemento fica visível; um texto ou imagem que começa com `opacity: 0` (ou `visibility: hidden`, `clip-path`, blur total) e só aparece depois de um `animation-delay` empurra o LCP pelo tempo do atraso mais a animação (o Lighthouse mostra isso como "Element render delay"). No mobile o LCP costuma ser o parágrafo de abertura do hero, não o título nem a imagem: confirme qual é no relatório (`perf-audit.py` imprime o elemento) e deixe esse elemento visível desde o primeiro paint. A coreografia de entrada pode continuar nos outros elementos; se o LCP também precisar de movimento, anime só `transform`, partindo de opacidade 1, sem atraso.
- `loading="lazy"` e `decoding="async"` abaixo da dobra.
- Use o componente de imagem do framework quando existir.
- Toda imagem raster (fornecida pelo cliente, gerada ou de banco) passa pelo pipeline abaixo antes de entrar no site.

#### Pipeline obrigatório de imagens raster
1. **Meça o tamanho exibido.** Com a página rodando, descubra a maior largura CSS que a imagem ocupa em cada breakpoint (375, 768, 1440, 1920 px). No navegador: `getBoundingClientRect().width` do elemento; sem navegador, calcule pelo layout (largura do container, colunas, `max-width`). Registre também a proporção do recorte (`object-fit`/`aspect-ratio`).
2. **Redimensione para larguras derivadas da medição, não para uma lista genérica.** Para cada breakpoint, gere a largura medida × 1 e × 2, mais as duas do PageSpeed (largura exibida no viewport de 412 px × 1,75 e no de 1350 px × 1), nunca maiores que o original. Entre dois candidatos vizinhos, no máximo ~15–20% de diferença: com candidatos esparsos (ex.: 400w e 720w para uma imagem exibida a 531 px), o navegador baixa o próximo acima e o PageSpeed acusa. Recorte na proporção exibida quando ela for fixa.
3. **Gere AVIF e WebP com compressão real**, nas mesmas larguras. Nunca converta PNG para JPG nem entregue o arquivo original.
   **AVIF (o que a maioria dos navegadores baixa):** `quality` 50–55, `effort` 6 (sharp: `{ quality: 50, effort: 6 }`). O critério do PageSpeed (0,167 byte/pixel) é o mesmo para os dois formatos, mas o AVIF comprime bem melhor, inclusive o canal alfa. Medido com sharp: camada de logo transparente a 375×202 px, 19,5 KiB em WebP `q70/alpha 50` (reprova; `q60/alpha 30` ainda reprova) contra 9,3 KiB em AVIF `quality 50` (passa, sem diferença visível ampliada 2×); foto muito detalhada a 1040 px, 126 KiB em WebP `q64` (reprova) contra 99 KiB em AVIF `quality 55` (passa). Confira ampliado: abaixo de ~45 o AVIF amolece contornos finos. A escala de qualidade do AVIF não é a do WebP: AVIF 50 fica, em aparência, perto de WebP 75; nunca use o mesmo número para os dois.
   **WebP (fallback):** qualidade de partida ~70–78 para fotos e ilustrações (com `-sharp_yuv` no `cwebp` quando houver texto ou bordas finas). Lossless e qualidade ≥ 90 quase sempre reprovam no critério de compressão abaixo; use só se o arquivo ainda passar nele. WebP com transparência também deve ser lossy **inclusive no canal alfa**: o sharp e vários encoders gravam o alfa sem perda por padrão (`alphaQuality: 100`), e em arte fina com transparência (traços de logo, filetes, ornamentos) o alfa pesa mais que a cor. Parta de `-q 70 -alpha_q 50` no `cwebp` (sharp: `{ quality: 70, alphaQuality: 50, effort: 6 }`) e suba o `alpha_q` só se as bordas serrilharem. Componentes de imagem de framework costumam expor só `quality`, sem controle do alfa; se a imagem transparente reprovar, gere os arquivos fora do componente (script com sharp/`cwebp` e `srcset` manual) ou, quando o fundo atrás dela for sempre o mesmo, achate a imagem sobre essa cor e elimine o alfa.
   O PageSpeed roda no Chrome, que aceita AVIF: é o AVIF que ele julga. O WebP serve os poucos navegadores sem AVIF; deixe-o dentro do critério sempre que possível, mas um WebP de fallback reprovado com o AVIF aprovado não aparece no relatório (o `build-audit.py` o lista como aviso, não como reprovação).
4. **Declare no markup.** `srcset` com as larguras geradas, `sizes` com a largura **medida** em cada breakpoint (um `sizes` de 500px para uma imagem que renderiza com 531 px faz o navegador pular para o candidato seguinte), `width`/`height` da versão 1×. Com `<picture>`, o `<source type="image/avif">` vem primeiro, com o mesmo `sizes`; `alt`, `width`, `height`, `loading`, `decoding`, `fetchpriority` e `class` ficam no `<img>`, que carrega o WebP:

   ```html
   <picture>
     <source type="image/avif" srcset="hero-480.avif 480w, hero-720.avif 720w, hero-960.avif 960w" sizes="(min-width: 1024px) 50vw, 100vw">
     <img src="hero-720.webp" srcset="hero-480.webp 480w, hero-720.webp 720w, hero-960.webp 960w" sizes="(min-width: 1024px) 50vw, 100vw"
          width="720" height="480" alt="…" loading="lazy" decoding="async">
   </picture>
   ```

   O `<picture>` não tem caixa própria: estilize o `<img>`. Seletores com `>` (`.hero > img`) deixam de casar quando o `<img>` passa para dentro do `<picture>`; ajuste-os. Imagem LCP com `preload`: `<link rel="preload" as="image" type="image/avif" imagesrcset="…" imagesizes="…" fetchpriority="high">` (o `type` evita o download em navegador sem AVIF). Imagens em CSS (`background-image`, `mask-image`) usam `image-set(url(x.avif) type("image/avif"), url(x.webp) type("image/webp"))`.
5. **Confira o resultado** com o snippet de verificação abaixo e inspecione visualmente (artefatos, banding, texto borrado). Referência: imagem de conteúdo < 200 KB, hero < 300 KB na versão 1×.

**Como o PageSpeed julga cada imagem** (critérios do código do Lighthouse, "Improve image delivery"):

| Aviso | Quando aparece | Como passar |
|---|---|---|
| "Aumentar o fator de compactação" | arquivo com mais de **0,167 byte por pixel do arquivo** (largura × altura do arquivo, não da tela) e economia estimada acima de 4 KiB | AVIF 50–55 (o formato que o PageSpeed recebe), WebP 70–78 no fallback, sem lossless, alfa lossy em imagens transparentes; `bytes ≤ largura × altura × 0,167 + 4096` |
| "Maior do que precisa ser" (com `srcset`) | pixels do arquivo além dos exibidos × densidade, valendo mais de **12 KiB** | candidatos próximos (passo 2) e `sizes` medido |
| "Maior do que precisa ser" (sem `srcset`) | qualquer sobra acima de 4 KiB | sempre `srcset` |

O PageSpeed emula mobile com viewport de 412 px a densidade 1,75 e desktop com 1350 px a densidade 1; teste nesses dois cenários.

**Logos e marcas:** SVG sempre que existir ou puder ser vetorizado (peça o vetor ao cliente). Logo raster com transparência, mesmo pequeno, costuma passar de 0,8 byte/pixel em lossless e é reprovado. Se for inevitável, AVIF com fallback WebP lossy com `-alpha_q 50` (ver passo 3), no tamanho exibido × 2; logo de arte fina pequeno pode reprovar mesmo assim (medido: 220 × 95 px com `-q 75 -alpha_q 80` fica em ~0,6 byte/pixel; 187 × 81 px reprova em WebP e em AVIF `quality 50`, e só passa em AVIF `quality 40`). Siga a escada até passar: AVIF 50 → AVIF 40–45 conferido ampliado → achatar sobre o fundo (quando ele é fixo) → vetorizar (pedir o vetor; sem ele, vetorizar o PNG com `vtracer`/`potrace`, com aprovação para instalar, e comparar lado a lado com o original antes de trocar) → decisão do usuário. "Pedir o SVG ao cliente" não encerra o item enquanto os degraus anteriores não foram tentados. Isso vale também para logos montados em camadas raster para animação: cada camada é uma imagem julgada separadamente. Não baixe duas versões do mesmo logo (positivo/negativo) quando só uma aparece: use `<picture>` com `media`, CSS ou um SVG com `currentColor`.

Ferramentas, conforme o disponível no projeto (verifique antes; peça aprovação para instalar):
```bash
# cwebp/avifenc (libwebp/libavif): redimensionam e convertem
cwebp -q 75 -resize 1440 0 origem.png -o public/img/hero-1440.webp
avifenc -q 50 -s 4 origem-1440.png public/img/hero-1440.avif   # avifenc não redimensiona: redimensione antes
# ImageMagick
magick origem.png -resize 1440x -quality 75 public/img/hero-1440.webp
magick origem.png -resize 1440x -quality 50 public/img/hero-1440.avif
# sharp-cli (via npx)
npx sharp-cli -i origem.png -o public/img/hero-1440.webp resize 1440 -- webp --quality 75
npx sharp-cli -i origem.png -o public/img/hero-1440.avif resize 1440 -- avif --quality 50
```
Mantenha o original fora da pasta pública (ex.: `assets-src/` ou `tmp/`) para poder regerar.

**Original guardado, entrega recortada.** O arquivo original (em alta resolução) pode e deve ficar no projeto como fonte; o que nunca pode acontecer é o navegador baixar um arquivo maior que o exibido. O PageSpeed acusa "imagem maior do que precisa ser" quando o arquivo entregue passa do tamanho exibido × densidade de pixels do dispositivo, mesmo que seja só 1,5×.

**Componentes de imagem do framework** (`next/image`, `astro:assets`, `@nuxt/image` etc.) já redimensionam e convertem, **mas só geram `srcset` quando configurados para isso**. Uma única `width` gera um único arquivo e nenhum `srcset`: todo dispositivo baixa a mesma imagem. Regras:

- **Astro:** use `<Picture formats={['avif']} fallbackFormat="webp" widths={[...]} sizes="…">`, com as larguras do passo 2 e o `sizes` medido. O `fallbackFormat` é obrigatório: sem ele, o `<img>` de fallback sai em **PNG** quando a origem é PNG (padrão do componente). Não ponha `'webp'` também em `formats`: o componente não remove duplicatas e gera um `<source>` WebP redundante. **Não passe `quality` no componente**: a prop vale para os dois formatos e sobrescreve a configuração; defina a qualidade por formato no serviço, `image: { service: sharpImageService({ avif: { quality: 50, effort: 6 }, webp: { quality: 72, alphaQuality: 50, effort: 6 } }) }`. `width` sozinho gera um único arquivo. `layout="constrained"` (Astro 5.10+) gera `srcset` automaticamente, mas com breakpoints genéricos e espaçados (640, 750, 828, 1080…) e um `sizes` que presume uma coluna; em layouts com colunas, sobrescreva `widths` e `sizes`.
- **Next (`next/image`):** não gera `<picture>`: entrega AVIF ou WebP na mesma URL conforme o cabeçalho `Accept`, desde que `images.formats: ['image/avif', 'image/webp']` esteja no `next.config` (o padrão é só WebP). `sizes` é obrigatório sempre que a imagem não tem largura fixa (com `fill` ou largura responsiva); sem ele, o navegador assume `100vw` e baixa a maior versão. Ajuste `quality` (~75). Com `output: 'export'` o otimizador não roda: gere os arquivos no build e use `<picture>` manual.
- **Nuxt (`<NuxtPicture>`):** `format="avif,webp"`, com `sizes` (ex.: `sizes="sm:100vw md:50vw lg:600px"`) e `densities="x1 x2"`.
- **CDN com conversão automática** (serviços de imagem que negociam pelo `Accept`): vale como alternativa ao `<picture>`; confira com `curl -H "Accept: image/avif,image/webp" -I <url>` que o `content-type` volta `image/avif` e que há `Vary: Accept`.
- **Qualquer framework:** o passo 1 continua obrigatório: o `sizes` precisa refletir a largura medida em cada breakpoint, não um chute. Confira no HTML gerado que existe o `<source type="image/avif">` (ou a negociação) e que o `<img>` de fallback aponta para WebP, não PNG/JPG.

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

`scripts/perf-audit.py` faz a mesma checagem a partir do Lighthouse, em mobile e desktop. `scripts/build-audit.py dist` confere o critério de compressão em **todos** os arquivos gerados no build, sem navegador: qualquer variante do `srcset` pode ser a escolhida em algum dispositivo.

**Exceções ao AVIF + WebP:** logos e ícones em SVG; `og:image` em JPG ou PNG (nem todo scraper de redes sociais lê WebP/AVIF); favicons nos formatos próprios (ICO/PNG/SVG); GIF/WebP animado, que vira vídeo (`<video muted loop playsinline>`) quando pesado.

O servidor precisa entregar `.avif` com `Content-Type: image/avif` e o mesmo cache das outras imagens ([references/server-config.md](references/server-config.md)); confira com `curl -I` numa URL `.avif` publicada.

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
- **Nada de medição síncrona na carga do script.** Não chame `atualizar()` no fim do módulo para "acertar o estado inicial": os observers já fazem isso no primeiro callback. Se precisar, agende com `requestAnimationFrame`. Isso vale para **uma única leitura** no nível superior do módulo, como `let lastY = scrollY;` ou `const h = header.offsetHeight;`: o script roda antes do primeiro layout, então essa leitura obriga o navegador a calcular o layout da página inteira naquele instante, e o PageSpeed atribui todo esse tempo (100 ms ou mais em mobile) à linha do script. Inicialize com um valor neutro e leia dentro do primeiro quadro:

  ```js
  // Errado: let lastY = scrollY;
  let lastY = 0;
  requestAnimationFrame(() => { lastY = scrollY; });
  ```
- **Animação em `transform`/`opacity`**, não em `top`, `left`, `width`, `height` ou `margin`.
- **Altura de acordeão, menu e marquee com CSS** (`grid-template-rows: 0fr → 1fr`, `interpolate-size: allow-keywords`, `<details>`), sem medir `scrollHeight`.
- **Bibliotecas de animação/scroll** (GSAP ScrollTrigger, Lenis, AOS, carrosséis) inicializadas depois do primeiro paint e só nas páginas que as usam.
- Se o reflow vier de script de terceiro (analytics, chat, beacon ou desafio anti-bot da CDN), registre a origem e avalie adiar ou remover; não é corrigível no código do projeto.

**Verificação (as três, nesta ordem):**
1. `python3 "${CLAUDE_SKILL_DIR}/scripts/build-audit.py" dist` lista toda leitura de geometria no nível superior dos scripts do build (inline e `.js`), com `arquivo:linha:coluna` no mesmo formato do PageSpeed. Tem que sair sem linhas no grupo `reflow`.
2. Revisão do código-fonte para o que o script não alcança (leituras dentro de handlers): `grep -rnE "getBoundingClientRect|offset(Top|Height|Width)|client(Height|Width)|scroll(Y|Top|Height)|inner(Height|Width)|getComputedStyle" src/`, conferindo que nenhuma ocorrência está em handler de rolagem/redimensionamento sem `requestAnimationFrame` ou depois de uma escrita no mesmo quadro. Ler a linha não basta: confira o que acontece antes dela no mesmo fluxo.
3. `scripts/perf-audit.py <url> --runs 3` (mostra o trecho do código na linha e coluna apontadas). Uma rodada limpa não prova nada, porque o resultado varia; três seguidas sem "Reflow forçado" do código do projeto, sim. No DevTools → Performance, blocos roxos "Layout" com aviso "Forced reflow" apontam a linha.

Com o PageSpeed apontando `/pagina/:L:C`, abra o HTML publicado (ou `dist/.../index.html`) na linha L, coluna C: é ali que está a leitura, mesmo que a revisão do código-fonte diga que "não sobrou nenhuma".

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
- **Auditoria do build (antes de publicar, sem rede):** `python3 "${CLAUDE_SKILL_DIR}/scripts/build-audit.py" dist --site <url-final>` confere leituras de geometria na carga dos scripts, o critério de compressão do PageSpeed em cada imagem gerada, PNG/JPG servidos, `<img>` sem `srcset`, excesso de `fetchpriority`, canonical/`og:url`/`og:image` absolutos, a imagem de compartilhamento (formato, 1200×630, ≤ 300 KB), `og:image:alt`, `twitter:image`, JSON-LD `WebSite`/`Organization`, `robots.txt`, sitemap e `favicon.ico`. Sai com código 1 enquanto houver reprovação: rode a cada build.
- **Auditoria de SEO on-page:** `python3 "${CLAUDE_SKILL_DIR}/scripts/seo-audit.py" <url-base>` percorre o sitemap e aponta títulos/descrições fora do limite ou duplicados, canonical errado, H1 ausente ou múltiplo, imagens sem `alt`, páginas com pouco texto, JSON-LD ausente ou inválido, `www`/HTTP sem redirect, favicon e `robots.txt`, além da prévia de compartilhamento: `og:image` absoluta, baixável, em JPG/PNG, com as dimensões declaradas e até 300 KB, e a home acessível para os robôs do Facebook, WhatsApp, X e LinkedIn (403 = prévia quebrada pela proteção contra bots). Funciona em produção ou no `preview` local (passe `--sitemap` se a URL do sitemap for outra).
- **Laboratório:** Lighthouse (`npx lighthouse <url> --view` ou DevTools) em modo mobile, contra o **build de produção** (`build` + `preview`/`start`), nunca contra o servidor de desenvolvimento.
- **Auditoria de performance focada:** `python3 "${CLAUDE_SKILL_DIR}/scripts/perf-audit.py" <url>` roda o Lighthouse em mobile e desktop e lista só o que falhou em cache, imagens (tamanho, compressão, formato), reflow forçado, árvore de rede, LCP, CLS, fontes e bloqueio de renderização, com as URLs afetadas. Aceita `--report arquivo.json` para analisar um relatório já salvo e `--runs 3` para repetir (reflow e LCP variam entre execuções; use antes de dar um item por resolvido). Cada grupo reprovado sai com o próximo passo. O item de cache só é válido contra o site publicado (o servidor de `preview` local não usa o `.htaccess`).
- **Campo:** PageSpeed Insights / CrUX para sites já publicados com tráfego.
- Registre os números reais obtidos, o ambiente de medição e as limitações (medição local não equivale a dados de campo).

---

## Escada de soluções

Todo item reprovado por `build-audit.py`, `perf-audit.py` ou `seo-audit.py` entra no ciclo **corrigir → build → auditar de novo** e só sai dele em um destes três estados (registrados no `qa-report.md`):

| Estado | Quando vale |
|---|---|
| **Resolvido** | A ferramenta que apontou o item não aponta mais (reflow e LCP: em 3 rodadas seguidas). |
| **Decisão do usuário** | Todos os degraus abaixo da decisão foram tentados ou são incompatíveis com algo que o usuário quer, e ele escolheu, com as opções e o custo de cada uma na frente (pergunta estruturada), manter a situação. Registre a data, a opção escolhida e o custo medido (ms, KiB, pontos). |
| **Fora do controle do projeto** | A causa está fora do código e da configuração entregues: script ou beacon de terceiro, CDN/painel/domínio de outra pessoa, limitação da hospedagem. Registre a evidência (URL do recurso, cabeçalho, quem administra). |

"Pendente", "aceito" ou "aguardando o cliente" sem um desses estados significa que o trabalho não acabou: suba para o próximo degrau. Pedir algo ao cliente (vetor, acesso, domínio) não encerra o item enquanto houver degrau que não dependa dele.

| Problema | Degraus, em ordem (pare no primeiro que zerar o item) |
|---|---|
| Compressão de imagem ("Aumentar o fator de compactação") | confirmar que o AVIF está sendo entregue (`<source type="image/avif">` ou negociação; o fallback não é PNG/JPG) → AVIF 50–55 sem lossless, alfa lossy no WebP (`alpha_q` 50) → AVIF 40–45 conferido ampliado → achatar sobre o fundo fixo → vetorizar (vetor do cliente ou `vtracer`/`potrace` com aprovação e comparação visual) → decisão do usuário |
| Imagem maior que o exibido | `sizes` igual à largura medida → larguras do `srcset` derivadas da medição, vizinhas a ≤ 20%, incluindo 412 × 1,75 e 1350 × 1 → recorte na proporção exibida → `<picture>` com `media` para recortes diferentes |
| `fetchpriority` não aplicado no LCP | ler o "Elemento LCP" do `perf-audit.py` (mobile e desktop) → `fetchpriority="high"` + `loading="eager"` nele, tirando de onde estava → `preload` se ele for descoberto tarde (CSS/JS) → se mobile e desktop têm LCPs diferentes, os dois (máximo 2) |
| Atraso de renderização do LCP | elemento LCP visível desde o primeiro paint (sem `opacity: 0`/`animation-delay`) → animar só `transform` partindo de opacidade 1 → mover a coreografia para outros elementos → decisão do usuário (manter a animação com o custo em segundos medido) |
| Reflow forçado | abrir a linha:coluna no HTML/JS publicado → tirar leitura de geometria do nível superior (`build-audit.py`) → observers no lugar de medições em evento → ler antes de escrever dentro de `requestAnimationFrame` → adiar bibliotecas para depois do primeiro paint → se o arquivo for de terceiro/CDN, fora do controle |
| Cache curto | regra no arquivo de configuração **da saída do build** → conferir com `curl -I` por extensão → CDN: Browser Cache TTL, regras de cache e purge → fora do controle (hospedagem sem acesso), com o cabeçalho como evidência |
| Canonical / `og:*` relativos ou ausentes | URL final no config do framework → excluir metadados de reescritas de caminho → decisão do usuário (publicar sem URL definida, com a prévia sem imagem como consequência) |
| Prévia de compartilhamento sem imagem | `og:image` absoluta https, JPG/PNG, 1200×630, ≤ 300 KB → robôs das redes liberados na CDN/firewall → limpar o cache da rede (Sharing Debugger, `?v=2`) → fora do controle (firewall de terceiro) |
| `robots.txt`, sitemap, `favicon.ico` | gerar no build → declarar o sitemap no `robots.txt` → em subpasta: Search Console + pedido ao dono do domínio → fora do controle |

Antes da decisão do usuário, apresente as opções com o custo de cada uma (ex.: "manter a camada do logo em AVIF 50: +3 KiB e o aviso continua; AVIF 40: o aviso some, contorno levemente mais macio; SVG: depende do vetor"). Uma decisão vale para aquele item; um problema novo, ou o mesmo em outra página, volta à escada.
