# Hyperframes Studio 🎥

> **Programmatic Web-Based Video Composition, Motion Design & AI Video Production Framework**

An end-to-end programmatic video studio leveraging [HeyGen Hyperframes](https://hyperframes.heygen.com/introduction) to build deterministic, high-performance HTML/CSS/JavaScript video compositions powered by GSAP, Three.js, Tailwind CSS, Canvas, and custom AI agent skills.

---

## ⚡ Architecture & Features

1. **Deterministic Motion Design**: Web-native timelines using GSAP, WAAPI, and CSS animations with strict frame-accurate timing (`data-start`, `data-duration`, `data-track-index`).
2. **16 AI Agent Skills (`.agents/skills/`)**:
   - `hyperframes` & `hyperframes-cli` — Framework syntax, timeline registration, and CLI tools.
   - `hyperframes-media` & `hyperframes-registry` — Media asset handling and component catalog.
   - `gsap` & `animejs` — Physics and tween orchestration.
   - `three` & `typegpu` — 3DWebGL and GPU-accelerated graphics.
   - `lottie` & `remotion-to-hyperframes` — Cross-format animation conversion.
   - `tailwind` & `css-animations` — Modern styling and animation primitives.
   - `asset-sourcing` & `website-to-hyperframes` — Web-to-video capture and asset pipelines.
3. **Automated Video Toolkit (`video-use/`)**: Python CLI for script execution, transcription, and asset pipeline integration.
4. **Motion Guidelines & Templates (`docs/`)**:
   - [`MOTION_PHILOSOPHY.md`](docs/MOTION_PHILOSOPHY.md) — Core principles for authentic motion design.
   - [`DESIGN_TEMPLATE.md`](docs/DESIGN_TEMPLATE.md) — Structural blueprints for video compositions.

---

## 📂 Repository Structure

```
hyperframes-studio/
├── .agents/skills/              # 16 custom Hyperframes agent skills
├── docs/                        # Motion philosophy & design templates
├── my-video/                    # Active video composition project
│   ├── composition/             # Main HTML5/GSAP compositions and renders
│   ├── AGENTS.md                # Agent instruction set & linting rules
│   └── package.json             # NPM scripts (dev, check, render, publish)
├── video-use/                   # Video automation & asset helpers
├── raw_footage/                 # Source video recordings & b-rolls
├── Refereneces and Examples/    # Motion video references, style bible & b-roll inspo
└── assets/                      # Shared media assets
```

---

## 🚀 Quickstart

```bash
# Preview composition in browser editor
cd my-video/composition
npm run dev

# Lint and validate timeline logic
npm run check

# Render composition to MP4
npm run render
```
