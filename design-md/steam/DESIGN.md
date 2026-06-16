# Steam Design System

> Digital gaming distribution platform with dark, immersive aesthetic. Navy blue gradients (#1b2838), Steam cyan accent (#66c0f4), and commerce-focused UI patterns for the world's largest PC gaming storefront.

A complete, AI-readable specification, structured by atomic design (atoms → molecules → organisms → templates). Drop this file into a project and an agent can rebuild the Steam visual language end to end. Ground-truth against the live site: **https://store.steampowered.com**

---

## 0. How to use this

Feed this file to an AI coding agent (Claude Code, Cursor, v0) as the design source of truth. Build from the atoms up: apply the tokens, assemble the molecules, then lay out the organisms and templates. When in doubt, check the source site above.

## 1. Visual Theme & Atmosphere

Anchor every surface on the neutral ramp and let the brand accent (`#1B2838`) carry the single most important action in any view. Surfaces stay quiet so content, data and imagery lead. Depth comes from hairline borders and restrained shadow, never heavy chrome. Every interactive element resolves to a documented token below.

---

# ATOMS — tokens

## 2. Brand Palette

The defining brand colours, as specified.

| Token | Hex | Role |
|-------|-----|------|
| `--background-darkest` | `#171A21` | Brand palette |
| `--background-primary` | `#1B2838` | Brand palette |
| `--background-secondary` | `#2A475E` | Brand palette |
| `--background-tertiary` | `#1E3A4C` | Brand palette |
| `--background-modal` | `#171D25` | Brand palette |
| `--background-input` | `#32465A` | Brand palette |
| `--accent-primary` | `#66C0F4` | Brand palette |
| `--accent-hover` | `#67C1F5` | Brand palette |
| `--accent-light` | `#A5D7F7` | Brand palette |
| `--accent-dark` | `#417A9B` | Brand palette |
| `--purchase-green` | `#5C7E10` | Brand palette |
| `--purchase-green-hover` | `#6D8F1A` | Brand palette |
| `--wishlist-blue` | `#4C6B8A` | Brand palette |
| `--text-primary` | `#C7D5E0` | Brand palette |
| `--text-secondary` | `#8F98A0` | Brand palette |
| `--text-muted` | `#6B7785` | Brand palette |
| `--text-bright` | `#FFFFFF` | Brand palette |
| `--text-price` | `#ACDBF5` | Brand palette |
| `--text-discount` | `#A4D007` | Brand palette |
| `--status-online` | `#57CBDE` | Brand palette |
| `--status-in-game` | `#90BA3C` | Brand palette |
| `--status-away` | `#A0A0A0` | Brand palette |
| `--status-offline` | `#636363` | Brand palette |
| `--review-negative` | `#A34C25` | Brand palette |

### Action
| Token | Hex | Role |
|-------|-----|------|
| `--primary` | `#1B2838` | Primary CTA, active state, brand signal |
| `--primary-hover` | `#16202D` | Hover / pressed state |
| `--on-primary` | `#FFFFFF` | Text/icon on primary fill |
| `--ink` | `#0a0a0c` | Primary text and headings |
| `--canvas` | `#FFFFFF` | Page background |

### Neutral ramp
| Token | Hex | Role |
|-------|-----|------|
| `--neutral-900` | `#0F172A` | Strong text |
| `--neutral-700` | `#334155` | Body text |
| `--neutral-500` | `#64748B` | Secondary text |
| `--neutral-400` | `#94A3B8` | Placeholder, disabled |
| `--neutral-300` | `#CBD5E1` | Strong borders |
| `--neutral-200` | `#E2E8F0` | Default borders, dividers |
| `--neutral-100` | `#F1F5F9` | Sunken fields, hover rows |
| `--neutral-50` | `#F8FAFC` | Subtle surface |

### Semantic states
| Token | Hex | Role |
|-------|-----|------|
| `--success` | `#16A34A` | Success, healthy, passing |
| `--warning` | `#F59E0B` | Warning, pending |
| `--error` | `#DC2626` | Error, destructive |
| `--info` | `#2563EB` | Links, informational |
| `--focus-ring` | `#1B2838` | 2px focus outline (3:1 min) |

## 3. Typography

```css
--font-display: Motiva Sans Bold;
--font-sans: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
--font-mono: Consolas, Monaco, "Courier New", monospace;
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
--radius-sm: 8px; --radius-md: 14px; --radius-lg: 16px; --radius-xl: 24px; --radius-full: 999px;
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

Build like Steam: Digital gaming distribution platform with dark, immersive aesthetic. Navy blue gradients (#1b2838), Steam cyan accent (#66c0f4), and commerce-focused UI patterns for the world's largest PC gaming storefront. Anchor on the neutral ramp, use `--primary` (`#1B2838`) for the single key action, render the navigation, hero and footer as specified, and apply the documented type, spacing, radius, motion and accessibility tokens throughout.
