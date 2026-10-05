#!/usr/bin/env python3
"""Auditoria de performance focada, a partir do Lighthouse. Somente leitura; só usa a biblioteca padrão.

Roda o Lighthouse (via npx, exige Node e Chrome) em mobile e desktop e lista apenas o que falhou em:
cache, imagens (tamanho exibido, compressão, formato), reflow forçado, árvore de dependência de rede,
LCP, CLS, fontes e bloqueio de renderização, com as URLs afetadas.

Uso:
  python3 perf-audit.py https://exemplo.com
  python3 perf-audit.py http://localhost:4321 --only mobile
  python3 perf-audit.py --report tmp/lighthouse/mobile.json   # analisa um relatório já salvo

Os relatórios ficam em ./tmp/lighthouse/ (relativo à pasta onde o comando foi executado).
O item de cache só é válido contra o site publicado: o servidor de preview local não usa .htaccess.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request

# Grupo -> IDs de auditoria. Inclui os nomes antigos e os "insights" (Lighthouse 12.6+/13).
GROUPS = [
    ("Cache", ["uses-long-cache-ttl", "cache-insight"]),
    ("Imagens", ["uses-responsive-images", "uses-optimized-images", "modern-image-formats",
                 "efficient-animated-content", "image-delivery-insight", "unsized-images"]),
    ("Reflow forçado", ["forced-reflow-insight"]),
    ("Árvore de rede", ["network-dependency-tree-insight", "critical-request-chains"]),
    ("LCP", ["lcp-discovery-insight", "prioritize-lcp-image", "lcp-lazy-loaded"]),
    ("CLS", ["cls-culprits-insight", "layout-shifts"]),
    ("Fontes", ["font-display-insight", "font-display"]),
    ("Bloqueio de renderização", ["render-blocking-insight", "render-blocking-resources"]),
    ("Terceiros", ["third-parties-insight", "third-party-summary"]),
]
METRICS = [("largest-contentful-paint", "LCP"), ("cumulative-layout-shift", "CLS"),
           ("total-blocking-time", "TBT"), ("first-contentful-paint", "FCP"), ("speed-index", "SI")]
NUMERIC = {"wastedBytes": "desperdício", "totalBytes": "total", "transferSize": "transferido",
           "cacheLifetimeMs": "cache", "wastedMs": "atraso", "reflowTime": "reflow",
           "navStartToEndTime": "fim", "score": "shift"}


def fmt(key, value):
    if key in ("wastedBytes", "totalBytes", "transferSize"):
        return f"{value / 1024:.1f} KiB"
    if key == "cacheLifetimeMs":
        days = value / 86400000
        return f"{days:.0f} dias" if days >= 1 else f"{value / 3600000:.1f} h"
    if key in ("wastedMs", "reflowTime", "navStartToEndTime"):
        return f"{value:.0f} ms"
    return f"{value:.3f}" if isinstance(value, float) else str(value)


def rows(node, out, seen):
    """Percorre details e extrai linhas (url + números relevantes) sem duplicar."""
    if isinstance(node, list):
        for item in node:
            rows(item, out, seen)
        return
    if not isinstance(node, dict):
        return
    url, line, col = node.get("url"), None, None
    if not isinstance(url, str):
        for child in ("source", "node", "entity"):
            c = node.get(child)
            if isinstance(c, dict) and isinstance(c.get("url"), str):
                url, line, col = c["url"], c.get("line"), c.get("column")
                break
    nums = {k: node[k] for k in NUMERIC if isinstance(node.get(k), (int, float)) and node[k]}
    if isinstance(url, str) and url.startswith("http") and (nums or "chains" not in node):
        key = (url, line, tuple(sorted(nums.items())))
        if key not in seen:
            seen.add(key)
            label = url if line is None else f"{url}:{line + 1}:{col or 0}"
            if any(m in url for m in CDN_MARKERS):
                label += "  [da CDN: não é controlado pelo .htaccess nem pelo código]"
            out.append((label, nums))
            if line is not None:
                snippet = source_snippet(url, line, col or 0)
                if snippet:
                    out.append((f"      trecho: …{snippet}…", {}))
    for k, v in node.items():
        if k not in ("source", "node", "entity") and isinstance(v, (dict, list)):
            rows(v, out, seen)


CDN_MARKERS = ("/cdn-cgi/", "cloudflareinsights.com")
_SOURCES = {}


def source_snippet(url, line, col, before=160, after=240):
    """Trecho do código na linha/coluna apontada (útil para scripts inline no HTML)."""
    if url not in _SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 perf-audit"})
            with urllib.request.urlopen(req, timeout=20) as r:
                _SOURCES[url] = r.read().decode("utf-8", "ignore").split("\n")
        except Exception:
            _SOURCES[url] = None
    lines = _SOURCES[url]
    if not lines or line >= len(lines):
        return None
    text = lines[line]
    return " ".join(text[max(0, col - before):col + after].split())


def notes(node, out):
    """Checklists reprovados e elementos (seletores) citados pela auditoria."""
    if isinstance(node, list):
        for item in node:
            notes(item, out)
    elif isinstance(node, dict):
        if node.get("type") == "checklist" and isinstance(node.get("items"), dict):
            for item in node["items"].values():
                if isinstance(item, dict) and item.get("value") is False:
                    out.append(f"reprovado: {item.get('label')}")
        elif node.get("type") == "node" and node.get("selector"):
            out.append(f"elemento: {node['selector']}")
        else:
            for v in node.values():
                if isinstance(v, (dict, list)):
                    notes(v, out)


def longest_chain(node):
    if isinstance(node, dict):
        lc = node.get("longestChain")
        if isinstance(lc, dict) and "duration" in lc:
            return lc["duration"]
        for v in node.values():
            r = longest_chain(v)
            if r is not None:
                return r
    elif isinstance(node, list):
        for v in node:
            r = longest_chain(v)
            if r is not None:
                return r
    return None


def failing(audit):
    mode = audit.get("scoreDisplayMode")
    if mode in ("notApplicable", "manual", "error"):
        return False
    score = audit.get("score")
    if score is None:  # informativo: só interessa se houver itens
        return bool((audit.get("details") or {}).get("items") or (audit.get("details") or {}).get("chains"))
    return score < 0.9


def lcp_breakdown(audit):
    """Elemento LCP e suas fases. Sai sempre: o insight costuma passar mesmo com atraso de renderização alto."""
    items = ((audit or {}).get("details") or {}).get("items") or []
    node = next((i for i in items if i.get("type") == "node"), None)
    phases = next((i.get("items") for i in items if i.get("type") == "table"), None) or []
    if not node and not phases:
        return
    if node:
        print(f"Elemento LCP: {node.get('selector')}  \"{(node.get('nodeLabel') or '')[:60]}\"")
    if phases:
        print("  fases: " + "  ".join(f"{p.get('label')} {p.get('duration', 0):.0f} ms" for p in phases))
    delay = next((p.get("duration", 0) for p in phases if p.get("subpart") == "elementRenderDelay"), 0)
    if delay > 1000:
        print("  ! atraso de renderização alto: verifique se o elemento LCP entra com opacity 0 ou animation-delay")


def analyze(path, label):
    with open(path, encoding="utf-8") as fh:
        lhr = json.load(fh)
    audits = lhr.get("audits", {})
    perf = (lhr.get("categories", {}).get("performance") or {}).get("score")
    print(f"\n=== {label} — {lhr.get('finalDisplayedUrl') or lhr.get('finalUrl')} "
          f"(Lighthouse {lhr.get('lighthouseVersion')}) ===")
    print(f"Performance: {round(perf * 100) if perf is not None else '?'}  |  " + "  ".join(
        f"{name} {audits[a].get('displayValue', '?')}" for a, name in METRICS if a in audits))
    lcp_breakdown(audits.get("lcp-breakdown-insight"))
    problems = 0
    for group, ids in GROUPS:
        found = [audits[i] for i in ids if i in audits and failing(audits[i])]
        if not found:
            continue
        print(f"\n[{group}]")
        seen = set()
        for audit in found:
            info = " (informativo)" if audit.get("score") is None else ""
            if not info:
                problems += 1
            print(f"  • {audit.get('title')}{info}" + (f" — {audit['displayValue']}" if audit.get("displayValue") else ""))
            lc = longest_chain(audit.get("details"))
            if lc is not None:
                print(f"    latência máxima do caminho crítico: {lc:.0f} ms")
            extra_notes = []
            notes(audit.get("details"), extra_notes)
            for n in dict.fromkeys(extra_notes):
                print(f"    {n}")
            out = []
            rows(audit.get("details"), out, seen)
            for url, nums in out[:12]:
                extra = ", ".join(f"{NUMERIC[k]} {fmt(k, v)}" for k, v in nums.items())
                print(url if url.startswith("      trecho") else f"    - {url}" + (f"  ({extra})" if extra else ""))
            if len(out) > 12:
                print(f"    … e mais {len(out) - 12}")
    if not problems:
        print("\nNenhuma falha nos grupos auditados.")
    return problems


def run_lighthouse(url, form, outdir):
    npx = shutil.which("npx")
    if not npx:
        sys.exit("npx não encontrado: instale o Node.js ou use --report com um JSON do Lighthouse.")
    path = os.path.join(outdir, f"{form}.json")
    cmd = [npx, "-y", "lighthouse", url, "--output=json", f"--output-path={path}", "--quiet",
           "--only-categories=performance", "--chrome-flags=--headless=new"]
    if form == "desktop":
        cmd.append("--preset=desktop")
    print(f"Rodando Lighthouse ({form})…", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(path):
        sys.exit(f"Lighthouse falhou ({form}):\n{result.stderr[-2000:]}")
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("url", nargs="?", help="URL a auditar (build de produção ou site publicado)")
    p.add_argument("--report", action="append", help="JSON do Lighthouse já salvo (pode repetir)")
    p.add_argument("--only", choices=["mobile", "desktop"], help="roda só um formato")
    p.add_argument("--outdir", default=os.path.join("tmp", "lighthouse"))
    args = p.parse_args()
    if not args.url and not args.report:
        p.error("informe uma URL ou --report")

    problems = 0
    if args.report:
        for path in args.report:
            problems += analyze(path, os.path.basename(path))
    else:
        os.makedirs(args.outdir, exist_ok=True)
        for form in [args.only] if args.only else ["mobile", "desktop"]:
            problems += analyze(run_lighthouse(args.url, form, args.outdir), form)
        if args.url.startswith(("http://localhost", "http://127.", "http://0.0.0.0")):
            print("\nAviso: em localhost, o grupo Cache reflete o servidor de preview, não a hospedagem.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
