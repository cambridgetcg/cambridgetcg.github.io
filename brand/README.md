# The Doors (cambridgetcg.github.io): brand

This folder will hold the hall's brand kit and media, made with storytold's Craft apps through the artcraft-brand
skill (the shared toolkit, kept in a private repository). `brandkit.json` records this project's details, and
`check.mjs` checks them. It is **planned**: the folder exists, the kit doesn't yet.

## The look

The hall: paper `#f6f1e7`, ink `#2b241c`, lamp `#b5651d`, with a dark scheme (`#17140f`, ink `#ece3d3`, lamp
`#e0a050`), set in ui-serif and Georgia. It arrived on 2026-10-09 in commit 0fb50083 (git author "YOU", co-author
"The Fable of the Eternal Universe"); whether a person or an agent chose it is not recorded.

Only the hall (`index.html`, `404.html`) is dressed here. Each door under `jekyll/` and `static/` is a public copy
of a private repository's page and keeps that page's own look.

Don't change the identity without its owner's word. Every asset here records who made it in `CREDITS.md`.

## What is here

| Path | What it is |
|---|---|
| `brandkit.json` | this project's details: the look, the pages whose heads must match the kit, what a deploy does |
| `CREDITS.md` | who made what, with fonts and licences |
| `check.mjs` | the check, copied from the shared toolkit; update it there, not here |

`brand.json` and `kit/` arrive with the kit. `pages.yml` copies named files only, so nothing here is published.

## Rebuild

There is no kit to rebuild yet. To check this folder, from the repository root:

```sh
node brand/check.mjs
```

## How the site uses it

Static pages at the repository root. Once a kit exists, `kit/web/head-snippet.html` goes early in the `<head>` of
`index.html` and `404.html` (listed under `site.html`, so the check compares their theme-color and color-scheme
with the kit), and the kit's icon files sit at the root and are added to the copy line in `pages.yml`. A root
`/favicon.ico` also becomes the fallback icon for any door under this host that declares none.

## Deploying

Every push to `main` builds and deploys GitHub Pages after the guard and gitleaks scans
(`.github/workflows/pages.yml`). `door-watch.yml` checks the doors' public promises daily and only reports.
