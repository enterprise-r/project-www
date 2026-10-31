# www.enterprise-r.com

Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading…) | the `page` block at the top of the page in `src/pages/` |
| Contact email | the `page` block in `src/pages/about.astro` |
| Homepage title image | `public/assets/logo-wide.svg` (large screens) and `public/assets/logo-compact.svg` (narrow) |
| Images (logo, favicons) | the matching file in `public/assets/`, copied from Drive `assets/logos/` |
| Styles | `src/styles/palette.css` (colours), `src/styles/base.css` (theme), `src/styles/home.css`, `src/styles/about.css` |
| Shared head and navigation | `src/layouts/Base.astro` |
| Enterprsr (Home button, and the R in the style-guide title) | `public/fonts/Enterprsr-Regular.woff2`, from Drive `assets/fonts/woff2/` |
| Audiowide and Rajdhani | `public/fonts/`. These are the subsetted files of the faces in Drive `assets/fonts/ttf/` |
| Custom domain | repo Settings → Pages → Custom domain (the Pages source is GitHub Actions, so no `CNAME` file is used) |

A new page = a new file in `src/pages/` using the `Base` layout. A text page also imports `src/styles/about.css`.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages in about a minute. You can edit files right on github.com. (Settings → Pages → Source must be **GitHub Actions**.)

## Local (optional, Node 24)

```sh
npm ci
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```

## Regenerating images

Logos, favicons and Enterprsr come from Google Drive `assets/`. Copy them into `public/` under the names the pages already use:

| Drive | Site |
|---|---|
| `logos/svg/logo-wide.svg` | `public/assets/logo-wide.svg` |
| `logos/svg/logo-compact.svg` | `public/assets/logo-compact.svg` |
| `logos/svg/logo-color.svg` | `public/assets/logo-color.svg` |
| `logos/svg/favicon.svg` | `public/assets/favicon.svg` |
| `logos/favicon/favicon.ico` | `public/assets/favicon.ico` |
| `logos/favicon/favicon-32.png` | `public/assets/favicon-32.png` |
| `logos/favicon/favicon-180.png` | `public/assets/apple-touch-icon.png` |
| `logos/favicon/favicon-192.png` | `public/assets/icon-192.png` |
| `logos/favicon/favicon-512.png` | `public/assets/icon-512.png` |
| `logos/logo-badge-1024.png` | `public/assets/logo.png` |
| `fonts/woff2/Enterprsr-Regular.woff2` | `public/fonts/Enterprsr-Regular.woff2` |
| `palette/palette.css` | `src/styles/palette.css` |

`palette.css` is copied as-is. It is generated from `palette.json` in Drive. Edit that JSON, then copy the CSS again. Do not edit the colours in this repo.

`logo.png` (the round badge) is not shown on any page. The wide lockup is named 320×61 and the compact lockup 320×128. The compact file is already the button. The wide file is transparent, and the homepage draws the pill around it.

`scripts/build-assets.py` does not draw those. It builds `og-image.jpg` and the About backdrops:

```sh
pip install cairosvg pillow          # cairosvg needs the system cairo library
python3 scripts/build-assets.py      # --mark SVG, --backdrop JPG, --backdrop-phone JPG, --out DIR to override
```

`og-image.jpg` (the 1200×630 link preview) is the WarpChi wallpaper (`art/warpchi.jpg`, from Drive `assets/wallpapers/`) with `logo-color.svg` small in the top-left corner.

The pages are a plain document on the company colour scheme (the LCARS extended palette, `src/styles/palette.css`). The page background is `--ui-bg` (`#0C040F`). There is no picture, star field, scrim or animation.

`base.css` is the theme: type, navigation, buttons, and the style-guide specimens. `home.css` and `about.css` hold only the rules those pages use. A text page imports `about.css`.

The navigation is one row: Home on the left, every other page on the right. The Home button reads ® (its accessible name is Home). Its fill is the inactive border (`--ui-border`) and the mark is bright green (`--ui-green-bright`, #9ADD6D). It does not change on hover. The other pages are lighter orange (`--ui-orange`, #F4B965) and switch to amber (`--ui-accent`, #F0A202) on hover. Keyboard focus is a 2 px near-white outline, 3 px off. `/showcase/` is the style guide. It is not in the menu, and it does not show a navigation bar.
