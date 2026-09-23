#!/usr/bin/env python3
"""Assemble aliyun/ai-agent-handbook into a single navigable Markdown book."""
import re, pathlib, datetime, sys

ROOT = pathlib.Path(__file__).resolve()
REPO = pathlib.Path(sys.argv[1]).resolve()

def nat(p):
    m = re.search(r'第\s*(\d+)\s*章', p.name)
    return (int(m.group(1)) if m else 999, p.name)

def chapters(d, pattern=r'第\s*\d+\s*章'):
    return sorted([p for p in (REPO/d).glob('*.md') if re.search(pattern, p.name)], key=nat)

def cases(d):
    return sorted((REPO/d).glob('*.md'), key=lambda p: p.name)

# ---------- book structure: (level, explicit_title or None -> use file H1, file or None)
BOOK = []
def add(level, title, file=None):
    BOOK.append({'level': level, 'title': title, 'file': file})

add(1, '前言', '00-preface/00-preface.md')
add(1, '2026 Agent 开发者调研报告', '2026-agent-survey-report.md')

PARTS = [
    ('架构篇', '01-architecture', '01-architecture/README.md'),
    ('构建篇', '02-build', '02-build/README.md'),
    ('运行篇', '03-run', '03-run/README.md'),
    ('治理篇', '04-governance', '04-governance/治理篇导读.md'),
    ('调优篇', '05-optimization', '05-optimization/调优篇导读.md'),
]
for part, d, intro in PARTS:
    add(1, part, None)
    add(2, None, intro)
    for f in chapters(d):
        add(2, None, str(f.relative_to(REPO)))

# 实践篇
add(1, '实践篇', None)
add(2, None, '06-case-study/README.md')
CASE_DIRS = [
    ('第 25 章　研发效能', '06-case-study/第25章 研发效能'),
    ('第 26 章　设计工程', '06-case-study/第26章 设计工程'),
    ('第 27 章　运维、安全与企业 IT', '06-case-study/第27章 运维、安全与企业IT'),
    ('第 28 章　客户、销售与运营', '06-case-study/第28章 客户、销售与运营'),
]
for title, d in CASE_DIRS:
    add(2, title, None)
    for f in cases(d):
        add(3, None, str(f.relative_to(REPO)))
for f in chapters('06-case-study'):
    add(2, None, str(f.relative_to(REPO)))

add(1, '总结与展望篇', None)
for f in chapters('07-conclusion'):
    add(2, None, str(f.relative_to(REPO)))

add(1, '附录：关于本书', None)

# ---------- helpers
def clean(text):
    # author annotations written as LaTeX \color spans -> plain text
    text = re.sub(r'\$\\color\{[^}]*\}\{([^}]*)\}\$', r'（\1）', text)

    # a few citation markers in the source link to an empty anchor; keep the
    # marker, drop the dead link
    text = re.sub(r'\[([^\]]{1,20})\]\(#\)', r'[\1]', text)

    # the source was exported from a WYSIWYG editor, which escaped _ [ ] * inside
    # LaTeX spans; undo that so the formulas actually parse
    def unescape_math(m):
        s = m.group(0)
        if not re.search(r'\\(math|frac|sum|pi|theta|tau|bar|left|right|alpha|beta|lambda|Delta)', s):
            return s
        return re.sub(r'\\([_\[\]*])', r'\1', s)
    text = re.sub(r'\$\$?[^$\n]{1,400}?\$\$?', unescape_math, text)
    return text

def norm_title(s):
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'^第\s*(\d+)\s*章\s*', lambda m: f'第 {m.group(1)} 章　', s)
    return s

def load(relpath, level):
    """Return (title, shifted_body) for a source file placed at heading `level`."""
    p = REPO / relpath
    raw = clean(p.read_text(encoding='utf-8'))
    lines = raw.splitlines()
    # locate first H1 as the title
    ti = next((i for i, l in enumerate(lines) if re.match(r'^#\s+\S', l)), None)
    if ti is None:
        title, body = p.stem.strip(), lines
    else:
        title = norm_title(re.sub(r'^#\s+', '', lines[ti]))
        body = lines[ti+1:]
    in_fence = False
    has_h1 = False
    for l in body:
        if re.match(r'^\s*(```|~~~)', l):
            in_fence = not in_fence
        elif not in_fence and re.match(r'^#\s+\S', l):
            has_h1 = True
            break
    shift = level if has_h1 else level - 1
    out, in_fence = [], False
    for l in body:
        if re.match(r'^\s*(```|~~~)', l):
            in_fence = not in_fence
            out.append(l); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', l) if not in_fence else None
        if m:
            new = min(6, len(m.group(1)) + shift)
            out.append('#' * new + ' ' + m.group(2).rstrip())
        else:
            out.append(l)
    # rewrite image/link paths to be relative to repo root
    depth_prefix = ''
    def fix(m):
        pre, target, rest = m.group(1), m.group(2), m.group(3)
        if re.match(r'^(https?:|#|mailto:|data:)', target):
            return m.group(0)
        t = (p.parent / target).resolve()
        try:
            t = t.relative_to(REPO)
        except ValueError:
            return m.group(0)
        return f'{pre}({t.as_posix()}{rest})'
    text = '\n'.join(out)
    text = re.sub(r'(!?\[[^\]]*\])\(<?([^)<>"\s]+)>?([^)]*)\)', fix, text)
    return title, text.strip('\n')

