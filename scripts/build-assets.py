#!/usr/bin/env python3
"""Render the site's images (public/assets/*.png) from logo source SVGs in enterprise-r/r-art.

The SVGs stay in r-art. Which files the site needs, and at what size, is a web concern,
so that list lives here (OUTPUTS below).

Needs: pip install cairosvg   (plus the system cairo library)
Usage: python3 scripts/build-assets.py [--badge SVG] [--mark SVG] [--out DIR]
  Defaults: --badge $R_ART_DIR/source/logo-badge-large.svg
            --mark  $R_ART_DIR/source/logo-refined.svg
            --out   public/assets       (R_ART_DIR defaults to ../r-art next to this repo)
"""
import io, os, sys
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R_ART = os.path.abspath(os.environ.get("R_ART_DIR", os.path.join(ROOT, "..", "r-art")))

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

SOURCES = {
    "badge": arg("--badge", os.path.join(R_ART, "source", "logo-badge-large.svg")),  # full badge
    "mark": arg("--mark", os.path.join(R_ART, "source", "logo-refined.svg")),        # RR monogram only
}
BACKDROP = arg("--backdrop", os.path.join(ROOT, "art", "warpchi.jpg"))  # WarpChi wallpaper (Drive Wallpapers/)
OUT = arg("--out", os.path.join(ROOT, "public", "assets"))

# name, source, size (square px), how:
#   "render" = draw the SVG as it is; "fit" = transparent square, visible artwork trimmed and fitted edge to edge, centred
OUTPUTS = [
    ("logo.png",             "badge", 1024, "render"),
    ("favicon-16.png",       "mark",    16, "fit"),
    ("favicon-32.png",       "mark",    32, "fit"),
    ("favicon-48.png",       "mark",    48, "fit"),
    ("apple-touch-icon.png", "mark",   180, "fit"),
    ("icon-192.png",         "mark",   192, "fit"),
    ("icon-512.png",         "mark",   512, "fit"),
]
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
        sys.exit(f"source SVG not found: {src}\nclone enterprise-r/r-art next to this repo, or set R_ART_DIR / --badge / --mark")
os.makedirs(OUT, exist_ok=True)
for name, src, size, how in OUTPUTS:
    dest = os.path.join(OUT, name)
    if how == "render":
        cairosvg.svg2png(url=SOURCES[src], write_to=dest, output_width=size, output_height=size)
    else:
        fitted(SOURCES[src], size).save(dest)
    print(f"{name:22s} {size:>4}px  <- {os.path.relpath(SOURCES[src], R_ART) if SOURCES[src].startswith(R_ART) else SOURCES[src]}")

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
print(f'{OG["name"]:22s} {W}x{H}  <- {os.path.relpath(BACKDROP, ROOT)} + mark')
