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


def main():
    projects = load("projects")
    blocks = {
        "publications": publications(),
        "projects-research": project_list(projects["research"]),
        "projects-community": project_list(projects["community"]),
        "experience": experience(),
        "writing": writing(),
        "talks": talks(),
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
