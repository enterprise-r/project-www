import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://www.enterprise-r.com",
  // Keep the built HTML readable (same layout as the hand-written page).
  compressHTML: false,
});
