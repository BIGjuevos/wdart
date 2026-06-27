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

# ---------------------------------------------------------------- crest.gif (official seal)
S = 300
crest = Image.new("RGB", (S, S), CREAM)
d = ImageDraw.Draw(crest)
cx = cy = S // 2
# outer rings
d.ellipse([8, 8, S-8, S-8], outline=NAVY, width=6)
d.ellipse([22, 22, S-22, S-22], fill=NAVY2, outline=GOLD, width=3)
d.ellipse([78, 78, S-78, S-78], outline=GOLD, width=2)
# inner disc
d.ellipse([86, 86, S-86, S-86], fill=CREAM)

def arc_text(draw, text, radius, start_deg, end_deg, fnt, fill, flip=False):
    n = len(text)
    if n == 1:
        ang = (start_deg + end_deg) / 2
    span = (end_deg - start_deg)
    for i, ch in enumerate(text):
        t = i / max(n - 1, 1)
        ang = start_deg + span * t
        rad = math.radians(ang)
        # char image
        bb = font_bbox(fnt, ch)
        cw, chh = bb
        ci = Image.new("RGBA", (cw + 4, chh + 4), (0, 0, 0, 0))
        ImageDraw.Draw(ci).text((2, 2), ch, font=fnt, fill=fill)
        rot = -(ang + 90) if not flip else -(ang - 90)
        ci = ci.rotate(rot, expand=1, resample=Image.BICUBIC)
        px = cx + radius * math.cos(rad) - ci.width / 2
        py = cy + radius * math.sin(rad) - ci.height / 2
        crest.paste(ci, (int(px), int(py)), ci)

def font_bbox(fnt, ch):
    bb = fnt.getbbox(ch)
    return (bb[2] - bb[0] + 1, bb[3] - bb[1] + 1)

ring_font = font("Georgia Bold.ttf", 17)
R = 122
# top arc text (reads left-to-right across the top)
arc_text(d, "WEB DEVELOPMENT ASSOCIATION", R, 205, 335, ring_font, GOLDLT)
# bottom arc
arc_text(d, "TABLES FOR LAYOUT", R, 145, 35, ring_font, GOLDLT, flip=True)
# side diamonds in the gaps
for ang in (180, 0):
    dx = cx + R*math.cos(math.radians(ang))
    dy = cy + R*math.sin(math.radians(ang))
    d.polygon([(dx, dy-6),(dx+6, dy),(dx, dy+6),(dx-6, dy)], fill=GOLDLT)

# center glyph </td>
glyph_font = font("Courier New Bold.ttf", 52)
g = "</td>"
bb = d.textbbox((0, 0), g, font=glyph_font)
d.text((cx - (bb[2]-bb[0])/2, cy - (bb[3]-bb[1])/2 - 20), g, font=glyph_font, fill=NAVY2)
# motto banner
mfont = font("Georgia Bold Italic.ttf", 15)
m = "STRUCTURA SUPER OMNIA"
bb = d.textbbox((0,0), m, font=mfont)
d.rectangle([cx-(bb[2]-bb[0])/2-10, cy+24, cx+(bb[2]-bb[0])/2+10, cy+48], fill=NAVY2)
d.text((cx-(bb[2]-bb[0])/2, cy+27), m, font=mfont, fill=GOLDLT)
# est
efont = font("Georgia.ttf", 13)
e = "EST. 2026"
bb = d.textbbox((0,0), e, font=efont)
d.text((cx-(bb[2]-bb[0])/2, cy+54), e, font=efont, fill=NAVY2)
crest.save(os.path.join(OUT, "crest.gif"))
print("wrote crest.gif", crest.size)

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
aw, ah = 96, 116
aw_img = Image.new("RGB", (aw, ah), CREAM)
d = ImageDraw.Draw(aw_img)
# ribbon tails
d.polygon([(38,60),(30,112),(48,96),(48,60)], fill=RED)
d.polygon([(58,60),(66,112),(48,96),(48,60)], fill=(110,16,16))
# medal
d.ellipse([20,8,76,64], fill=GOLD, outline=NAVY, width=3)
d.ellipse([28,16,68,56], outline=GOLDLT, width=2)
fa = font("Georgia Bold.ttf", 9)
for i,(line) in enumerate(["COOL","SITE","AWARD"]):
    bb = d.textbbox((0,0), line, font=fa)
    d.text((48-(bb[2]-bb[0])/2, 20+i*12), line, font=fa, fill=NAVY)
# caption
fc = font("Arial Bold.ttf", 9)
cap="WDART APPROVED"
bb=d.textbbox((0,0),cap,font=fc)
d.text((aw/2-(bb[2]-bb[0])/2, 104), cap, font=fc, fill=NAVY2)
aw_img.save(os.path.join(OUT, "award.gif"))
print("wrote award.gif", (aw,ah))

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
