#!/usr/bin/env python3
"""Fill the data-driven lists in index.html from data/*.json.

Each list sits between <!--data:NAME--> and <!--/data:NAME--> in index.html.
Edit the JSON, then run:

  python3 _build/render.py        # rewrite the lists in index.html
  python3 _i18n/i18n.py extract   # see which strings are new
  python3 _i18n/i18n.py build     # regenerate /id and /zh

Folders starting with "_" are not published by GitHub Pages (Jekyll).
"""
import json, os, re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load(name):
    with open(os.path.join(ROOT, "data", name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def t(s):
    return escape(s, quote=False)


def a(s):
    return escape(s, quote=True)


def link(url, label, cls):
    ext = url.startswith("http")
    target = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{a(url)}"{target}>{t(label)}</a>'


def entry(title_html, meta, aside):
    meta_html = f'\n        <div class="entry__meta">{meta}</div>' if meta else ""
    aside_html = f'\n      <div class="entry__aside">{t(aside)}</div>' if aside else ""
    return (f'    <li class="entry">\n      <div class="entry__body">\n        {title_html}{meta_html}\n'
            f'      </div>{aside_html}\n    </li>')


def entries(items, cls="entries"):
    return f'\n  <ol class="{cls}">\n' + "\n".join(items) + '\n  </ol>\n  '


def publications():
    items = []
    for p in sorted(load("publications"), key=lambda p: -p["year"]):
        badge = " · ".join(x for x in (p.get("quartile"), p.get("index")) if x)
        meta = "".join(f"<span>{t(x)}</span>" for x in (p["venue"], p["authors"]) if x)
        if badge:
            meta = f'<span class="badge">{t(badge)}</span>' + meta
        title = link(p["url"], p["title"], "entry__title") if p.get("url") else f'<div class="entry__title">{t(p["title"])}</div>'
        items.append(entry(title, meta, str(p["year"])))
    return entries(items)


def project_list(rows):
    items = []
    for p in sorted(rows, key=lambda p: -p["year"]):
        lead = "badge badge--lead" if p["role"] == "Principal Investigator" else "badge"
        meta = f'<span class="{lead}">{t(p["role"])}</span><span>{t(p["scheme"])}</span>'
        aside = " · ".join(x for x in (str(p["year"]), p.get("funding")) if x)
        items.append(entry(f'<div class="entry__title">{t(p["title"])}</div>', meta, aside))
    return entries(items)


def experience():
    rows = []
    for e in load("experience"):
        rows.append(f'    <li class="timeline__item">\n      <div class="timeline__period">{t(e["period"])}</div>\n'
                    f'      <div>\n        <h4 class="timeline__role">{t(e["role"])}</h4>\n'
                    f'        <div class="timeline__place">{t(e["place"])}</div>\n'
                    f'        <p class="timeline__desc">{t(e["desc"])}</p>\n      </div>\n    </li>')
    return '\n  <ol class="timeline">\n' + "\n".join(rows) + '\n  </ol>\n  '


def month(d):
    if not d:
        return "Coming soon"
    y, m = d.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def writing():
    items = []
    for w in load("writing"):
        title = link(w["url"], w["title"], "entry__title") if w.get("url") else f'<div class="entry__title entry__title--soon">{t(w["title"])}</div>'
        items.append(entry(title, "", month(w["date"])))
    return entries(items, "entries entries--compact")


def talks():
    items = []
    for k in sorted(load("talks"), key=lambda k: -k["year"]):
        meta = f'<span class="badge">{t(k["format"])}</span><span>{t(k["event"])}</span>'
        items.append(entry(link(k["url"], k["title"], "entry__title"), meta, str(k["year"])))
    return entries(items)


PLAY = ('<svg viewBox="0 0 68 48" aria-hidden="true"><path d="M66.5 7.7A8.5 8.5 0 0 0 60.5 1.7C55.2.3 34 .3 34 .3s-21.2 0-26.5 1.4a8.5 8.5 0 0 0-6 6C.1 13 .1 24 .1 24s0 11 1.4 16.3a8.5 8.5 0 0 0 6 6C12.8 47.7 34 47.7 34 47.7s21.2 0 26.5-1.4a8.5 8.5 0 0 0 6-6C67.9 35 67.9 24 67.9 24s0-11-1.4-16.3z"/>'
        '<path d="M45 24 27 14v20z" fill="#fff"/></svg>')


def episode(e):
    watch = f'https://www.youtube.com/watch?v={e["youtube"]}'
    thumb = (f'<a class="episode__thumb" href="{a(watch)}" target="_blank" rel="noopener" data-yt="{a(e["youtube"])}" aria-label="{a("Play video: " + e["title"])}">'
             f'<img src="https://i.ytimg.com/vi/{a(e["youtube"])}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">'
             f'<span class="episode__play">{PLAY}</span><span class="episode__time">{t(e["duration"])}</span></a>')
    related = ""
    if e.get("related"):
        r = e["related"]
        related = f'\n          <p class="episode__related">Companion article: <a href="{a(r["url"])}">{t(r["title"])}</a></p>'
    return (f'      <li class="episode">\n        {thumb}\n        <div class="episode__body">\n'
            f'          <div class="entry__meta"><span class="badge">Episode {e["episode"]}</span><span>{month(e["date"])}</span></div>\n'
            f'          {link(watch, e["title"], "entry__title")}\n'
            f'          <p class="episode__summary">{t(e["summary"])}</p>{related}\n'
            f'        </div>\n      </li>')


def lectures():
    out = []
    for s in load("lectures"):
        eps = "\n".join(episode(e) for e in sorted(s["episodes"], key=lambda e: e["episode"]))
        out.append(f'  <div class="series">\n    <h3 class="series__title">{t(s["series"])}</h3>\n'
                   f'    <p class="series__summary">{t(s["summary"])}</p>\n    <ol class="episodes">\n{eps}\n    </ol>\n  </div>')
    return "\n" + "\n".join(out) + "\n  "


def main():
    projects = load("projects")
    blocks = {
        "publications": publications(),
        "projects-research": project_list(projects["research"]),
        "projects-community": project_list(projects["community"]),
        "experience": experience(),
        "writing": writing(),
        "talks": talks(),
        "lectures": lectures(),
    }
    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    for name, body in blocks.items():
        html, n = re.subn(rf"(<!--data:{name}-->).*?(<!--/data:{name}-->)",
                          lambda m: m.group(1) + body + m.group(2), html, flags=re.S)
        assert n == 1, f"marker data:{name} not found in index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("rendered", ", ".join(blocks))


if __name__ == "__main__":
    main()
