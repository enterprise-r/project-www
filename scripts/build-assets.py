#!/usr/bin/env python3
"""Render the site's derived images in public/assets/.

Lockups and favicons are the files from Google Drive assets/logos/.
Copy those in. This script does not draw them. It builds the link-preview JPEG.

Needs: pip install cairosvg pillow   (cairosvg needs the system cairo library)
Usage: python3 scripts/build-assets.py [--mark SVG] [--backdrop JPG] [--out DIR]
  Defaults: --mark      public/assets/logo-color.svg   (Drive assets/logos/svg/logo-color.svg)
            --backdrop  ../project-branding/wallpapers/warpchi.jpg   (a project-branding checkout next to this repo)
            --out       public/assets
"""
import io, os, sys
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

SOURCES = {
    "mark": arg("--mark", os.path.join(ROOT, "public", "assets", "logo-color.svg")),  # colour mark, transparent
}
BACKDROP = arg("--backdrop", os.path.join(os.path.dirname(ROOT), "project-branding", "wallpapers", "warpchi.jpg"))  # WarpChi wallpaper
OUT = arg("--out", os.path.join(ROOT, "public", "assets"))

# Link preview (og:image): the backdrop scaled and centre-cropped to 1200x630, the mark small in the top-left corner.
OG = {"name": "og-image.jpg", "size": (1200, 630), "mark": 72, "margin": 32, "quality": 85}

RENDER_PX = 4096  # the long side the SVG is rasterised at to find its visible bounds
DIRECT_MAX = 48   # sizes up to this are drawn straight at the target size (crisp favicons);
                  # larger ones are cut from the 4096 px render and scaled down with LANCZOS

ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

_fitted = {}
def _fit(svg_path):
    """Render the SVG as it is at RENDER_PX, trim to its visible pixels (alpha > 0) and return the
    trimmed image centred on a transparent square, plus that square in SVG user units."""
    if svg_path not in _fitted:
        w, h = Image.open(io.BytesIO(cairosvg.svg2png(url=svg_path))).size
        k = RENDER_PX / max(w, h)
        W, H = round(w * k), round(h * k)
        img = Image.open(io.BytesIO(cairosvg.svg2png(url=svg_path, output_width=W, output_height=H))).convert("RGBA")
        box = img.getchannel("A").getbbox()
        if box is None:
            sys.exit(f"{svg_path}: renders fully transparent")
        img = img.crop(box)
        side = max(img.size)
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
        # the same square in user units (viewBox mapped onto W x H, preserveAspectRatio xMidYMid meet)
        vb = ET.parse(svg_path).getroot().get("viewBox")
        vx, vy, vw, vh = map(float, vb.replace(",", " ").split()) if vb else (0.0, 0.0, float(w), float(h))
        s = min(W / vw, H / vh)
        ox, oy = (W - vw * s) / 2, (H - vh * s) / 2
        cx = vx + ((box[0] + box[2]) / 2 - ox) / s
        cy = vy + ((box[1] + box[3]) / 2 - oy) / s
        u = max(box[2] - box[0], box[3] - box[1]) / s
        _fitted[svg_path] = (square, (cx - u / 2, cy - u / 2, u, u))
    return _fitted[svg_path]

def fitted(svg_path, size):
    """The SVG trimmed to its visible artwork, centred on a transparent square with no margin, at
    `size` px. Handles any SVG cairosvg can draw."""
    square, (x, y, u, _) = _fit(svg_path)
    if size > DIRECT_MAX:
        return square.resize((size, size), Image.LANCZOS)
    # small sizes: same SVG, root viewBox set to the visible square, drawn straight at `size` px
    tree = ET.parse(svg_path)
    root = tree.getroot()
    root.set("viewBox", f"{x:.4f} {y:.4f} {u:.4f} {u:.4f}")
    root.set("width", str(size))
    root.set("height", str(size))
    root.set("preserveAspectRatio", "xMidYMid meet")
    png = cairosvg.svg2png(bytestring=ET.tostring(root), url=svg_path, output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")

for src in SOURCES.values():
    if not os.path.isfile(src):
        sys.exit(f"source SVG not found: {src} (set --mark)")
os.makedirs(OUT, exist_ok=True)

if not os.path.isfile(BACKDROP):
    sys.exit(f"backdrop not found: {BACKDROP} (set --backdrop)")
W, H = OG["size"]
bg = Image.open(BACKDROP).convert("RGB")
k = max(W / bg.width, H / bg.height)
bg = bg.resize((round(bg.width * k), round(bg.height * k)), Image.LANCZOS)
x, y = (bg.width - W) // 2, (bg.height - H) // 2
bg = bg.crop((x, y, x + W, y + H))
m = OG["mark"]
mark = fitted(SOURCES["mark"], m)
bg.paste(mark, (OG["margin"], OG["margin"]), mark)
bg.save(os.path.join(OUT, OG["name"]), quality=OG["quality"], optimize=True, progressive=True)
print(f'{OG["name"]:22s} {W}x{H}  <- {os.path.relpath(BACKDROP, ROOT) if BACKDROP.startswith(ROOT) else BACKDROP} + mark')
