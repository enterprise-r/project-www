# www.enterprise-r.com

Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading, email…) | the `page` block at the top of `src/pages/index.astro` |
| Images (logo, favicons) | replace the file in `public/assets/` **with the same name**; no code change |
| Styles | `src/styles/site.css` |
| Shared head, backdrop, top frame | `src/layouts/Base.astro` |
| Fonts (self-hosted) | `public/fonts/` |
| Custom domain | `public/CNAME` |

A new page = a new file in `src/pages/` using the `Base` layout.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages in about a minute. You can edit files right on github.com. (Settings → Pages → Source must be **GitHub Actions**.)

## Local (optional, Node 24)

```sh
npm ci
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```

## Regenerating images

The PNGs in `public/assets/` are rendered from logo SVGs in the private repo `enterprise-r/r-art`. Which files and sizes the site needs is listed in `scripts/build-assets.py` (`OUTPUTS`). Clone r-art next to this repo, then:

```sh
pip install cairosvg pillow          # cairosvg needs the system cairo library
python3 scripts/build-assets.py      # R_ART_DIR=…, --badge/--mark SVG, --out DIR to override
```

`logo.png` is `source/logo-badge-large.svg`; the favicons and icons are `source/logo-refined.svg` fitted to a transparent square.
