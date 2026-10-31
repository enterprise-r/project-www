#!/usr/bin/env python3
"""Regenerate public/assets/*.png from the logo sources in enterprise-r/r-art.

Sources stay in r-art (source/); this script only renders them.
  logo.png                     <- source/logo-badge-large.svg rendered at 1024
  favicon-16/32/48.png,
  apple-touch-icon.png (180),
  icon-192.png, icon-512.png   <- source/gen_final.py  logo-<N>.png

Needs: pip install cairosvg pillow   (plus the system cairo library)
Usage: R_ART_DIR=../r-art python3 scripts/build-assets.py [--out DIR]
       (R_ART_DIR defaults to ../r-art next to this repo; --out defaults to public/assets)
"""
import os, shutil, sys, tempfile
import cairosvg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R_ART = os.path.abspath(os.environ.get("R_ART_DIR", os.path.join(ROOT, "..", "r-art")))
SRC = os.path.join(R_ART, "source")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "public", "assets")
ICONS = {"favicon-16.png": 16, "favicon-32.png": 32, "favicon-48.png": 48,
         "apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512}

if not os.path.isfile(os.path.join(SRC, "gen_final.py")):
    sys.exit(f"r-art sources not found in {SRC}: clone enterprise-r/r-art there or set R_ART_DIR")
os.makedirs(OUT, exist_ok=True)

# 1. Logo: the badge (ink disc, glow from the bottom, gradient ring, RR).
cairosvg.svg2png(url=os.path.join(SRC, "logo-badge-large.svg"),
                 write_to=os.path.join(OUT, "logo.png"), output_width=1024, output_height=1024)
print("logo.png")

# 2. Icons: run r-art's gen_final.py into a temp dir. Its output dir is hardcoded,
#    so redirect it in memory (r-art itself is not modified).
tmp = tempfile.mkdtemp()
code = open(os.path.join(SRC, "gen_final.py")).read()
code = code.replace("OUT='/workspace/logo/asset2'", f"OUT={tmp!r}")
if repr(tmp) not in code:
    sys.exit("gen_final.py changed: its OUT line was not found; update scripts/build-assets.py")
cwd = os.getcwd(); os.chdir(SRC)  # gen_final.py reads gen.py and shapes.json from the cwd
try:
    exec(compile(code, "gen_final.py", "exec"), {"__name__": "__main__"})
finally:
    os.chdir(cwd)
for name, n in ICONS.items():
    shutil.copyfile(os.path.join(tmp, f"logo-{n}.png"), os.path.join(OUT, name))
    print(name)
shutil.rmtree(tmp)
print("wrote", OUT)
