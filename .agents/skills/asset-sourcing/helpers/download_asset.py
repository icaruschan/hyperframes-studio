#!/usr/bin/env python3
"""Download assets from search results or direct URLs into organized project structure."""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)


def sanitize_filename(name, max_length=80):
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._")
    return name[:max_length] if len(name) > max_length else name


def guess_extension(url, content_type=None):
    ext = Path(urlparse(url).path).suffix.lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
               ".mp4", ".webm", ".mov", ".avi",
               ".mp3", ".wav", ".ogg", ".flac",
               ".json", ".lottie"):
        return ext
    if content_type:
        ct_map = {
            "image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
            "image/webp": ".webp", "image/svg+xml": ".svg",
            "video/mp4": ".mp4", "video/webm": ".webm",
            "audio/mpeg": ".mp3", "audio/wav": ".wav", "audio/ogg": ".ogg",
        }
        for ct, extension in ct_map.items():
            if ct in content_type:
                return extension
    return ".bin"


TYPE_DIRS = {
    "photo": "photos", "image": "photos",
    "video": "videos",
    "sfx": "sfx", "sound": "sfx", "audio": "music",
    "music": "music",
    "icon": "icons", "svg": "icons",
    "lottie": "animations",
    "font": "fonts",
    "misc": "misc",
}


def download_file(url, output_path):
    headers = {"User-Agent": "VideoStudio-AssetSourcer/1.0"}
    resp = requests.get(url, headers=headers, stream=True, timeout=30)
    resp.raise_for_status()

    total = int(resp.headers.get("content-length", 0))
    downloaded = 0
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total and sys.stdout.isatty():
                pct = (downloaded / total) * 100
                sys.stdout.write(f"\r   Progress: {pct:.0f}% ({downloaded // 1024}KB / {total // 1024}KB)")
                sys.stdout.flush()

    if total and sys.stdout.isatty():
        sys.stdout.write("\n")
    return output_path


def download_from_entry(entry, output_dir, name=None):
    url = entry.get("download") or entry.get("url")
    if not url or url.startswith("https://pixabay.com/music/") or url.startswith("https://studio.youtube.com"):
        note = entry.get("note", "")
        page = entry.get("page", url or "")
        print(f"  ⚠️  Manual download needed: {entry.get('title', 'untitled')}")
        print(f"      Visit: {page}")
        if note:
            print(f"      Note: {note}")
        return None

    asset_type = entry.get("type", "misc")
    platform = entry.get("platform", "unknown")
    title = entry.get("title", "untitled")
    subdir = TYPE_DIRS.get(asset_type, "misc")

    if name:
        filename = sanitize_filename(name)
    else:
        filename = sanitize_filename(f"{platform}_{entry.get('id', 'x')}_{title[:40]}")

    ext = guess_extension(url)
    if not filename.endswith(ext):
        filename += ext

    output_path = os.path.join(output_dir, subdir, filename)

    print(f"  Downloading [{asset_type}]: {title[:50]}")
    print(f"      From: {platform}")
    print(f"      To:   {output_path}")

    try:
        download_file(url, output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"      Done ({size_kb:.0f} KB)")
        return output_path
    except Exception as e:
        print(f"      FAILED: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Download assets from search results or URLs")
    parser.add_argument("source", help="Direct URL or path to search results JSON")
    parser.add_argument("-o", "--output-dir", default="./assets", help="Output directory")
    parser.add_argument("-n", "--name", help="Custom filename (no extension)")
    parser.add_argument("-i", "--index", type=int, help="Index from JSON manifest (0-based)")
    parser.add_argument("--all", action="store_true", help="Download all results from manifest")
    parser.add_argument("-t", "--type", default="misc", help="Asset type for directory organization")
    args = parser.parse_args()

    if args.source.endswith(".json") and os.path.exists(args.source):
        with open(args.source) as f:
            manifest = json.load(f)
        if not isinstance(manifest, list):
            manifest = [manifest]

        if args.all:
            downloaded = []
            for entry in manifest:
                result = download_from_entry(entry, args.output_dir)
                if result:
                    downloaded.append(result)
            print(f"\nDownloaded {len(downloaded)}/{len(manifest)} assets to {args.output_dir}/")
        elif args.index is not None:
            if 0 <= args.index < len(manifest):
                download_from_entry(manifest[args.index], args.output_dir, args.name)
            else:
                print(f"Error: index {args.index} out of range (0–{len(manifest)-1})")
        else:
            print(f"Found {len(manifest)} assets in manifest:")
            for i, entry in enumerate(manifest):
                print(f"  [{i}] {entry.get('type', '?'):6s} | {entry.get('platform', '?'):10s} | {entry.get('title', 'untitled')[:50]}")
            print(f"\nUse --index N to download one, or --all to download everything")
    else:
        entry = {
            "url": args.source, "download": args.source,
            "type": args.type, "platform": "direct",
            "title": args.name or Path(urlparse(args.source).path).stem,
            "id": "direct",
        }
        download_from_entry(entry, args.output_dir, args.name)


if __name__ == "__main__":
    main()
