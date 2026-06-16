# design.md — Product Requirements

_Working PRD. Updated 2026-06-17 (overnight session)._

## The problem

AI agents can build almost any UI now. What they can't do is **taste**. Point Claude Code or Cursor at a blank project and it produces generic, soulless screens, because it has no design point of view to build from. Designers know this; the missing input is a **design system the agent can read**.

A `DESIGN.md` solves that: a single plain-markdown file describing a visual language (colour, type, spacing, components, layouts) that an agent reads to build every screen consistently. The format is emerging fast. But there's no good way to **find, compare, judge or generate** them. The existing collections are README link-dumps made by developers, token lists with no soul, no preview, no fidelity to the real brand.

## What we're solving

**Give AI builders a fast way to find or generate a design system they'd actually ship with.** Browse a look, see it rendered faithfully, judge it, copy the file, drop it in, build. And when the look you want isn't in the library, **point at any URL and generate it.**

## Who it's for

The **forward-deployed creative** — the person shipping real products with agents who carries taste into the build. Designers who code, engineers with an eye, solo founders, agency teams. They don't want a token dump; they want "make it look like *this*" to actually work.

## The core insight (validated tonight)

A generic, token-driven preview **does not** look like the brand. We rendered Steam from extracted tokens and got a *white* site, when Steam is dark navy with a blue-gradient CTA. Fidelity lives in the specifics: the real nav items, the gradient buttons, the hero composition, the actual canvas.

So the product has two tiers:
- **Flagship tier** — brands rendered with real component fidelity (nav, hero, footer, button hierarchy, type), checked against the live site. Proven on **Steam (9/10), Linear (9/10), Stripe (8.5/10), Notion (8/10)**.
- **Long tail** — token-level approximations, honestly framed as "palette + type impression", not a clone.

Quality over a misleading 256.

## What exists today

- **Live gallery** (GitHub Pages): 256 systems, self-styled cards, category filters, search, spec-completeness rating with a transparent breakdown, source-site links.
- **Atomic detail view**: every system opens to an atomic spec sheet — Voice & type → Colour → Signature blocks (nav/hero/footer) → Components → Foundations → Source. Copy/Download/Visit.
- **Atomic `DESIGN.md` schema** (`enrich_all.py`): atoms (tokens) → molecules (components) → organisms (nav/hero/footer) → templates (page layouts) → guardrails, with the source URL baked in.
- **4 flagship brands** rendered faithfully.

## The thing to build next: URL → spec

The scalable answer, and arguably a product in its own right. Point at a URL, get an accurate `DESIGN.md` + render data:

1. **Extract** real tokens from the live site (colours, type, spacing, radius, shadows). Reuse `extract-design-system` (Chromium/DOM scrape) or our own Chrome-driven extractor — no guessing, real CSS.
2. **Screenshot** the site.
3. **Author** with Claude vision: read tokens + screenshot → write the atomic `DESIGN.md` and the flagship render JSON (nav, hero, CTA, footer).
4. **Drop in** → faithful card + modal + a genuine build-from file.

Packaged as a skill: `/design-extract <url>`. This is how the flagship tier scales from 4 to many.

## Success looks like

- A builder browses, finds a look, copies the file, and their agent ships screens that genuinely look like it.
- "Paste a URL → get a design.md" works in under a minute and looks like the site.
- The library is something you scroll and think "yes, I'll use that for this project."

## Open questions

- Name: keep `design.md`, or brand it (Specimen)?
- Flagship coverage: how many brands earn the full treatment?
- Is the URL→spec extractor the headline product, with the gallery as its showcase?
- Account/home: JK-D-S-N vs dotjk; custom domain.

## Roadmap

1. **Now:** flagship set proven (done: 4). Atomic schema (done). Source links (done).
2. **Next:** build `/design-extract <url>` v0 (Chrome extract + vision author), run on 10 brands.
3. **Then:** scale flagship tier via the extractor; retune the completeness score to reward structure over raw token count.
4. **Later:** the generator layer (URL/screenshots → original starter systems), shareable permalinks, deploy + domain.
