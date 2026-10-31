# Motion Philosophy — Universal Reference

> Re-read before starting any new composition.
> Principles extracted from professional motion-graphics spots.
> Style-specific choices are clearly marked — adapt them to YOUR brand.

---

## 0 · Universal Laws (always true, any style)

1. **One idea per beat. Cut fast.** Target ~1.5s per scene. Each visual lands ONE concept and moves on. If a scene says two things, split it.
2. **Camera never sleeps.** Even on "still" frames, something moves — objects drift, backgrounds shift, textures breathe. Static = death.
3. **Motion blur masks cuts.** Transitions using streak/blur trails convey energy AND hide cuts. Hard cuts feel cheap; motion-blurred transitions feel expensive.
4. **Object metaphors carry meaning.** Assign visual objects to concepts. Return them later for callbacks. Visual continuity = brand.
5. **Palette is symbolic, not decorative.** Each color owns one concept. Don't drop a color in just because it looks nice — assign it a meaning. Max 5 active hues.
6. **Type is a character.** Words can SCALE 8×, MORPH, COMPRESS, GLOW. Typography drives ~60% of storytelling. A text-only beat can be the strongest beat.
7. **Hold the hero shot.** Logo reveal = ~2s of stillness. Outro card = 5+ seconds. Speed earns space for stillness to land. Kinetic chaos → calm = catharsis.
8. **One unifying texture across everything.** Pick ONE visual system (grid, particles, grain, geometric shapes, organic blobs) and thread it through every scene. That system is the spine of the piece.
9. **Timelines must fill their slots.** (HyperFrames-specific) Every GSAP timeline ends with `tl.to({}, { duration: SLOT_DURATION }, 0)` as a no-op duration anchor. Non-negotiable — prevents black frame flashes.
10. **Render determinism.** No `Math.random()`, `Date.now()`, or unseeded PRNGs in render loops. Use seeded/harmonic hashes for "random-looking" reproducible values.
11. **Visual verification.** Always draft-render and look at extracted frames. Lint passing ≠ design working.

---

## 1 · Style Archetypes (pick yours)

These are DIFFERENT valid aesthetics. Nate's "Infinite" style is just one. Choose the archetype that matches your brand, then adapt the recipes below.

| Archetype | Canvas | Text Treatment | Mood | Examples |
|-----------|--------|---------------|------|----------|
| **Dark Cinematic** | Black/near-black, 90% negative space | Chrome gradients, halo glow | Premium, dramatic, tech | Stripe promos, fintech launches, SaaS dark mode |
| **Clean Minimal** | White/light gray | Crisp dark type, no effects | Elegant, trustworthy, editorial | Apple product pages, Notion, Linear |
| **Brand Bold** | Saturated brand color | Large white/contrast type | Energetic, confident, playful | Spotify Wrapped, Nike, Figma |
| **Gradient Flow** | Animated gradient backgrounds | White or dark type with subtle shadow | Modern, creative, dynamic | Instagram, Vercel, Arc |
| **Editorial** | Off-white/cream with accent borders | Serif + sans-serif mix | Sophisticated, authoritative | NYT, The Economist, Monocle |
| **Neon/Cyberpunk** | Dark with color bleeds | Glowing, outlined type | Edgy, nightlife, gaming | Discord, gaming trailers |

### Per-archetype canvas rules

**Dark Cinematic:** Negative space IS the design. Color earns its place. Light reads as premium. Use vignettes, subtle grids, film grain.

**Clean Minimal:** Whitespace IS the design. Shadows are subtle. Motion is restrained and precise. Typography does the heavy lifting.

**Brand Bold:** The brand color IS the canvas. Contrast is king. Motion is punchy and rhythmic. Icons and illustrations carry meaning.

**Gradient Flow:** The gradient IS the energy. Keep elements simple on top. Motion follows the flow direction.

**Editorial:** Typography hierarchy IS the design. Restrained motion. Elegant transitions. Let the content breathe.

---

## 2 · Three-Act Structure (any promo)

- **Act 1 (0–30%):** Problem → metaphor → brand reveal
- **Act 2 (30–75%):** Benefits (rule of threes) → product surfaces → product names
- **Act 3 (75–100%):** Foundation → CTA → silence

The **rule of threes** works everywhere: 3 benefits, 3 surfaces, 3 product names.

---

## 3 · Background Recipes

