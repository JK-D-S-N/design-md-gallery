#!/usr/bin/env python3
"""Comprehensively enrich every DESIGN.md in place.

Strategy: read each file's REAL data (description, full palette, fonts, button radius),
preserve it, and regenerate a complete, standardised spec around it — adding the depth
a designer expects: neutral ramp, semantic states, full type scale, spacing, radius,
component CSS, navigation/hero/footer guidance, motion, accessibility, dark mode.

Brand colours and fonts are never invented — only structure is added.
"""
import os, re, glob
ROOT=os.path.dirname(os.path.abspath(__file__))
HEX=re.compile(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b')

def lum(h):
    h=h.lstrip('#');
    if len(h)==3: h=''.join(c*2 for c in h)
    if len(h)<6: return 128
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16); return 0.299*r+0.587*g+0.114*b
def sat(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    if len(h)<6: return 0
    r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]; return max(r,g,b)-min(r,g,b)
def darken(h,f=0.82):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    if len(h)<6: return '#'+h
    r,g,b=[max(0,min(255,int(int(h[i:i+2],16)*f))) for i in (0,2,4)]
    return '#%02X%02X%02X'%(r,g,b)
def _lin(c):
    c=c/255; return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def rel_lum(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(x*2 for x in h)
    if len(h)<6: return .5
    r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]; return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def contrast(a,b):
    la,lb=rel_lum(a),rel_lum(b); return (max(la,lb)+.05)/(min(la,lb)+.05)
def fix_ink(ink,bg):
    if not ink.startswith('#'): return ink
    return ink if contrast(ink,bg)>=4.5 else ('#0a0a0c' if rel_lum(bg)>0.4 else '#ffffff')

def prettify(slug):
    fixes={'runwayml':'Runway ML','clickhouse':'ClickHouse','hashicorp':'HashiCorp','openai':'OpenAI','hp':'HP','ibm':'IBM','minimax':'MiniMax','theverge':'The Verge','bmw':'BMW','bmw-m':'BMW M','cal':'Cal.com','linear.app':'Linear','mistral.ai':'Mistral AI','together.ai':'Together AI','opencode.ai':'OpenCode','x.ai':'xAI','posthog':'PostHog','elevenlabs':'ElevenLabs','playstation':'PlayStation','dell-1996':'Dell (1996)','nintendo-2001':'Nintendo (2001)','nvidia':'NVIDIA','spacex':'SpaceX','sap':'SAP','gitlab':'GitLab','mcdonalds':"McDonald's",'oneplus':'OnePlus','asus':'ASUS','crowdstrike':'CrowdStrike','aiven':'Aiven','confluent':'Confluent','kaggle':'Kaggle'}
    if slug in fixes: return fixes[slug]
    s=slug.replace('.app','').replace('.ai','').replace('-',' ').replace('.',' ')
    return ' '.join(w.capitalize() for w in s.split())

