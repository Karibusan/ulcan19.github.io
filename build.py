#!/usr/bin/env python3
"""Assemble the notes pages and compute their CSP hashes.

The site enforces script-src and style-src by sha256 hash, so a page whose
inline blocks change by one byte stops executing them. Rather than update
the header by hand, build it: the hash is derived from the exact bytes that
end up in the file.

Usage:  python3 build.py          # writes the pages
        python3 build.py --check  # verifies existing pages still match
"""

import base64
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent


def sha256_csp(content: str) -> str:
    digest = hashlib.sha256(content.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def read(name: str) -> str:
    return (HERE / name).read_text(encoding="utf-8").rstrip("\n")


SHARED_CSS = read("_shared.css")
ARTICLE_CSS = read("_article.css")
LANG_JS = read("_lang.js")

HEAD = """<!DOCTYPE html>
<!--
  Same rules as the front page: one file, no build output you cannot read,
  no third-party anything. The CSP below is enforced by hash, so if you
  change a byte of the inline style or script, the page stops executing it.
  Regenerate with build.py rather than editing the hashes by hand.

  Disclosure policy: /.well-known/security.txt
  - Yan
-->
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src {script_hash}; style-src {style_hash}; img-src 'self' data:; connect-src 'none'; form-action 'none'; base-uri 'none'; upgrade-insecure-requests">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="{og_type}">
<link rel="canonical" href="{canonical}">
<style>
{css}
</style>
</head>
<body>
<div class="langbar">
  <div class="wrap">
    <a class="sig" href="/">Yan Urquiza</a>
    <div class="langs" role="group" aria-label="Language">
      <button type="button" data-lang="en" aria-pressed="true">EN</button>
      <button type="button" data-lang="fr" aria-pressed="false">FR</button>
    </div>
  </div>
</div>
<div class="wrap">
{body}
<footer>
  <p><a href="/notes/" data-en="All notes" data-fr="Toutes les notes"></a> &nbsp;·&nbsp; <a href="/" data-en="Home" data-fr="Accueil"></a> &nbsp;·&nbsp; <a href="mailto:ulcan19@pm.me">ulcan19@pm.me</a></p>
  <p class="foot-note" data-en="No trackers. No analytics. No third-party fonts or scripts. Static files, served as-is."
     data-fr="Aucun traceur. Aucune analytique. Aucune police ni script tiers. Des fichiers statiques, servis tels quels."></p>
</footer>
</div>
<script>
{js}
</script>
</body>
</html>
"""

ARTICLE_BODY = """<header class="post-head">
  <p class="eyebrow" data-en="Note &middot; Detection engineering" data-fr="Note &middot; Ingénierie de détection"></p>
  <h1 data-en="Guardrails retrieved by similarity are guardrails that don&rsquo;t fire"
      data-fr="Un garde-fou récupéré par similarité est un garde-fou qui ne se déclenche pas"></h1>
  <p class="standfirst" data-en="Agent memory that stores rules and knowledge in one vector index has a silent control failure built into it."
     data-fr="Une mémoire d&rsquo;agent qui range règles et connaissances dans un même index vectoriel embarque une défaillance de contrôle silencieuse."></p>
  <p class="meta"><time datetime="2026-08-28">2026-08-28</time></p>
</header>

<article class="prose">
{en}

{fr}
</article>
"""

INDEX_BODY = """<header class="post-head">
  <p class="eyebrow" data-en="Notes" data-fr="Notes"></p>
  <h1 data-en="Notes" data-fr="Notes"></h1>
  <p class="standfirst" data-en="Occasional writing on detection engineering, security architecture, and the systems I build."
     data-fr="Écrits occasionnels sur l&rsquo;ingénierie de détection, l&rsquo;architecture de sécurité, et les systèmes que je construis."></p>
</header>

<section class="prose">
<ul class="notes-list">
  <li>
    <span class="d"><time datetime="2026-08-28">2026-08-28</time></span>
    <h2><a href="/notes/guardrails-retrieved-by-similarity/"
           data-en="Guardrails retrieved by similarity are guardrails that don&rsquo;t fire"
           data-fr="Un garde-fou récupéré par similarité est un garde-fou qui ne se déclenche pas"></a></h2>
    <p data-en="A rule&rsquo;s trigger condition is not its content. Store policy in a similarity index and your controls fail open, silently &mdash; the same failure mode as a detection rule that never fires."
       data-fr="La condition de déclenchement d&rsquo;une règle n&rsquo;est pas son contenu. Rangez la politique dans un index de similarité et vos contrôles échouent en silence &mdash; le mode de défaillance d&rsquo;une règle de détection qui ne se déclenche jamais."></p>
  </li>
</ul>
</section>
"""

PAGES = {
    "notes/guardrails-retrieved-by-similarity/index.html": dict(
        title="Guardrails retrieved by similarity are guardrails that don't fire — Yan Urquiza",
        og_title="Guardrails retrieved by similarity are guardrails that don't fire",
        description="A rule's trigger condition is not its content. Storing agent policy in a similarity index builds a control that fails open, silently.",
        og_type="article",
        canonical="https://yan.kitaribu.xyz/notes/guardrails-retrieved-by-similarity/",
        css=SHARED_CSS + "\n" + ARTICLE_CSS,
        body=ARTICLE_BODY.format(en=read("_article_en.html"), fr=read("_article_fr.html")),
    ),
    "notes/index.html": dict(
        title="Notes — Yan Urquiza",
        og_title="Notes — Yan Urquiza",
        description="Occasional writing on detection engineering, security architecture, and the systems I build.",
        og_type="website",
        canonical="https://yan.kitaribu.xyz/notes/",
        css=SHARED_CSS + "\n" + ARTICLE_CSS,
        body=INDEX_BODY,
    ),
}


def render(spec: dict) -> str:
    return HEAD.format(
        script_hash=sha256_csp("\n" + LANG_JS + "\n"),
        style_hash=sha256_csp("\n" + spec["css"] + "\n"),
        js=LANG_JS,
        **{k: v for k, v in spec.items() if k != "css"},
        css=spec["css"],
    )


def main() -> int:
    check = "--check" in sys.argv
    failures = 0
    for path, spec in PAGES.items():
        target = HERE / path
        rendered = render(spec)
        if check:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current != rendered:
                print(f"STALE {path}")
                failures += 1
            else:
                print(f"ok    {path}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print(f"wrote {path}  ({len(rendered):,} bytes)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
