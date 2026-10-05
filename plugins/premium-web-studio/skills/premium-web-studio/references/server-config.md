# Configuração de servidor: compressão e cache

Todo projeto entregue sai com compressão e cache de navegador configurados para a hospedagem real. Identifique a hospedagem no discovery (ou pergunte) e gere **apenas** o arquivo correspondente. **Se a hospedagem for desconhecida, gere o `.htaccess`** (Apache/LiteSpeed é o caso mais comum em hospedagem compartilhada; em servidor que não o lê, o arquivo é inofensivo). Nunca entregue sem nenhuma configuração: sem ela, vale o padrão do servidor ou da CDN (muitas vezes 7 dias ou menos), e o PageSpeed acusa "política de cache ineficiente" em imagens e fontes.

## O arquivo precisa chegar à pasta publicada

O erro mais comum é criar o arquivo na raiz do repositório, onde o build o ignora. Coloque-o na pasta que o build copia sem processar:

| Stack | Onde criar | Onde aparece após o build |
|---|---|---|
| Astro, Vite, SvelteKit (static), Nuxt (`generate`) | `public/.htaccess` | `dist/.htaccess` (ou `build/`, `.output/public/`) |
| Eleventy | raiz + `addPassthroughCopy(".htaccess")` | `_site/.htaccess` |
| Hugo | `static/.htaccess` | `public/.htaccess` |
| HTML sem build | raiz publicada | a própria raiz |

Depois do build, confirme: `ls -la dist/.htaccess` (ajuste a pasta). Se o site for publicado em subpasta (`dominio.com/projeto/`), o `.htaccess` vai na raiz dessa subpasta e vale para ela.

## Divisão de responsabilidades

| Tarefa | Onde acontece |
|---|---|
| **Minificação** de HTML, CSS e JS | No **build** (Vite, Astro, Next, esbuild, Lightning CSS, `html-minifier-terser`). O servidor não minifica: `.htaccess` e afins só comprimem o que recebem. Em site HTML puro sem build, adicione um passo de minificação (ex.: `npx html-minifier-terser`, `npx esbuild --minify`, `npx lightningcss --minify`) gerando a pasta publicada. |
| **Compressão** (Brotli, com gzip de fallback) | No servidor/CDN, via configuração abaixo. |
| **Cache de navegador** | No servidor/CDN, via `Cache-Control`. |

## Política de cache

| Recurso | `Cache-Control` |
|---|---|
| Assets com hash no nome (`app.3f9a1c.js`) | `public, max-age=31536000, immutable` (1 ano) |
| Imagens, fontes, CSS e JS sem hash | `public, max-age=2592000` (**30 dias, mínimo**; é o limite abaixo do qual o PageSpeed acusa "política de cache ineficiente") |
| HTML | `no-cache` (revalida sempre, para publicar mudanças na hora) |

Prefira nomes com hash ou versão (`style.css?v=2` não basta em alguns proxies; use `style.v2.css`) para poder usar 1 ano sem risco de servir arquivo velho.

## Apache / LiteSpeed (hospedagem compartilhada) — `.htaccess`

Coloque na raiz pública (`public_html/` ou a pasta de saída do build, ex.: `dist/`, `public/`). Os blocos `<IfModule>` evitam erro 500 se um módulo faltar. LiteSpeed lê o mesmo arquivo.

```apache
# ---------- Compressão ----------
# Brotli (Apache 2.4.26+ com mod_brotli)
<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/css text/xml text/javascript application/javascript application/json application/xml application/rss+xml application/manifest+json image/svg+xml font/ttf font/otf
</IfModule>

# gzip de fallback (navegadores/servidores sem Brotli)
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css text/xml text/javascript application/javascript application/json application/xml application/rss+xml application/manifest+json image/svg+xml font/ttf font/otf
</IfModule>

# ---------- Tipos MIME ----------
<IfModule mod_mime.c>
  AddType image/webp .webp
  AddType image/avif .avif
  AddType font/woff2 .woff2
  AddType application/manifest+json .webmanifest
</IfModule>

# ---------- Cache de navegador ----------
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 30 days"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType application/json "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType text/javascript "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/avif "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType video/mp4 "access plus 1 year"
</IfModule>

<IfModule mod_headers.c>
  <FilesMatch "\.(css|js|mjs|webp|avif|jpe?g|png|gif|svg|ico|woff2?|mp4|webm)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\.(html?|json|xml|txt)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
  Header append Vary Accept-Encoding
</IfModule>
```

