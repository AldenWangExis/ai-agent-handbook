#!/usr/bin/env python3
"""Last-mile fixes that only the PDF edition needs.

    pdf-source.py <in.md> <out.md>
"""
import pathlib
import re
import sys

t = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")

# LaTeX builds its own table of contents, so drop the hand-written one and place
# \tableofcontents after the introduction, which itself stays out of the listing.
t = re.sub(r'\n# 目录 \{#toc\}\n.*?(?=\n# 前言 \{)', '\n', t, flags=re.S)
t = t.replace('# 关于本合订本 {#sec-000}',
              '# 关于本合订本 {#sec-000 .unnumbered .unlisted}')
t = t.replace('\n# 前言 {',
              '\n```{=latex}\n\\clearpage\n\\tableofcontents\n\\clearpage\n```\n\n# 前言 {', 1)

# a handful of decorative glyphs are missing from the PDF fonts
subs = {chr(0x2460 + i): f'({i + 1})' for i in range(10)}
subs.update({'🌰': '（举例）', '➊': '(1)', '➋': '(2)', '➌': '(3)', 'ꔷ': '·',
             'μ': 'µ', '₊': '+', '₋': '-', 'ₜ': 't', 'ₙ': 'n', 'ᵢ': 'i'})
subs.update(dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉', '01234567890123456789')))
for a, b in subs.items():
    t = t.replace(a, b)


def width(s):
    """Rough print width: CJK and full-width punctuation take two columns."""
    return sum(2 if ord(c) > 0x2e7f else 1 for c in s)


def wrap_line(line, limit=86):
    """Soft-wrap one code line, preferring a break at whitespace."""
    indent = re.match(r'[ \t]*', line).group(0) + '  '
    out = []
    while width(line) > limit:
        cut, w = 0, 0
        for i, c in enumerate(line):
            w += 2 if ord(c) > 0x2e7f else 1
            if w > limit:
                break
            cut = i + 1
        brk = max(line.rfind(' ', len(indent), cut), line.rfind('\t', len(indent), cut))
        if brk < cut // 2:
            brk = cut
        out.append(line[:brk].rstrip())
        line = indent + line[brk:].lstrip()
    out.append(line)
    return out


def wrap_code_blocks(text):
    """xelatex cannot break long code lines here, so wrap them beforehand."""
    out, fence = [], None
    for line in text.split('\n'):
        m = re.match(r'[ \t]*(`{3,}|~{3,})', line)
        if m:
            fence = None if fence and m.group(1)[0] == fence else (fence or m.group(1)[0])
            out.append(line)
        elif fence and width(line) > 86:
            out.extend(wrap_line(line))
        else:
            out.append(line)
    return '\n'.join(out)


t = wrap_code_blocks(t)

pathlib.Path(sys.argv[2]).write_text(t, encoding="utf-8")
