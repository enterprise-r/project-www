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
