#!/usr/bin/env python3
"""About backdrop PREVIEWS for portrait desktop screens (?bg=fill|tall). The WarpChi masters in art/
are only read, never written.

tall: a new web source, public/assets/preview/about-backdrop-tall.jpg (9:16, 2560 x 4552): the desktop
      picture untouched in the middle band (same 2560 px resize as about-backdrop.jpg), and 1556 px of
      space added above and below. The added space is
        - the sky colour measured in the picture's empty corners (#02060F),
        - the colours of the picture's edge carried outwards as a soft, uneven glow that fades into
          the sky in ~300 px (the purple and silver wisps carry on and die out); the outer 170 px of
          the picture (sky and wisp ends only, far from the ship and the hand) are eased into it,
        - stars cut from the picture's clean star field (top left, no grid), dark sky removed,
          laid in random flipped and turned tiles, so the density, size and colour are the picture's.
fill: public/assets/preview/stars-{a,b,c}.svg, three star tiles in the picture's density and
      colours, drawn by the CSS (site.css, "Portrait backdrop") at three co-prime sizes, so the
      repeat never lines up.

Usage: python3 scripts/build-portrait-previews.py
"""
import os, random
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "assets", "preview")
W, H = 2560, 1440
TALL_H = 4552                       # 9:16, the narrowest portrait desktop (1080 x 1920, 1440 x 2560)
E = (TALL_H - H) // 2
rng = np.random.default_rng(7)
random.seed(7)

pic = np.asarray(Image.open(os.path.join(ROOT, "art", "warpchi.jpg")).convert("RGB")
                 .resize((W, H), Image.LANCZOS)).astype(np.float32)
clean = pic[0:220, 0:1100]          # star field with no grid and no vortex
sky = np.median(clean.reshape(-1, 3), 0)
stars_src = np.clip(clean - ndimage.median_filter(clean, size=(15, 15, 1)), 0, 255)

def star_layer(h, w, t=200):
    out = np.zeros((h, w, 3), np.float32)
    for y in range(0, h, t):
        for x in range(0, w, t):
            sy, sx = rng.integers(0, clean.shape[0] - t), rng.integers(0, clean.shape[1] - t)
            p = stars_src[sy:sy + t, sx:sx + t]
            if rng.random() < .5: p = p[::-1]
            if rng.random() < .5: p = p[:, ::-1]
            if rng.random() < .5: p = p.transpose(1, 0, 2)
            out[y:y + t, x:x + t] = p[:min(t, h - y), :min(t, w - x)]
    return out

def noise(h, w, sigma):
    n = ndimage.gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), sigma)
    return n / n.std()

FEATHER = 170                       # rows of the picture's outer edge eased into the new space

def extension(p):
    """p: the picture, with the seam at row 0. Returns (E new rows, nearest first; the eased picture)."""
    edge = ndimage.gaussian_filter(p[:60].mean(0), sigma=(28, 0))              # the edge's colours
    d = np.arange(-FEATHER, E, dtype=np.float32)[:, None, None]
    wisps = 1 + 0.45 * noise(len(d), W, 45)[..., None]                         # uneven, nebulous
    fade = np.exp(-np.clip(d, 0, None) / 300) * np.clip(wisps, 0.2, 2)
    glow = sky + (edge - sky)[None] * fade * 0.85
    new = glow[FEATHER:] + star_layer(E, W)
    u = 1 - np.arange(FEATHER, dtype=np.float32)[:, None, None] / FEATHER     # 1 at the seam, 0 inside
    ease = 0.9 * u * u * (3 - 2 * u)                                             # smoothstep
    eased = p.copy()
    eased[:FEATHER] = p[:FEATHER] * (1 - ease) + glow[:FEATHER][::-1] * ease
    return new, eased

top, eased = extension(pic)
bottom, eased = extension(eased[::-1])
tall = np.concatenate([top[::-1], eased[::-1], bottom])
os.makedirs(OUT, exist_ok=True)
img = Image.fromarray(np.uint8(np.clip(tall, 0, 255).round()))
for w, q in ((2560, 72), (1600, 72)):   # q72: dark space, no visible loss next to the q84 picture
    name = "about-backdrop-tall.jpg" if w == 2560 else f"about-backdrop-tall-{w}.jpg"
    (img if w == 2560 else img.resize((w, round(TALL_H * w / W)), Image.LANCZOS)).save(
        os.path.join(OUT, name), quality=q, optimize=True, progressive=True)
    print(name, os.path.getsize(os.path.join(OUT, name)) // 1024, "KB")

# Star tiles for ?bg=fill, in the picture's own pixels (2560 wide); the CSS scales them with the
# picture (background-size in vw), so a star is as big and as dense as in the picture at any width.
lum = clean.mean(2)
lab, n = ndimage.label(lum - ndimage.median_filter(lum, 15) > 24)  # stars, not the faint dust
pos = ndimage.maximum_position(lum, lab, range(1, n + 1))
cols = np.array([clean[y, x] for y, x in pos])                    # each star's colour at its centre
peaks = cols.mean(1)
density = n / lum.size                                            # stars per picture pixel
print("stars per 1000 x 1000 picture px:", round(density * 1e6), "sky", sky.round())
for name, t in (("a", 487), ("b", 613), ("c", 761)):
    k = int(density * t * t / 3)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{t}" height="{t}" viewBox="0 0 {t} {t}">']
    for _ in range(k):
        c = cols[rng.integers(len(cols))]
        b = float(rng.choice(peaks)) / 255
        r = 1.1 + 0.9 * rng.random() ** 3 + 0.6 * b   # >= 1.1 so a star survives the zoom-out
        x, y = rng.random() * t, rng.random() * t
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}" opacity="{min(1, .45 + b):.2f}"/>')
    out.append("</svg>")
    open(os.path.join(OUT, f"stars-{name}.svg"), "w").write("".join(out))
    print(f"stars-{name}.svg", k, "stars", os.path.getsize(os.path.join(OUT, f"stars-{name}.svg")) // 1024, "KB")
