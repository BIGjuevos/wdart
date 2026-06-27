# WDART — Design Document

**Date:** 2026-06-27
**Author:** Ryan Null (with Claude)
**Status:** Draft for review

## Premise

WDART — the **Web Development Association for the Re-instatement of Tables for Layout** —
is a fictional trade association that argues, in total earnest white-paper prose, that the
industry erred when it abandoned `<table>`-based layout. The site advocates for tables and
"older style HTML" with a completely straight face.

**The joke is structural, not stated:** the site itself is built entirely in tables with
zero CSS. It practices exactly what it preaches. The reader is in on a joke the site never
admits to. Tone is sincere and professional; the comedy comes from dramatic irony and the
gap between confident prose and a 2001-era medium.

Live at `wdart.org`, hosted on DigitalOcean App Platform as a static site.

## Voice & Tone

- **Serious, bureaucratic, white-paper.** Reads like a real (if dated) standards body.
- The position is **confidently, knowably wrong** about modern best practices. The reader
  supplies the irony; the site never winks in the prose.
- **Punch the position, never the people.** Where the site is wrong about accessibility or
  mobile, the humor targets the absurd *stance*, not the users that stance would harm.
- Light vintage accents (one ironic marquee, a hit counter) puncture the seriousness ~10%
  of the time. 90% straight face.

## Hard Constraints (the bit, enforced)

These are non-negotiable — the integrity of the joke depends on them.

| Concern   | Rule |
|-----------|------|
| Files     | Single `index.html` at repo root + an `assets/` folder of GIFs. |
| Layout    | 100% nested `<table>` + `spacer.gif`. Fixed `width=760`, `align=center`. No fluid/responsive layout of any kind. |
| Styling   | **Zero CSS.** No `<style>`, no `style=`, no `class=`. Presentation via `<font>`, `bgcolor`, `background`, `align`, table `border` bevels, `<center>`, `<hr>`, `<marquee>`, `<blink>`. |
| JavaScript| Vintage gags only (hit counter, `window.status` scroller, `document.write` date, "best viewed" line). No frameworks, no modern APIs. `language="JavaScript"` attribute for flavor. |
| Assets    | All self-hosted (no external CDNs/fonts/analytics) — staying in character. |
| Responsive| Explicitly none. The page is 760px wide on every device, forever. |

## Assets to Generate

Generated locally with an image tool (ImageMagick or Python/PIL), committed to `assets/`:

- `spacer.gif` — 1×1 transparent GIF (the load-bearing pixel).
- `bg.gif` — subtle tiled background texture (~100×100), tasteful not garish.
- `crest.gif` — official-looking WDART emblem: laurels, a large `</td>` glyph, motto banner
  reading **STRUCTURA SUPER OMNIA** ("structure above all").
- `construction.gif` — animated "Under Construction" badge (era-authentic).
- `badge-bestviewed.gif` — "Best Viewed in Netscape Navigator at 800×600" badge.
- `award.gif` — a faux "Cool Site of the Day" / award badge.
- Webring nav arrows may be plain text/`bgcolor` cells if image generation is constrained.

If any image proves impractical to generate well, fall back to an HTML-attribute equivalent
(e.g., a `bgcolor` cell with `<font>`), never to CSS.

## Section Lineup (9 sections, single scrollable page)

1. **Masthead** — `crest.gif`, full association name spelled out, tagline
   ("Reinstating structure, one `<td>` at a time"), "Est. 2026," and a table-bar nav of
   in-page anchor links. `window.status` welcome message on load.
2. **The Mission** — deadpan manifesto: the web lost its way when it divorced structure
   from presentation; WDART exists to restore order.
3. **Our Official Position on "Responsive" Design** — sober dismissal of media queries and
   fluid layout. *"A website shall be 760 pixels wide — on every device, in perpetuity. We
   call this consistency."*
4. **The Comparative Analysis** — a `<table>` (of course) pitting Tables against
   Flexbox/Grid/etc. across absurd criteria (Pixel Fidelity, Honesty, Nostalgia, Spiritual
   Weight). Tables win every row.
5. **Membership** — three tiers in a table (Associate / Cell / Rowspan Fellow) with benefits,
   plus a beveled "JOIN" `mailto:` link.
6. **Approved Techniques & Downloads** — reverent notes on the spacer GIF, nested tables, and
   the holy `<center>` tag. Offers `spacer.gif` as a genuine "free download."
7. **Our Distinguished Corporate Sponsors** — table grid of defunct old-web companies, each
   with a beveled faux-logo cell, years active, and a one-line blurb. Tiny footnote quietly
   notes every listed sponsor is no longer operational and that WDART sees no reason to
   update the list. Initial roster (flexible):
   - Netscape Navigator (1994–2008) — "Without `<blink>`, we are nothing."
   - GeoCities (1994–2009) — "Twelve nested tables and a starfield."
   - Macromedia Fireworks (1998–2005) — "Sliced your JPEG into 47 cells, automatically."
   - Microsoft FrontPage (1995–2003) — "Generated the spacer GIFs so you didn't have to."
   - AltaVista (1995–2013) — "Indexed your `<table>` with pride."
   - Adobe/Macromedia Flash (1996–2020) — "Layout's flashier cousin. We forgive them."
   - CompuServe (1989–2009) — "Keyword: TABLES."
   - Excite (1995–2001) — "A portal. To more tables."
8. **Frequently Refuted Objections** — FAQ where "But accessibility?" / "But mobile?" /
   "But maintainability?" receive confidently, obviously-wrong answers. Dramatic irony does
   the work; no winking. Stays tasteful per the tone rules above.
9. **Footer** — webring buttons, live JS hit counter ("You are visitor #…"), "Best Viewed in
   Netscape Navigator at 800×600" badge, an award badge, one ironic `<marquee>`, and
   **"A project by Ryan Null"** linking to https://codebehavingbadly.com. `mailto:` contact.

## Deployment (DigitalOcean App Platform)

- Static site, **no build step**. DO serves `index.html` from repo root.
- Add `.do/app.yaml` declaring a single `static_site` component, source = this repo,
  `index_document: index.html`, and the `wdart.org` domain.
- The user handles DNS and `doctl`/dashboard auth; this project prepares all files ready to
  push and deploy.

## Out of Scope (YAGNI)

- No real membership/auth, no real form submission (mailto only).
- No backend, no database, no analytics.
- No build tooling, bundlers, or package manager.
- No actual responsive/mobile support (by design).

## Open Items / Defaults Chosen

- **Footer credit:** "Ryan Null" (matches git/email; user wrote "Ryann" — assumed typo).
- **Motto:** "STRUCTURA SUPER OMNIA." Easily swapped.
- **Sponsor roster:** the 8 above; can add/cut during implementation.
