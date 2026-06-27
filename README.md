# WDART

The official website of the **Web Development Association for the Re-instatement of
Tables for Layout** — a fictional trade association that argues, with a completely straight
face, that the industry erred when it abandoned `<table>`-based layout.

The joke is structural: the site advocates for tables and "older style HTML," and is itself
built entirely in nested tables with **zero CSS**. It practices exactly what it preaches.

Live at **[wdart.org](https://wdart.org)**. A project by
[Ryan Null](https://codebehavingbadly.com).

## The rules (enforced)

- **One page:** `index.html` + an `assets/` folder of hand-generated GIFs.
- **Layout:** 100% nested `<table>` + `spacer.gif`, fixed `width=760`, `align=center`.
- **Styling:** not one byte of CSS. Presentation via `<font>`, `bgcolor`, `background`,
  `align`, table `border` bevels, `<center>`, `<hr>`, `<marquee>`.
- **JavaScript:** vintage gags only — a live hit counter, `window.status`, a
  `document.lastModified` stamp, and an 800×600 resolution nag.
- **Responsive design:** none, by design. The page is 760px wide on every device, forever.

## Project layout

```
index.html                     the entire website
favicon.ico                    a tiny table-grid icon
assets/                        spacer.gif, crest.gif, badges, backgrounds, etc.
.do/app.yaml                   DigitalOcean App Platform spec (static site)
docs/superpowers/specs/        the design document
tools/gen_assets.py            regenerates every GIF in assets/ (requires Pillow)
```

## Regenerating the assets

All images are generated, not downloaded:

```sh
python3 tools/gen_assets.py
```

## Local preview

```sh
python3 -m http.server 8753
# open http://localhost:8753/
```

## Deploying to DigitalOcean App Platform

Static site, no build step.

```sh
doctl apps create --spec .do/app.yaml      # first deploy
# doctl apps update <APP_ID> --spec .do/app.yaml   # subsequent updates
```

Then point `wdart.org`'s DNS at DigitalOcean (the dashboard shows the exact records);
the domains in `.do/app.yaml` provision automatically with managed TLS.