def readme_appendix():
    raw = clean((REPO/'README.md').read_text(encoding='utf-8'))
    lines = raw.splitlines()
    keep, skip = [], False
    for l in lines:
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if m:
            h = m.group(2).strip()
            # drop the repo-navigation tables: the generated TOC replaces them
            skip = h in ('目录结构', '章节导航', '实践案例导航')
            if h in ('README', 'AI Agent HandBook'):
                skip = True
                continue
            if not skip:
                keep.append('#' * min(6, len(m.group(1)) + 1) + ' ' + h)
            continue
        if not skip:
            keep.append(l)
    text = '\n'.join(keep)
    # relative links in prose -> absolute GitHub URLs
    text = re.sub(r'\]\(<?\./([^)<>]+)>?\)',
                  lambda m: '](https://github.com/aliyun/ai-agent-handbook/blob/main/' +
                            m.group(1).replace(' ', '%20') + ')', text)
    return text.strip('\n')

# ---------- assemble
for i, e in enumerate(BOOK):
    e['id'] = f'sec-{i+1:03d}'
    if e['file']:
        t, b = load(e['file'], e['level'])
        e['body'] = b
        if not e['title']:
            e['title'] = t
    else:
        e['body'] = ''
BOOK[-1]['body'] = readme_appendix()

today = datetime.date.today().isoformat()
UPSTREAM = 'https://github.com/aliyun/ai-agent-handbook'
FORK = 'https://github.com/AldenWangExis/ai-agent-handbook'
BLOG = 'https://aldenwangexis.github.io/posts/ai-agent-handbook-offline-bundle/'

head = f"""---
title: AI Agent HandBook
subtitle: 企业级 Agent 的架构、构建、运行、治理与调优
author: 阿里云 · AI Agent HandBook 社区
lang: zh-CN
date: {today}
---

# 关于本合订本 {{#sec-000}}

《AI Agent HandBook》是阿里云与一线实践团队共同编写的开源白皮书。它沿着 Agent 的生命周期展开：先判断什么样的任务值得交给 Agent、该选多深的架构，再讲 Harness 如何组织任务、上下文与工具调用，Agent 在生产环境里怎样运行、被观测和约束，以及上线之后如何用轨迹数据、黄金数据集和 Badcase 回归把它持续调好。书的后半部分收录了研发效能、设计工程、智能运维、客户与运营等场景的一线案例。

原项目一章一个文件，在 GitHub 上挑着看很顺手；想从头到尾读一遍，或者丢进阅读器、整本发给同事，就有点费劲。这个仓库做的事情很简单：把三十章按原顺序接成一份完整文档，插图一张没少，目录点得动，另外出了 EPUB 和 PDF 两个适合离线看的版本。原项目 README 里那几张分章导航表在这里用不上了，下面的目录就是它；README 剩下的内容放在文末的「附录：关于本书」。

- 原项目：<{UPSTREAM}>
- 本仓库：<{FORK}>
- 在线阅读（单页 Markdown）：<{BLOG}>
- 创建日期：{today}
- 许可：原项目采用 Apache License 2.0，本合订本沿用同一许可；转载或再分发时请保留许可声明与原作者署名。

# 目录 {{#toc}}

"""

toc = []
for e in BOOK:
    indent = '  ' * (e['level'] - 1)
    toc.append(f'{indent}- [{e["title"]}](#{e["id"]})')

def render(anchor_style):
    # anchor_style: 'attr'  -> pandoc header attributes (used for the EPUB build)
    #               'html'  -> explicit <a id> anchors (renders cleanly on GitHub)
    h = head if anchor_style == 'attr' else head.replace(' {#sec-000}', '').replace(' {#toc}', '')
    if anchor_style == 'html':
        h = h.replace('# 关于本合订本', '<a id="sec-000"></a>\n\n# 关于本合订本').replace('# 目录', '<a id="toc"></a>\n\n# 目录')
    out = [h + '\n'.join(toc) + '\n']
    for e in BOOK:
        hashes = '#' * e['level']
        if anchor_style == 'attr':
            out.append(f'\n\n{hashes} {e["title"]} {{#{e["id"]}}}\n')
        else:
            out.append(f'\n\n<a id="{e["id"]}"></a>\n\n{hashes} {e["title"]}\n')
        if e['body']:
            out.append(e['body'] + '\n')
    return ''.join(out)

out = REPO / 'AI-Agent-Handbook-合订本.md'
out.write_text(render('html'), encoding='utf-8')
src = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else REPO / '.book-pandoc.md'
src.write_text(render('attr'), encoding='utf-8')
print(f'wrote {out}  ({out.stat().st_size/1024:.0f} KB, {len(BOOK)} entries)')
print(f'wrote {src} (pandoc source)')
