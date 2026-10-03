#!/usr/bin/env python3
"""Auditoria de SEO on-page a partir do sitemap. Somente leitura; só usa a biblioteca padrão.

Uso:
  python3 seo-audit.py https://exemplo.com
  python3 seo-audit.py http://localhost:4321 --sitemap http://localhost:4321/sitemap-index.xml
  python3 seo-audit.py https://exemplo.com --limit 50 --min-words 300
"""
import argparse
import collections
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
TITLE_RANGE = (30, 65)
DESC_RANGE = (70, 160)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def fetch(url, follow=True, method="GET"):
    """Retorna (status, headers, corpo, url final). Status é texto em erro de rede."""
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    try:
        with opener.open(req, timeout=25) as r:
            body = r.read().decode("utf-8", "ignore") if method == "GET" else ""
            return r.status, dict(r.headers), body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), "", url
    except Exception as e:  # rede, DNS, TLS
        return f"erro: {e}", {}, "", url


def header(headers, name):
    return next((v for k, v in headers.items() if k.lower() == name.lower()), None)


def meta(doc, name):
    tag = re.search(r'<meta[^>]+(?:name|property)=["\']%s["\'][^>]*>' % re.escape(name), doc, re.I)
    if not tag:
        return None
    content = re.search(r'content=["\']([^"\']*)', tag.group(0))
    return html.unescape(content.group(1)).strip() if content else ""


def jsonld_types(doc):
    types, invalid = [], 0
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', doc, re.S | re.I):
        try:
            data = json.loads(block)
        except ValueError:
            invalid += 1
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                t = node.get("@type")
                if t:
                    types.extend(t if isinstance(t, list) else [t])
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return sorted(set(types)), invalid


def sitemap_urls(url, seen=None):
    seen = seen or set()
    if url in seen:
        return []
    seen.add(url)
    status, _, body, _ = fetch(url)
    if status != 200:
        print(f"  ! sitemap {url} -> {status}")
        return []
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", body)
    if "<sitemapindex" in body:
        urls = []
        for child in locs:
            urls += sitemap_urls(html.unescape(child), seen)
        return urls
    if "<lastmod>" not in body:
        print(f"  ! {url} sem <lastmod>")
    return [html.unescape(u) for u in locs]


def audit_page(url, base, min_words):
    status, headers, doc, final = fetch(url)
    issues = []
    if status != 200:
        return url, [f"HTTP {status}"], {}
    if final.rstrip("/") != url.rstrip("/"):
        issues.append(f"redireciona para {final}")

    title = re.search(r"<title[^>]*>(.*?)</title>", doc, re.S | re.I)
    title = html.unescape(re.sub(r"\s+", " ", title.group(1))).strip() if title else ""
    desc = meta(doc, "description") or ""
    if not title:
        issues.append("sem <title>")
    elif not TITLE_RANGE[0] <= len(title) <= TITLE_RANGE[1]:
        issues.append(f"title com {len(title)} caracteres")
    if not desc:
        issues.append("sem meta description")
    elif not DESC_RANGE[0] <= len(desc) <= DESC_RANGE[1]:
        issues.append(f"description com {len(desc)} caracteres")

    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', doc, re.I) \
        or re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', doc, re.I)
    robots = (meta(doc, "robots") or "") + " " + (header(headers, "X-Robots-Tag") or "")
    noindex = "noindex" in robots.lower()
    if not canonical and not noindex:
        issues.append("sem canonical")
    elif canonical and canonical.group(1).rstrip("/") != url.rstrip("/"):
        issues.append(f"canonical aponta para {canonical.group(1)}")
    if noindex:
        issues.append("noindex (está no sitemap)")

    h1 = re.findall(r"<h1[\s>]", doc, re.I)
    if len(h1) != 1:
        issues.append(f"{len(h1)} H1")
    if not re.search(r"<html[^>]+lang=", doc, re.I):
        issues.append("sem lang no <html>")

    imgs = re.findall(r"<img\b[^>]*>", doc, re.I)
    no_alt = sum(1 for i in imgs if not re.search(r"\balt=", i, re.I))
    no_dims = sum(1 for i in imgs if not re.search(r"\bwidth=", i, re.I))
    if no_alt:
        issues.append(f"{no_alt} img sem alt")
    if no_dims:
        issues.append(f"{no_dims} img sem width/height")

    for prop in ("og:title", "og:description", "og:image"):
        if not meta(doc, prop):
            issues.append(f"sem {prop}")

    types, invalid = jsonld_types(doc)
    if invalid:
        issues.append(f"{invalid} JSON-LD inválido")
    if not types:
        issues.append("sem JSON-LD")
    path = urllib.parse.urlparse(url).path.strip("/")
    if path and "BreadcrumbList" not in types:
        issues.append("sem BreadcrumbList")

    text = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", doc)
    words = len(re.sub(r"<[^>]+>", " ", text).split())
    if words < min_words and not noindex:
        issues.append(f"~{words} palavras")

    fonts = len(re.findall(r'rel=["\']preload["\'][^>]*\.woff2', doc, re.I))
    if fonts > 2:
        issues.append(f"{fonts} fontes com preload")

    return url, issues, {"title": title, "desc": desc, "types": types}


