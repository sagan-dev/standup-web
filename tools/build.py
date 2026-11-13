#!/usr/bin/env python3
"""Generates the static pages (all languages in content.json) of standup.sagan.dev. Run: python3 tools/build.py"""
import os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://standup.sagan.dev"
GITHUB = "https://github.com/sagan-dev/Standup"
APPSTORE = "https://apps.apple.com/app/id6817507284"
MAIL = "michal@sagan.dev"
ASSET_V = "3"

with open(os.path.join(ROOT, "content.json"), encoding="utf-8") as f:
    CONTENT = json.load(f)

T = CONTENT["T"]
FEATURES = CONTENT["FEATURES"]
REQS = CONTENT["REQS"]
HOME = CONTENT["HOME"]
PRIVACY = CONTENT["PRIVACY"]
SUPPORT = CONTENT["SUPPORT"]

# Native display name for each language, used in the language switcher and <html lang>
NATIVE = {
 "en": "English", "pl": "Polski", "ar": "العربية", "ca": "Català", "cs": "Čeština",
 "da": "Dansk", "de": "Deutsch", "el": "Ελληνικά", "es": "Español", "es-MX": "Español (México)",
 "fi": "Suomi", "fr": "Français", "fr-CA": "Français (Canada)", "he": "עברית", "hi": "हिन्दी",
 "hr": "Hrvatski", "hu": "Magyar", "id": "Bahasa Indonesia", "it": "Italiano", "ja": "日本語",
 "ko": "한국어", "ms": "Bahasa Melayu", "nb": "Norsk bokmål", "nl": "Nederlands",
 "pt-BR": "Português (Brasil)", "pt-PT": "Português (Portugal)", "ro": "Română", "ru": "Русский",
 "sk": "Slovenčina", "sv": "Svenska", "th": "ไทย", "tr": "Türkçe", "uk": "Українська",
 "vi": "Tiếng Việt", "zh-Hans": "简体中文", "zh-Hant": "繁體中文",
}

# en first (no URL prefix), then the rest in a fixed, readable order
LANGS = ["en"] + sorted((c for c in T if c != "en"), key=lambda c: NATIVE.get(c, c))

def url(lang, path):
    p = T[lang]["prefix"] + path
    return p if p else "/"

def lang_switcher(lang, path):
    links = "\n".join(
        f'    <a href="{url(code, path)}" hreflang="{code}" lang="{code}"'
        f'{" class=\"current\"" if code == lang else ""}>{NATIVE.get(code, code)}</a>'
        for code in LANGS)
    return f"""<details class="langpicker">
    <summary>{NATIVE.get(lang, lang)}</summary>
    <div class="langlist">
{links}
    </div>
  </details>"""

def layout(lang, path, title, desc, body, page_class=""):
    t = T[lang]
    canon = BASE + url(lang, path)
    nav = t["nav"]
    home = url(lang, "/")
    hreflang_tags = "\n".join(f'<link rel="alternate" hreflang="{code}" href="{BASE + url(code, path)}">' for code in LANGS)
    hreflang_tags += f'\n<link rel="alternate" hreflang="x-default" href="{BASE + url("en", path)}">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
{hreflang_tags}
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/icon.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#1f6bff">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css?v={ASSET_V}">
</head>
<body class="{page_class}">
<header class="site"><div class="wrap">
  <a class="brand" href="{home}"><img src="/assets/icon.png" width="28" height="28" alt=""><span>Standup</span></a>
  <nav class="main" aria-label="Main">
    <a class="hide-sm" href="{url(lang, '/')}#features">{nav['features']}</a>
    <a href="{url(lang, '/privacy')}">{nav['privacy']}</a>
    <a href="{url(lang, '/support')}">{nav['support']}</a>
    {lang_switcher(lang, path)}
  </nav>
</div></header>
<main>
{body}
</main>
<footer class="site"><div class="wrap">
  <div>{t['footer_made']}</div>
  <div><a href="{url(lang, '/privacy')}">{nav['privacy']}</a> · <a href="{url(lang, '/support')}">{nav['support']}</a> · <a href="{GITHUB}">{t['opensrc']}</a></div>
  <div style="flex-basis:100%;font-size:13px">{t['footer_disc']}</div>
