#!/usr/bin/env python3
"""Auditoria da pasta do build (dist/, out/, build/...). Somente leitura; só usa a biblioteca padrão; não acessa a rede.

Pega antes da publicação, de forma determinística, o que o PageSpeed e as redes sociais só mostram depois:
  - JS: leitura de geometria (scrollY, offsetHeight, getBoundingClientRect...) na execução inicial do script,
    que força o layout da página inteira na carga ("Reflow forçado"), com arquivo:linha:coluna no formato do PageSpeed;
  - imagens: cada arquivo raster gerado contra o critério de compressão do PageSpeed (bytes <= pixels x 0,167 + 4 KiB;
    WebP de fallback de <picture> com AVIF vira aviso), <img> raster fora de <picture> com AVIF,
    PNG/JPG servidos fora das exceções, <img> raster sem srcset e excesso de fetchpriority;
  - SEO e compartilhamento: canonical, og:url e og:image absolutos (reescritas de caminho relativo quebram a prévia),
    og:image em JPG/PNG com 1200x630 e <= 300 KB, og:image:alt, twitter:image, JSON-LD (WebSite/Organization),
    robots.txt, sitemap e favicon.ico.

Uso:
  python3 build-audit.py dist
  python3 build-audit.py dist --site https://www.exemplo.com/          # URL pública final (domínio + subpasta, se houver)
  python3 build-audit.py out --site https://exemplo.com/blog/ --ignore "_astro/og-*"

Sai com código 1 quando há reprovação. Rode a cada build até sair com 0 ou até cada item restante estar
classificado conforme SEO-PERFORMANCE.md#escada-de-soluções.
"""
import argparse
import fnmatch
import html
import json
import os
import re
import struct
import sys
import urllib.parse

GEOMETRY = re.compile(
    r"\b(?:scrollY|scrollX|pageYOffset|pageXOffset|innerWidth|innerHeight)\b"
    r"|\.(?:offset(?:Top|Left|Width|Height)|client(?:Top|Left|Width|Height)|scroll(?:Top|Left|Width|Height)|innerText)\b"
    r"|\b(?:getBoundingClientRect|getClientRects|getComputedStyle|scrollIntoView)\s*\("
    r"|\.focus\s*\("
)
RASTER = (".webp", ".avif", ".jpg", ".jpeg", ".png")
EXEMPT = re.compile(r"(^|/)(og[-_]|social|share|twitter|apple-touch-icon|android-chrome|favicon|icon-|mstile)", re.I)
BPP, SLACK = 0.167, 4096
problems = []
fallbacks = set()  # arquivos de fallback (WebP) de <picture> com AVIF: o PageSpeed (Chrome) não os baixa


def fail(group, msg):
    problems.append(group)
    print(f"  !! {msg}")


# ---------- JS: leituras de geometria na execução inicial ----------