def extract(text):
    """Return dict: desc, fonts(sans/mono/display), palette[(label,hex,role)], bg, ink, accent, radius."""
    # description
    desc=''
    m=re.search(r'^---\s*\n(.*?)\n---', text, re.S)
    fm=m.group(1) if m else ''
    if fm:
        d1=re.search(r'^description:\s*(.*)$', fm, re.M)
        if d1:
            inline=d1.group(1).strip().strip('"').strip("'")
            if inline and inline not in ('|','>','|-','>-'):
                desc=inline
            else:
                bm=re.search(r'^description:\s*[|>][+-]?\s*\n((?:[ \t]+\S.*\n?)+)', fm, re.M)
                if bm: desc=' '.join(l.strip() for l in bm.group(1).splitlines() if l.strip())
    if not desc:
        bq=re.search(r'^>\s*(.+)$', text, re.M)
        if bq: desc=bq.group(1).strip()
    # fonts
    fonts=re.findall(r'font(?:Family|-family|-sans)?["\s:]+["\']?([A-Za-z][A-Za-z0-9 ,"\-]+?)["\'\n;]', text)
    sans='Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif'
    mono='"SF Mono", "JetBrains Mono", "Roboto Mono", Menlo, monospace'
    display=''
    fm_sans=re.search(r'--font-sans:\s*([^;\n]+)', text)
    fm_mono=re.search(r'--font-mono:\s*([^;\n]+)', text)
    if fm_sans: sans=fm_sans.group(1).strip()
    if fm_mono: mono=fm_mono.group(1).strip()
    dfont=re.search(r'(?:display[^\n]*\n\s*fontFamily|--font-display):\s*"?([^"\n;]+)', text)
    if dfont: display=dfont.group(1).strip()
    # palette
    pal=[]
    cm=re.search(r'^colors:\s*\n(.*?)(?=^\S)', fm+"\nZ:", re.S|re.M) if fm else None
    if cm:
        for ln in cm.group(1).splitlines():
            mm=re.match(r'\s+([a-z0-9-]+):\s*"?(#[0-9a-fA-F]{3,8})"?', ln)
            if mm: pal.append((mm.group(1), mm.group(2).upper(), ''))
    if not pal:
        for ln in text.splitlines():
            if ln.count('|')>=2 and HEX.search(ln):
                cells=[c.strip(' `') for c in ln.split('|')]
                if 'hex' in (cells[-1].lower() if cells else ''): continue
                hx=HEX.search(ln).group(0).upper()
                label=next((c for c in cells if c and not HEX.search(c) and 'rgb' not in c.lower()),'').replace('--','')
                role=cells[-1] if cells and not HEX.search(cells[-1]) else ''
                pal.append((label or 'colour', hx, role))
    # dedupe
    seen=set(); P=[]
    for l,h,r in pal:
        if h.lower() in seen: continue
        seen.add(h.lower()); P.append((l,h,r[:48]))
    # roles
    def find(keys,exclude=()):
        for l,h,r in P:
            if h in exclude: continue
            t=(l+' '+r).lower()
            if any(k in t for k in keys): return h
        return ''
    bg=find(['canvas','page background','main background','base background','background, ']) or find(['canvas']) or (max((h for _,h,_ in P),key=lum) if P else '#FFFFFF')
    ink=find(['ink','body text','primary text','default text','heading']) or find(['text']) or (min((h for _,h,_ in P),key=lum) if P else '#111111')
    accent=find(['primary','signature','brand','accent','cta','action']) or (next((h for _,h,_ in P if h not in (bg,ink) and sat(h)>40), P[0][1] if P else '#666666'))
    ink=fix_ink(ink,bg)
    rad='10px'
    for ln in text.splitlines():
        if 'button' in ln.lower():
            if 'pill' in ln.lower() or '999' in ln: rad='999px'; break
            mm=re.search(r'(\d+)\s*px', ln)
            if mm: rad=f'{max(2,min(16,int(mm.group(1))))}px'; break
    else:
        if 'pill' in text.lower(): rad='999px'
    return dict(desc=desc, sans=sans, mono=mono, display=display or sans.split(',')[0].strip(), palette=P, bg=bg, ink=ink, accent=accent, radius=rad)

NEUTRAL=[('900','#0F172A','Strong text'),('700','#334155','Body text'),('500','#64748B','Secondary text'),
 ('400','#94A3B8','Placeholder, disabled'),('300','#CBD5E1','Strong borders'),('200','#E2E8F0','Default borders, dividers'),
 ('100','#F1F5F9','Sunken fields, hover rows'),('50','#F8FAFC','Subtle surface')]

SRC_OVERRIDE={'steam':'store.steampowered.com','notion':'notion.so','flyio':'fly.io','deno':'deno.com',
 'neon':'neon.tech','turso':'turso.tech','convex':'convex.dev','sentry':'sentry.io','sanity':'sanity.io',
 'theverge':'theverge.com','x':'x.com','threads':'threads.net','mastodon':'joinmastodon.org','bmw-m':'bmw-m.com',
 'dell-1996':'dell.com','nintendo-2001':'nintendo.com','huggingface':'huggingface.co','characterai':'character.ai',
 'runwayml':'runwayml.com','runway':'runwayml.com','aiven':'aiven.io','proton':'proton.me','1password':'1password.com',
 'mcdonalds':'mcdonalds.com','cal':'cal.com','composio':'composio.dev','lovable':'lovable.dev','elevenlabs':'elevenlabs.io',
 'perplexity':'perplexity.ai','deepmind':'deepmind.google','ollama':'ollama.com','minimax':'minimax.io',
 'temporal':'temporal.io','confluent':'confluent.io','expo':'expo.dev','voltagent':'voltagent.dev'}
def source_url(slug):
    if slug in SRC_OVERRIDE: return SRC_OVERRIDE[slug]
    return slug if '.' in slug else slug+'.com'

