#!/usr/bin/env python3
"""
Generate one Markdown file per topic found in docs/install.txt.

Usage: python3 scripts/generate_install_topics.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL_TXT = ROOT / 'docs' / 'install.txt'
OUT_DIR = ROOT / 'docs' / 'documentation' / 'install'
DOCS_ORDER = ROOT / 'docs' / 'documentation' / '_order.yaml'


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = s.replace('&', 'and')
    s = re.sub(r"[^a-z0-9]+", '-', s)
    s = re.sub(r"-+", '-', s)
    s = s.strip('-')
    if not s:
        s = 'untitled'
    return s


def parse_titles(lines):
    titles = []
    seen = set()
    for ln in lines:
        if '──' in ln:
            # take text after the last em-dash marker
            parts = ln.split('──')
            title = parts[-1].strip()
            if title and title not in seen:
                titles.append(title)
                seen.add(title)
    return titles


def make_md(title, path: Path):
    content = f'''---
title: {title}
excerpt: "TODO: Add excerpt for {title}"
hidden: false
---
# {title}

TODO: Add content for "{title}".

'''
    path.write_text(content, encoding='utf-8')


def main():
    if not INSTALL_TXT.exists():
        print(f"{INSTALL_TXT} not found")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with INSTALL_TXT.open('r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]

    titles = parse_titles(lines)
    print(f'Found {len(titles)} topics')

    order_entries = []
    for t in titles:
        slug = slugify(t)
        filename = OUT_DIR / f"{slug}.md"
        if not filename.exists():
            make_md(t, filename)
        order_entries.append(slug)

    # Update docs/documentation/_order.yaml to include install
    if DOCS_ORDER.exists():
        txt = DOCS_ORDER.read_text(encoding='utf-8')
        lines = [l.rstrip('\n') for l in txt.splitlines()]
        if 'install' not in ''.join(lines):
            lines.append('\n- install')
            DOCS_ORDER.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            print('Updated docs/documentation/_order.yaml to include install')
    else:
        DOCS_ORDER.write_text('- install\n', encoding='utf-8')
        print('Created docs/documentation/_order.yaml with install')

    # Write an _order.yaml inside install folder listing all slugs
    order_path = OUT_DIR / '_order.yaml'
    with order_path.open('w', encoding='utf-8') as f:
        for s in order_entries:
            f.write(f"- {s}\n")

    print(f'Wrote {len(order_entries)} markdown files to {OUT_DIR}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
