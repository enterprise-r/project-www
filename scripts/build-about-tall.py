#!/usr/bin/env python3
"""About backdrop for portrait and near-square screens that are not phones (site.css, "About picture
on portrait and near-square screens"). The WarpChi masters in art/ are only read, never written.

public/assets/about-backdrop-tall.{avif,webp,jpg} (9:16, 2560 x 4552) and -1600.{avif,webp,jpg}: the
desktop picture untouched in the middle band (same 2560 px resize as about-backdrop.jpg), and 1556 px
of space added above and below. The added space is
  - the sky colour measured in the picture's empty corners (#02060F),
  - the colours of the picture's edge carried outwards as a soft, uneven glow that fades into the sky
    in ~300 px (the purple and silver wisps carry on and die out); the outer 170 px of the picture
    (sky and wisp ends only, far from the ship and the hand) are eased into it,
  - stars cut from the picture's clean star field (top left, no grid), dark sky removed, laid in
    random flipped and turned tiles, so the density, size and colour are the picture's.

Usage: python3 scripts/build-about-tall.py
"""
import os, random
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "assets")
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
img = Image.fromarray(np.uint8(np.clip(tall, 0, 255).round()))
for w in (2560, 1600):
    base = os.path.join(OUT, "about-backdrop-tall" + ("" if w == 2560 else f"-{w}"))
    im = img if w == 2560 else img.resize((w, round(TALL_H * w / W)), Image.LANCZOS)
    im.save(base + ".jpg", quality=72, optimize=True, progressive=True)  # q72: dark space, no visible loss
    im.save(base + ".webp", quality=74, method=6)
    im.save(base + ".avif", quality=55, speed=4)
    for ext in ("avif", "webp", "jpg"):
        print(os.path.basename(base) + "." + ext, os.path.getsize(base + "." + ext) // 1024, "KB")