O modelo usa 1 ano para assets porque pressupõe nomes com hash/versão. **Se os arquivos não tiverem hash** (ex.: `style.css` fixo, editado à mão), troque `max-age=31536000, immutable` por `max-age=2592000` (30 dias) e os `ExpiresByType ... "1 year"` por `"30 days"`.

Se o projeto já tem `.htaccess` (redirects, WordPress, HTTPS), **acrescente** os blocos sem apagar as regras existentes; no WordPress, fora do bloco `# BEGIN WordPress ... # END WordPress`.

## Nginx

```nginx
brotli on;               # requer o módulo ngx_brotli
brotli_types text/plain text/css text/javascript application/javascript application/json application/xml image/svg+xml;
gzip on;
gzip_vary on;
gzip_types text/plain text/css text/javascript application/javascript application/json application/xml image/svg+xml;

location ~* \.(css|js|mjs|webp|avif|jpe?g|png|gif|svg|ico|woff2?|mp4|webm)$ {
  add_header Cache-Control "public, max-age=31536000, immutable";
}
location ~* \.html?$ {
  add_header Cache-Control "no-cache";
}
```

## Netlify / Cloudflare Pages — `_headers` na pasta publicada

Compressão é automática. Configure só o cache:

```
/*.html
  Cache-Control: no-cache
/assets/*
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
```

Ajuste os caminhos às pastas reais do build.

## Proxy de CDN na frente do servidor (ex.: Cloudflare com nuvem laranja)

Quando há uma CDN como proxy (sinais: cabeçalhos `cf-cache-status`/`server: cloudflare`, requisições a `/cdn-cgi/` ou `static.cloudflareinsights.com`), ela pode reescrever o `Cache-Control` que o servidor envia:

**Diagnóstico rápido:** compare o cabeçalho com a CDN ligada e desligada (pausar o proxy ou acessar a origem direto). Se o valor muda só com a CDN ligada, a CDN está reescrevendo. Um sinal típico é o `expires` com exatamente o TTL da CDN (ex.: 7 dias).

Passo a passo para o usuário (Cloudflare; outras CDNs têm opções equivalentes):

1. **Caching → Configuration → Browser Cache TTL** em **"Respect Existing Headers"**. Um valor fixo (ex.: 7 dias) reescreve `Expires`/`Cache-Control` vindos do `.htaccess`.
2. **Caching → Cache Rules** e **Rules → Page Rules**: toda regra com "Browser TTL"/"Browser Cache TTL" fixo passa para **"Respect origin"** ou é removida.
3. **Caching → Configuration → Purge Everything**, senão as cópias guardadas continuam com os cabeçalhos antigos. Repita sempre que mudar o `.htaccess`.
4. Conferir com `curl -sI <url-de-um-asset>` duas vezes: na segunda deve vir `cf-cache-status: HIT`, e nas duas o `cache-control` (e o `expires`, se houver) deve ser o do `.htaccess`.
5. Rodar o PageSpeed de novo alguns minutos depois. O que sobrar em `/cdn-cgi/` ou `cloudflareinsights` é da própria CDN (itens abaixo).

Recursos da CDN que o `.htaccess` não controla:

