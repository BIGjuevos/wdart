# Contributing to WDART

So. You wish to contribute to the cause.

The Association welcomes the labour of the faithful, provided that labour is laid out in
tables. What follows is doctrine, not preference. Read it before you open a pull request.

---

## The Doctrine (non-negotiable)

These rules are what make the project what it is. A contribution that violates them is not a
contribution; it is a provocation.

- **One page.** Everything lives in `index.html` plus the `assets/` folder. Resist the urge
  to "split things out." Things that love each other should not be separated.
- **Tables for layout. Always.** Every column, sidebar, and panel is a `<table>`,
  `<tr>`, and `<td>`. Nest them as deeply as your editor will tolerate. `spacer.gif` is your
  only ruler.
- **Not one byte of CSS.** No `<style>` blocks, no `style=` attributes, no `class=`. Use
  `<font>`, `bgcolor`, `background`, `align`, table `border` bevels, `<center>`, `<hr>`, and
  `<marquee>`. If you find yourself reaching for `flex` or `grid`, step away from the keyboard.
- **No responsive design.** The page is **760 pixels wide** on every device, in perpetuity.
  Media queries are confessions; we do not make them.
- **JavaScript only in period.** Small, era-appropriate gags are welcome (a hit counter, a
  `window.status` message, a `document.lastModified` stamp). Frameworks are not. If it didn't
  exist by 2003, neither should it appear here.

Pull requests are reviewed **in source order**.

---

## Project layout

```
index.html                     the entire website
favicon.ico                    a tiny table-grid icon
assets/                        spacer.gif, crest, badges, backgrounds, sponsor logos
assets/crest_new.png           the master seal artwork (externally supplied)
assets/logos/                  vintage sponsor logos (originals + normalised *_cell.png tiles)
tools/gen_assets.py            regenerates the generated assets via Pillow
.do/app.yaml                   DigitalOcean App Platform spec (static site)
docs/superpowers/specs/        the design document
```

## Regenerating assets

Most images are generated. Editing the seal art (`assets/crest_new.png`) or a raw sponsor
logo (`assets/logos/<slug>.png`) and re-running the generator will rebuild the circular
crest, the normalised sponsor tiles, the award rosette, the construction banner, and the
backgrounds:

```sh
python3 tools/gen_assets.py
```

Requires [Pillow](https://python-pillow.org/) (`pip install pillow`).

## Local preview

```sh
python3 -m http.server 8753
# open http://localhost:8753/
```

## Deployment

The site runs on DigitalOcean App Platform as a static site (no build step), deployed from
a public git clone of this repo per `.do/app.yaml`.

```sh
# first deploy
doctl apps create --spec .do/app.yaml --project-id <PROJECT_ID>
# redeploy after pushing changes
doctl apps create-deployment <APP_ID>
```

Because we deploy via public git clone rather than the GitHub integration, a `git push` does
**not** auto-deploy — trigger a deployment with the command above.

---

## Submitting work

1. Keep changes in character. The Association is sincere; so should your copy be.
2. Verify it renders by actually opening it in a browser. Screenshot if you can.
3. Confirm you added **zero** CSS. This is verifiable. Please verify it.
4. Open a pull request. Describe it, ideally, in a table.

Welcome to the cause.
