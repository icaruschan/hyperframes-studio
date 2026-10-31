# DESIGN.md — Brand Spec Template

> Copy this file into each new video project as `DESIGN.md`.
> Fill in YOUR brand details. Every composition must trace its palette,
> typography, and motion choices back to this file.

## Style Prompt

<!-- Write 2–3 sentences describing the overall feel.
     Example format: "[Brand] is a ___, ___, ___-driven brand — '[analogy].'
     Compositions should feel like ___. The mood is ___, ___, and ___." -->

_[Describe your brand's visual identity and emotional tone here]_

## Colors

<!-- Pick 5–7 tokens max. Assign each a ROLE, not just a name.
     Use CSS custom properties so every composition can import them. -->

| Token | Hex | Role |
|---|---|---|
| `--brand-bg` | `#______` | Primary background |
| `--brand-surface` | `#______` | Cards, panels, surfaces |
| `--brand-border` | `#______` | Borders, dividers, hairlines |
| `--brand-accent` | `#______` | Primary accent — highlights, CTAs |
| `--brand-accent-2` | `#______` | Secondary accent — use sparingly |
| `--brand-text` | `#______` | Primary text |
| `--brand-text-dim` | `#______` | Secondary/meta text |

> **Rule:** every color must own a MEANING. If you can't name what it communicates, delete it.

### brand-tokens.css

```css
:root {
  --brand-bg: #______;
  --brand-surface: #______;
  --brand-border: #______;
  --brand-accent: #______;
  --brand-accent-2: #______;
  --brand-text: #______;
  --brand-text-dim: #______;
}
```

## Typography

<!-- Pick exactly 2 fonts. One for display/headlines, one for labels/data.
     Load from Google Fonts CDN — no custom font files needed. -->

- **[Display Font] ([Weight])** — sans/serif. Use for: headlines, body copy, taglines.
- **[Mono/Label Font] ([Weight])** — monospace/sans. Use for: UI labels, stats, numbers, CTAs.

Pair them — never use only one. [Label font] above [Display font] headlines is the house pattern.

### Google Fonts import

```html
<link href="https://fonts.googleapis.com/css2?family=[Font1]:wght@300;700&family=[Font2]:wght@500&display=swap" rel="stylesheet">
```

## Logo

- File: `assets/[your-logo].png` — description of the logo, transparent bg.
- CSS treatment on dark backgrounds: `filter: drop-shadow(0 0 __px rgba(___,___,___,___));`
- Clearspace: half a logo-height of margin on all sides.
- Never recolor. Never stretch. Never add effects beyond the spec treatment.

## Motion Rules

- **Entrance only** (per Hyperframes rule): every element animates in via `gsap.from()`. Transitions between scenes handle exits.
- **Easing palette:**
  - Entrances: `power3.out`, `expo.out`, `back.out(1.4)`, `power4.out`
  - Hand-offs into transitions: `power2.in`
  - Ambient loops: `sine.inOut`
- **Use at least 3 different eases per scene.** Vary the feel.
- **Duration bands:** snap entrances 0.3–0.5s, headline entrances 0.5–0.8s, ambient drifts 2–4s.
- **Offset first animation** 0.1–0.3s from scene start.
- **Text stagger:** 0.04–0.08s per character for display type, 0.12–0.18s per word for headlines.

## Transitions

<!-- Pick 3–4 transition types. Assign each a PURPOSE.
     Don't use every transition — consistency > variety. -->

| Scene Change | Transition | Duration | Ease |
|---|---|---|---|
| Default | Push slide left | 0.35s | `power2.inOut` |
| Opener/climax | Zoom through | 0.35s | `power4.inOut` |
| Wind-down/outro | Blur crossfade | 0.5s | `sine.inOut` |

## Iconography

<!-- Define the icon style: stroke weight, color, fill vs. outline -->

Thin stroke, ___px weight, `var(--brand-accent)`, no fills.

## What NOT to Do

<!-- List 5–8 hard rules. These prevent drift as the project grows. -->

1. **No full-screen linear gradients** on dark backgrounds — H.264 banding.
2. **No colors outside the palette.** If it's not in the table above, it's not in the video.
3. **No system fonts.** Only the two fonts listed above.
4. **No `transparent` keyword in gradients** — use `rgba(r,g,b,0)` for shader compatibility.
5. **No `Math.random()` or `Date.now()`** — render determinism.
6. **No exit animations** except on the final scene — transitions handle exits.
7. **No stretching the logo.** Keep aspect ratio. Respect clearspace.

## Asset References

- `assets/[your-logo].png` — official logo
- `assets/brand-tokens.css` — CSS `:root` vars imported by every composition
- `assets/[brand-guideline].pdf` — the source brand guidelines (if applicable)
