#!/usr/bin/env python3
"""Render ```mermaid blocks to images and (optionally) rasterize SVG figures.

Uses headless Chrome as the renderer: mermaid is loaded from the jsDelivr CDN,
so this step needs network access. Without it the mermaid blocks simply stay
as code, which is what the Markdown edition ships anyway.

    render-diagrams.py <in.md> <out.md> <resource-dir> <work-dir> svg|png
"""
import base64, hashlib, html, json, pathlib, re, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11/+esm"
FENCE = re.compile(r'^```mermaid[ \t]*\n(.*?)^```[ \t]*$', re.S | re.M)


def chrome(args, timeout=300):
    return subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                           *args], capture_output=True, timeout=timeout)


def render_mermaid(blocks, work):
    """blocks: list of mermaid source strings -> list of svg file paths."""
    out = work / "diagrams"
    out.mkdir(parents=True, exist_ok=True)
    todo = [(i, b) for i, b in enumerate(blocks)
            if not (out / f"mmd-{hashlib.sha1(b.encode()).hexdigest()[:10]}.svg").exists()]
    names = [out / f"mmd-{hashlib.sha1(b.encode()).hexdigest()[:10]}.svg" for b in blocks]
    if todo:
        page = work / "mermaid-render.html"
        page.write_text(
            '<!doctype html><meta charset="utf-8"><body>\n'
            + "".join(f'<div class="slot" id="slot{i}"></div>\n' for i, _ in todo)
            + '<script type="module">\n'
            + f'import mermaid from "{MERMAID}";\n'
            + 'mermaid.initialize({startOnLoad:false, theme:"neutral", '
              'flowchart:{htmlLabels:false, useMaxWidth:false}, '
              'sequence:{useMaxWidth:false}, gantt:{useMaxWidth:false}, '
              'fontFamily:"PingFang SC, Hiragino Sans GB, sans-serif"});\n'
            + f'const defs = {json.dumps([b for _, b in todo])};\n'
            + f'const ids = {json.dumps([i for i, _ in todo])};\n'
            + 'for (let k = 0; k < defs.length; k++) {\n'
              '  try { const { svg } = await mermaid.render("m" + k, defs[k]);\n'
              '        document.getElementById("slot" + ids[k]).innerHTML = svg; }\n'
              '  catch (e) { document.getElementById("slot" + ids[k]).textContent = "MERMAID-ERROR " + e.message; }\n'
              '}\n</script>', encoding="utf-8")
        dom = chrome(["--virtual-time-budget=60000", "--dump-dom",
                      page.resolve().as_uri()]).stdout.decode("utf-8", "replace")
        for i, src in todo:
            m = re.search(rf'<div class="slot" id="slot{i}">(.*?)</div>\s*(?=<div class="slot"|<script)',
                          dom, re.S)
            body = m.group(1) if m else ""
            if not body.startswith("<svg"):
                print(f"  ! mermaid block {i} did not render: {html.unescape(body)[:80]}", file=sys.stderr)
                continue
            names[i].write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body, encoding="utf-8")
    return names


def rasterize(svg_path, png_path, scale=1.5):
    if png_path.exists() and png_path.stat().st_mtime >= svg_path.stat().st_mtime:
        return png_path
    svg = svg_path.read_text(encoding="utf-8", errors="replace")
    svg = re.sub(r'^<\?xml[^>]*\?>\s*', '', svg)
    vb = re.search(r'viewBox="([-\d.eE]+)\s+([-\d.eE]+)\s+([\d.eE]+)\s+([\d.eE]+)"', svg)
    if vb:
        w, h = float(vb.group(3)), float(vb.group(4))
    else:
        w = float(re.search(r'width="(\d+)', svg).group(1))
        h = float(re.search(r'height="(\d+)', svg).group(1))
    wrap = png_path.with_suffix(".html")
    wrap.write_text(
        f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;padding:0;'
        f'background:#fff}}svg{{width:{w}px;height:{h}px;display:block}}</style>{svg}',
        encoding="utf-8")
    chrome([f"--force-device-scale-factor={scale}",
            f"--window-size={int(w)},{int(h)}",
            f"--screenshot={png_path}", "--virtual-time-budget=8000",
            wrap.resolve().as_uri()])
    wrap.unlink(missing_ok=True)
    return png_path


def main():
    src, dst, resdir, work, mode = sys.argv[1:6]
    src, dst = pathlib.Path(src), pathlib.Path(dst)
    resdir, work = pathlib.Path(resdir), pathlib.Path(work)
    text = src.read_text(encoding="utf-8")

    blocks = [m.group(1) for m in FENCE.finditer(text)]
    svgs = render_mermaid(blocks, work) if blocks else []

    # mermaid fences -> image references, dropped into the resource tree
    def sub(m, it=iter(range(len(blocks)))):
        i = next(it)
        svg = svgs[i]
        if not svg.exists():
            return m.group(0)
        if mode == "png":
            png = svg.with_suffix(".png")
            rasterize(svg, png)
            target = png
        else:
            target = svg
        rel = f"diagrams/{target.name}"
        (resdir / "diagrams").mkdir(parents=True, exist_ok=True)
        (resdir / rel).write_bytes(target.read_bytes())
        return f"![]({rel})"
    text = FENCE.sub(sub, text)

    # xelatex cannot read SVG: rasterize the figures that ship as SVG
    if mode == "png":
        def svg_ref(m):
            rel = m.group(1) + ".svg"
            source = resdir / rel
            if not source.exists():
                return m.group(0)
            png = work / "rasterized" / (rel.replace("/", "_")[:-4] + ".png")
            png.parent.mkdir(parents=True, exist_ok=True)
            rasterize(source, png)
            (resdir / rel[:-4]).with_suffix(".png").write_bytes(png.read_bytes())
            return f"({m.group(1)}.png"
        text = re.sub(r'\((assets/imgs/[^)\s]+?)\.svg(?=[\s)])', svg_ref, text)

    # the alt text in this book is always the original file name; it only shows up
    # as a bogus figure caption, so drop it
    text = re.sub(r'!\[[^\]]*\]\(', '![](', text)
    dst.write_text(text, encoding="utf-8")
    print(f"  diagrams: {sum(1 for s in svgs if s.exists())}/{len(blocks)} mermaid blocks rendered")


if __name__ == "__main__":
    main()