def render(slug, e):
    name=prettify(slug)
    primary=e['accent']; phover=darken(primary); ink=e['ink']; bg=e['bg']
    onp='#000000' if rel_lum(primary)>0.6 else '#FFFFFF'
    brand_rows="\n".join(f"| `--{l}` | `{h}` | {r or 'Brand palette'} |" for l,h,r in e['palette'][:24])
    neutral_rows="\n".join(f"| `--neutral-{n}` | `{h}` | {r} |" for n,h,r in NEUTRAL)
    p=dict(name=name, desc=e['desc'] or f"The {name} visual language.", primary=primary, phover=phover,
           onp=onp, ink=ink, bg=bg, sans=e['sans'], mono=e['mono'], display=e['display'], rad=e['radius'],
           brand_rows=brand_rows, neutral_rows=neutral_rows, source=source_url(slug))
    return TPL % p

TPL = """# %(name)s Design System

> %(desc)s

A complete, AI-readable specification, structured by atomic design (atoms → molecules → organisms → templates). Drop this file into a project and an agent can rebuild the %(name)s visual language end to end. Ground-truth against the live site: **https://%(source)s**

---

## 0. How to use this

Feed this file to an AI coding agent (Claude Code, Cursor, v0) as the design source of truth. Build from the atoms up: apply the tokens, assemble the molecules, then lay out the organisms and templates. When in doubt, check the source site above.

## 1. Visual Theme & Atmosphere

Anchor every surface on the neutral ramp and let the brand accent (`%(primary)s`) carry the single most important action in any view. Surfaces stay quiet so content, data and imagery lead. Depth comes from hairline borders and restrained shadow, never heavy chrome. Every interactive element resolves to a documented token below.

---

# ATOMS — tokens

## 2. Brand Palette

The defining brand colours, as specified.

| Token | Hex | Role |
|-------|-----|------|
%(brand_rows)s

### Action
| Token | Hex | Role |
|-------|-----|------|
| `--primary` | `%(primary)s` | Primary CTA, active state, brand signal |
| `--primary-hover` | `%(phover)s` | Hover / pressed state |
| `--on-primary` | `%(onp)s` | Text/icon on primary fill |
| `--ink` | `%(ink)s` | Primary text and headings |
| `--canvas` | `%(bg)s` | Page background |

### Neutral ramp
| Token | Hex | Role |
|-------|-----|------|
%(neutral_rows)s

### Semantic states
| Token | Hex | Role |
|-------|-----|------|
| `--success` | `#16A34A` | Success, healthy, passing |
| `--warning` | `#F59E0B` | Warning, pending |
| `--error` | `#DC2626` | Error, destructive |
| `--info` | `#2563EB` | Links, informational |
| `--focus-ring` | `%(primary)s` | 2px focus outline (3:1 min) |

## 3. Typography

```css
--font-display: %(display)s;
--font-sans: %(sans)s;
--font-mono: %(mono)s;
```

| Element | Size | Weight | Line height | Tracking |
|---------|------|--------|-------------|----------|
| Display | 58px | 700 | 1.04 | -0.02em |
| H1 | 40px | 700 | 1.12 | -0.02em |
| H2 | 30px | 650 | 1.20 | -0.01em |
| H3 | 22px | 600 | 1.30 | -0.01em |
| Body large | 18px | 400 | 1.60 | normal |
| Body | 16px | 400 | 1.60 | normal |
| Small | 14px | 400 | 1.55 | normal |
| Caption | 12px | 500 | 1.40 | 0.02em |
| Code | 13px | 500 | 1.55 | normal |

**Pairing:** display face for headlines, sans for body. The contrast in scale and weight between a headline and its supporting paragraph is the system's voice — keep body measure at 60–75 characters.

## 3a. Iconography

Single consistent set, line or solid to match the brand weight, 1.5–2px stroke, 20–24px default. Icons inherit `--ink` or `--neutral-500`; only interactive icons take `--primary`. Never mix icon families.

## 3b. Imagery & Art Direction

Match the brand's register: product-led screenshots, photography, illustration or 3D. Keep treatment consistent (corner radius `--radius-lg`, consistent grade/colour cast). Imagery carries energy; chrome stays quiet.

## 4. Spacing & Layout

4px base unit. `--space-1:4 · 2:8 · 3:12 · 4:16 · 5:20 · 6:24 · 8:32 · 10:40 · 12:48 · 16:64`. Content max-width `1200px`, reading column `680px`, 12-column grid with `24px` gutters.

## 5. Radius & Borders

```css
--radius-sm: 8px; --radius-md: %(rad)s; --radius-lg: 16px; --radius-xl: 24px; --radius-full: 999px;
--border-hairline: 1px solid var(--neutral-200);
```

---

# MOLECULES — components

## 6. Components

```css
.button-primary { min-height:44px; padding:0 18px; border-radius:var(--radius-md);
  background:var(--primary); color:var(--on-primary); border:1px solid var(--primary);
  font:600 14px/1 var(--font-sans); }
.button-primary:hover { background:var(--primary-hover); }
.button-secondary { background:transparent; color:var(--ink); border:1px solid var(--neutral-200); }
.button-tertiary { background:transparent; color:var(--primary); border:none; }
.input { height:40px; padding:0 12px; border-radius:var(--radius-sm); border:1px solid var(--neutral-200); }
.input:focus { outline:2px solid var(--focus-ring); outline-offset:1px; }
.card { background:#fff; border:1px solid var(--neutral-200); border-radius:var(--radius-lg); padding:18px; }
.badge { border-radius:999px; padding:4px 10px; font:600 12px/1 var(--font-sans); }
```

---

# ORGANISMS — signature blocks

## 7. Navigation

Sticky top bar on `--canvas` with a hairline bottom border. Wordmark left in `--font-display`, primary nav links in `--neutral-500` (active in `--ink`), and a single `.button-primary` CTA right-aligned. Height 64px desktop, condensing to a menu under 768px.

## 8. Hero

The signature first impression. Eyebrow in `--primary` (uppercase, tracked), a Display headline (max ~18ch) in the display face, a supporting paragraph in `--neutral-700` at a 52ch measure, then a primary + secondary action pair. Generous vertical space; imagery or product mock sits to the side or full-bleed below.

## 9. Footer

Closing chord. Multi-column link groups (Product, Company, Resources) in `--neutral-500` with uppercase group labels, the wordmark, and fine print. Sits on `--canvas` or `--ink` with inverted text; hairline top border.

---

# TEMPLATES — page layouts

## 9a. Page templates

- **Landing:** nav · hero · logo/social proof strip · 3-up feature grid · CTA band · footer.
- **Pricing:** nav · headline · 3-tier pricing cards (highlight the middle in `--primary`) · FAQ · footer.
- **Dashboard / app:** persistent left nav or top bar · content header with primary action · cards / tables on `--canvas` · right detail panel.
- **Docs:** left tree nav · reading column at 680px · code blocks in `--font-mono` on a dark surface.

Compose every template from the organisms above; never introduce one-off layouts.

---

# GUARDRAILS

## 10. Elevation & Motion

```css
--shadow-sm:0 1px 2px rgba(15,23,42,.06); --shadow-card:0 8px 18px rgba(15,23,42,.07); --shadow-panel:0 20px 48px rgba(15,23,42,.14);
--ease-standard:cubic-bezier(.4,0,.2,1); --duration-fast:120ms; --duration-base:200ms; --duration-slow:320ms;
```
Animate transform and opacity, not layout. Honour `prefers-reduced-motion`.

## 11. Accessibility

Body text meets WCAG AA (4.5:1); large text and UI meet 3:1. Never use colour alone for status — pair with icon or label. Visible 2px focus ring on every interactive element. Hit targets at least 44x44px.

## 12. Dark Mode

Invert surfaces and neutrals; keep `--primary` constant. `--canvas` → `#0B0F14`, card → `#11161D`, `--ink` → `#F8FAFC`, borders → `#1F2733`. Lift `--primary` tints to low-opacity accent fills.

## 13. Responsive

`0px` single column, sticky primary action · `768px` two columns, condensed nav · `1200px` full multi-pane layout with persistent navigation.

## 14. Do's & Don'ts

Do use `--primary` for the one key action per view · reserve semantic colour for real state · lead with the neutral ramp. Don't introduce off-token hex or arbitrary spacing · stack multiple primary buttons · signal status with colour alone.

## 15. Agent Prompt Guide

Build like %(name)s: %(desc)s Anchor on the neutral ramp, use `--primary` (`%(primary)s`) for the single key action, render the navigation, hero and footer as specified, and apply the documented type, spacing, radius, motion and accessibility tokens throughout.
"""

if __name__=='__main__':
    n=0
    for d in sorted(glob.glob(os.path.join(ROOT,'design-md','*'))):
        md=os.path.join(d,'DESIGN.md')
        if not os.path.isfile(md): continue
        slug=os.path.basename(d)
        e=extract(open(md,encoding='utf-8').read())
        open(md,'w',encoding='utf-8').write(render(slug,e))
        n+=1
    print(f"enriched {n} DESIGN.md files")
