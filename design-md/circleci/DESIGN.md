# CircleCI Design System

> A CI/CD platform built around pipeline status clarity. Near-black surfaces host code and logs; green signals validation and successful delivery, while red and yellow are reserved exclusively for pipeline states and failures.

---

## 1. Visual Theme & Atmosphere

CircleCI pairs a clean light canvas with a single load-bearing brand accent and a disciplined neutral ramp. Surfaces stay quiet so product data, code and status carry the meaning. Depth is communicated with hairline borders and soft shadows rather than heavy chrome, and every interactive element resolves to one of the documented tokens below.

## 2. Color Palette & Roles

### Brand & action
| Token | Hex | Role |
|-------|-----|------|
| `--primary` | `#00B871` | Primary CTA, active state, brand signal |
| `--primary-hover` | `#008F5A` | Hover / pressed state for primary |
| `--primary-subtle` | `#E9F9F1` | Tinted callout / selected background |
| `--on-primary` | `#FFFFFF` | Text/icon on primary fill |
| `--circle-red` | `#DC2626` | Failed build |
| `--circle-yellow` | `#F59E0B` | Running / queued state |
| `--circle-black` | `#111111` | Hero and code/log surface |

### Neutrals (text, surfaces, borders)
| Token | Hex | Role |
|-------|-----|------|
| `--ink` | `#111111` | Primary text, headings, dark surfaces |
| `--neutral-900` | `#0F172A` | Strong text |
| `--neutral-700` | `#334155` | Body text |
| `--neutral-500` | `#64748B` | Secondary text, captions |
| `--neutral-400` | `#94A3B8` | Placeholder, disabled text |
| `--neutral-300` | `#CBD5E1` | Strong borders |
| `--neutral-200` | `#E2E8F0` | Default borders, dividers, inputs |
| `--neutral-100` | `#F1F5F9` | Sunken fields, hover rows |
| `--surface-page` | `#F8FAFC` | Page background |
| `--surface-card` | `#FFFFFF` | Cards, panels, tables |
| `--surface-raised` | `#FFFFFF` | Modals, popovers, menus |

### Semantic states
| Token | Hex | Role |
|-------|-----|------|
| `--success` | `#16A34A` | Success, healthy, passing |
| `--success-subtle` | `#DCFCE7` | Success background |
| `--warning` | `#F59E0B` | Warning, pending, queued |
| `--warning-subtle` | `#FEF3C7` | Warning background |
| `--error` | `#DC2626` | Error, failed, destructive |
| `--error-subtle` | `#FEE2E2` | Error background |
| `--info` | `#2563EB` | Links, informational |
| `--focus-ring` | `#00B871` | 2px focus outline (3:1 min against surface) |

## 3. Typography

```css
--font-sans: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
--font-mono: "SF Mono", "JetBrains Mono", "Roboto Mono", Menlo, monospace;
```

| Element | Size | Weight | Line height | Tracking |
|---------|------|--------|-------------|----------|
| Display | 58px | 700 | 1.04 | -0.02em |
| H1 / Page title | 40px | 700 | 1.12 | -0.02em |
| H2 / Section | 30px | 650 | 1.20 | -0.01em |
| H3 | 22px | 600 | 1.30 | -0.01em |
| H4 | 18px | 600 | 1.35 | normal |
| Body large | 18px | 400 | 1.60 | normal |
| Body | 16px | 400 | 1.60 | normal |
| Body small | 14px | 400 | 1.55 | normal |
| Caption | 12px | 500 | 1.40 | 0.02em |
| Code | 13px | 500 | 1.55 | normal |

## 4. Spacing & Layout Grid

4px base unit. Use the ramp; never arbitrary values.

| Token | Value | Token | Value |
|-------|-------|-------|-------|
| `--space-1` | 4px | `--space-6` | 24px |
| `--space-2` | 8px | `--space-8` | 32px |
| `--space-3` | 12px | `--space-10` | 40px |
| `--space-4` | 16px | `--space-12` | 48px |
| `--space-5` | 20px | `--space-16` | 64px |

Content max-width `1200px`; reading column `680px`; 12-column grid with `24px` gutters.

## 5. Radius & Borders

```css
--radius-sm: 8px;   /* inputs, badges */
--radius-md: 10px;  /* buttons, controls */
--radius-lg: 16px;  /* cards, panels */
--radius-xl: 24px;  /* feature surfaces */
--radius-full: 999px;
--border-hairline: 1px solid var(--neutral-200);
```

