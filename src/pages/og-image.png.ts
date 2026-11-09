// Link preview (og:image): 1200x400, the wide logo 1000 px wide, centred on the title bar colour.
import type { APIRoute } from "astro";
import sharp from "sharp";
import logo from "../../public/assets/logo-wide.svg?raw";
import palette from "../styles/palette.json";

// The title bar background in styles/bar.css (header).
const bar = palette.groups.flatMap((g) => g.colours).find((c) => c.var === "--ui-border")!.hex;

export const GET: APIRoute = async () => {
  const mark = await sharp(Buffer.from(logo), { density: 72 * 1000 / 320 * 2 }).resize({ width: 1000 }).png().toBuffer();
  const png = await sharp({ create: { width: 1200, height: 400, channels: 3, background: bar } })
    .composite([{ input: mark, gravity: "centre" }])
    .removeAlpha()
    .png()
    .toBuffer();
  return new Response(png, { headers: { "Content-Type": "image/png" } });
};
