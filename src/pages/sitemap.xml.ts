// Sitemap: the indexed pages only (not /showcase/ or the 404, which are noindex).
import type { APIRoute } from "astro";

const pages = ["/", "/about/", "/login/"];

export const GET: APIRoute = ({ site }) => {
  const urls = pages.map((p) => `  <url><loc>${new URL(p, site).href}</loc></url>`).join("\n");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;
  return new Response(xml, { headers: { "Content-Type": "application/xml" } });
};
