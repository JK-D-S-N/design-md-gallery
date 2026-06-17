# design.md — Product Requirements

_Rewritten 2026-06-17 after researching Google's official DESIGN.md spec and the wider landscape._

## The problem

AI agents can build almost any UI, but with no taste. Point Claude Code / Cursor / Stitch at a blank project and you get generic, soulless screens. The missing input is a **design system the agent can read.** A `DESIGN.md` is that input.

But two gaps:
1. **The standard stops at mechanics.** Google Labs open-sourced DESIGN.md (Apache 2.0, alpha) — YAML tokens (`colors`, `typography`, `spacing`, `rounded`, `components`) + prose (Overview, Colours, Typography, Layout, Elevation, Shapes, Components, Do's/Don'ts). The orthodox guidance: keep it to mechanical tokens, concise, "not a full design system." So agents get colour and type, but not the **essence** of a brand.
2. **No good way to get one.** Existing collections (voltagent, Khalidabdi, designmd.app, getdesign.md) are scraped token-dumps or themed costumes. None capture what makes a brand *that brand*, and none are generated faithfully on demand.

## What we're building

A way for an **AI builder to get a genuine head-start in a brand's essence** — then make their own decisions. Not a copy. The Monzo example: a brief says "they like Monzo." Click Monzo → pull its tone of voice, colour, spacing, components, the three things that make it distinctive → now design from there: swap the logo, tweak the typeface and a couple of core colours, ship something in that spirit.

Two surfaces:
- **The gallery** — browse, see each system rendered faithfully, copy/download the file. (The showcase.)
- **The extractor** — point at any URL → an accurate, essence-rich `DESIGN.md`. (The product.)

## Who it's for

The **forward-deployed creative** — designers who build, engineers with taste, founders, agency teams shipping with agents. They want "give me a head-start that feels like X," not a token file.

## The DESIGN.md we author — schema

Built **on top of** Google's spec (so our files are standard-compatible), extended with the essence layer the standard omits. Sections:

**Foundations (standard, mechanical):**
- `colors` — palette + semantic roles, with the brand's signature colour called out.
- `typography` — display + body faces, scale, pairing.
- `spacing`, `rounded`, elevation, shapes.

**Components (standard section, but we go deep):**
- Button hierarchy — **primary / secondary / tertiary**, with real shape + fill + states.
- The **lockup** (logo + wordmark treatment), **navigation**, **hero**, **footer**.
- Real component property mappings + variants (hover/active), per the spec.

**Layout & signature sections (added 2026-06-17 — the "how they compose a page" layer):**
- **Grid & measurements** — content max-width, column count, gutters, section rhythm (the rough numbers a builder needs to lay out like them).
- **Signature section patterns** — the brand's recognisable compositions, not just nav/hero/footer. e.g. Linear's centred **"Built for the future" CTA box**, the **4-up horizontal feature row** (Plan / Build / Diffs / Monitor), the **horizontal testimonial cards** (the blue + lime quote pair), **text/image splits**, and **blog / case-study** layouts (linear.app/customers/cursor). Each: structure, proportions, when to use.
- These are the "templates" layer made concrete and brand-specific. This is often where a brand is *most* recognisable.

**Essence layer (our extension — the differentiator):**
- **The three distinctives** — the 2-3 things that make this brand unmistakable (e.g. Stripe's gradient flourishes, Linear's keyboard-dense calm, Steam's dark capsule cards). Named, specific.
- **Tone of voice** — short. How they write: button labels, descriptors, microcopy. A few real examples + the rule.

**Guardrails:** Do's and Don'ts.

Everything verified against the real site. Nothing invented — if it's not observable, it's omitted.

## How we build it efficiently

The lesson from hand-tuning: **never author from memory.** The pipeline:
1. **Read the rendered site** — headless Chrome → computed DOM + CSS. Real hex, real fonts, real radius, real nav text, real hero copy, real footer, real button styles. (Not raw `curl` — sites are JS-rendered and minified.)
2. **Screenshot** — for gestalt and the verification diff.
3. **Author** — Claude reads DOM + screenshot → writes the DESIGN.md to the schema above, observable-only.
4. **Verify (the moat)** — build a sample screen from the spec alone → screenshot → diff against source → fidelity score → iterate.
5. **Drop in** — faithful card + modal + a real build-from file.

Packaged as `/design-extract <url>`. Start with **5–10 brands, get the schema right**, then scale toward the full ~250.

## Differentiators

1. **The extractor is the product; the gallery is the demo.** Generate, don't just curate.
2. **Verified fidelity** — a spec proven to rebuild the look, with a match score. Nobody does this.
3. **Essence, not mechanics** — components, three distinctives, tone of voice. The superset above the standard.
4. **Taste** — a designer's judgment about which few things matter, rendered faithfully. Quality over a 454-entry costume box.

## Success looks like

- Click Monzo → get a head-start that genuinely feels like Monzo, then make it yours.
- "Paste a URL → essence-rich DESIGN.md" in under a minute, verified to match.
- A builder ships in a brand's spirit without copying it.

## Compatibility

Our YAML frontmatter conforms to Google's DESIGN.md spec (`colors`/`typography`/`spacing`/`rounded`/`components`); the essence layer rides in extra prose sections the spec preserves. So our files work in Stitch, Cursor, Claude Code today, and are richer than the baseline.

## Roadmap

1. **Now:** schema locked (this doc). DOM extractor v0 (headless Chrome, no untrusted deps).
2. **Next:** author 5–10 brands to the full schema, verified. Get it right.
3. **Then:** the build→diff→score verification loop; retune the gallery's completeness score to reward essence over raw token count.
4. **Scale:** run the extractor across the library toward 250.
5. **Later:** original starter systems; deploy + domain.

## Open questions

- Name: keep `design.md`, or brand it (Specimen)?
- Is the extractor the headline product, gallery as showcase? (Leaning yes.)
- Account/home: JK-D-S-N vs dotjk; custom domain.
- How many brands earn full essence treatment vs token-only.
