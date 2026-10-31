# www.enterprise-r.com

The Enterprise-R website. Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

Part of [enterprise-r/project-foundation](https://github.com/enterprise-r/project-foundation). The logos, palette and fonts are built by [enterprise-r/project-branding](https://github.com/enterprise-r/project-branding) and shipped to Google Drive `assets/`. This repo copies them in.

Pages: Home (`/`), About (`/about/`), 404 (`/404.html`) and the unlisted `/showcase/`.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading, contact email) | the `page` block at the top of the page in `src/pages/` |
| Logo and favicons | `public/assets/`. The title bar in `src/layouts/Base.astro` shows `logo-wide.svg` on large screens and `logo-compact.svg` on narrow ones |
| Styles | `src/styles/palette.css` (colours), `src/styles/base.css` (theme), `src/styles/about.css`, `src/styles/ui.css` (style guide) |
| Shared head, title bar, navigation and footer (social links: `social`) | `src/layouts/Base.astro` |
| Page not found | `src/pages/404.astro` |
| Enterprsr (Home button) | `public/fonts/Enterprsr-Regular.woff2`, from Drive `assets/fonts/woff2/` |
| Audiowide and Rajdhani | `public/fonts/`. Google Fonts makes the latin and latin-ext subsets (Audiowide 400, Rajdhani 500 and 600) of the faces in Drive `assets/fonts/ttf/` |
| 3x1 banner (link preview and the style guide's picture) | the Drive file id `bannerId` in `src/banner.js` |
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

Copy each file from Google Drive `assets/` into this repo under the same name: `logos/svg/` and `logos/favicon/` into `public/assets/`, `fonts/woff2/` and `fonts/licenses/` into `public/fonts/`, and `palette/` into `src/styles/`. Three favicons are renamed: `favicon-180.png` to `apple-touch-icon.png`, `favicon-192.png` to `icon-192.png`, and `favicon-512.png` to `icon-512.png`.

`palette.css` is project-branding's `palette/palette.css` (generated from `palette/palette.json` there), copied as-is, with `palette.json` next to it for the style guide's swatches. To change a colour, change it in project-branding, then copy both files again. Do not edit the colours in this repo.

A lockup is the wordmark and the mark together (wide and compact). The plate is the inactive-border shape behind the mark. Geometry is in project-branding [`logo/README.md`](https://github.com/enterprise-r/project-branding/blob/main/logo/README.md).

The link preview (`og:image`) and the style guide's sample picture are not in this repo. Both hotlink the 3x1 banner from Drive (`assets/banners/banner-3x1.png`).

## Design

The pages are a plain document on the Enterprise-R palette (`src/styles/palette.css`). Where a colour is used is the `use` line in `src/styles/palette.json`. `base.css` is the theme: type, the title bar with the navigation, and the footer. It uses only `--ui-*` variables. `about.css` holds only the rules the text pages use. The style guide is `ui.css`.

The title bar is one full-width stripe with the logo in the middle: the wide lockup, or the compact one at 640 px and below, where the title has its own row and the buttons go below it. On Home the logo is the page heading (`h1`).

The Home button reads ® (its accessible name is Home). It floats fixed at the bottom left of the bar and does not change on hover. Scrolled down, it goes back to the top; at the top, it goes to the home page. Every other page sits at the bottom right of the bar. Keyboard focus is a 2 px outline, 3 px off.

The footer is a slim stripe with the LinkedIn and GitHub icons in the middle. The icons are inline paths from Simple Icons (CC0). On short pages it sits at the bottom of the window.

On About, the email sits centred in a bubble.