</div></footer>
</body>
</html>
"""

# ------------------------------------------------------------------ landing

def landing(lang):
    t = T[lang]; h = HOME[lang]
    cards = "\n".join(
        f'<div class="card">{f"<span class=tag>{tag}</span>" if tag else ""}<h3>{html.escape(ti)}</h3><p>{html.escape(tx)}</p></div>'
        for ti, tx, tag in FEATURES[lang])
    rt, ritems, rnote = REQS[lang]
    reqs = "".join(f"<li>{html.escape(i)}</li>" for i in ritems)
    body = f"""<div class="wrap">
<section class="hero">
  <img class="icon" src="/assets/icon.png" width="120" height="120" alt="Standup icon">
  <h1>{t['name']}</h1>
  <p class="sub">{html.escape(t['tagline'])}</p>
  <div class="btns">
    <a class="btn primary" href="{APPSTORE}">{t['coming']}</a>
    <a class="btn" href="{GITHUB}">{t['opensrc']}</a>
  </div>
  <div class="shot"><img src="/assets/popover.png" width="920" height="634" alt="Standup popover: current desk height, raise and lower buttons, stand and sit presets, and the meeting automation card"></div>
</section>
<section id="features">
  <h2>{h['feat_h']}</h2>
  <p class="lead">{h['feat_lead']}</p>
  <div class="grid">
{cards}
  </div>
</section>
<section>
  <div class="two">
    <div class="card"><h3>{rt}</h3><ul class="clean">{reqs}</ul><p style="margin-top:10px;font-size:13px">{rnote}</p></div>
    <div class="card"><h3>{h['open_h']}</h3><p>{h['open_p']}</p><p style="margin-top:10px"><a href="{GITHUB}">github.com/sagan-dev/Standup →</a></p></div>
  </div>
</section>
</div>"""
    return layout(lang, "/", t["name"] + " — macOS", t["meta_home"], body)

# ------------------------------------------------------------------ privacy / support

def doc_page(lang, kind):
    t = T[lang]
    if kind == "privacy":
        title, meta, content = PRIVACY[lang]
        body = f'<div class="wrap"><article class="doc"><h1>{title}</h1><p class="meta">{meta}</p>{content}</article></div>'
        return layout(lang, "/privacy", f"{title} — {t['name']}", t["meta_privacy"], body)
    title, intro, faqs, ch, contact = SUPPORT[lang]
    items = "\n".join(f"<details><summary>{q}</summary>{a}</details>" for q, a in faqs)
    body = f'<div class="wrap"><article class="doc"><h1>{title}</h1><p class="meta">{intro}</p>{items}<h2>{ch}</h2><p>{contact}</p></article></div>'
    return layout(lang, "/support", f"{title} — {t['name']}", t["meta_support"], body)

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

urls = []
for lang in LANGS:
    pre = T[lang]["prefix"].lstrip("/")
    write(f"{pre}/index.html" if pre else "index.html", landing(lang))
    write(f"{pre}/privacy/index.html" if pre else "privacy/index.html", doc_page(lang, "privacy"))
    write(f"{pre}/support/index.html" if pre else "support/index.html", doc_page(lang, "support"))
    urls += [url(lang, "/"), url(lang, "/privacy"), url(lang, "/support")]

not_found = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found — Standup</title><link rel="stylesheet" href="/style.css?v={ASSET_V}"><link rel="icon" href="/assets/favicon-32.png"></head><body><div class="wrap"><section class="hero"><img class="icon" src="/assets/icon.png" width="96" height="96" alt=""><h1>404</h1><p class="sub">This page does not exist.</p><div class="btns"><a class="btn primary" href="/">Standup home</a></div></section></div></body></html>"""
write("404.html", not_found)
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
sm = "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in urls)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
write("vercel.json", '{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
print("built", len(urls), "pages in", len(LANGS), "languages")
