#!/usr/bin/env python3
"""Turn the assembled Markdown into a Chirpy post.

    publish-blog.py <book.md> <blog-repo-root>

Writes _posts/<date>-ai-agent-handbook-offline-bundle.md. Images are left in the
GitHub repository and referenced by their raw URLs, so the blog repo stays small.
"""
import datetime
import pathlib
import re
import sys

SLUG = "ai-agent-handbook-offline-bundle"
RAW = "https://raw.githubusercontent.com/AldenWangExis/ai-agent-handbook/main/"
TITLE = "AI Agent HandBook 合订本：阿里云开源白皮书的单文件离线版"
DESCRIPTION = ("把阿里云开源的《AI Agent HandBook》三十章合并成一份可离线阅读的完整文档，"
               "保留原书顺序、插图与可跳转目录，另提供 EPUB 与 PDF。")

book, blog = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = book.read_text(encoding="utf-8")

# drop the pandoc YAML block; Chirpy supplies its own front matter
text = re.sub(r'\A---\n.*?\n---\n+', '', text, flags=re.S)

# the anchors are plain <a id> tags for GitHub's sake; kramdown can put the same
# ids on the headings themselves, which keeps html-proofer happy
text = re.sub(r'<a id="([^"]+)"></a>\n\n(#{1,6} .+)', r'\2 {#\1}', text)

# Chirpy posts start their headings at h2, so push everything down one level
text = re.sub(r'^(#{1,6})(?= )', lambda m: '#' * min(6, len(m.group(1)) + 1), text, flags=re.M)

# images live in the GitHub repo, not in the blog
text = re.sub(r'\((assets/imgs/[^)\s]+)', lambda m: '(' + RAW + m.group(1), text)

date = datetime.date.today()
front = f"""---
title: "{TITLE}"
description: {DESCRIPTION}
author: Alden
date: {date} 09:00:00 +0800
categories: [LLM Engineering, Agent]
tags: [Agent, Architecture, Handbook, Alibaba Cloud, Reading Notes]
pin: false
mermaid: true
comments: true
---

> 本文是开源项目 [aliyun/ai-agent-handbook](https://github.com/aliyun/ai-agent-handbook) 的全书合订版，按原书顺序合并，内容与许可（Apache License 2.0）均归原作者所有。EPUB 与 PDF 版本见 [AldenWangExis/ai-agent-handbook](https://github.com/AldenWangExis/ai-agent-handbook)。
{{: .prompt-info }}

"""

# the book quotes prompt templates containing {{...}}, which Liquid would try to
# evaluate; keep the whole body literal
if '{{' in text or '{%' in text:
    text = "{% raw %}\n" + text.strip('\n') + "\n{% endraw %}\n"

out = blog / "_posts" / f"{date}-{SLUG}.md"
out.write_text(front + text.lstrip('\n'), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")