### Universal (any style)
| Background | How to build |
|-----------|-------------|
| **Vignette** | `radial-gradient(ellipse at center, transparent 30%, [canvas-color] 100%)`, `pointer-events: none`. Adapt color to your canvas. |
| **Sparkle/particle drift** | 20–40 absolute `div`s, GSAP `stagger.from('random')` opacity, `repeat: -1, yoyo: true` |
| **Subtle grain** | Three `radial-gradient`s at tile sizes 3/5/7px, low alpha. Deterministic, headless-safe. Or `npx hyperframes add grain-overlay` |

### Dark canvas
| Background | How to build |
|-----------|-------------|
| **Perspective grid floor** | `repeating-linear-gradient` × 2 axes + `transform: perspective(800px) rotateX(60deg)`. Animate `background-position-y` for parallax. |
| **Speed lines** | `repeating-linear-gradient` with GSAP scrolling `background-position-x` |
| **Liquid-glass card** | Diagonal gradient + `backdrop-filter: blur(14px) saturate(1.12)` + inner highlight |

### Light canvas
| Background | How to build |
|-----------|-------------|
| **Soft shadow cards** | `box-shadow: 0 4px 24px rgba(0,0,0,0.08)` + `border: 1px solid rgba(0,0,0,0.06)` |
| **Dot grid** | `radial-gradient(circle, rgba(0,0,0,.1) 1px, transparent 1px)` with `background-size: 24px 24px` |
| **Gradient mesh** | Multiple `radial-gradient` layers at different positions, soft pastels, blurred |

---

## 4 · Type System

### Universal principles
- **Word-by-word kinetic reveal** (NOT character-by-character — words land harder)
- **Type SCALES dramatically.** Labels at 48px, hero at 480px+. Use `font-size: clamp()` + `scale`.
- **Word-reveal carrier pattern.** First word carries momentum with the biggest slide; subsequent words decay: `360 → 120 → 60 → 25 → 12px`.
- **Per-beat font variety** (different families per beat) sells "different universes."

### Style-dependent treatments

**Dark canvas:**
```css
/* Chrome gradient */
background: linear-gradient(180deg, #ffffff 0%, #999999 60%, #cccccc 100%);
-webkit-background-clip: text; color: transparent;
/* Halo glow */
text-shadow: 0 0 20px rgba(255,255,255,0.6), 0 0 40px rgba(255,255,255,0.3);
```

**Light canvas:**
```css
/* Sharp dark type */
color: #1a1a1a;
/* Subtle depth */
text-shadow: 0 1px 2px rgba(0,0,0,0.08);
/* Accent underline or highlight */
background: linear-gradient(transparent 60%, var(--brand-accent-20) 60%);
```

**Brand bold:**
```css
/* High contrast on brand color */
color: #ffffff;
font-weight: 900;
/* Knockout effect */
-webkit-text-stroke: 2px currentColor; color: transparent;
```

---

## 5 · Motion Catalog (universal)

| Move | GSAP Recipe |
|------|-------------|
| **Camera dolly through type** | `tl.fromTo(text, { scale: 1, opacity: 1 }, { scale: 8, opacity: 0, duration: 1.5, ease: 'power2.in' })` |
| **Light-streak whip** | `gsap.fromTo(streak, { xPercent: -150 }, { xPercent: 250, duration: 0.4, ease: 'power3.in' })` — fire AT the cut |
| **Word ghost reveal** | `stagger: 0.35` with overlapping exits/entrances (~0.15s overlap) |
| **Object morph drift** | Two `div`s: A exits right + shrinks, B enters from same vector |
| **3D spin reveal** | `tl.from(obj, { rotateY: 90, duration: 0.8, ease: 'back.out(1.4)' })` + `transform-style: preserve-3d` |
| **Color recolor (no cut)** | `tl.to(':root', { '--accent': '#newcolor', duration: 0.6 })` — same DOM, meaning shifts |
| **Slide-up device reveal** | `tl.from(phone, { y: '100%', duration: 1, ease: 'power3.out' })` |
| **Floating cluster drift** | `gsap.to(items, { y: '-=15', duration: 2, repeat: -1, yoyo: true, ease: 'sine.inOut', stagger: { each: 0.4, from: 'random' } })` |
| **Cut-the-curve whip** | Exit: `{ y: -150, filter: "blur(30px)", 0.33s, power2.in }` / Entry: `{ y: 0, filter: "blur(0px)", 1.0s, power2.out }` |
| **Faux-cursor click** | 7 tweens: cursor compress → target compress → ripple → release → overshoot → settle |

---

## 6 · Transition Catalog

