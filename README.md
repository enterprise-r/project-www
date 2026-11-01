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
| Custom domain | repo Settings → Pages → Custom domain (the Pages source is GitHub Actions, so no `CNAME` file is used) |

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
python3 scripts/build-assets.py      # R_ART_DIR=…, --badge/--mark SVG, --backdrop JPG, --out DIR to override
```

`logo.png` is `source/logo-badge-large.svg`; the favicons and icons are `source/logo-refined.svg` fitted to a transparent square. `og-image.jpg` (the 1200×630 link preview) is the WarpChi wallpaper (`art/warpchi.jpg`, from Drive `Wallpapers/`) with the mark small in the top-left corner.

The Enterprise-R lockup in the top-left corner (`src/components/ElbowLockup.astro`) is inline SVG, not a web font: the word "Enterprise-" is drawn from the Enterprsr font (r-art, spacing and kerning from the built font) and the R is the full-colour logo. Inline SVG is pixel-exact at any size, the colour R cannot come from a font, and the font files stay out of this public repo. On scroll the corner morphs into the logo-only bubble: the word slides left and tucks in behind the logo (transforms and clip-paths only; reduced motion swaps instantly). See the corner in `src/styles/site.css`.

Highlights: navigation, the Home corner, links and ordinary buttons use the normal highlight (a lighter fill on hover, a 2 px `--nav-focus` outline 3 px off on keyboard focus; the corner also keeps its focused-field border). The lime ring (`--act-ring`, #8DFF3C) is only for a form's primary action button: give it the class `btn-primary` inside a `<form>`. The /showcase/ page shows both.
