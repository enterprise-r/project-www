import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.enterprise-r.com",
  // Keep the built HTML readable.
  compressHTML: false,
  // Stylesheets stay files. Auto would inline about.css into the HTML.
  build: { inlineStylesheets: "never" },
  vite: {
    build: {
      // wait.svg is under Vite's 4kb inline limit; keep theme icons as files
      // so the waiting icon's CSS animation runs in <img>.
      assetsInlineLimit: (id, buf) => {
        if (String(id).includes("theme/icons/")) return false;
        return buf.length < 4096;
      },
    },
  },
});
