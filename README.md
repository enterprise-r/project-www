# www.enterprise-r.com

The Enterprise-R website. Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

Part of [enterprise-r/project-foundation](https://github.com/enterprise-r/project-foundation). Logos, palette, fonts and Dark-® come from [enterprise-r/project-branding](https://github.com/enterprise-r/project-branding), shipped to Google Drive `assets/`. This repo copies them in.

Pages: Home (`/`), About (`/about/`), 404 (`/404.html`) and `/showcase/`. The showcase is in the bar as "UI of the future". It is `noindex` and not in the sitemap.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading, contact email) | the `page` block at the top of the page in `src/pages/` |
| Logo and favicons | `public/assets/`. The bar shows `logo-wide.svg`, then `logo-compact.svg` at 52rem and below |
| Styles | `src/styles/`: `palette.css` (colours), `theme/` (Dark-®), `bar.css` (title bar), `footer.css`, `home.css`, `about.css`, `transition.css`, `ui.css` (style guide) |
| Shared head, title bar and navigation | `src/layouts/Base.astro` |
| Social links | the `social` list in `src/components/Footer.astro` |
| Home and 404 terminal | `src/components/HomeWait.astro` and `src/styles/home.css` |
| Page not found | `src/pages/404.astro` |
| Search engines | `public/robots.txt`, and the indexed pages in `src/pages/sitemap.xml.ts` |
| Fonts | `src/styles/fonts/woff2/`. The theme loads them from `../fonts/woff2/` |
| Link preview (`og:image`) | `src/pages/og-image.png.ts` |
| Custom domain | repo Settings → Pages → Custom domain (Pages source is GitHub Actions, so there is no `CNAME` file) |

A new page is a file in `src/pages/` that uses the `Base` layout. About imports `src/styles/about.css`.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages in about a minute. Files can be edited on github.com. Settings → Pages → Source must be **GitHub Actions**.

## Local (optional, Node 24)

```sh
npm ci
npm run dev      # http://localhost:4321
npm run build    # output in dist/
```

## Brand assets

Brand files come from the project-branding build (`build.sh`), shipped to Drive `assets/`. To refresh one, copy it in again. Do not edit a copied file here.

| In this repo | From |
|---|---|
| `public/assets/logo-wide.svg`, `logo-compact.svg`, `favicon.svg` | Drive `assets/logos/svg/` |
| `public/assets/favicon.ico`, `favicon-32.png` | Drive `assets/logos/favicon/` |
| `public/assets/apple-touch-icon.png`, `icon-192.png`, `icon-512.png` | Drive `assets/logos/favicon/` `favicon-180.png`, `favicon-192.png`, `favicon-512.png`, renamed |
| `public/assets/warpchi.*`, `hyper-j.*` | Home (warpchi) and About / 404 (hyper-j). Sources are project-branding `wallpapers/`, saved here as jpg, avif and webp |
| `src/styles/theme/` | Drive `assets/theme/`, the whole directory, copied as-is |
| `src/styles/fonts/woff2/*.woff2` | Drive `assets/fonts/woff2/` |
| `public/fonts/OFL-*.txt` | Drive `assets/fonts/licenses/` |
| `src/styles/palette.css`, `palette.json` | Drive `assets/palette/palette.css` and project-branding `palette/palette.json` |

`/og-image.png` (1200x400) is not a file in the repo. `src/pages/og-image.png.ts` draws `logo-wide.svg` 1000 px wide on the title-bar colour (`--ui-border`) at build time, with sharp (Astro already installs it).

`palette.css` is generated from `palette.json`. Change a colour in project-branding, then copy both files again. A colour's `use` line says where this site uses it.

Dark-® is `src/styles/theme/`. What it does is in `theme/README.md`. It loads fonts from `../fonts/woff2/`. This site imports `src/styles/palette.css`. The `palette.css` inside `assets/theme/` is for a project that links the theme on its own.

A lockup is the wordmark and the mark together (wide and compact). The plate is the inactive-border shape behind the mark. Geometry is in project-branding [`logo/README.md`](https://github.com/enterprise-r/project-branding/blob/main/logo/README.md).

## Pages

The bar (`bar.css`) is one stripe: breadcrumbs on the left, the logo in the middle, one button on the right. Breakpoints follow the bar's width, not the window's. At 52rem and below the lockup becomes compact. At 40rem and below the compact logo docks to the left edge and the breadcrumbs wrap onto a second row. On Home the logo is the page heading (`h1`). Scrolled down on Home, that logo returns to the top. Otherwise it links home.

The ® crumb is Home. On Home it is the current page and does not navigate. When the logo docks, that crumb is hidden, because the docked logo already marks the root.

Home and the 404 share open stripes and one terminal (`home.css`). Home uses warpchi. The 404 uses hyper-j and turns the terminal 45 degrees. About uses hyper-j as well. Its plates are in `about.css`.

The footer is a slim stripe: LinkedIn, X and GitHub, inline paths from Simple Icons (CC0). On a short page it sits at the bottom of the window. On Home, the 404 and About the stripe is open and the icons switch to Foreground, so they stay legible on the wallpaper.
