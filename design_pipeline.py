#!/usr/bin/env python3
"""
GM Süd V8 Premium — 5-Agent NIM Design Pipeline
=================================================
Uses LiteLLM → Nvidia NIM (Nemotron 3 Super 120B) to run 5 sequential
agents that collaboratively design a DL tri-fold flyer from the brief.

Usage:
    export NVIDIA_NIM_API_KEY="nvapi-..."
    python3 design_pipeline.py

Output:
    src/v8-premium/front.html   (outside spread)
    src/v8-premium/back.html    (inside spread)
    src/v8-premium/index.css    (print stylesheet)
"""

import os, sys, json, textwrap
from pathlib import Path
from litellm import completion

# ── Config ──────────────────────────────────────────────────────────────
MODEL = "nvidia_nim/meta/llama-3.1-70b-instruct"
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src" / "v8-premium"
BRIEF_PATH = PROJECT_ROOT / "briefs" / "2025-03-28_FlyerBriefing-GM-Süd.txt"
FEEDBACK_PATH = PROJECT_ROOT / "briefs" / "feedback.txt"
CANVAS_PATH = PROJECT_ROOT.parent.parent / "templates" / "dl-trifold-canvas.html"

# Verify API key — LiteLLM expects NVIDIA_NIM_API_KEY
# but the user may have it as NVIDIA_API_KEY
if not os.environ.get("NVIDIA_NIM_API_KEY"):
    fallback = os.environ.get("NVIDIA_API_KEY", "")
    if fallback:
        os.environ["NVIDIA_NIM_API_KEY"] = fallback
        print("ℹ️   Mapped NVIDIA_API_KEY → NVIDIA_NIM_API_KEY for LiteLLM")
    else:
        print("❌  Set NVIDIA_NIM_API_KEY first:  export NVIDIA_NIM_API_KEY='nvapi-...'")
        sys.exit(1)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def call_agent(name: str, system: str, user: str, temperature: float = 0.7) -> str:
    """Call a NIM agent and return its response text."""
    print(f"\n{'='*60}")
    print(f"🤖  Agent: {name}")
    print(f"{'='*60}")
    resp = completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=temperature,
        max_tokens=8000,
    )
    text = resp.choices[0].message.content
    print(f"✅  {name} finished ({len(text)} chars)")
    return text

def save(filename: str, content: str):
    path = SRC_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"💾  Saved → {path}")


# ── Load Inputs ─────────────────────────────────────────────────────────
brief    = read(BRIEF_PATH)
feedback = read(FEEDBACK_PATH)
canvas   = read(CANVAS_PATH)

SHARED_CONTEXT = f"""
## PROJECT CONTEXT
You are part of a 5-agent design team creating a DL tri-fold (Wickelfalz) flyer for GM Süd GmbH, a German facility management company.

### Print Specs (MANDATORY — do NOT change these)
- Canvas: 303mm × 216mm (A4 landscape + 3mm bleed all sides)
- Trim: 297mm × 210mm
- CSS variables: --spread-w: 303mm; --spread-h: 216mm; --bleed: 3mm;
- Outside panels: Flap=97mm+bleed | BackCover=100mm | FrontCover=100mm+bleed
- Inside panels: InsideLeft=100mm+bleed | InsideCentre=100mm | InnerFlap=97mm+bleed
- Font: Inter 400/500/600/700/800 (Google Fonts)
- Palette: Navy #1C244B, Sky #52B1E1, Warm White #FAFBFC
- Body font min 10pt, captions min 8pt

### Available Assets (use these paths exactly)
- ../../assets/gmsued_logo.png — Company logo
- ../../assets/v8_hero_building.png — Hero (modern commercial glass building, Munich)
- ../../assets/v8_texture_abstract.png — Geometric hexagonal pattern (dark navy)

### Client Brief
{brief}

### Client Feedback (CRITICAL — address every point)
{feedback}

### Key Feedback Translation
- "Design noch nicht ansprechend, eher altmodisch" → Design is not appealing, looks OLD-FASHIONED
- "niemals dunkle Farben ohne weissen Rand am Rand" → NEVER dark colors without white border at the edge
- "zu unpersönlich, kein Faden, zuviel Groß geschrieben" → Too impersonal, no thread, TOO MUCH CAPITALISATION
- "Überschriften bitte wegnehmen" → REMOVE excessive headings
- "zuviel Text ohne Inhalt der mit uns verbindet" → Too much text without content that connects
- "Mehr Design Mut" → MORE DESIGN COURAGE
- "weniger Word Dokument Optik" → LESS Word-document look
- "verspielter, ohne volltöne" → More PLAYFUL, WITHOUT solid tones
- "es kann auch unser Haus als Hintergrund sein" → Building as background is fine

### Canvas Template
{canvas}
"""


