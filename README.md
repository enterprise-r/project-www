# www.enterprise-r.com

The Enterprise-R website. Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

Part of [enterprise-r/project-foundation](https://github.com/enterprise-r/project-foundation). The logos, palette and fonts are built by [enterprise-r/project-branding](https://github.com/enterprise-r/project-branding) and shipped to Google Drive `assets/`. This repo copies them in.

Pages: Home (`/`), About (`/about/`), 404 (`/404.html`) and the unlisted `/showcase/`.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading, contact email) | the `page` block at the top of the page in `src/pages/` |
| Logo and favicons | `public/assets/`. The title bar in `src/layouts/Base.astro` shows `logo-wide.svg` |
| Styles | `src/styles/palette.css` (colours), `src/styles/base.css` (theme), `src/styles/about.css`, `src/styles/ui.css` (style guide) |
| Shared head, title bar, navigation and footer (social links: `social`) | `src/layouts/Base.astro` |
| Page not found | `src/pages/404.astro` |
| Search engines | `public/robots.txt`, and the indexed pages listed in `src/pages/sitemap.xml.ts` |
| Enterprsr (Home button) | `public/fonts/Enterprsr-Regular.woff2`, from Drive `assets/fonts/woff2/` |
| Audiowide and Rajdhani | `public/fonts/`. Google Fonts makes the latin and latin-ext subsets (Audiowide 400, Rajdhani 500 and 600) of the faces in Drive `assets/fonts/ttf/` |
| Link preview picture (`og:image`) | `src/pages/og-image.png.ts`, built from `public/assets/logo-wide.svg` on the title bar colour |
| Style guide's sample picture | the `banner` hotlink at the top of `src/pages/showcase.astro` |
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

## Brand assets

Every brand file comes from the project-branding build (`build.sh`), shipped to Google Drive `assets/`. To refresh one, copy it in again from there.

| In this repo | From |
|---|---|
| `public/assets/logo-wide.svg`, `favicon.svg` | Drive `assets/logos/svg/` |
| `public/assets/favicon.ico`, `favicon-32.png` | Drive `assets/logos/favicon/` |
| `public/assets/apple-touch-icon.png`, `icon-192.png`, `icon-512.png` | Drive `assets/logos/favicon/` `favicon-180.png`, `favicon-192.png`, `favicon-512.png`, renamed |
| `public/fonts/Enterprsr-Regular.woff2` | Drive `assets/fonts/woff2/` |
| `public/fonts/audiowide-*.woff2`, `rajdhani-*.woff2` | Google Fonts subsets of the faces in Drive `assets/fonts/ttf/` (see above) |
| `public/fonts/OFL-Enterprsr.txt`, `OFL-Audiowide.txt`, `OFL-Rajdhani.txt` | Drive `assets/fonts/licenses/` |
| `src/styles/palette.css` | Drive `assets/palette/palette.css` |
| `src/styles/palette.json` | project-branding `palette/palette.json` |

The link preview (`og:image`, `/og-image.png`, 1200x400) is not a file in this repo: `src/pages/og-image.png.ts` renders `public/assets/logo-wide.svg` 1000 px wide on the title bar colour (`--ui-border`) at build time, with sharp (which Astro already installs).

The `/showcase/` sample picture is the 3x1 banner, hotlinked from Drive `assets/banners/banner-3x1.png` as `https://lh3.googleusercontent.com/d/<id>=w1600` (the `banner` line in `src/pages/showcase.astro`). The file must be viewable by anyone with the link.

`palette.css` is project-branding's `palette/palette.css` (generated from `palette/palette.json` there), copied as-is, with `palette.json` next to it for the style guide's swatches. To change a colour, change it in project-branding, then copy both files again. Do not edit the colours in this repo.

A lockup is the wordmark and the mark together (wide and compact). The plate is the inactive-border shape behind the mark. Geometry is in project-branding [`logo/README.md`](https://github.com/enterprise-r/project-branding/blob/main/logo/README.md).

## Design

The pages are a plain document on the Enterprise-R palette (`src/styles/palette.css`). Where a colour is used is the `use` line in `src/styles/palette.json`. `base.css` is the theme: type, the title bar with the navigation, and the footer. It uses only `--ui-*` variables. `about.css` holds only the rules the text pages use. The style guide is `ui.css`.

The title bar is one full-width stripe with the logo in the middle: the wide lockup on every screen; at 640 px and below the title has its own row on the page background and the buttons go below it. On Home the logo is the page heading (`h1`).

The Home button reads ® (its accessible name is Home). It floats fixed at the bottom left of the bar and does not change on hover. Scrolled down, it goes back to the top; at the top, it goes to the home page. Every other page sits at the bottom right of the bar. Keyboard focus is a 2 px outline, 3 px off.

Breadcrumbs (`.crumbs`) are the same buttons joined in one row on a diagonal (a `clip-path` slant), one per level, with only the last rounded on the right, and the root as the lone R (®) in Enterprsr: parents Magenta (`--crumb`, they are links), the page you are on Green (sage). Any nav button or crumb can carry a menu (`details.bar-menu`): a caret on the left of the button, which takes its hover colour while open, and a stack of the same squared buttons on the title bar colour underneath, for a page's subpages or a crumb's siblings. Button labels keep their colour on hover. Both live in `base.css` and are shown in `/showcase/`.

Form buttons are the same button with a role: generic (no class) Orange, `.primary` Green (sage), `.clear` (and any reset button) Cyan, `.cancel` Red, each brighter on hover (`--act-*` in `base.css`).

The footer is a slim stripe with the LinkedIn and GitHub icons in the middle. The icons are inline paths from Simple Icons (CC0). On short pages it sits at the bottom of the window.

On About, the email sits centred in a bubble.
