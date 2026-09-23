#!/usr/bin/env bash
# Rebuild the offline bundle (Markdown + EPUB + PDF) from the chapter sources.
#
#   ./tools/build.sh            # everything
#   ./tools/build.sh md         # single-file Markdown only
#   ./tools/build.sh epub pdf   # pick targets
#
# Requires: pandoc, xelatex (for the PDF), and macOS `sips` for image downscaling.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${TMPDIR:-/tmp}/aiagent-book-build"
TARGETS="${*:-md epub pdf}"
want() { [[ " $TARGETS " == *" $1 "* ]]; }

mkdir -p "$WORK"

# 1. assemble: AI-Agent-Handbook-合订本.md (delivered) + a pandoc-flavoured source
python3 "$REPO/tools/build-book.py" "$REPO" "$WORK/book-pandoc.md"
want md && echo "built: $REPO/AI-Agent-Handbook-合订本.md"
if ! want epub && ! want pdf; then exit 0; fi

# 2. image mirror for e-book targets: max 1400px, JPEG q82 (SVG stays vector)
if [ ! -d "$WORK/res" ]; then
  cd "$REPO"
  find assets -type d -exec mkdir -p "$WORK/res/{}" \;
  find assets -type f | while read -r f; do
    cp "$f" "$WORK/res/$f"
    case "${f##*.}" in
      svg|SVG) ;;
      *) sips -s format jpeg -s formatOptions 82 -Z 1400 "$WORK/res/$f" --out "$WORK/res/${f%.*}.jpg" >/dev/null 2>&1 \
           && [ "$f" != "${f%.*}.jpg" ] && rm -f "$WORK/res/$f" ;;
    esac
  done
fi
python3 - "$WORK/book-pandoc.md" <<'PY'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding='utf-8')
p.write_text(re.sub(r'(\(assets/imgs/[^)\s]+?)\.(png|PNG|jpg|jpeg|JPG|JPEG|gif|GIF)(?=[\s)])', r'\1.jpg', t), encoding='utf-8')
PY

if want epub; then
  pandoc "$WORK/book-pandoc.md" \
    -f markdown+east_asian_line_breaks -t epub3 \
    --resource-path="$WORK/res" \
    --toc --toc-depth=3 --split-level=1 \
    --css="$REPO/tools/epub.css" \
    --epub-cover-image="$REPO/tools/cover.jpg" \
    --metadata lang=zh-CN --mathml \
    -o "$REPO/AI-Agent-Handbook.epub"
  echo "built: $REPO/AI-Agent-Handbook.epub"
fi

if want pdf; then
  # xelatex needs raster images and chokes on a handful of decorative glyphs
  if [ ! -d "$WORK/res-pdf" ]; then
    cp -R "$WORK/res" "$WORK/res-pdf"
    cd "$WORK/res-pdf"
    for f in $(find assets -iname '*.svg'); do
      sips -s format jpeg -s formatOptions 90 -Z 1600 "$f" --out "${f%.*}.jpg" >/dev/null 2>&1 && rm -f "$f"
    done
  fi
  python3 - "$WORK/book-pandoc.md" "$WORK/book-pdf.md" <<'PY'
import re, sys, pathlib
t = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
t = re.sub(r'(\(assets/imgs/[^)\s]+?)\.(svg|SVG)(?=[\s)])', r'\1.jpg', t)
subs = {chr(0x2460 + i): f'({i+1})' for i in range(10)}
subs.update({'🌰': '（举例）', '➊': '(1)', '➋': '(2)', '➌': '(3)', 'ꔷ': '·', 'μ': 'µ'})
subs.update(dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉', '01234567890123456789')))
subs.update({'₊': '+', '₋': '-', 'ₜ': 't', 'ₙ': 'n', 'ᵢ': 'i'})
for a, b in subs.items():
    t = t.replace(a, b)
pathlib.Path(sys.argv[2]).write_text(t, encoding='utf-8')
PY
  pandoc "$WORK/book-pdf.md" \
    -f markdown+east_asian_line_breaks \
    --pdf-engine=xelatex --resource-path="$WORK/res-pdf" \
    --toc --toc-depth=3 --top-level-division=chapter \
    -V documentclass=report -V geometry:margin=2.2cm -V fontsize=11pt \
    -V mainfont="Times New Roman" -V monofont="Menlo" \
    -V CJKmainfont="Songti SC" -V CJKsansfont="PingFang SC" -V CJKmonofont="PingFang SC" \
    -V colorlinks=true -V linkcolor=RoyalBlue -V urlcolor=RoyalBlue \
    -o "$REPO/AI-Agent-Handbook.pdf"
  echo "built: $REPO/AI-Agent-Handbook.pdf"
fi