# ═══════════════════════════════════════════════════════════════════════
# AGENT 1: Brief Analyst
# ═══════════════════════════════════════════════════════════════════════
agent1_output = call_agent(
    name="Brief Analyst",
    system=textwrap.dedent("""
    You are a German-language print design brief analyst.
    Your job is to:
    1. Parse the client brief + feedback and produce a PRECISE content map.
    2. Map each piece of text to exactly one of the 6 DL panels.
    3. Flag any feedback constraints that affect layout.
    4. Output a JSON structure with panel assignments.

    RULES:
    - ALL output text MUST be in German (from the brief, not invented)
    - Do NOT add headings the client didn't write — they asked to REMOVE excessive headings
    - Keep text personal, connected, concise
    - Respect the brief's page numbering (Seite 1 = Front Cover = S1-Right, etc.)

    Output format:
    ```json
    {
      "panels": {
        "s1_right_front_cover": { "role": "Front Cover", "headline": "...", "subline": "...", "body": "...", "cta": "...", "assets": ["logo", "hero_building"] },
        "s1_centre_back_cover": { "role": "Contact/CTA", ... },
        "s1_left_flap": { "role": "Zielgruppen", ... },
        "s2_left_inside": { "role": "Unternehmen + Leistungen", ... },
        "s2_centre_inside": { "role": "Leistungen Detail", ... },
        "s2_right_inner_flap": { "role": "USP/Warum GM Süd", ... }
      },
      "design_constraints": ["..."]
    }
    ```
    """),
    user=SHARED_CONTEXT,
    temperature=0.3,
)

# ═══════════════════════════════════════════════════════════════════════
# AGENT 2: Layout Architect
# ═══════════════════════════════════════════════════════════════════════
agent2_output = call_agent(
    name="Layout Architect",
    system=textwrap.dedent("""
    You are a senior print layout architect specialising in DL tri-fold flyers.
    You receive a content map from the Brief Analyst and the canvas template.

    Your job is to produce TWO complete HTML files:
    1. front.html — Outside spread (S1: Flap | Back Cover | Front Cover)
    2. back.html — Inside spread (S2: Inside Left | Inside Centre | Inner Flap)

    RULES:
    - Use the EXACT canvas template structure provided (panel classes, spread structure, fold guides)
    - Use the panel class names from the template: panel-s1-left, panel-s1-center, panel-s1-right, panel-s2-left, panel-s2-center, panel-s2-right
    - Link to index.css (same directory) — do NOT put styling in the HTML
    - Insert the EXACT German text from the content map — do NOT invent or translate
    - Use semantic HTML: h1 for the SINGLE main headline per cover, h2 sparingly, h3 for sub-items
    - Respect the client feedback: FEWER headings, more flowing text, personal tone
    - Include fold guides and spread labels from the template
    - Reference assets with ../../assets/ paths
    - Add meaningful CSS classes for the CSS Designer agent to target
    - Safe zone padding is handled by CSS — just use the panel structure
    - Include the debug grid script from the template

    Output format:
    ===FRONT_HTML_START===
    (complete front.html content)
    ===FRONT_HTML_END===
    ===BACK_HTML_START===
    (complete back.html content)
    ===BACK_HTML_END===
    """),
    user=f"{SHARED_CONTEXT}\n\n## Brief Analyst Output\n{agent1_output}",
    temperature=0.4,
)

# ═══════════════════════════════════════════════════════════════════════
# AGENT 3: CSS Designer
# ═══════════════════════════════════════════════════════════════════════
agent3_output = call_agent(
    name="CSS Designer",
    system=textwrap.dedent("""
    You are a world-class print CSS designer with a reputation for stunning, modern, PLAYFUL layouts.
    You receive the HTML from the Layout Architect and must produce a SINGLE index.css file.

    YOUR DESIGN PHILOSOPHY (from client feedback):
    - MORE DESIGN COURAGE — this is NOT a Word document
    - PLAYFUL — use asymmetry, overlapping elements, dynamic angles, unexpected white space
    - NO SOLID TONES at edges — use gradients, transparency, textures instead
    - WHITE BORDER at all edges — enforce via safe zone padding (6mm minimum from canvas edge)
    - Use the hero building image as a background with glassmorphism overlays
    - Use the abstract texture subtly (low opacity multiply blend)
    - Typography: varied weights and sizes to create visual rhythm, NOT uniform blocks
    - Cards with rounded corners, subtle shadows, frosted glass effects
    - Accent lines, decorative shapes (::before/::after pseudo-elements)
    - Process steps with numbered circles
    - Checkmark lists for USPs

    MANDATORY CSS TOKENS (use these exact values):
    :root {
        --spread-w: 303mm;
        --spread-h: 216mm;
        --bleed: 3mm;
    }

    Panel widths MUST match:
    - S1: .panel-s1-left = calc(97mm + var(--bleed)), .panel-s1-center = 100mm, .panel-s1-right = calc(100mm + var(--bleed))
    - S2: .panel-s2-left = calc(100mm + var(--bleed)), .panel-s2-center = 100mm, .panel-s2-right = calc(97mm + var(--bleed))

    Include:
    - @import for Inter font
    - Print @media overrides (hide guides, shadows, outlines)
    - @page size rule
    - All component styling for the HTML classes

    Output ONLY the CSS file content, nothing else. Start with the @import line.
    """),
    user=f"{SHARED_CONTEXT}\n\n## Layout HTML\n{agent2_output}",
    temperature=0.6,
)

