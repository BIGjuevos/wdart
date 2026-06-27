#!/usr/bin/env python3
"""Generate all WDART vintage GIF assets. Zero external deps beyond Pillow."""
import os, math
from PIL import Image, ImageDraw, ImageFont

import os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

FONTS = "/System/Library/Fonts/Supplemental/"
def font(name, size):
    try:
        return ImageFont.truetype(FONTS + name, size)
    except Exception:
        return ImageFont.load_default()

# palette
NAVY   = (10, 35, 66)
NAVY2  = (0, 43, 92)
GOLD   = (201, 162, 39)
GOLDLT = (224, 192, 90)
CREAM  = (245, 240, 225)
RED    = (140, 22, 22)
BLACK  = (17, 17, 17)
YELLOW = (255, 204, 0)
WHITE  = (255, 255, 255)
NSGREEN= (0, 153, 0)

def save_gif(img, name, transparency=None):
    p = img.convert("P", palette=Image.ADAPTIVE, colors=255)
    kw = {}
    if transparency is not None:
        # find palette index nearest to transparency color handled by caller
        kw["transparency"] = transparency
    p.save(os.path.join(OUT, name), **kw)
    print("wrote", name, img.size)

# ---------------------------------------------------------------- spacer.gif
sp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
sp.save(os.path.join(OUT, "spacer.gif"), transparency=0)
print("wrote spacer.gif (1x1 transparent)")

