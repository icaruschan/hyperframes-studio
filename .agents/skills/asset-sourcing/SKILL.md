---
name: asset-sourcing
description: Search and download free creative assets (photos, videos, SFX, icons, music) from Pexels, Pixabay, Freesound, Iconify, and Google Fonts. No paid subscriptions needed. Use when gathering assets for motion graphics, video editing, or HyperFrames compositions.
---

## What this does
Unified search + download across **free** asset platforms. One query, multiple platforms searched in parallel, organized downloads into a structured `assets/` directory.

## Platforms

| Platform | Asset Types | API Key Required | Key Source |
|----------|------------|-----------------|------------|
| Pexels | Photos, Videos | Yes (free) | [pexels.com/api](https://www.pexels.com/api/) |
| Pixabay | Photos, Videos | Yes (free) | [pixabay.com/api/docs](https://pixabay.com/api/docs/) |
| Freesound | Sound effects | Yes (free) | [freesound.org/apiv2/apply](https://freesound.org/apiv2/apply/) |
| Iconify | SVG icons (200K+) | No | — |
| Pixabay Music | Music tracks | No (manual) | Browse [pixabay.com/music](https://pixabay.com/music/) |
| Google Fonts | Fonts | No | Browse [fonts.google.com](https://fonts.google.com) |

## Setup
Add API keys to `video-use/.env` (same file as ELEVENLABS_API_KEY):

```
PEXELS_API_KEY=your_key_here
PIXABAY_API_KEY=your_key_here
FREESOUND_API_KEY=your_key_here
```

All keys are free. The skill works with whatever keys are present — missing keys just skip that platform.

## Helpers

### search_assets.py
```bash
python helpers/search_assets.py "dark tech background" -t photo -n 5
python helpers/search_assets.py "woosh impact" -t sfx -n 8
python helpers/search_assets.py "coding icon" -t icon -n 10
python helpers/search_assets.py "cinematic aerial" -t video -n 5
python helpers/search_assets.py "lofi chill" -t music
python helpers/search_assets.py "abstract particles" --json -o results.json
```

**Types:** `all`, `photo`, `video`, `sfx`, `icon`, `music`
**Flags:** `-n` limit per platform, `--json` machine output, `-o` save to file

### download_asset.py
```bash
# Download from a direct URL
python helpers/download_asset.py "https://example.com/photo.jpg" -o ./assets

# Download from search results JSON
python helpers/download_asset.py results.json --index 0 -o ./assets
python helpers/download_asset.py results.json --all -o ./assets
```

Downloads are organized into subdirectories: `photos/`, `videos/`, `sfx/`, `music/`, `icons/`, `fonts/`.

## Workflow
1. **Search:** `search_assets.py "query" -t type -o results.json`
2. **Review:** Agent or user reviews the results
3. **Download:** `download_asset.py results.json --all -o ./assets`
4. **Use:** Reference downloaded files in HyperFrames compositions or video-use projects

## Agent usage
When the user asks for assets, run `search_assets.py` with a relevant query, review the results, and download the best matches. Always confirm with the user before bulk downloading. Organize into the project's `assets/` directory.