def top_level_mask(code):
    """Devolve o código com tudo que não é nível superior (corpos de função, strings, comentários) trocado por espaços."""
    out = list(code)
    n, i = len(code), 0
    depth, paren, arrow = 0, 0, None  # arrow: nível de parênteses onde termina o corpo de uma arrow sem chaves
    base =1 if re.match(r"\s*[!;(]*\s*(?:async\s*)?(?:function\b[^{]*|\([^)]*\)\s*=>\s*)\{", code) else 0  # IIFE
    tmpl = []  # pilha de profundidade de chaves ao entrar em ${ dentro de template
    prev = ""  # último caractere significativo (para distinguir regex de divisão)

    def blank(a, b):
        for k in range(a, min(b, n)):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = code[i]
        if c in "'\"":
            j = i + 1
            while j < n and code[j] != c and code[j] != "\n":
                j += 2 if code[j] == "\\" else 1
            blank(i, j + 1)
            i, prev = j + 1, "a"
            continue
        if c == "`" or (c == "}" and tmpl and depth == tmpl[-1]):
            if c == "}":
                tmpl.pop()
            j = i + 1
            while j < n and code[j] != "`" and not (code[j] == "$" and code[j + 1:j + 2] == "{"):
                j += 2 if code[j] == "\\" else 1
            blank(i, j + 1)
            if j < n and code[j] == "$":
                tmpl.append(depth)
                i = j + 2
            else:
                i = j + 1
            prev = "a"
            continue
        if code.startswith("//", i):
            j = code.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
            continue
        if code.startswith("/*", i):
            j = code.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(i, j)
            i = j
            continue
        if c == "/" and (prev == "" or prev in "(,=:[!&|?{};+-*%<>~^"):
            j, cls = i + 1, False
            while j < n and code[j] != "\n":
                if code[j] == "\\":
                    j += 2
                    continue
                if code[j] == "[":
                    cls = True
                elif code[j] == "]":
                    cls = False
                elif code[j] == "/" and not cls:
                    break
                j += 1
            blank(i, j + 1)
            i, prev = j + 1, "a"
            continue
        if depth <= base:
            # Corpo de arrow function sem chaves (`() => el.offsetWidth`) também só roda depois.
            if code.startswith("=>", i) and code[i + 2:].lstrip()[:1] != "{":
                arrow = arrow if arrow is not None else paren
            elif c in "([":
                paren += 1
            elif c in ")]":
                paren -= 1
                if arrow is not None and paren < arrow:
                    arrow = None
            elif c in ",;" and arrow is not None and paren == arrow:
                arrow = None
        if c == "{":
            depth += 1
            inner = depth > base
        else:
            inner = depth > base or arrow is not None
            if c == "}":
                depth -= 1
        if inner and c != "\n":
            out[i] = " "
        if not c.isspace():
            prev = c
        i += 1
    return "".join(out)


def scan_js(code, label, line_offset=0, col_offset=0):
    masked = top_level_mask(code)
    hits = []
    for m in GEOMETRY.finditer(masked):
        before = code[:m.start()]
        line = before.count("\n")
        col = m.start() - (before.rfind("\n") + 1)
        if line == 0:
            col += col_offset
        start = max(0, m.start() - 60)
        snippet = " ".join(code[start:m.end() + 60].split())
        hits.append((line + line_offset + 1, col, m.group(0).strip(".( "), snippet))
    for line, col, prop, snippet in hits[:8]:
        fail("reflow", f"{label}:{line}:{col}  `{prop}` lido na execução inicial do script: …{snippet}…")
    if len(hits) > 8:
        fail("reflow", f"{label}: e mais {len(hits) - 8} leituras de geometria no nível superior")


# ---------- Imagens ----------

def dimensions(path):
    with open(path, "rb") as fh:
        data = fh.read(256 * 1024)
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if data[:2] == b"\xff\xd8":
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return w, h
                i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            kind = data[12:16]
            if kind == b"VP8 ":
                w, h = struct.unpack("<HH", data[26:30])
                return w & 0x3FFF, h & 0x3FFF
            if kind == b"VP8L":
                b = int.from_bytes(data[21:25], "little")
                return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
            if kind == b"VP8X":
                return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
        if b"ftypavif" in data[:32] or b"ftypavis" in data[:32]:
            sizes = [struct.unpack(">II", data[m.end() + 4:m.end() + 12]) for m in re.finditer(b"ispe", data)]
            if sizes:
                return max(sizes, key=lambda s: s[0] * s[1])
    except (struct.error, IndexError):
        pass
    return None


