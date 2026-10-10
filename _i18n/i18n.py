#!/usr/bin/env python3
"""Build Indonesian (/id/) and Chinese (/zh/) copies of the English pages.

English pages at the site root are the source. Translations live in
_i18n/<lang>/<page-key>.json as {source_html: translated_html}.

  python3 _i18n/i18n.py extract   # write _i18n/src/<page-key>.json (strings to translate)
  python3 _i18n/i18n.py build     # add switcher to EN pages, write id/ and zh/ pages

Folders starting with "_" are not published by GitHub Pages (Jekyll).
"""
import json, os, re, sys
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://iwiradika.github.io"
PAGES = ["index.html"] + sorted("blog/" + f for f in os.listdir(os.path.join(ROOT, "blog")) if f.endswith(".html"))
LANGS = {"en": "English", "id": "Bahasa Indonesia", "zh": "中文"}
SHORT = {"en": "EN", "id": "ID", "zh": "中文"}
HTML_LANG = {"en": "en", "id": "id", "zh": "zh-Hans"}

INLINE = {"a", "em", "strong", "b", "i", "span", "small", "sub", "sup", "code", "br", "abbr", "u", "mark", "tspan", "q", "cite", "s", "kbd", "var"}
SKIP = {"script", "style", "noscript"}
ATTRS = ["alt", "title", "aria-label", "placeholder"]
META = {"description", "og:title", "og:description", "og:image:alt", "twitter:title", "twitter:description"}


def key(page):
    return page.replace("/", "__").replace(".html", "")


