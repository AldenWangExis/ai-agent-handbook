#!/usr/bin/env python3
"""Download Alidocs Markdown images and rewrite their links to local assets."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import mimetypes
import os
import re
import shutil
import tempfile
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]\n]*)\]\("
    r"(?P<url>https?://[^\s)]+)"
    r"(?P<title>\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?"
    r"\)"
)
CHAPTER_RE = re.compile(r"第\s*(\d+)\s*章")
INTERNAL_HOSTS = {
    "alidocs.dingtalk.com",
    "alidocs.oss-cn-zhangjiakou.aliyuncs.com",
}
DENIED_IMAGE_SHA256 = "06834905b43b9aae0acc978c0661e5841b91f523a628474ed7e431e858e82706"


def group_for(path: Path) -> str:
    match = CHAPTER_RE.search(path.as_posix())
    if match:
        return f"chapter-{int(match.group(1)):02d}"
    if path.stem == "2026 Agent 开发者调研报告":
        return "2026-agent-developer-survey"
    safe = re.sub(r"[^0-9A-Za-z_-]+", "-", path.stem).strip("-").lower()
    return safe or "misc"


def image_extension(data: bytes, url: str, content_type: str | None) -> str:
    signatures = (
        (b"\x89PNG\r\n\x1a\n", ".png"),
        (b"\xff\xd8\xff", ".jpg"),
        (b"GIF87a", ".gif"),
        (b"GIF89a", ".gif"),
        (b"RIFF", ".webp"),
        (b"BM", ".bmp"),
    )
    stripped = data.lstrip()
    if stripped.startswith(b"<svg") or (stripped.startswith(b"<?xml") and b"<svg" in stripped[:1024]):
        return ".svg"
    for signature, extension in signatures:
        if data.startswith(signature):
            if extension != ".webp" or data[8:12] == b"WEBP":
                return extension
    if content_type:
        mime = content_type.split(";", 1)[0].strip().lower()
        extension = mimetypes.guess_extension(mime)
        if extension and mime.startswith("image/"):
            return ".jpg" if extension == ".jpe" else extension
    suffix = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".avif"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    raise ValueError("response is not a recognized image")


def download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ai-agent-handbook-image-localizer/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type")
        final_url = response.geturl()
    if not data:
        raise ValueError("empty response")
    final_path = urllib.parse.urlsplit(final_url).path.rstrip("/").lower()
    if final_path.endswith("/noauth.png"):
        raise PermissionError("Alidocs redirected to the no-permission placeholder")
    if hashlib.sha256(data).hexdigest() == DENIED_IMAGE_SHA256:
        raise PermissionError("Alidocs returned the no-permission placeholder image")
    return data, image_extension(data, url, content_type)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--jobs", type=int, default=12)
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = root / "assets" / "imgs"

    documents: dict[Path, str] = {}
    occurrences: list[tuple[Path, str]] = []
    for path in sorted(root.rglob("*.md")):
        if output_root in path.parents:
            continue
        text = path.read_text(encoding="utf-8")
        documents[path] = text
        for match in IMAGE_RE.finditer(text):
            url = match.group("url")
            if urllib.parse.urlsplit(url).hostname in INTERNAL_HOSTS:
                occurrences.append((path, url))

    if not occurrences:
        print("No internal Alidocs image links found.")
        return 0

    unique_urls = sorted({url for _, url in occurrences})
    print(f"Downloading {len(unique_urls)} unique images from {len(occurrences)} references...")
    downloaded: dict[str, tuple[bytes, str]] = {}
    failures: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(download, url): url for url in unique_urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                downloaded[url] = future.result()
            except Exception as exc:
                failures.append((url, str(exc)))

    if failures:
        print(f"Failed to download {len(failures)} images; no files or Markdown were changed:")
        for url, error in failures:
            print(f"  {error}: {url}")
        return 1

    mappings: dict[tuple[Path, str], Path] = {}
    group_counters: defaultdict[str, int] = defaultdict(int)
    group_url_paths: dict[tuple[str, str], Path] = {}
    for path, url in occurrences:
        group = group_for(path.relative_to(root))
        key = (group, url)
        if key not in group_url_paths:
            group_counters[group] += 1
            _, extension = downloaded[url]
            group_url_paths[key] = Path(group) / f"image-{group_counters[group]:03d}{extension}"
        mappings[(path, url)] = group_url_paths[key]

    staging = Path(tempfile.mkdtemp(prefix="localize-alidocs-images-"))
    try:
        staged_assets = staging / "imgs"
        for (group, url), relative_path in group_url_paths.items():
            destination = staged_assets / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(downloaded[url][0])

        rewritten: dict[Path, str] = {}
        for path, original in documents.items():
            def replace(match: re.Match[str]) -> str:
                url = match.group("url")
                local = mappings.get((path, url))
                if local is None:
                    return match.group(0)
                absolute_asset = output_root / local
                relative_asset = os.path.relpath(absolute_asset, path.parent).replace(os.sep, "/")
                title = match.group("title") or ""
                return f"![{match.group('alt')}]({relative_asset}{title})"

            updated = IMAGE_RE.sub(replace, original)
            if updated != original:
                rewritten[path] = updated

        if output_root.exists():
            raise FileExistsError(f"refusing to replace existing directory: {output_root}")
        output_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staged_assets), str(output_root))
        for path, updated in rewritten.items():
            path.write_text(updated, encoding="utf-8")
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    total_bytes = sum(len(data) for data, _ in downloaded.values())
    checksum = hashlib.sha256("\n".join(unique_urls).encode()).hexdigest()[:12]
    print(
        f"Localized {len(occurrences)} references to {len(group_url_paths)} files "
        f"across {len(group_counters)} directories ({total_bytes / 1024 / 1024:.1f} MiB)."
    )
    print(f"Source URL set checksum: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
