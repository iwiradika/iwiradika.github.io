# Dr. I Nyoman Indhi Wiradika - Personal Website

Professional academic portfolio and blog of Dr. I Nyoman Indhi Wiradika, focusing on Educational Assessment, Psychometrics, and Informatics Education.

## 🚀 Overview

This website serves as a digital portfolio for my research, publications, and academic contributions. It features a modern, responsive design and includes a blog section where I share insights on advanced educational measurement techniques.

### Key Features
- **Publications Archive:** Chronological list of research papers with Scopus Q-indexing and SINTA integration.
- **Interactive Blog:** In-depth articles on psychometrics, such as Cognitive Diagnostic Models (CDM).
- **Data Visualizations:** Interactive SVG-based charts demonstrating student competency trajectories and model response curves.
- **Dynamic Styling:** Built-in "Tweaks" system for personalizing colors and layouts.

## 🛠️ Tech Stack
- **Frontend:** Vanilla HTML5, CSS3, and JavaScript.
- **Visualizations:** Custom SVG animations and Intersections Observer API for scroll-reveal effects.
- **Hosting:** GitHub Pages.

## 📚 Blog Highlights
The featured article, **"Understanding Cognitive Diagnostic Models,"** explores how the G-DINA model provides a more granular diagnosis of student mastery compared to Classical Test Theory. It includes visualizations of:
- **Q-matrix mapping:** Connecting test items to cognitive attributes.
- **G-DINA response curves:** Probability functions for attribute mastery.
- **Developmental Trajectories:** Longitudinal analysis of student progress.

## 📬 Contact
- **Email:** iwiradika@undiksha.ac.id
- **Affiliation:** Universitas Pendidikan Ganesha
- **Research Profiles:** [SINTA](https://sinta.kemdiktisaintek.go.id/authors/profile/6806385) | [Google Scholar](https://scholar.google.com/citations?user=54Ggga0AAAAJ&hl=en)

---
© 2026 Dr. I Nyoman Indhi Wiradika

## 🌐 Languages

The site is available in English (default, site root), Bahasa Indonesia (`/id/`) and Chinese (`/zh/`). Every page has an EN · ID · 中文 switcher and `hreflang` links.

English pages are the source. Translations live in `_i18n/<lang>/<page>.json` (same order as `_i18n/src/<page>.json`; `"="` keeps the English text). Literal replacements inside scripts or CSS go in `<page>.raw.json`.

```bash
python3 _i18n/i18n.py extract   # refresh the list of strings after editing an English page
python3 _i18n/i18n.py build     # add the switcher to English pages and regenerate /id and /zh
```

After `extract`, add the new or changed strings to both translation files before running `build`.