def soup_of(path):
    with open(path, encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def has_text(el):
    return any(isinstance(s, NavigableString) and not isinstance(s, Comment) and re.search(r"[A-Za-z]", s)
               for s in el.descendants)


def all_inline(el):
    for d in el.descendants:
        if getattr(d, "name", None) and d.name not in INLINE:
            return False
    return True


def candidate(el):
    return getattr(el, "name", None) and el.name not in SKIP and has_text(el) and all_inline(el)


def units(soup):
    out = []
    root = soup.body or soup
    for el in root.find_all(True):
        if el.find_parent(SKIP):
            continue
        if candidate(el) and not candidate(el.parent):
            out.append(el)
    return out


def bare_texts(soup):
    """Text nodes sitting next to non-inline siblings (e.g. text after an <svg> icon)."""
    out = []
    root = soup.body or soup
    for s in root.find_all(string=True):
        if isinstance(s, Comment) or not re.search(r"[A-Za-z]{2,}", s):
            continue
        par = s.parent
        if par is None or par.name in SKIP or par.find_parent(SKIP):
            continue
        if candidate(par) or any(candidate(a) for a in par.parents if getattr(a, "name", None)):
            continue
        out.append(s)
    return out


def worth(s):
    t = re.sub(r"<[^>]+>", "", s).strip()
    if not re.search(r"[A-Za-z]{2,}", t):
        return False
    if re.fullmatch(r"[\w.+-]+@[\w.-]+|https?://\S+|[\w.-]+\.(org|com|io|edu)(/\S*)?", t):
        return False
    return True


def collect(soup):
    strings = []
    if soup.title and soup.title.string:
        strings.append(soup.title.string.strip())
    for m in soup.find_all("meta"):
        if (m.get("name") in META or m.get("property") in META) and m.get("content"):
            strings.append(m["content"])
    for el in units(soup):
        strings.append(el.decode_contents().strip())
    for s in bare_texts(soup):
        strings.append(str(s).strip())
    for el in (soup.body or soup).find_all(True):
        if el.find_parent(SKIP):
            continue
        for a in ATTRS:
            if el.get(a):
                strings.append(el[a])
    seen, res = set(), []
    for s in strings:
        if s and s not in seen and worth(s):
            seen.add(s)
            res.append(s)
    return res


def extract():
    os.makedirs(os.path.join(ROOT, "_i18n/src"), exist_ok=True)
    for p in PAGES:
        res = collect(BeautifulSoup(strip_i18n(open(os.path.join(ROOT, p), encoding="utf-8").read()), "html.parser"))
        with open(os.path.join(ROOT, "_i18n/src", key(p) + ".json"), "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        print(p, len(res), "strings")


# ---------- switcher ----------
SWITCH_CSS = """<style id="lang-switch-css">
.lang-switch{display:inline-flex;align-items:center;gap:2px;border:1px solid #dde1e8;border-radius:999px;padding:2px;background:#fff;font:600 .72rem 'Inter',system-ui,sans-serif;line-height:1}
.lang-switch a{display:block;padding:.38rem .6rem;border-radius:999px;color:#4a5f7e;text-decoration:none;letter-spacing:.02em}
.lang-switch a:hover{color:#032454;background:#f3f5f8}
.lang-switch a[aria-current="true"]{background:#032454;color:#fff}
.lang-slot{display:flex;align-items:center;gap:1rem}
@media(max-width:640px){.lang-switch a{padding:.36rem .5rem}}
</style>"""


def page_url(lang, page):
    pre = "" if lang == "en" else lang + "/"
    path = pre + page
    return SITE + "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)


def rel_link(from_lang, page, to_lang):
    depth = page.count("/") + (0 if from_lang == "en" else 1)
    up = "../" * depth
    pre = "" if to_lang == "en" else to_lang + "/"
    return up + pre + page


def switcher_html(lang, page):
    a = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        a.append(f'<a href="{rel_link(lang, page, l)}" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}" title="{LANGS[l]}"{cur} data-lang="{l}">{SHORT[l]}</a>')
    script = ("<script>document.querySelectorAll('.lang-switch a').forEach(function(a){a.addEventListener('click',function(){"
              "try{localStorage.setItem('site-lang',a.dataset.lang)}catch(e){}})});</script>")
    return f'<div class="lang-switch" role="navigation" aria-label="Language">{"".join(a)}</div>', script


MARK = re.compile(r"<!--i18n:(\w+)-->.*?<!--/i18n:\1-->\n?", re.S)


def strip_i18n(html):
    return MARK.sub("", html)


def inject(html, lang, page):
    sw, script = switcher_html(lang, page)
    links = "".join(f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{page_url(l, page)}">' for l in LANGS)
    links += f'<link rel="alternate" hreflang="x-default" href="{page_url("en", page)}">'
    head = f"<!--i18n:head-->{SWITCH_CSS}{links}<!--/i18n:head-->\n"
    html = re.sub(r"</head>", lambda m: head + "</head>", html, count=1)
    if re.search(r"<button[^>]*nav-toggle", html):
        html = re.sub(r"(<button[^>]*nav-toggle)", lambda m: f"<!--i18n:sw-->{sw}<!--/i18n:sw-->\n" + m.group(1), html, count=1)
    else:
        html, n = re.subn(r'(<a[^>]*class="(?:nav-)?back"[^>]*>.*?</a>)', lambda m: f'<!--i18n:sw0--><div class="lang-slot">{sw}<!--/i18n:sw0-->{m.group(1)}<!--i18n:sw1--></div><!--/i18n:sw1-->', html, count=1, flags=re.S)
        assert n == 1, page
    html = re.sub(r"</body>", lambda m: f"<!--i18n:js-->{script}<!--/i18n:js-->\n</body>", html, count=1)
    return html


def is_translated_target(url, page):
    u = url.split("#")[0].split("?")[0]
    if page == "index.html":
        return u.startswith("blog/") and u.endswith(".html")
    return u in ("../index.html",) or (u.endswith(".html") and "/" not in u)


def rewrite_paths(soup, page):
    for el in soup.find_all(True):
        for attr in ("href", "src", "poster", "data-src"):
            v = el.get(attr)
            if not v or re.match(r"^(https?:|mailto:|tel:|#|data:|/|javascript:)", v):
                continue
            if attr == "href" and is_translated_target(v, page):
                continue
            el[attr] = "../" + v


def translate_soup(soup, tr):
    def T(s):
        return tr.get(s.strip(), s) if s else s
    if soup.title and soup.title.string:
        soup.title.string = T(soup.title.string)
    for m in soup.find_all("meta"):
        if (m.get("name") in META or m.get("property") in META) and m.get("content"):
            m["content"] = T(m["content"])
    for el in units(soup):
        src = el.decode_contents().strip()
        if src in tr and tr[src] != src:
            el.clear()
            frag = BeautifulSoup(tr[src], "html.parser")
            for c in list(frag.contents):
                el.append(c)
    for s in bare_texts(soup):
        k = str(s).strip()
        if k in tr and tr[k] != k:
            s.replace_with(str(s).replace(k, tr[k]))
    for el in (soup.body or soup).find_all(True):
        if el.find_parent(SKIP):
            continue
        for a in ATTRS:
            if el.get(a) and el[a] in tr:
                el[a] = tr[el[a]]


def build():
    missing_total = 0
    for page in PAGES:
        src_path = os.path.join(ROOT, page)
        raw = strip_i18n(open(src_path, encoding="utf-8").read())
        en_html = inject(raw, "en", page)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(en_html)
        for lang in ("id", "zh"):
            tpath = os.path.join(ROOT, "_i18n", lang, key(page) + ".json")
            if not os.path.exists(tpath):
                print("no translation:", lang, page)
                continue
            tr = json.load(open(tpath, encoding="utf-8"))
            if isinstance(tr, list):  # same order as _i18n/src/<key>.json
                src = json.load(open(os.path.join(ROOT, "_i18n/src", key(page) + ".json"), encoding="utf-8"))
                assert len(src) == len(tr), (lang, page, len(src), len(tr))
                tr = {s: (s if v == "=" else v) for s, v in zip(src, tr)}  # "=" keeps the English text
            jpath = os.path.join(ROOT, "_i18n", lang, key(page) + ".raw.json")
            js = json.load(open(jpath, encoding="utf-8")) if os.path.exists(jpath) else {}
            soup = BeautifulSoup(raw, "html.parser")
            miss = [s for s in collect(soup) if s not in tr]
            missing_total += len(miss)
            for s in miss[:5]:
                print("  MISSING", lang, page, s[:70])
            translate_soup(soup, tr)
            soup.html["lang"] = HTML_LANG[lang]
            rewrite_paths(soup, page)
            can = soup.find("link", rel="canonical")
            if can:
                can["href"] = page_url(lang, page)
            ogu = soup.find("meta", property="og:url")
            if ogu:
                ogu["content"] = page_url(lang, page)
            out = os.path.join(ROOT, lang, page)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                html = str(soup)
                for a, b in js.items():  # literal replacements in scripts/CSS
                    assert a in html, (lang, page, a)
                    html = html.replace(a, b)
                f.write(inject(html, lang, page))
            print("built", lang, page, "missing", len(miss))
    print("total missing", missing_total)


if __name__ == "__main__":
    {"extract": extract, "build": build}[sys.argv[1]]()