def audit_images(root, ignore):
    print("\n== Imagens (critério de compressão do PageSpeed: bytes <= largura x altura x 0,167 + 4 KiB)")
    bad, served_legacy, total, soft = [], [], 0, []
    for dirpath, _, files in os.walk(root):
        for f in files:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if not f.lower().endswith(RASTER) or any(fnmatch.fnmatch(rel, g) for g in ignore):
                continue
            if EXEMPT.search(rel):
                continue
            total += 1
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                served_legacy.append(rel)
            dims = dimensions(path)
            if not dims:
                continue
            size, px = os.path.getsize(path), dims[0] * dims[1]
            limit = px * BPP + SLACK
            if size > limit:
                (soft if rel in fallbacks else bad).append((size - limit, rel, dims, size, size / px))
    for _, rel, (w, h), size, bpp in sorted(bad, reverse=True)[:25]:
        fail("compressao", f"{rel}  {w}x{h}  {size / 1024:.1f} KiB  ({bpp:.3f} byte/pixel; limite "
             f"{(w * h * BPP + SLACK) / 1024:.1f} KiB)")
    if len(bad) > 25:
        fail("compressao", f"e mais {len(bad) - 25} arquivos acima do limite")
    for rel in served_legacy[:10]:
        fail("formato", f"{rel}: PNG/JPG na saída do build (use WebP/AVIF; exceções: og:image, favicons, apple-touch-icon)")
    if soft:
        print(f"  .. {len(soft)} WebP de fallback acima do critério (só navegadores sem AVIF baixam; o PageSpeed julga o AVIF): "
              + ", ".join(r for _, r, *_ in sorted(soft, reverse=True)[:5]) + (" …" if len(soft) > 5 else ""))
    if not bad and not served_legacy:
        print(f"  ok {total - len(soft)} arquivos raster dentro do critério")
    elif bad:
        print("     Próximo degrau: confirmar que o AVIF é entregue (<picture> com fallback WebP) e seguir a escada em"
              " SEO-PERFORMANCE.md (AVIF 40–45 conferido ampliado, achatar, vetorizar).")


# ---------- HTML: SEO, compartilhamento, imagens e scripts ----------

def attr(tag, name):
    m = re.search(r'\b%s\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))' % re.escape(name), tag, re.I)
    return html.unescape(next(g for g in m.groups() if g is not None)) if m else None


def meta(doc, key):
    for tag in re.findall(r"<meta\b[^>]*>", doc, re.I):
        if (attr(tag, "property") or attr(tag, "name") or "").lower() == key:
            return attr(tag, "content")
    return None


