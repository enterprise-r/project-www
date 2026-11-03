# www.enterprise-r.com

The Enterprise-R website. Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

Where this sits: the logos, palette and fonts are built by [enterprise-r/project-branding](https://github.com/enterprise-r/project-branding) and shipped to Google Drive `assets/`. This repo copies them in as-is.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading…) | the `page` block at the top of the page in `src/pages/` |
| Contact email | the `page` block in `src/pages/about.astro` |
| Title bar logo | `src/layouts/Base.astro`, showing `public/assets/logo-wide.svg` (large screens) and `public/assets/logo-compact.svg` (narrow) |
| Images (logo, favicons) | the matching file in `public/assets/`, copied from Drive `assets/logos/` |
| Styles | `src/styles/palette.css` (colours), `src/styles/base.css` (theme), `src/styles/about.css`, `src/styles/ui.css` (style guide) |
| Shared head, title bar, navigation and footer (social links: `social`) | `src/layouts/Base.astro` |
| Page not found | `src/pages/404.astro` |
| Enterprsr (Home button) | `public/fonts/Enterprsr-Regular.woff2`, from Drive `assets/fonts/woff2/` |
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
| `logos/svg/favicon.svg` | `public/assets/favicon.svg` |
| `logos/favicon/favicon.ico` | `public/assets/favicon.ico` |
| `logos/favicon/favicon-32.png` | `public/assets/favicon-32.png` |
| `logos/favicon/favicon-180.png` | `public/assets/apple-touch-icon.png` |
| `logos/favicon/favicon-192.png` | `public/assets/icon-192.png` |
| `logos/favicon/favicon-512.png` | `public/assets/icon-512.png` |
| `fonts/woff2/Enterprsr-Regular.woff2` | `public/fonts/Enterprsr-Regular.woff2` |
| `fonts/licenses/OFL-*.txt` (Enterprsr, Audiowide, Rajdhani) | `public/fonts/` (same names) |
| `palette/palette.css` | `src/styles/palette.css` |
| `palette/palette.json` | `src/styles/palette.json` |

`palette.css` is project-branding's `palette/palette.css` (generated from `palette/palette.json` there), copied as-is, with `palette.json` next to it for the style guide's swatches. To change a colour, change it in project-branding, then copy both files again. Do not edit the colours in this repo.

The lockup geometry is described in project-branding [`logo/README.md`](https://github.com/enterprise-r/project-branding/blob/main/logo/README.md).

The link preview (`og:image`) and the style guide's sample picture are not in this repo. Both hotlink the 3x1 banner from Drive (`assets/banners/banner-3x1.png`).

## Design

The pages are a plain document on the Enterprise-R palette (`src/styles/palette.css`), with the page background `--ui-bg`. `base.css` is the theme: type, the title bar with the navigation, the footer, and the style-guide specimens. It uses only `--ui-*` variables. `about.css` holds only the rules the text pages use.

The title bar is one full-width `--ui-border` stripe with the logo in the middle: the wide lockup, or the compact one at 640 px and below, where the title has its own row and the buttons go below it. On Home the logo is the page heading (`h1`).

The Home button reads ® (its accessible name is Home), on `--ui-border` with the mark in `--ui-green-bright`. It floats fixed at the bottom left of the bar and does not change on hover. Scrolled down, it goes back to the top; at the top, it goes to the home page. Every other page sits at the bottom right of the bar. The current page is `--ui-green` (hover `--ui-green-bright`). Other pages are `--ui-orange` (hover `--ui-accent`). Keyboard focus is a 2 px `--ui-fg-bright` outline, 3 px off.

The footer is a slim `--ui-border` stripe with the LinkedIn and GitHub icons in the middle, black (`--ink`), amber on hover. The icons are inline paths from Simple Icons (CC0). On short pages it sits at the bottom of the window.

On About, the email sits centred in a bubble with a thin `--ui-border` border, and the @ is `--ui-orange`.

`/404.html` (`src/pages/404.astro`) is the page-not-found page. It is not indexed.

`/showcase/` is the style guide (`src/pages/showcase.astro`, `src/styles/ui.css`). It is not in the menu and not indexed: open it directly.