- O **beacon de Web Analytics/RUM** injetado pela CDN (`beacon.min.js` → `/cdn-cgi/rum`) costuma ser a cadeia mais longa da árvore de dependência de rede. Se o projeto não usa esses dados, desative o RUM/Web Analytics automático no painel da CDN (essa configuração é do painel, não do código; oriente o usuário).
- **Scripts da própria CDN** (`/cdn-cgi/challenge-platform/...` da proteção anti-bot, o beacon acima) aparecem em "cache ineficiente" com 4 h ou 1 dia. O `.htaccess` não os alcança: ou se desativa o recurso no painel, ou se aceita o aviso e registra a origem no relatório de QA. Na Cloudflare (documentação de 2026):
  - **Desafio anti-bot:** Security → Settings, filtro "Bot traffic", desligar **Bot Fight Mode** (link direto: `https://dash.cloudflare.com/?to=/:account/:zone/security/settings`). Com Bot Fight Mode ligado, o JavaScript Detections não pode ser desligado sozinho.
  - **Beacon:** página Web Analytics (`https://dash.cloudflare.com/?to=/:account/web-analytics`) → **Manage site** → **Disable**. No plano Free o RUM vem ligado automaticamente.

O painel muda de nomes e de idioma: passe os links diretos `dash.cloudflare.com/?to=...` ao usuário em vez de só o caminho de menus e, na dúvida, confira a documentação atual (`developers.cloudflare.com`).

### Cabeçalho `Expires` diferente do `max-age`

Hospedagens LiteSpeed/Apache costumam acrescentar um `Expires` padrão (ex.: 7 dias) mesmo com o `Cache-Control` correto. Navegadores e o Lighthouse usam o `max-age` quando ele existe e ignoram o `Expires`, então a resposta abaixo **está certa**:

```http
cache-control: public, max-age=31536000, immutable
expires: <data daqui a 7 dias>
```

Se o PageSpeed ainda acusar 7 dias depois do deploy, confira nesta ordem: o resultado é de antes da publicação ou veio de uma cópia antiga (cada data center da CDN guarda a sua, e o PageSpeed roda de outra região que o `curl` local não alcança; ele também reaproveita resultados recentes da mesma URL). Se o `curl` já mostra o cabeçalho certo, não mexa em mais nada: espere de 30 a 60 minutos e rode de novo; `cf-cache-status: HIT` com cabeçalho antigo (purgue a CDN); ou as URLs acusadas são da CDN (item anterior). O framework de site estático (Astro, Vite, Eleventy) não envia cabeçalhos: quem decide é o servidor, a CDN ou o arquivo de configuração da hospedagem.

Essas configurações ficam fora do repositório: registre-as como passo de entrega para o usuário quando você não tiver acesso ao painel.

## Vercel — `vercel.json`

Compressão automática; assets do Next.js (`/_next/static`) já saem com cache de 1 ano. Para pastas próprias:

```json
{
  "headers": [
    {
      "source": "/(img|fonts)/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    }
  ]
}
```

## Verificação

Com o site publicado (ou em staging que use o mesmo servidor):

```bash
curl -sI -H "Accept-Encoding: br, gzip" https://exemplo.com/ | grep -iE "content-encoding|cache-control"
curl -sI -H "Accept-Encoding: br, gzip" https://exemplo.com/caminho/app.css | grep -iE "content-encoding|cache-control"
curl -sI https://exemplo.com/caminho/imagem.webp | grep -iE "cache-control|cf-cache-status"
curl -sI https://exemplo.com/caminho/fonte.woff2 | grep -iE "cache-control|cf-cache-status"
```

Teste **pelo menos uma URL real de cada extensão servida** (`.webp`, `.avif`, `.woff2`, `.css`, `.js`, `.svg`), pegando os caminhos do HTML publicado. Esperado: `content-encoding: br` (ou `gzip`) em HTML/CSS/JS/SVG e `max-age` ≥ 2592000 em imagens, CSS, JS e fontes. Se o `max-age` vier diferente do que o `.htaccess` define, ou o arquivo não foi publicado (confira o `ls` acima no servidor) ou a CDN está sobrescrevendo (seção anterior). O script `scripts/perf-audit.py` aponta os recursos com cache curto a partir do Lighthouse. Confirme no PageSpeed que o item de cache ineficiente não aparece. Servidor local de desenvolvimento não reflete essa configuração; se não houver ambiente publicado, registre a verificação como pendente.
