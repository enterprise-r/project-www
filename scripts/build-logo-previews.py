#!/usr/bin/env python3
"""Logo PREVIEWS only (?logo=... on the site): recoloured copies of the r-art logo SVGs, rendered to
public/assets/preview/. The r-art masters and the live public/assets files are never written.

Variants: the dark green R (#0E6A3C) recoloured to a sage, plus a thin gap between the R and its
counter (the silver hole), so the hole reads as a hole again. The gap follows the counter contour:
it is the counter path itself, stroked with round joins underneath the counter fill, so only its
outer half shows (gap width = GAP user units).
  gap lime   : the gap filled with the outline lime #8DFF3C
  gap purple : the gap filled with the page purple #0C040F (page background; the badge disc is #0E0012)
  gap cut    : a true knockout, the R and its outline masked away so the background shows through

Usage: python3 scripts/build-logo-previews.py [--gap UNITS]   (R_ART_DIR defaults to ../r-art)
"""
import io, os, re, sys
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R_ART = os.path.abspath(os.environ.get("R_ART_DIR", os.path.join(ROOT, "..", "r-art")))
OUT = os.path.join(ROOT, "public", "assets", "preview")
GAP = float(sys.argv[sys.argv.index("--gap") + 1]) if "--gap" in sys.argv else 28.0
SRC = {"badge": os.path.join(R_ART, "source", "logo-badge-large.svg"),
       "mark": os.path.join(R_ART, "source", "logo-refined.svg")}
SAGES = {"sage": "#77AF8A", "deep": "#659474"}
GAPS = {"lime": "#8DFF3C", "purple": "#0C040F", "cut": None}

def variant(svg, fill, gap):
    svg = re.sub(r'(<path id="r-fill" d="[^"]+" fill=")#0E6A3C(")', rf'\g<1>{fill}\2', svg)
    counter_d = re.search(r'<path id="r-counter" d="([^"]+)"', svg).group(1)
    if gap is not None:   # a ring in the gap colour under the counter fill
        ring = (f'<path id="r-gap" d="{counter_d}" fill="{gap}" stroke="{gap}" '
                f'stroke-width="{2 * GAP:g}" stroke-linejoin="round"/>')
        svg = svg.replace('<path id="r-counter"', ring + '<path id="r-counter"', 1)
    else:                 # knockout: mask the outline and the fill with the grown counter
        mask = (f'<mask id="r-cut" maskUnits="userSpaceOnUse" x="-5000" y="-5000" width="10000" height="10000">'
                f'<rect x="-5000" y="-5000" width="10000" height="10000" fill="#fff"/>'
                f'<path d="{counter_d}" fill="#000" stroke="#000" stroke-width="{2 * GAP:g}" stroke-linejoin="round"/></mask>')
        svg = svg.replace('<defs>', '<defs>' + mask, 1)
        svg = re.sub(r'(<path id="r-outline".*?/>\s*<path id="r-fill".*?/>)', r'<g mask="url(#r-cut)">\1</g>', svg, count=1, flags=re.S)
    return svg

def raster(svg, width):
    """Render to RGBA. CairoSVG ignores <mask>, so a knockout is composited here: everything under
    the R, then the R (outline + fill) with the mask's black shape cut out of its alpha, then the
    counter on top. Browsers render the SVG's own mask the same way."""
    png = lambda s: Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=width, output_height=width if 'viewBox="0 0 1024 1024"' in s else None))).convert("RGBA")
    m = re.search(r'<mask id="r-cut".*?</mask>', svg, flags=re.S)
    if not m:
        return png(svg)
    plain = svg.replace(m.group(0), "")
    group = re.search(r'<g mask="url\(#r-cut\)">(.*?)</g>', plain, flags=re.S)
    r_layers, counter = group.group(1), re.search(r'<path id="r-counter".*?/>', plain).group(0)
    cut = re.search(r'<path d="[^"]+" fill="#000".*?/>', m.group(0)).group(0)
    under = plain.replace(group.group(0), "").replace(counter, "")
    def only(content):  # the same document and transforms, with just `content` inside the logo group
        s = re.sub(r'<g id="backdrop">.*?</g>|<g id="ring">.*?</g>', "", plain, flags=re.S)
        return re.sub(r'(<g id="logo"[^>]*>).*</g>', lambda g: g.group(1) + content + "</g>", s, count=1, flags=re.S)
    base, r, hole, top = png(under), png(only(r_layers)), png(only(cut)), png(only(counter))
    a = Image.eval(hole.getchannel("A"), lambda v: 255 - v)
    r.putalpha(Image.composite(r.getchannel("A"), Image.new("L", r.size, 0), a))
    base.alpha_composite(r); base.alpha_composite(top)
    return base

def fitted(svg, size, render=4096):
    img = raster(svg, render)
    img = img.crop(img.getchannel("A").getbbox())
    side = max(img.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    return sq.resize((size, size), Image.LANCZOS)

os.makedirs(OUT, exist_ok=True)
for s, fill in SAGES.items():
    for g, gap in GAPS.items():
        name = f"{s}-{g}"
        badge = variant(open(SRC["badge"]).read(), fill, gap)
        mark = variant(open(SRC["mark"]).read(), fill, gap)
        open(os.path.join(OUT, f"mark-{name}.svg"), "w").write(mark)
        raster(badge, 1024).save(os.path.join(OUT, f"logo-{name}.png"))
        fitted(mark, 192).save(os.path.join(OUT, f"icon-192-{name}.png"))
        print(name, fill, gap or "knockout", f"gap {GAP:g} units")
