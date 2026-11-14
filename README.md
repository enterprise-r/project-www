# www.enterprise-r.com

The Enterprise-R website. Public repo (needed for GitHub Pages on the Free tier). Built with [Astro](https://astro.build), plain HTML/CSS, no frameworks.

Part of [enterprise-r/project-foundation](https://github.com/enterprise-r/project-foundation). Logos, palette, fonts and Dark-R come from [enterprise-r/project-branding](https://github.com/enterprise-r/project-branding), shipped to Google Drive `assets/`. This repo copies them in.

Pages: Home (`/`), About (`/about/`), Login (`/login/`), 404 (`/404.html`) and `/showcase/`. The showcase is the web UI, linked from the login page. It is `noindex` and not in the sitemap.

## Where things are

| To change… | Edit |
|---|---|
| Page text (title, heading, contact email) | the `page` block at the top of the page in `src/pages/` |
| Logo and favicons | `public/assets/`. The bar shows `logo-wide.svg`, then `logo-compact.svg` at 52rem and below |
| Styles | `src/styles/`: `palette.css` (colours), `theme/` (Dark-R), `bar.css` (title bar), `footer.css`, `home.css`, `about.css`, `login.css`, `ui.css` (style guide) |
| Shared head, title bar and navigation | `src/layouts/Base.astro` |
| Social links | the `social` list in `src/components/Footer.astro` |
| Home and 404 terminal | `src/components/HomeWait.astro` and `src/styles/home.css` |
| Page not found | `src/pages/404.astro` |
| Search engines | `public/robots.txt`, and the indexed pages in `src/pages/sitemap.xml.ts` |
| Fonts | `src/styles/fonts/woff2/`. The theme loads them from `../fonts/woff2/` |
| Custom domain | repo Settings → Pages → Custom domain (Pages source is GitHub Actions, so there is no `CNAME` file) |

A new page is a file in `src/pages/` that uses the `Base` layout. About imports `src/styles/about.css`. Login imports `src/styles/login.css`.

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
| `public/assets/warpchi.*`, `hyper-j.*` | Showcase terminal sample (warpchi). Site wallpaper is hyper-j, set once in `bar.css`. Sources are project-branding `wallpapers/`, saved here as jpg, avif and webp |
| `src/styles/theme/` | Drive `assets/theme/`, the whole directory, copied as-is |
| `src/styles/fonts/woff2/*.woff2` | Drive `assets/fonts/woff2/` |
| `public/fonts/OFL-*.txt` | Drive `assets/fonts/licenses/` |
| `src/styles/palette.css`, `palette.json` | Drive `assets/palette/palette.css` and project-branding `palette/palette.json` |

`palette.css` is generated from `palette.json`. Change a colour in project-branding, then copy both files again. A colour's `use` line says where this site uses it.

Dark-R is `src/styles/theme/`. Where the showcase paints the name, the R is ® in Enterprsr and that character is not read. What it does is in `theme/README.md`. It loads fonts from `../fonts/woff2/`. This site imports `src/styles/palette.css`. The `palette.css` inside `assets/theme/` is for a project that links the theme on its own.

A lockup is the wordmark and the mark together (wide and compact). The plate is the inactive-border shape behind the mark. Geometry is in project-branding [`logo/README.md`](https://github.com/enterprise-r/project-branding/blob/main/logo/README.md).

## Pages

The bar (`bar.css`) is one stripe: breadcrumbs on the left, the logo in the middle, links and submenus on the right. Breadcrumbs show the active page. A page that also has a nav button leaves the nav while you are on it and shows there as the self-link. On Home the right nav is About and Login. On About it is Login. On Login it is About. Breakpoints follow the bar's width, not the window's. At 52rem and below the lockup becomes compact. At 40rem and below the compact logo docks to the left edge and the breadcrumbs wrap onto a second row. On Home the logo is the page heading (`h1`). It links home.

The ® crumb is Home. On Home it is the current page and does not navigate. When the logo docks, that crumb is hidden, because the docked logo already marks the root.

hyper-j is the site wallpaper, set once in `bar.css`. The style guide and the login page keep the flat page colour. Home and the 404 share one terminal and a mote field (`HomeWait.astro`, `Motes.astro`, `home.css`). The 404 turns the terminal 45 degrees. About's plates are in `about.css`.

The footer is a slim stripe: LinkedIn, X and GitHub, inline paths from Simple Icons (CC0). On a short page it sits at the bottom of the window. On the wallpaper the stripe is open and the icons switch to Foreground, so they stay legible on the page behind the stripe.
