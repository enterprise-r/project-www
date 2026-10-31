import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.enterprise-r.com",
  // Keep the built HTML readable.
  compressHTML: false,
  // Stylesheets stay files. Auto would inline about.css into the HTML.
  build: { inlineStylesheets: "never" },
});