def site_checks(base):
    print("== Verificações gerais")
    parsed = urllib.parse.urlparse(base)
    host = parsed.netloc
    alt_host = host[4:] if host.startswith("www.") else "www." + host
    is_local = host.startswith(("localhost", "127.")) or ":" in host
    variants = [] if is_local else [f"http://{host}/", f"https://{alt_host}/", f"http://{alt_host}/"]
    for v in variants:
        status, _, _, _ = fetch(v, follow=False, method="HEAD")
        _, _, _, final = fetch(v)
        ok = status in (301, 308) and urllib.parse.urlparse(final).netloc == host
        note = "" if ok else "  (deveria redirecionar com 301 para a canônica)"
        print(f"  {'ok' if ok else '!!'} {v} -> {status}, termina em {final}{note}")
    for path in ("robots.txt", "favicon.ico", "pagina-inexistente-seo-audit"):
        status, headers, body, _ = fetch(f"{base}/{path}")
        expected = 404 if path.startswith("pagina") else 200
        print(f"  {'ok' if status == expected else '!!'} /{path} -> {status} (esperado {expected})")
        if path == "robots.txt" and status == 200:
            if re.search(r"(?im)^disallow:\s*/\s*$", body):
                print("  !! robots.txt bloqueia o site inteiro")
            sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", body)
            print(f"     sitemaps declarados: {sitemaps or 'nenhum'}")
    status, headers, _, _ = fetch(f"{base}/", method="HEAD")
    print(f"     HTML Cache-Control: {header(headers, 'Cache-Control')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="URL base do site, sem barra final")
    ap.add_argument("--sitemap", help="URL do sitemap (padrão: lido do robots.txt ou /sitemap.xml)")
    ap.add_argument("--limit", type=int, default=200, help="máximo de páginas auditadas")
    ap.add_argument("--min-words", type=int, default=250, help="alerta abaixo desta contagem de palavras")
    args = ap.parse_args()
    base = args.base.rstrip("/")

    site_checks(base)

    sitemap = args.sitemap
    if not sitemap:
        _, _, robots, _ = fetch(f"{base}/robots.txt")
        found = re.findall(r"(?im)^sitemap:\s*(\S+)", robots)
        sitemap = found[0] if found else f"{base}/sitemap.xml"
    print(f"\n== Sitemap: {sitemap}")
    urls = sitemap_urls(sitemap)
    if not urls:
        print("  !! nenhuma URL encontrada; auditando só a home")
        urls = [f"{base}/"]
    urls = urls[: args.limit]
    print(f"  {len(urls)} URLs")

    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda u: audit_page(u, base, args.min_words), urls))

    # Problemas presentes em todas as páginas vêm do layout: listados uma vez só
    common = set.intersection(*(set(i) for _, i, _ in results)) if len(results) > 1 else set()
    if common:
        print("\n== Em todas as páginas (provavelmente no layout)")
        for issue in sorted(common):
            print(f"  {issue}")

    print("\n== Páginas com problemas")
    clean = 0
    for url, issues, _ in results:
        issues = [i for i in issues if i not in common]
        if issues:
            print(f"  {urllib.parse.urlparse(url).path or '/'}: " + "; ".join(issues))
        else:
            clean += 1
    print(f"  ({clean} de {len(results)} páginas sem problemas)")

    print("\n== Duplicados")
    for field, label in (("title", "title"), ("desc", "description")):
        counts = collections.Counter(d[field] for _, _, d in results if d.get(field))
        dups = {k: v for k, v in counts.items() if v > 1}
        for value, n in dups.items():
            pages = [urllib.parse.urlparse(u).path or "/" for u, _, d in results if d.get(field) == value]
            print(f"  {label} repetido {n}x: \"{value[:70]}\" -> {', '.join(pages)}")
        if not dups:
            print(f"  ok nenhum {label} repetido")

    print("\n== Tipos JSON-LD por quantidade de páginas")
    types = collections.Counter(t for _, _, d in results for t in d.get("types", []))
    print("  " + ", ".join(f"{t} ({n})" for t, n in types.most_common()) if types else "  nenhum")


if __name__ == "__main__":
    sys.exit(main())