## 6. Components

```css
.button-primary { min-height: 44px; padding: 0 18px; border-radius: var(--radius-md);
  background: var(--primary); color: var(--on-primary); border: 1px solid var(--primary);
  font: 600 14px/1 var(--font-sans); }
.button-primary:hover { background: var(--primary-hover); border-color: var(--primary-hover); }
.button-secondary { min-height: 44px; padding: 0 18px; border-radius: var(--radius-md);
  background: var(--surface-card); color: var(--ink); border: 1px solid var(--neutral-200); }
.button-ghost { background: transparent; color: var(--ink); border: 1px solid transparent; }
.input { height: 40px; padding: 0 12px; border-radius: var(--radius-sm);
  border: 1px solid var(--neutral-200); background: var(--surface-card); color: var(--ink); }
.input:focus { outline: 2px solid var(--focus-ring); outline-offset: 1px; border-color: var(--primary); }
.card { background: var(--surface-card); border: 1px solid var(--neutral-200);
  border-radius: var(--radius-lg); padding: 18px; }
.badge { border-radius: var(--radius-full); padding: 4px 10px; font: 500 12px/1 var(--font-sans); }
.badge-success { background: var(--success-subtle); color: #15803D; }
.table { width: 100%; border-collapse: collapse; }
.table th { text-align: left; font: 600 12px/1.4 var(--font-sans); color: var(--neutral-500); }
.table td { border-top: 1px solid var(--neutral-200); padding: 12px 0; }
.code-block { background: var(--ink); color: #fff; border-radius: var(--radius-lg);
  padding: 16px; font: 500 13px/1.55 var(--font-mono); }
```

## 7. Elevation & Shadows

```css
--shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
--shadow-card: 0 8px 18px rgba(15, 23, 42, 0.07);
--shadow-panel: 0 20px 48px rgba(15, 23, 42, 0.14);
```

Elevate sparingly: cards rest on the page, only menus, popovers and modals lift.

## 8. Motion & Transitions

```css
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
--ease-emphasis: cubic-bezier(0.2, 0, 0, 1);
--duration-fast: 120ms;   /* hover, focus */
--duration-base: 200ms;   /* most UI */
--duration-slow: 320ms;   /* overlays, sheets */
```

Animate transform and opacity, not layout. Honour `prefers-reduced-motion`.

## 9. Accessibility

- Body text meets WCAG AA (4.5:1); large text and UI meet 3:1.
- Never use colour alone for status — pair with an icon or label.
- Visible 2px focus ring on every interactive element; never remove focus styles.
- Hit targets at least 44x44px; respect `prefers-reduced-motion` and `prefers-color-scheme`.

## 10. Dark Mode

| Token | Light | Dark |
|-------|-------|------|
| `--surface-page` | `#F8FAFC` | `#0B0F14` |
| `--surface-card` | `#FFFFFF` | `#11161D` |
| `--ink` | `#111111` | `#F8FAFC` |
| `--neutral-200` | `#E2E8F0` | `#1F2733` |
| `--primary` | `#00B871` | `#00B871` |

Keep the brand accent constant; invert surfaces and neutrals, and lift `--primary-subtle` to a low-opacity tint of the accent.

## 11. Responsive Behavior

| Breakpoint | Min width | Behavior |
|------------|-----------|----------|
| Mobile | `0px` | Single column, stacked panels, sticky primary action |
| Tablet | `768px` | Two-column layouts, condensed navigation |
| Desktop | `1200px` | Full multi-pane console with persistent navigation |

## 12. Do's and Don'ts

- Do use `--primary` for the single most important action per view.
- Do reserve semantic colours for real state, never decoration.
- Do lead with the neutral ramp; let the accent punctuate.
- Don't introduce off-ramp hex values or arbitrary spacing.
- Don't stack multiple primary buttons in one region.
- Don't communicate status with colour alone.

## 13. Agent Prompt Guide

Build like CircleCI: A CI/CD platform built around pipeline status clarity. Near-black surfaces host code and logs; green signals validation and successful delivery, while red and yellow are reserved exclusively for pipeline states and failures. Anchor every surface on the neutral ramp, use `--primary` (`#00B871`) for the single key action, reserve semantic colours for true state, and apply the documented type, spacing, radius, motion and accessibility tokens throughout.