# ═══════════════════════════════════════════════════════════════════════
# AGENT 4: Content QA (German Copy Auditor)
# ═══════════════════════════════════════════════════════════════════════
agent4_output = call_agent(
    name="Content QA",
    system=textwrap.dedent("""
    You are a German-language copy editor and print QA specialist.
    You review the HTML output for:
    1. German text accuracy — compare EVERY line against the original brief
    2. Excessive capitalisation — flag any ALL-CAPS or unnecessary uppercase
    3. Heading count — the client wants FEWER headings
    4. Personal tone — text should feel warm, connected, not corporate boilerplate
    5. Print safety — no text within 6mm of canvas edge, minimum 10pt body text
    6. Asset paths — must use ../../assets/ prefix
    7. Panel widths — must match the spec exactly

    Output a JSON report:
    ```json
    {
      "status": "PASS" or "NEEDS_FIXES",
      "issues": [
        { "file": "front.html", "line": "...", "issue": "...", "fix": "..." }
      ],
      "fixed_front_html": "... (only if NEEDS_FIXES, the corrected HTML)",
      "fixed_back_html": "... (only if NEEDS_FIXES, the corrected HTML)"
    }
    ```

    If status is PASS, omit the fixed_html fields.
    If status is NEEDS_FIXES, include the COMPLETE corrected HTML files.
    """),
    user=f"{SHARED_CONTEXT}\n\n## HTML to Review\n{agent2_output}\n\n## CSS\n{agent3_output}",
    temperature=0.2,
)

# ═══════════════════════════════════════════════════════════════════════
# AGENT 5: Final Assembler & Polish
# ═══════════════════════════════════════════════════════════════════════
agent5_output = call_agent(
    name="Final Assembler",
    system=textwrap.dedent("""
    You are the final assembler. You receive the output from all previous agents
    and produce the FINAL, PRODUCTION-READY files.

    You must output exactly THREE blocks:

    ===FINAL_FRONT_HTML===
    (complete front.html — use QA-corrected version if available, otherwise Layout Architect version)
    ===END_FINAL_FRONT_HTML===

    ===FINAL_BACK_HTML===
    (complete back.html — same logic)
    ===END_FINAL_BACK_HTML===

    ===FINAL_CSS===
    (complete index.css from CSS Designer)
    ===END_FINAL_CSS===

    RULES:
    - EVERY file must be complete and valid (no placeholders, no truncation)
    - HTML files must link to index.css
    - All German text must be exactly from the brief
    - Incorporate any QA fixes
    - CSS must include ALL the premium styling from Agent 3
    - Do NOT add comments like "rest of CSS here" — include EVERYTHING
    """),
    user=f"""
## Brief Analyst Content Map
{agent1_output}

## Layout Architect HTML
{agent2_output}

## CSS Designer Stylesheet
{agent3_output}

## Content QA Report
{agent4_output}

{SHARED_CONTEXT}
""",
    temperature=0.2,
)


# ── Extract & Save Files ────────────────────────────────────────────────
def extract_between(text: str, start: str, end: str) -> str:
    """Extract content between two markers."""
    s = text.find(start)
    e = text.find(end)
    if s == -1 or e == -1:
        return ""
    return text[s + len(start):e].strip()

front = extract_between(agent5_output, "===FINAL_FRONT_HTML===", "===END_FINAL_FRONT_HTML===")
back  = extract_between(agent5_output, "===FINAL_BACK_HTML===", "===END_FINAL_BACK_HTML===")
css   = extract_between(agent5_output, "===FINAL_CSS===", "===END_FINAL_CSS===")

if front:
    save("front.html", front)
else:
    print("⚠️  Could not extract front.html from Agent 5 output")
    print("    Saving raw Agent 2 output for inspection...")
    save("front_raw.txt", agent2_output)

if back:
    save("back.html", back)
else:
    print("⚠️  Could not extract back.html from Agent 5 output")
    save("back_raw.txt", agent2_output)

if css:
    save("index.css", css)
else:
    print("⚠️  Could not extract index.css from Agent 5 output")
    save("css_raw.txt", agent3_output)


print(f"\n{'='*60}")
print("🎉  Pipeline complete!")
print(f"{'='*60}")
print(f"Files saved to: {SRC_DIR}")
print("Open front.html and back.html in a browser to review.")
print("Use Cmd+G to toggle fold/bleed debug guides.")
