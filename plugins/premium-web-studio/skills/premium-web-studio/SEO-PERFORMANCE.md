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

**Componentes de imagem do framework** (`next/image`, `astro:assets`, `@nuxt/image` etc.) já redimensionam e convertem; nesse caso, o passo 1 continua obrigatório para escrever `sizes` correto, e confirme que o formato de saída inclui WebP/AVIF.

**Exceções:** logos e ícones em SVG; `og:image` em JPG ou PNG (nem todo scraper de redes sociais lê WebP); favicons nos formatos próprios (ICO/PNG/SVG).

- Vídeos de fundo: comprimidos, `muted`, `playsinline`, com `poster`, desativados com reduced motion e em conexões lentas quando possível; prefira não usá-los no hero mobile.

### Fontes
- Self-host (ou o otimizador de fontes do framework) em WOFF2.
- Subset conforme os idiomas do site (ex.: latin + latin-ext para idiomas com acentos; cyrillic, greek, vietnamese etc. quando necessário) e apenas os pesos usados; prefira fontes variáveis quando substituem vários arquivos.
- `font-display: swap` (ou `optional` para fontes não essenciais).
- `preload` apenas da fonte usada acima da dobra — no máximo 1–2 arquivos. Pré-carregar todas as variações compete com a imagem LCP pela banda e piora o LCP.
- Métricas de fallback ajustadas (`size-adjust`, `ascent-override`) para reduzir CLS — `next/font` e Fontsource fazem isso.

### JavaScript
- Envie o mínimo de JS: renderize no servidor/estático, hidrate apenas o interativo (ilhas, Server Components).
- Code splitting por rota; `import()` dinâmico para componentes pesados abaixo da dobra (mapas, players, gráficos, carrosséis).
- Evite bibliotecas pesadas para tarefas simples (ver [ENGINEERING.md](ENGINEERING.md#dependências)).
- Quebre tarefas longas (> 50 ms) em interações; evite handlers síncronos pesados (INP).
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
- `preconnect` apenas para origens críticas de terceiros (máximo 2–3).

### Como medir
- **Auditoria de SEO on-page:** `python3 "${CLAUDE_SKILL_DIR}/scripts/seo-audit.py" <url-base>` percorre o sitemap e aponta títulos/descrições fora do limite ou duplicados, canonical errado, H1 ausente ou múltiplo, imagens sem `alt`, páginas com pouco texto, JSON-LD ausente ou inválido, `www`/HTTP sem redirect, favicon e `robots.txt`. Funciona em produção ou no `preview` local (passe `--sitemap` se a URL do sitemap for outra).
- **Laboratório:** Lighthouse (`npx lighthouse <url> --view` ou DevTools) em modo mobile, contra o **build de produção** (`build` + `preview`/`start`), nunca contra o servidor de desenvolvimento.
- **Campo:** PageSpeed Insights / CrUX para sites já publicados com tráfego.
- Registre os números reais obtidos, o ambiente de medição e as limitações (medição local não equivale a dados de campo).
