#!/usr/bin/env python3
"""Unified asset search across free platforms: Pexels, Pixabay, Freesound, Iconify."""

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)


def load_env():
    """Load API keys from .env files and environment variables."""
    env_paths = [
        Path(__file__).resolve().parent.parent.parent.parent.parent / "video-use" / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path.home() / "Developer" / "video-use" / ".env",
    ]
    keys = {}
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if v and k not in keys:
                            keys[k] = v
    for key in ["PEXELS_API_KEY", "PIXABAY_API_KEY", "FREESOUND_API_KEY"]:
        if key not in keys and os.environ.get(key):
            keys[key] = os.environ[key]
    return keys


# ── Pexels ───────────────────────────────────────────────────────────────────

def search_pexels_photos(query, limit, api_key):
    resp = requests.get(
        "https://api.pexels.com/v1/search",
        params={"query": query, "per_page": limit},
        headers={"Authorization": api_key},
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for p in resp.json().get("photos", []):
        results.append({
            "platform": "pexels", "type": "photo", "id": p["id"],
            "title": p.get("alt", f"Pexels photo {p['id']}"),
            "preview": p["src"]["medium"], "download": p["src"]["large2x"],
            "width": p["width"], "height": p["height"],
            "photographer": p.get("photographer", "Unknown"),
            "page": p["url"],
        })
    return results


def search_pexels_videos(query, limit, api_key):
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        params={"query": query, "per_page": limit},
        headers={"Authorization": api_key},
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for v in resp.json().get("videos", []):
        files = sorted(v.get("video_files", []), key=lambda f: f.get("width", 0), reverse=True)
        best = files[0] if files else {}
        results.append({
            "platform": "pexels", "type": "video", "id": v["id"],
            "title": f"Pexels video {v['id']}",
            "preview": v.get("image", ""), "download": best.get("link", ""),
            "width": best.get("width", 0), "height": best.get("height", 0),
            "duration": v.get("duration", 0), "page": v["url"],
        })
    return results


# ── Pixabay ──────────────────────────────────────────────────────────────────

def search_pixabay_images(query, limit, api_key):
    resp = requests.get(
        "https://pixabay.com/api/",
        params={"key": api_key, "q": query, "per_page": max(limit, 3), "image_type": "all"},
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for h in resp.json().get("hits", []):
        results.append({
            "platform": "pixabay", "type": "photo", "id": h["id"],
            "title": h.get("tags", f"Pixabay image {h['id']}"),
            "preview": h["previewURL"], "download": h["largeImageURL"],
            "width": h["imageWidth"], "height": h["imageHeight"],
            "page": h["pageURL"],
        })
    return results


def search_pixabay_videos(query, limit, api_key):
    resp = requests.get(
        "https://pixabay.com/api/videos/",
        params={"key": api_key, "q": query, "per_page": max(limit, 3)},
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for h in resp.json().get("hits", []):
        vids = h.get("videos", {})
        large = vids.get("large", vids.get("medium", {}))
        results.append({
            "platform": "pixabay", "type": "video", "id": h["id"],
            "title": h.get("tags", f"Pixabay video {h['id']}"),
            "preview": "", "download": large.get("url", ""),
            "width": large.get("width", 0), "height": large.get("height", 0),
            "duration": h.get("duration", 0), "page": h["pageURL"],
        })
    return results


# ── Freesound ────────────────────────────────────────────────────────────────

def search_freesound(query, limit, api_key):
    resp = requests.get(
        "https://freesound.org/apiv2/search/text/",
        params={
            "query": query, "page_size": limit,
            "fields": "id,name,tags,description,duration,previews,avg_rating,url",
            "token": api_key,
        },
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for s in resp.json().get("results", []):
        pv = s.get("previews", {})
        results.append({
            "platform": "freesound", "type": "sfx", "id": s["id"],
            "title": s["name"],
            "description": s.get("description", "")[:200],
            "preview": pv.get("preview-lq-mp3", ""),
            "download": pv.get("preview-hq-mp3", ""),
            "duration": round(s.get("duration", 0), 1),
            "rating": s.get("avg_rating", 0),
            "page": s.get("url", f"https://freesound.org/people/unknown/sounds/{s['id']}/"),
        })
    return results


# ── Iconify ──────────────────────────────────────────────────────────────────

def search_iconify(query, limit):
    resp = requests.get(
        "https://api.iconify.design/search",
        params={"query": query, "limit": limit},
        timeout=10,
    )
    resp.raise_for_status()
    results = []
    for icon in resp.json().get("icons", [])[:limit]:
        prefix, name = icon.rsplit(":", 1) if ":" in icon else ("", icon)
        results.append({
            "platform": "iconify", "type": "icon", "id": icon,
            "title": icon,
            "preview": f"https://api.iconify.design/{prefix}/{name}.svg?height=64",
            "download": f"https://api.iconify.design/{prefix}/{name}.svg",
            "format": "svg",
            "page": f"https://icon-sets.iconify.design/{prefix}/?query={name}",
        })
    return results


# ── Simple Icons (brand logos — no API key) ──────────────────────────────────

_SIMPLE_ICONS_CACHE = None

def _load_simple_icons():
    global _SIMPLE_ICONS_CACHE
    if _SIMPLE_ICONS_CACHE is not None:
        return _SIMPLE_ICONS_CACHE
    try:
        resp = requests.get(
            "https://raw.githubusercontent.com/nicedoc/simple-icons/master/site/data.json",
            timeout=10,
        )
        resp.raise_for_status()
        _SIMPLE_ICONS_CACHE = resp.json()
    except Exception:
        # Fallback: try the npm CDN index
        try:
            resp = requests.get("https://cdn.simpleicons.org/data.json", timeout=10)
            resp.raise_for_status()
            _SIMPLE_ICONS_CACHE = resp.json()
        except Exception:
            _SIMPLE_ICONS_CACHE = []
    return _SIMPLE_ICONS_CACHE


def search_simple_icons(query, limit):
    """Search Simple Icons for brand logos (2800+ brands, no key needed)."""
    query_lower = query.lower()
    results = []
    # Try direct CDN hit first (slug = lowercase, no spaces)
    slug = query_lower.replace(" ", "").replace(".", "dot")
    try:
        resp = requests.head(f"https://cdn.simpleicons.org/{slug}", timeout=5, allow_redirects=True)
        if resp.status_code == 200:
            results.append({
                "platform": "simpleicons", "type": "logo", "id": slug,
                "title": f"{query} (brand logo)",
                "preview": f"https://cdn.simpleicons.org/{slug}/666666",
                "download": f"https://cdn.simpleicons.org/{slug}",
                "download_white": f"https://cdn.simpleicons.org/{slug}/FFFFFF",
                "download_black": f"https://cdn.simpleicons.org/{slug}/000000",
                "format": "svg",
                "page": f"https://simpleicons.org/?q={query}",
            })
    except Exception:
        pass
    # Also search Iconify's brand icon sets for more logo results
    try:
        resp = requests.get(
            "https://api.iconify.design/search",
            params={"query": f"{query} logo", "limit": limit},
            timeout=10,
        )
        resp.raise_for_status()
        for icon in resp.json().get("icons", [])[:limit]:
            prefix, name = icon.rsplit(":", 1) if ":" in icon else ("", icon)
            results.append({
                "platform": "iconify", "type": "logo", "id": icon,
                "title": icon,
                "preview": f"https://api.iconify.design/{prefix}/{name}.svg?height=64",
                "download": f"https://api.iconify.design/{prefix}/{name}.svg",
                "format": "svg",
                "page": f"https://icon-sets.iconify.design/{prefix}/?query={name}",
            })
    except Exception:
        pass
    return results[:limit]


# ── LottieFiles (animated assets — no API key for search) ────────────────────

def search_lottiefiles(query, limit):
    """Search LottieFiles for free animated assets."""
    try:
        resp = requests.get(
            "https://lottie.host/api/v1/search",
            params={"query": query, "per_page": limit},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("data", data.get("results", []))[:limit]:
            lottie_url = item.get("lottie_url", item.get("file", ""))
            results.append({
                "platform": "lottiefiles", "type": "lottie", "id": item.get("id", ""),
                "title": item.get("title", item.get("name", "Lottie animation")),
                "preview": item.get("preview_url", item.get("gif_url", "")),
                "download": lottie_url,
                "format": "json",
                "page": item.get("url", f"https://lottiefiles.com/search?q={query}"),
            })
        return results
    except Exception:
        # Fallback: return browse link
        q = query.replace(" ", "+")
        return [{
            "platform": "lottiefiles", "type": "lottie", "id": "browse",
            "title": f"Browse LottieFiles: {query}",
            "preview": "", "download": "",
            "page": f"https://lottiefiles.com/search?q={q}",
            "note": "Browse and download from LottieFiles website",
        }]


# ── Google Fonts (no key needed for download) ────────────────────────────────

def search_google_fonts(query, limit):
    """Search Google Fonts catalog."""
    try:
        resp = requests.get(
            "https://fonts.google.com/metadata/fonts",
            headers={"User-Agent": "VideoStudio/1.0"},
            timeout=10,
        )
        resp.raise_for_status()
        text = resp.text
        # Google Fonts metadata starts with )]}' — strip it
        if text.startswith(")]}"):
            text = text[text.index("\n") + 1:]
        data = json.loads(text)
        query_lower = query.lower()
        results = []
        for fam in data.get("familyMetadataList", []):
            name = fam.get("family", "")
            category = fam.get("category", "")
            if query_lower in name.lower() or query_lower in category.lower():
                slug = name.replace(" ", "+")
                results.append({
                    "platform": "google_fonts", "type": "font", "id": name,
                    "title": f"{name} ({category})",
                    "preview": f"https://fonts.google.com/specimen/{slug}",
                    "download": f"https://fonts.google.com/download?family={slug}",
                    "format": "ttf/otf zip",
                    "category": category,
                    "page": f"https://fonts.google.com/specimen/{slug}",
                })
            if len(results) >= limit:
                break
        return results
    except Exception:
        return []


# ── Music (manual link — no API) ────────────────────────────────────────────

def search_music_links(query):
    q = query.replace(" ", "%20")
    return [{
        "platform": "pixabay_music", "type": "music", "id": "browse",
        "title": f"Browse Pixabay Music: {query}",
        "preview": "", "download": "",
        "page": f"https://pixabay.com/music/search/{q}/",
        "note": "Manual download from website",
    }, {
        "platform": "youtube_audio_library", "type": "music", "id": "browse",
        "title": f"Browse YouTube Audio Library: {query}",
        "preview": "", "download": "",
        "page": "https://studio.youtube.com/channel/UC/music",
        "note": "Manual download from YouTube Studio",
    }]


# ── Main search engine ──────────────────────────────────────────────────────

def run_search(query, asset_type="all", limit=5, keys=None):
    keys = keys or {}
    tasks = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        if asset_type in ("all", "photo", "image"):
            if keys.get("PEXELS_API_KEY"):
                tasks.append(pool.submit(search_pexels_photos, query, limit, keys["PEXELS_API_KEY"]))
            if keys.get("PIXABAY_API_KEY"):
                tasks.append(pool.submit(search_pixabay_images, query, limit, keys["PIXABAY_API_KEY"]))

        if asset_type in ("all", "video"):
            if keys.get("PEXELS_API_KEY"):
                tasks.append(pool.submit(search_pexels_videos, query, limit, keys["PEXELS_API_KEY"]))
            if keys.get("PIXABAY_API_KEY"):
                tasks.append(pool.submit(search_pixabay_videos, query, limit, keys["PIXABAY_API_KEY"]))

        if asset_type in ("all", "sfx", "sound", "audio"):
            if keys.get("FREESOUND_API_KEY"):
                tasks.append(pool.submit(search_freesound, query, limit, keys["FREESOUND_API_KEY"]))

        if asset_type in ("all", "icon", "svg"):
            tasks.append(pool.submit(search_iconify, query, limit))

        if asset_type in ("all", "logo"):
            tasks.append(pool.submit(search_simple_icons, query, limit))

        if asset_type in ("all", "lottie", "animation"):
            tasks.append(pool.submit(search_lottiefiles, query, limit))

        if asset_type in ("all", "font"):
            tasks.append(pool.submit(search_google_fonts, query, limit))

        if asset_type in ("all", "music"):
            tasks.append(pool.submit(search_music_links, query))

        all_results = []
        for future in as_completed(tasks):
            try:
                all_results.extend(future.result())
            except Exception as e:
                print(f"  Warning: search failed: {e}", file=sys.stderr)
    return all_results


def main():
    parser = argparse.ArgumentParser(description="Search free asset platforms")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-t", "--type", default="all",
                        choices=["all", "photo", "image", "video", "sfx", "sound", "audio",
                                 "icon", "svg", "logo", "lottie", "animation", "font", "music"])
    parser.add_argument("-n", "--limit", type=int, default=5, help="Results per platform")
    parser.add_argument("-o", "--output", help="Save results to JSON file")
    parser.add_argument("--json", action="store_true", help="JSON-only output")
    args = parser.parse_args()

    keys = load_env()

    if not args.json:
        available = [l for k, l in [("PEXELS_API_KEY", "Pexels"), ("PIXABAY_API_KEY", "Pixabay"),
                                     ("FREESOUND_API_KEY", "Freesound")] if keys.get(k)]
        missing = [l for k, l in [("PEXELS_API_KEY", "Pexels"), ("PIXABAY_API_KEY", "Pixabay"),
                                   ("FREESOUND_API_KEY", "Freesound")] if not keys.get(k)]
        extra = " + Iconify" if args.type in ("all", "icon", "svg") else ""
        print(f"Searching for: \"{args.query}\" (type: {args.type})")
        print(f"  Platforms: {', '.join(available)}{extra}")
        if missing:
            print(f"  Missing keys (skipped): {', '.join(missing)}")
        print()

    results = run_search(args.query, args.type, args.limit, keys)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No results found.")
            return
        by_type = {}
        for r in results:
            by_type.setdefault(r["type"], []).append(r)
        emoji = {"photo": "IMG", "video": "VID", "sfx": "SFX", "icon": "ICO", "music": "MUS"}
        for t, items in by_type.items():
            tag = emoji.get(t, "???")
            print(f"[{tag}] {t.upper()} — {len(items)} results")
            print("-" * 60)
            for i, item in enumerate(items, 1):
                print(f"  [{i}] {item['title'][:60]}")
                print(f"      Platform: {item['platform']}")
                if item.get("duration"):
                    print(f"      Duration: {item['duration']}s")
                if item.get("width"):
                    print(f"      Size: {item['width']}x{item.get('height', '?')}")
                dl = item.get("download") or item.get("page", "N/A")
                print(f"      URL: {dl[:90]}")
                print()

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        if not args.json:
            print(f"Saved {len(results)} results to {args.output}")


if __name__ == "__main__":
    main()
