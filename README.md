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

The Home logo is `logo-color.svg`, the flat colour logo (silver mirrored R, sage R, amber #F0A202 bowl; r-art `logo-flat/amber`, unchanged). `logo.png` (the round badge, `source/logo-badge-large.svg`) is no longer shown on any page; the favicons and icons are `source/logo-refined.svg` fitted to a transparent square. `og-image.jpg` (the 1200×630 link preview) is the WarpChi wallpaper (`art/warpchi.jpg`, from Drive `Wallpapers/`) with the mark small in the top-left corner.

The Enterprise-R lockup in the top-left corner (`src/components/ElbowLockup.astro`) is the word "Enterprise-" as live text in the Enterprsr web font and the full-colour logo R as inline SVG (the colour R cannot come from a font). Enterprsr 1.002 (`public/fonts/Enterprsr-Regular.woff2`, 3 KB, OFL, licence in `public/fonts/Enterprsr-OFL.txt`, preloaded, `font-display: swap` with Audiowide as the fallback) is used for the corner word, the Home H1 and the /showcase/ H1, always with `ss03`: the plain typographic R, not the logo R that is the font's default. On scroll the corner morphs into the logo-only bubble: the word slides left and tucks in behind the logo (transforms and clip-paths only; reduced motion swaps instantly). See the corner in `src/styles/site.css`.

Highlights: navigation, the Home corner, links and ordinary buttons use the normal highlight (a lighter fill on hover, a 2 px `--nav-focus` outline 3 px off on keyboard focus; the corner also keeps its focused-field border). The lime ring (`--act-ring`, #8DFF3C) is only for a form's primary action button, and only on hover: give it the class `btn-primary` inside a `<form>`. Keyboard focus on it is the normal `--nav-focus` outline. The /showcase/ page shows both. The /showcase/ page has no site header (`<Base header={false}>`).