| Transition | When to use | How |
|-----------|-------------|-----|
| **Light-streak whip** | Default between energy beats | Custom div + GSAP, or `npx hyperframes add whip-pan` |
| **Push slide** | Sequential content (most common, ~60%) | `xPercent: -100` exit, `xPercent: 100 → 0` entry |
| **Zoom-through** | Text into 3D space / climax opener | `npx hyperframes add cinematic-zoom` |
| **Cross-warp morph** | Object A becoming object B | `npx hyperframes add cross-warp-morph` |
| **Color recolor** | Two related ideas, same composition | CSS variables + GSAP tween, no cut |
| **Blur crossfade** | Wind-down into CTA / gentle transition | Both scenes visible, blur + opacity tween |
| **Flash-through-white** | Major act break | `npx hyperframes add flash-through-white` |
| **Hard cut on action** | When motion peaks | Align `data-start` with the motion peak frame |

---

## 7 · Pacing Discipline

- **Default scene length:** 1.0–2.0s. Longer = hero moment or outro only.
- **Reveal cadence:** new visual element every 0.3–0.6s within a scene.
- **Word-reveal stagger:** 0.3–0.4s narrative, 0.5–0.6s dramatic emphasis.
- **Transition duration:** 0.3–0.5s.
- **Hold durations:**
  - Logo crystallization: **1.5–2s**
  - Final CTA card: **4–6s**
  - Section headlines: **1–1.5s** read time after fully revealed
- **The breathing rule:** every ~7–8s of kinetic density, give a 1s rest beat.

---

## 8 · Audio Mix Defaults

| Layer | `data-volume` | Role |
|------|---------------|------|
| Voiceover | `1.0` | Primary, drives timing |
| Underscore (warm pad) | `0.15` | Barely there — sets mood |
| SFX (clicks, whooshes) | `0.2` | Tails allowed to bleed |

Music-free is valid. Pad-only is premium. Full music cue is last resort.

---

## 9 · Easing Reference

| Purpose | Ease | Duration |
|---|---|---|
| Word reveal (slide-in) | `expo.out` | 0.20–0.33s |
| Generic element enter | `power2.out` | 0.2–0.5s |
| Generic element exit | `power2.in` | 0.2–0.33s |
| Beat-to-beat whip EXIT | `expo.in` / `power2.in` | 0.2–0.33s |
| Beat-to-beat whip ENTRY | `expo.out` / `power2.out` | 0.5–1.0s |
| Camera pan between stops | `power2.inOut` | 1.2–2.3s |
| Linear hold | `"none"` | 0.4–0.65s |
| Bouncy card settle | `back.out(1.2–1.5)` | 0.3–0.5s |
| Click compress | `power4.in` | 0.07s |
| Click release | `back.out(3)` | 0.30s |
| Continuous rotation | `"none"` | full beat |
| Breathe / drift | `sine.inOut` yoyo | 2–4s, `repeat: -1` |

**Stagger values:**
- Chrome sweep across words: `0.04`
- Grid ripple per-column: `0.019`
- Code-stream lines: `0.06`
- Scaffold output lines: `0.08–0.12s`

---

## 10 · Pre-Flight Checklist

- [ ] Average scene length ≤ 2s in mid-section
- [ ] No dead air > 1s except deliberate holds
- [ ] Every transition uses motion (no hard fades)
- [ ] Color palette ≤ 5 active hues, each with a meaning
- [ ] Text treatment matches chosen style archetype
- [ ] Background texture/motion on every scene (no flat static fills)
- [ ] One visual callback minimum (element that returns later)
- [ ] Outro holds for 4+ seconds
- [ ] Visual verification done — extracted frames, confirmed
- [ ] Every timeline ends with `tl.to({}, { duration: SLOT_DURATION }, 0)`
- [ ] All tween end-times snap to multiples of `1/fps`
- [ ] Ran timeline-duration diagnostic in Studio devtools

---

## 11 · Anti-Patterns (what NOT to do)

- ❌ Motionless text fades — always add scale, blur, or direction
- ❌ Hard cuts between scenes — every cut needs a transition element
- ❌ Unstyled default type — apply your archetype's text treatment
- ❌ 6+ colors — you're decorating, not communicating
- ❌ No callbacks — a visual element appearing once wastes a setup
- ❌ Outro ending on the last beat — hold the CTA for 4+ seconds
- ❌ Scenes that say two things — split them
- ❌ Static backgrounds — every bg needs at least one moving element
- ❌ `Math.random()` / `Date.now()` — renders must be deterministic
- ❌ Skipping draft-render review — lint passing ≠ design working

---

## 12 · TL;DR

> **One idea per beat, styled not default, kinetic not still, callbacks not novelty, hold the hero, breathe the outro — one unifying texture across everything, every timeline fills its slot, every exit snaps to a frame boundary, and every cut hides inside a transition.**
