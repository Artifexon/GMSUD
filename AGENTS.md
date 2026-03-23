# AGENTS.md — GMSUD Flyer Project

## Project Overview
GM Süd GmbH facility management flyer — DL tri-fold (Wickelfalz), German language.
HTML/CSS-based print design exported to PDF via Ghostscript CMYK pipeline.

## Codebase Structure
```
assets/          — Images, logos, generated graphics
briefs/          — Client brief (the source of truth for ALL content)
src/v8-premium/  — Current active version (V8)
templates/       — Reusable canvas template
```

## Print Canvas Standard (MANDATORY)
All flyer files MUST use these exact CSS variables:
```css
:root {
    --spread-w: 303mm;   /* 297mm trim + 6mm bleed */
    --spread-h: 216mm;   /* 210mm trim + 6mm bleed */
    --bleed: 3mm;
}
```
- Canvas = 303mm × 216mm (A4 landscape + 3mm bleed all sides)
- Safe zone = 3mm inside trim edge (use `inset: calc(var(--bleed) + 3mm)`)
- Fold guides at 97mm and 197mm from left edge (outside spread)
- Fold guides at 100mm and 200mm from left edge (inside spread)

### Panel Widths — Outside Spread (front.html)
| Panel | Width | Role |
|-------|-------|------|
| S1-Left (Flap) | `calc(97mm + var(--bleed))` | Flap — 2mm narrower to prevent buckling |
| S1-Centre | `100mm` | Back Cover |
| S1-Right | `calc(100mm + var(--bleed))` | Front Cover |

### Panel Widths — Inside Spread (back.html)
| Panel | Width | Role |
|-------|-------|------|
| S2-Left | `calc(100mm + var(--bleed))` | Inside Left |
| S2-Centre | `100mm` | Inside Middle |
| S2-Right | `calc(97mm + var(--bleed))` | Inner Flap |

## Design Style: Corporate & Professional
- **Palette:** Navy `#1C244B`, Sky `#52B1E1`, Warm White `#FAFBFC`
- **Font:** Inter (400/500/600/700/800) — Google Fonts
- **Layout:** 6-column grid, Hero → Proof → CTA pattern, Z-pattern eye flow
- **Paper:** Silk/Satin coated 170 GSM (recommended)

## RULES (Non-negotiable)
1. **Language:** All visible text MUST be German (from the brief in `briefs/`)
2. **No web-native UI:** ZERO buttons, "Click here", "Download" — use QR codes + short URLs only
3. **Bleed:** 3mm on all edges — content that touches edge must extend into bleed
4. **Safe zone:** No text/logos within 6mm of canvas edge (3mm bleed + 3mm safety)
5. **Fold clearance:** No text within 5mm of fold lines
6. **Font sizes:** Body 10pt min, captions 8pt min — never smaller
7. **Images:** Use files from `assets/` — do NOT invent image paths
8. **CSS:** Use `:root` variables for all dimensions — never hardcode mm values for canvas/bleed

## Available Assets
- `gmsued_logo.png` — Company logo
- `v8_hero_building.png` — Generated hero (modern commercial glass building, Munich)
- `v8_texture_abstract.png` — Geometric hexagonal pattern (dark navy, for watermark overlays)
- `modern_commercial_building_1773758968165.png` — Alternative building photo
