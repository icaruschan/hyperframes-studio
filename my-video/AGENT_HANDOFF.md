# Agent Handoff: Premium Editorial Motion Video Edit (Authoritative Alignment Complete)

This document provides a comprehensive technical overview, historical context, previous bugs, exact resolutions, and the current state of the **Claude Design Edit** project. It is designed to act as a seamless handoff for the next AI agent or developer taking over the workspace.

---

## 🎯 Project Overview & Creative Goals

The goal of this project is to build a **premium, 60fps cinematic editorial edit** in **HyperFrames HTML** (a frame-by-frame web rendering engine) utilizing advanced motion design principles.

### Visual & Stylistic Requirements:
1. **Typography Pairing**:
   - **Readable Sans**: Clean, high-impact sans-serif uppercase for standard words using Google Font **Inter** (Weight: 900, size: 130px, heavy letter-spacing: -3px).
   - **Emphasis Script**: Elegant, free cursive script for accent/emphasis words using Google Font **Great Vibes** (Size: 210px, soft white diffused bloom effect via `text-shadow`).
   - **Emphasis Words**: Only select high-impact words are highlighted in cursive: `Claude`, `fundamentally`, `design`, `work.`, `Figma`, `immense`, `pressure`, `exactly`, `why.`.
2. **Premium Center-Bottom Captions**:
   - Replaced floating, wandering captions with a structured, single-word kinetic text player.
   - Anchored exactly at the bottom-center (`bottom: 120px`).
   - Only one word is shown at a time in the exact same spot, creating a highly polished, snappy reading flow.
3. **Apple-Style Frosted Glass UI Cards**:
   - Absolute-positioned frosted glass cards (`#claude-ui` and `#figma-ui`) with a heavy background blur (`backdrop-filter: blur(25px)`), subtle top-light border reflection (`border-top: 1px solid rgba(255,255,255,0.25)`), and soft drop shadows.
   - These slide and spring-pop onto the screen exactly in sync with their spoken mentions.
4. **Cinematic Motion & Overlay**:
   - Gentle, dynamic camera push-ins scaling the background video on key spoken phrases (e.g., scaling to `1.12x` during `"fundamentally changes"` and `1.09x` during `"Figma"`).
   - A global 4% opacity animated noise/film grain overlay to add organic texture.

### Complete Spoken Transcript:
> *"Claude just dropped a new platform that fundamentally changes how we do design work. And if you've been wondering why tools like Figma are under immense pressure right now, this is exactly why."*

---

## ⚠️ Major Historical Obstacles & Technical Bugs

Before the current implementation, the video suffered from severe quality and sync issues:

### 1. Chaotic Caption Layout (Aesthetic Failure)
* **Problem**: Words were scattered in a loose, wrapping layout floating randomly across the viewport. This felt undisciplined, disorganized, and ruined the high-end premium aesthetic.
* **Fix**: Built a stacked, single-word center-bottom container. Every word transitions in the exact same coordinates, utilizing a snappy GSAP spring pop (`duration: 0.12s`, `ease: "back.out(1.5)"`) and a rapid exit (`duration: 0.06s`) to prevent overlapping text.

### 2. Video Seek Lag / Frame-Dropping in Headless Chrome (Engine Bottleneck)
* **Problem**: During headless MP4 rendering, the video and captions drifted significantly out of sync. Captions and cards were popping up up to **1.5 seconds early** or lagging behind.
* **Discovery**: The source talking head video (`assets/Claude Design footage.mp4`) had **sparse keyframes (GOP interval up to 10.42 seconds apart)**. Because HyperFrames captures frames deterministically by seeking Chrome to exact millisecond intervals, Chrome was forced to decode up to 10 seconds of video on every single seek. This choked the rendering engine, causing massive lag and dropped frames.
* **Fix**: Re-encoded the source footage via `ffmpeg` to force a dense keyframe interval of 15 frames (0.5s):
  ```powershell
  ffmpeg -y -i "assets/Claude Design footage_raw.mp4" -c:v libx264 -g 15 -keyint_min 15 -pix_fmt yuv420p -c:a aac -b:a 256k "assets/Claude Design footage.mp4"
  ```
  This immediately resolved all browser rendering lag, enabling instantaneous, frame-accurate seeking.

### 3. Inaccurate Timing & Defects A & B (Authoritative Alignment Complete)
* **Defect A — Captions**: The inline `transcript` array in `index.html` had hand-tuned `start`/`end` timings that drifted from the source of truth, `transcript.json`.
* **Defect B — UI Cards**: The Claude and Figma glass card entrances were hand-coded to `0.15` and `8.80` instead of starting exactly when the words were spoken.
* **Resolution**: Completely aligned all timings in `index.html` to be **derived directly and synchronously from `transcript.json`** using the standard `AUDIO_OFFSET = -0.05` lead:
  - Caption `popTime` positions now match `Math.max(0, transcript[i].start + AUDIO_OFFSET)` exactly within 0 ms.
  - Caption `hideTime` positions now match `Math.max(0, transcript[i].end + AUDIO_OFFSET)` exactly within 0 ms.
  - `#claude-ui` entrance pop triggers at `Math.max(0, transcript[0].start + AUDIO_OFFSET)` (`0.0s` from `transcript.json`).
  - `#figma-ui` entrance pop triggers at `Math.max(0, transcript[22].start + AUDIO_OFFSET)` (`8.58s` from `transcript.json`).

---

## 🛠️ Current Workspace Architecture & Status

All files in the workspace are highly optimized, lint-clean, and verified correct:

### 1. File Structure:
- `index.html` — The main composition, root timeline, typography pairing, frosted glass cards, kinetic caption animations, and background video scaling effects. Paused and registered on `window.__timelines["main"]`. All timings derived authoritatively from `transcript.json`.
- `package.json` — Pre-scaffolded script triggers.
- `assets/` — Media assets including `Claude Design footage.mp4` (keyframe-dense), SVG icons (`claude-ai-icon.svg`, `figma-icon.svg`).
- `renders/` — Render outputs. The latest fully-aligned clean export is:
  `C:\Users\Dreys\OneDrive\Documents\Antigravity workspace\Hyperframes\my-video\composition\renders\composition_2026-05-18_14-33-57.mp4`

### 2. State & Quality Check:
- **Lint Check**: Run `npm run check` in `composition/`. It completes with **0 errors** and passes WCAG AA contrast validation.
- **Render Validation**: Successfully generated `composition_2026-05-18_14-33-57.mp4`. Captions, glass cards, camera zoom adjustments, and audio are in **absolute 100% flawless synchronization**.

---

## 🚀 Next Steps / Handoff Recommendations

If the user wants to extend or add new scenes to the composition:
1. **Maintain Keyframe Denseness**: If you source new background footage, ALWAYS verify keyframe spacing. If keyframes are sparse (GOP > 30), re-encode immediately using the `-g 15` rule to prevent Chrome seek delays.
2. **Follow the Wave Pattern**: When modifying or adding audio-synchronized elements, always ensure they are derived from `transcript.json`.
3. **Preserve Contrast & Layout**: Ensure the frosted glass cards keep their saturation and background blur values to retain high readability against the moving video layer.