def local_file(root, page_rel, url, site):
    """Mapeia uma URL (absoluta ou relativa) para um arquivo dentro do build."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in ("http", "https"):
        path = parsed.path
        if site:
            base = urllib.parse.urlparse(site).path
            if path.startswith(base):
                path = path[len(base):]
        candidates = [path.lstrip("/")]
        candidates += [path.lstrip("/").split("/", k)[-1] for k in range(1, path.count("/"))]
    else:
        candidates = [os.path.normpath(os.path.join(os.path.dirname(page_rel), parsed.path)).replace(os.sep, "/").lstrip("/")]
    for c in candidates:
        p = os.path.join(root, urllib.parse.unquote(c))
        if c and os.path.isfile(p):
            return p
    return None


def urls_of(tag):
    """URLs de src/srcset (inclusive data-*) de uma tag <img> ou <source>."""
    out = [attr(tag, a) for a in ("src", "data-src") if attr(tag, a)]
    for a in ("srcset", "data-srcset"):
        out += [p.split()[0] for p in (attr(tag, a) or "").split(",") if p.strip()]
    return out


def is_abs(u):
    return bool(u) and u.startswith(("https://", "http://"))


def audit_page(root, rel, site, home):
    path = os.path.join(root, rel)
    with open(path, encoding="utf-8", errors="ignore") as fh:
        doc = fh.read()
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', doc, re.I) or rel.startswith("404"):
        indexable = False
    else:
        indexable = True
    print(f"\n== {rel}")

    canonical = None
    for tag in re.findall(r"<link\b[^>]*>", doc, re.I):
        if (attr(tag, "rel") or "").lower() == "canonical":
            canonical = attr(tag, "href")
    if indexable:
        if not canonical:
            fail("seo", "sem <link rel=canonical> (defina a URL final do site no build)")
        elif not is_abs(canonical):
            fail("seo", f"canonical relativo: {canonical}")
        elif site and not canonical.startswith(site):
            fail("seo", f"canonical fora da URL final informada: {canonical}")

    og_url, og_img = meta(doc, "og:url"), meta(doc, "og:image")
    if indexable and not is_abs(og_url):
        fail("social", f"og:url ausente ou relativo ({og_url})")
    if not og_img:
        fail("social", "sem og:image (a prévia no WhatsApp/Facebook/LinkedIn sai sem imagem)")
    else:
        if not og_img.startswith("https://"):
            fail("social", f"og:image precisa ser URL absoluta com https (está \"{og_img}\"); scrapers não resolvem caminho relativo")
        f = local_file(root, rel, og_img, site)
        if f:
            dims, size = dimensions(f), os.path.getsize(f)
            fmt = os.path.splitext(f)[1].lower()
            if fmt not in (".jpg", ".jpeg", ".png"):
                fail("social", f"og:image em {fmt}: use JPG ou PNG (nem todo scraper lê WebP/AVIF)")
            if dims and (dims[0] < 1200 or dims[1] < 630):
                fail("social", f"og:image com {dims[0]}x{dims[1]} (mínimo 1200x630)")
            if dims and (meta(doc, "og:image:width"), meta(doc, "og:image:height")) != (str(dims[0]), str(dims[1])):
                fail("social", f"og:image:width/height ({meta(doc, 'og:image:width')}x{meta(doc, 'og:image:height')}) "
                     f"diferente do arquivo ({dims[0]}x{dims[1]})")
            if size > 300 * 1024:
                fail("social", f"og:image com {size / 1024:.0f} KB (máximo 300 KB; o WhatsApp descarta prévias pesadas)")
        elif not is_abs(og_img) or site:
            fail("social", f"og:image não encontrada no build: {og_img}")
        for key in ("og:image:alt", "og:title", "og:description", "twitter:card", "twitter:image"):
            if not meta(doc, key):
                fail("social", f"sem {key}")
    if indexable and "max-image-preview:large" not in (meta(doc, "robots") or ""):
        print("  .. sem <meta name=robots content=\"max-image-preview:large\"> (imagens grandes no Google/Discover)")

    types, abs_bad = set(), []
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', doc, re.S | re.I):
        try:
            data = json.loads(block)
        except ValueError:
            fail("seo", "JSON-LD inválido")
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                t = node.get("@type")
                types.update(t if isinstance(t, list) else [t] if t else [])
                for k in ("url", "logo", "image", "@id"):
                    v = node.get(k)
                    if isinstance(v, str) and not is_abs(v) and not v.startswith("#"):
                        abs_bad.append(f"{k}={v}")
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    if indexable and not types:
        fail("seo", "sem JSON-LD")
    if home and types and not {"WebSite"} & types:
        fail("seo", "home sem WebSite no JSON-LD (o Google usa o name dele como nome do site nos resultados)")
    if home and types and not types & {"Organization", "LocalBusiness", "Person"} and not any(t.endswith(("Organization", "Business", "Service")) for t in types):
        fail("seo", "home sem Organization/LocalBusiness/Person no JSON-LD")
    for b in abs_bad[:5]:
        fail("seo", f"JSON-LD com URL relativa: {b}")

    # <picture> com <source type="image/avif">: o <img> e os demais <source> são fallback.
    with_avif = set()
    for pic in re.findall(r"<picture\b.*?</picture>", doc, re.S | re.I):
        tags = re.findall(r"<(?:source|img)\b[^>]*>", pic, re.I)
        if not any((attr(t, "type") or "").lower() == "image/avif" for t in tags):
            continue
        for t in tags:
            if (attr(t, "type") or "").lower() == "image/avif":
                continue
            if t.lower().startswith("<img"):
                with_avif.add(t)
            for u in urls_of(t):
                f = local_file(root, rel, u, site)
                if f:
                    fallbacks.add(os.path.relpath(f, root).replace(os.sep, "/"))

    imgs = re.findall(r"<img\b[^>]*>", doc, re.I)
    high = [i for i in imgs if (attr(i, "fetchpriority") or "").lower() == "high"]
    if len(high) > 2:
        fail("lcp", f"{len(high)} imagens com fetchpriority=high (deixe só o elemento LCP medido)")
    no_avif = []
    for i in imgs:
        src = attr(i, "src") or attr(i, "data-src") or ""
        if not src.lower().split("?")[0].endswith(RASTER):
            continue
        if not (attr(i, "srcset") or attr(i, "data-srcset")):
            fail("imagens", f"<img> raster sem srcset: {src}")
        if i not in with_avif:
            no_avif.append(src)
    for src in no_avif[:8]:
        fail("formato", f"<img> raster fora de <picture> com <source type=\"image/avif\">: {src}")
    if len(no_avif) > 8:
        fail("formato", f"e mais {len(no_avif) - 8} <img> sem AVIF")
    print(f"  .. fetchpriority=high em: {', '.join(attr(i, 'src') or '?' for i in high) or 'nenhuma imagem'} "
          "(confira se é o elemento LCP que o perf-audit.py imprime, no mobile e no desktop)")

    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", doc, re.S | re.I):
        tipo = (attr(m.group(1), "type") or "").lower()
        if tipo and tipo not in ("module", "text/javascript", "application/javascript"):
            continue
        start = m.start(2)
        line = doc.count("\n", 0, start)
        col = start - (doc.rfind("\n", 0, start) + 1)
        scan_js(m.group(2), rel, line, col)


def site_files(root, site):
    print("\n== Arquivos do site")
    for name in ("robots.txt", "favicon.ico"):
        print(f"  {'ok' if os.path.isfile(os.path.join(root, name)) else '!!'} {name}")
        if not os.path.isfile(os.path.join(root, name)):
            problems.append("seo")
    sitemaps = [f for f in os.listdir(root) if re.match(r"sitemap.*\.xml$", f)]
    if sitemaps:
        print(f"  ok sitemap: {', '.join(sitemaps)}")
    else:
        fail("seo", "sem sitemap*.xml na raiz do build")
    robots = os.path.join(root, "robots.txt")
    if os.path.isfile(robots):
        body = open(robots, encoding="utf-8", errors="ignore").read()
        decl = re.findall(r"(?im)^sitemap:\s*(\S+)", body)
        if not decl:
            fail("seo", "robots.txt sem linha Sitemap:")
        for s in decl:
            if not is_abs(s):
                fail("seo", f"Sitemap no robots.txt precisa ser absoluto: {s}")
    if site and urllib.parse.urlparse(site).path.strip("/"):
        print(f"  .. o site fica numa subpasta ({urllib.parse.urlparse(site).path}): robots.txt e favicon.ico só valem na raiz"
              " do domínio. Envie o sitemap no Search Console (propriedade de prefixo de URL) e peça ao dono do domínio"
              " para declará-lo no robots.txt da raiz; registre o que ficar fora do seu controle.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="pasta de saída do build (ex.: dist)")
    ap.add_argument("--site", help="URL pública final, com barra no fim (ex.: https://www.exemplo.com/ ou https://host.com/subpasta/)")
    ap.add_argument("--ignore", action="append", default=[], help="glob de arquivos a ignorar (relativo ao build; pode repetir)")
    ap.add_argument("--limit", type=int, default=30, help="máximo de páginas HTML auditadas")
    args = ap.parse_args()
    root = args.dir
    if not os.path.isdir(root):
        sys.exit(f"pasta não encontrada: {root}")
    site = args.site and (args.site if args.site.endswith("/") else args.site + "/")
    if not site:
        print("Aviso: sem --site. Informe a URL pública final para conferir canonical, og:url e og:image.")

    pages = sorted(os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/")
                   for d, _, fs in os.walk(root) for f in fs if f.endswith(".html"))
    pages.sort(key=lambda p: (p != "index.html", p.count("/"), p))
    for rel in pages[:args.limit]:
        audit_page(root, rel, site, rel == "index.html")
    if len(pages) > args.limit:
        print(f"\n({len(pages) - args.limit} páginas não auditadas; aumente --limit)")

    print("\n== Scripts (.js) do build: leitura de geometria na execução inicial")
    before = problems.count("reflow")
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith((".js", ".mjs")):
                p = os.path.join(d, f)
                rel = os.path.relpath(p, root).replace(os.sep, "/")
                if any(fnmatch.fnmatch(rel, g) for g in args.ignore):
                    continue
                scan_js(open(p, encoding="utf-8", errors="ignore").read(), rel)
    if problems.count("reflow") == before:
        print("  ok nenhuma leitura de geometria no nível superior dos arquivos .js")

    audit_images(root, args.ignore)
    site_files(root, site)

    if problems:
        groups = sorted(set(problems))
        print(f"\nResultado: {len(problems)} reprovações ({', '.join(groups)}). Corrija, rode o build e repita.")
        sys.exit(1)
    print("\nResultado: nenhuma reprovação.")


if __name__ == "__main__":
    main()
