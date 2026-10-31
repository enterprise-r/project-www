import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.enterprise-r.com",
  // Keep the built HTML readable (same layout as the hand-written page).
  compressHTML: false,
  // Page sheets stay files. Auto would inline home.css and about.css into the HTML.
  build: { inlineStylesheets: "never" },
});