# ---------------------------------------------------------------- bg.gif (tiled ledger)
TS = 48
bg = Image.new("RGB", (TS, TS), NAVY)
d = ImageDraw.Draw(bg)
grid = (18, 46, 84)
d.line([(0, 0), (TS, 0)], fill=grid)
d.line([(0, 0), (0, TS)], fill=grid)
# faint center crosshatch
d.line([(0, TS//2), (TS, TS//2)], fill=(14, 40, 74))
d.line([(TS//2, 0), (TS//2, TS)], fill=(14, 40, 74))
bg.save(os.path.join(OUT, "bg.gif"))
print("wrote bg.gif", bg.size)

# ---------------------------------------------------------------- crest.png (official seal)
# The seal artwork itself is supplied externally (assets/crest_new.png). Here we just
# crop it to a clean circle with an anti-aliased alpha edge so it floats on the navy
# masthead with the gold pinstripe ring as its visible border.
def process_crest(out=300, ss=4):
    srcp = os.path.join(OUT, "crest_new.png")
    if not os.path.exists(srcp):
        print("SKIP crest: assets/crest_new.png not found")
        return
    src = Image.open(srcp).convert("RGBA")
    W, H = src.size
    mask = Image.new("L", (W*ss, H*ss), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, W*ss-1, H*ss-1], fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)
    circ = src.copy()
    circ.putalpha(mask)
    circ.resize((out, out), Image.LANCZOS).save(os.path.join(OUT, "crest.png"))
    print("wrote crest.png (circular from crest_new.png)", (out, out))

process_crest(300, 4)

# ---------------------------------------------------------------- sponsor logo tiles
# Originals live in assets/logos/<slug>.png (downloaded vintage brand logos). We
# normalise each into a uniform white tile so the sponsor grid stays tidy.
def process_sponsor_tiles(tw=156, th=56):
    LOG = os.path.join(OUT, "logos")
    if not os.path.isdir(LOG):
        print("SKIP sponsor tiles: assets/logos not found")
        return
    slugs = ["netscape","geocities","macromedia","frontpage",
             "altavista","flash","compuserve","excite"]
    boxw, boxh = tw - 14, th - 12
    made = 0
    for s in slugs:
        srcp = os.path.join(LOG, s + ".png")
        if not os.path.exists(srcp):
            print("  missing logo:", s); continue
        im = Image.open(srcp).convert("RGBA")
        bb = im.getbbox()
        if bb: im = im.crop(bb)
        r = min(boxw/im.width, boxh/im.height)
        im = im.resize((max(1,int(im.width*r)), max(1,int(im.height*r))), Image.LANCZOS)
        tile = Image.new("RGB", (tw, th), WHITE)
        tile.paste(im, ((tw-im.width)//2, (th-im.height)//2), im)
        tile.save(os.path.join(LOG, s + "_cell.png"))
        made += 1
    print("wrote %d sponsor tiles (%dx%d)" % (made, tw, th))

process_sponsor_tiles()

# ---------------------------------------------------------------- construction.gif (animated)
CW, CH = 230, 38
def constr_frame(offset):
    im = Image.new("RGB", (CW, CH), YELLOW)
    d = ImageDraw.Draw(im)
    # hazard stripes top & bottom
    stripe_h = 7
    for y in (0, CH - stripe_h):
        for x in range(-stripe_h*2, CW + stripe_h*2, stripe_h*2):
            xx = x + (offset % (stripe_h*2))
            d.polygon([(xx, y), (xx+stripe_h, y), (xx, y+stripe_h)], fill=BLACK)
            d.polygon([(xx+stripe_h, y), (xx+stripe_h*2, y), (xx+stripe_h*2, y+stripe_h), (xx+stripe_h, y+stripe_h)], fill=BLACK)
            d.rectangle([xx, y, xx+stripe_h, y+stripe_h], fill=BLACK)
    d.rectangle([0,0,CW-1,CH-1], outline=BLACK)
    f = font("Arial Black.ttf", 15)
    txt = "UNDER CONSTRUCTION"
    bb = d.textbbox((0,0), txt, font=f)
    d.text((CW/2-(bb[2]-bb[0])/2, CH/2-(bb[3]-bb[1])/2-1), txt, font=f, fill=BLACK)
    return im
f1 = constr_frame(0).convert("P", palette=Image.ADAPTIVE, colors=16)
f2 = constr_frame(7).convert("P", palette=Image.ADAPTIVE, colors=16)
f1.save(os.path.join(OUT, "construction.gif"), save_all=True, append_images=[f2],
        duration=350, loop=0)
print("wrote construction.gif (animated)", (CW, CH))

# ---------------------------------------------------------------- badge-bestviewed.gif (88x31)
bw, bh = 88, 31
bv = Image.new("RGB", (bw, bh), BLACK)
d = ImageDraw.Draw(bv)
d.rectangle([0,0,bw-1,bh-1], outline=(90,90,90))
d.rectangle([0,0,bw-1,9], fill=NSGREEN)
f6 = font("Arial Bold.ttf", 8)
f7 = font("Arial.ttf", 8)
d.text((3,1), "BEST VIEWED IN", font=f6, fill=BLACK)
d.text((4,11), "Netscape", font=font("Georgia Bold.ttf", 11), fill=(120,200,255))
d.text((6,22), "800x600  16-bit", font=font("Arial.ttf",7), fill=(200,200,200))
bv.save(os.path.join(OUT, "badge-bestviewed.gif"))
print("wrote badge-bestviewed.gif", (bw,bh))

# ---------------------------------------------------------------- award.gif (rosette)
def render_award(aw=96, ah=116, ss=4):
    s = ss
    W, H = aw*s, ah*s
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    cx = W//2
    medal_cy = 36*s
    medal_r = 30*s
    # ribbon tails
    d.polygon([(cx-10*s, medal_cy+18*s),(cx-18*s, H-4*s),(cx, H-18*s)], fill=(120,16,16))
    d.polygon([(cx+10*s, medal_cy+18*s),(cx+18*s, H-4*s),(cx, H-18*s)], fill=RED)
    # fluted rosette edge (gold gear-ish disc behind medal)
    pts = []
    spokes = 24
    for k in range(spokes*2):
        a = math.pi*k/spokes
        rr = medal_r+6*s if k % 2 == 0 else medal_r+1*s
        pts.append((cx+rr*math.cos(a), medal_cy+rr*math.sin(a)))
    d.polygon(pts, fill=(168,132,20))
    # medal
    d.ellipse([cx-medal_r, medal_cy-medal_r, cx+medal_r, medal_cy+medal_r],
              fill=GOLD, outline=NAVY, width=3*s)
    d.ellipse([cx-medal_r+6*s, medal_cy-medal_r+6*s, cx+medal_r-6*s, medal_cy+medal_r-6*s],
              outline=GOLDLT, width=2*s)
    fa = font("Georgia Bold.ttf", 9*s)
    lines = ["COOL","SITE","AWARD"]
    for i, ln in enumerate(lines):
        bb = d.textbbox((0,0), ln, font=fa)
        d.text((cx-(bb[2]-bb[0])/2 - bb[0], medal_cy - 16*s + i*11*s - bb[1]),
               ln, font=fa, fill=NAVY)
    # caption
    fc = font("Arial Bold.ttf", 9*s)
    cap = "WDART APPROVED"
    bb = d.textbbox((0,0), cap, font=fc)
    d.text((cx-(bb[2]-bb[0])/2 - bb[0], H-12*s - bb[1]), cap, font=fc, fill=NAVY2)
    return img.resize((aw, ah), Image.LANCZOS)

award = render_award()
award.convert("P", palette=Image.ADAPTIVE, colors=255).save(os.path.join(OUT, "award.gif"))
print("wrote award.gif", award.size)

# ---------------------------------------------------------------- headerbar tile (navy gradient-ish)
hb = Image.new("RGB", (8, 34), NAVY2)
d = ImageDraw.Draw(hb)
for y in range(34):
    shade = int(92 - (abs(y-17)/17)*40)
    d.line([(0,y),(8,y)], fill=(0, int(shade*0.55), shade))
hb.save(os.path.join(OUT, "headerbar.gif"))
print("wrote headerbar.gif", hb.size)

print("\nDONE -> assets in", OUT)
print(os.listdir(OUT))
