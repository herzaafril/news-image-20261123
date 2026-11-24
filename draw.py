#!/usr/bin/env python3
"""Draw the news-image-20261123 V2 entry: a richer newspaper front-page
dashboard summing up Monday 23 November 2026. V2 vs V1: a Monday timeline
strip, richer lead illustrations, CONFIRMED/OFFICIAL tags, a taller map with
a Europe zoom inset and bigger pins. V2 art pass (Herza: "biar ada seni nya,
biar ga kosong banget"): fuller scene illustrations in all 8 panels,
masthead/footer ornaments, map graticule + compass rose + ships, a framed
region key with count chips, and shaded list rows. 1024x1024 PNG, drawn with
PIL (no AI image generation, so every letter is crisp). Run: python3 draw.py
Writes entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (22, 22, 22)
GREY = (105, 105, 105)
LIGHT_GREY = (210, 205, 192)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
BLUE = (29, 78, 137)
TEAL = (15, 118, 110)
SEA = (208, 226, 240)
LAND = (214, 206, 178)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FDIR + "DejaVuSerif-Bold.ttf"
SERIF = FDIR + "DejaVuSerif.ttf"
SANS_B = FDIR + "DejaVuSans-Bold.ttf"
SANS = FDIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=font(SERIF_B, 40),
       fill=INK, anchor="ma")
for dx in (168, 856):
    d.polygon([(dx, 20), (dx + 8, 28), (dx, 36), (dx - 8, 28)], fill=RED)
d.rectangle([16, 58, 1008, 92], fill=INK)
for dx in (40, 984):
    d.polygon([(dx, 67), (dx + 7, 75), (dx, 83), (dx - 7, 75)],
              fill=(255, 210, 90))
d.text((W // 2, 62), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 24),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 97),
       "Every story on this page happened, or was first reported, on Monday 23 November 2026",
       font=font(SANS, 13), fill=GREY, anchor="ma")
d.line([16, 118, 1008, 118], fill=INK, width=2)
d.line([16, 121, 1008, 121], fill=INK, width=1)

# ---------------------------------------------------------------- timeline strip
# Replaces V1's stats strip: the Atlas-format rival runs a "THE DAY IN UTC"
# strip, and timed events prove the day. Local times (zones differ).
d.rectangle([16, 126, 1008, 152], fill=(16, 28, 52))
d.line([16, 126, 1008, 126], fill=(255, 210, 90), width=2)
d.line([16, 152, 1008, 152], fill=(255, 210, 90), width=2)
tl_x = 26
d.text((tl_x, 133), "MONDAY'S TIMELINE", font=font(SANS_B, 11),
       fill=(255, 210, 90))
tl_x += d.textlength("MONDAY'S TIMELINE  ", font=font(SANS_B, 11))
tl_items = [
    ("03:28", "Dymer: woman, 79, rescued"),
    ("07:00", "Brussels airports shut"),
    ("12:00", "Shuri Castle reopens"),
    ("15:30", "Burnham presents EU deal"),
]
for t, txt in tl_items:
    seg = t + " " + txt + "   ·   "
    if tl_x + d.textlength(seg, font=font(SANS, 11)) > 1000:
        break
    d.text((tl_x, 133), t, font=font(SANS_B, 11), fill=(120, 230, 160))
    tl_x += d.textlength(t + " ", font=font(SANS_B, 11))
    d.text((tl_x, 133), txt, font=font(SANS, 11), fill=(230, 235, 245))
    tl_x += d.textlength(txt, font=font(SANS, 11))
    d.text((tl_x, 133), "   ·   ", font=font(SANS, 11), fill=(120, 140, 170))
    tl_x += d.textlength("   ·   ", font=font(SANS, 11))
d.line([16, 156, 1008, 156], fill=INK, width=1)

# ---------------------------------------------------------------- illustrations
def panel(x, y, w, h, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=1)
    return d


def ill_cop31(x, y, w, h):
    panel(x, y, w, h, (14, 74, 74))
    # globe
    cx, cy, r = x + 78, y + h // 2 + 4, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 190, 220),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - 20, cy - r, cx + 20, cy + r], outline=(255, 255, 255), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.arc([cx - r, cy - 24, cx + r, cy + 24], 0, 360, fill=(255, 255, 255), width=1)
    # landmasses on the globe
    d.polygon([(cx - 30, cy - 18), (cx - 12, cy - 26), (cx - 2, cy - 10),
               (cx - 18, cy - 2)], fill=(110, 190, 130))
    d.polygon([(cx + 6, cy + 8), (cx + 26, cy + 2), (cx + 32, cy + 20),
               (cx + 12, cy + 26)], fill=(110, 190, 130))
    d.ellipse([cx - 6, cy + 22, cx + 10, cy + 34], fill=(110, 190, 130))
    # summit hall: curtain backdrop, flag row above the table, delegates
    for bx in range(x + 140, x + w - 4, 18):
        d.rectangle([bx, y + 4, bx + 9, y + h - 30], fill=(12, 62, 62))
    tx, ty = x + 150, y + h - 44
    for i, col in enumerate([(30, 90, 180), (40, 160, 90), (230, 200, 40),
                             (200, 60, 40), (150, 80, 180), (220, 140, 30),
                             (60, 180, 200)]):
        fx = tx + 6 + i * 21
        d.line([fx, ty - 48, fx, ty - 26], fill=(255, 255, 255), width=2)
        d.rectangle([fx, ty - 48, fx + 15, ty - 39], fill=col)
    for sx in (tx + 14, tx + 38, tx + 62, tx + 86, tx + 110, tx + 134):
        d.ellipse([sx - 6, ty - 30, sx + 6, ty - 18], fill=(30, 40, 45))
        d.rectangle([sx - 9, ty - 18, sx + 9, ty], fill=(30, 40, 45))
    # chandelier + red carpet
    d.line([x + 165, y + 4, x + 165, y + 16], fill=(255, 210, 90), width=2)
    d.ellipse([x + 158, y + 16, x + 172, y + 26], fill=(255, 210, 90))
    for lx in (x + 156, x + 165, x + 174):
        d.ellipse([lx - 2, y + 27, lx + 2, y + 31], fill=(255, 240, 180))
    d.rectangle([tx - 6, ty + 28, tx + 156, ty + 34], fill=(140, 30, 30))
    d.rectangle([tx, ty, tx + 150, ty + 8], fill=(240, 230, 200))
    d.rectangle([tx + 12, ty + 8, tx + 20, ty + 28], fill=(240, 230, 200))
    d.rectangle([tx + 130, ty + 8, tx + 138, ty + 28], fill=(240, 230, 200))
    d.text((x + 12, y + h - 24), "ANTALYA · COP31", font=font(SANS_B, 11),
           fill=(170, 230, 220))
    # NO DEAL stamp
    st = Image.new("RGBA", (130, 44), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([2, 2, 127, 41], outline=(255, 70, 60), width=4)
    sd.text((65, 22), "NO DEAL", font=font(SANS_B, 20), fill=(255, 70, 60),
            anchor="mm")
    st = st.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(st, (x + w - 142, y + 6), st)


def ill_dymer(x, y, w, h):
    panel(x, y, w, h, (52, 58, 74))
    # dusk sky + moon
    d.ellipse([x + w - 52, y + 10, x + w - 26, y + 36], fill=(240, 230, 190))
    # standing part of the block
    bx, by, bw, bh = x + 30, y + 34, 130, h - 54
    d.rectangle([bx, by, bx + bw, by + bh], fill=(150, 150, 158))
    for r in range(4):
        for c in range(4):
            wx = bx + 12 + c * 30
            wy = by + 12 + r * 22
            col = (255, 210, 90) if (r + c) % 3 == 0 else (70, 76, 90)
            d.rectangle([wx, wy, wx + 16, wy + 12], fill=col)
    # collapsed section: jagged break + rubble
    d.polygon([(bx + bw, by + 10), (bx + bw + 70, by + 30),
               (bx + bw + 40, by + 60), (bx + bw + 78, by + 90),
               (bx + bw + 20, by + bh), (bx + bw, by + bh)],
              fill=(110, 108, 112))
    d.polygon([(bx + bw - 10, by + bh), (bx + bw + 90, by + bh),
               (bx + bw + 130, by + bh), (bx + bw + 60, by + bh - 26),
               (bx + bw + 20, by + bh - 12)], fill=(90, 88, 92))
    # rescue lights
    for lx, ly in [(bx + bw + 46, by + bh - 14), (bx + bw + 96, by + bh - 6),
                   (bx + 60, by + bh - 4)]:
        d.ellipse([lx - 4, ly - 4, lx + 4, ly + 4], fill=(255, 170, 40))
    # rescue crane + searchlight beams (richer scene than V1)
    kx = x + w - 30
    d.line([kx, y + 40, kx, by + bh], fill=(200, 190, 170), width=4)
    d.line([kx, y + 40, kx - 70, y + 40], fill=(200, 190, 170), width=4)
    d.line([kx - 70, y + 40, kx - 70, y + 66], fill=(200, 190, 170), width=2)
    d.polygon([(kx - 74, y + 66), (kx - 66, y + 66), (kx - 70, y + 76)],
              fill=(255, 170, 40))
    # stars, smoke, rescue workers, ambulance
    for sx, sy in [(x + 180, y + 12), (x + 200, y + 18), (x + 240, y + 10),
                   (x + 250, y + 34), (x + 196, y + 30)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(230, 230, 240))
    for sx, sy, sr in [(x + 215, y + 28, 7), (x + 236, y + 19, 9),
                       (x + 258, y + 26, 6)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(115, 115, 122))
    for wx, wy in [(bx + bw + 30, by + bh - 26), (bx + bw + 62, by + bh - 30),
                   (bx + bw + 88, by + bh - 20)]:
        d.ellipse([wx - 3, wy - 12, wx + 3, wy - 6], fill=(255, 210, 150))
        d.pieslice([wx - 4, wy - 15, wx + 4, wy - 7], 180, 360,
                   fill=(255, 200, 40))
        d.rectangle([wx - 3, wy - 6, wx + 3, wy + 2], fill=(230, 120, 40))
    d.rectangle([x + 155, y + 121, x + 205, y + 136], fill=(240, 240, 240))
    d.rectangle([x + 176, y + 123, x + 180, y + 131], fill=(220, 40, 40))
    d.rectangle([x + 173, y + 126, x + 183, y + 130], fill=(220, 40, 40))
    d.ellipse([x + 163, y + 133, x + 171, y + 139], fill=(20, 20, 20))
    d.ellipse([x + 189, y + 133, x + 197, y + 139], fill=(20, 20, 20))
    d.ellipse([x + 178, y + 118, x + 184, y + 122], fill=(255, 60, 60))
    d.text((x + 12, y + h - 24), "DAY OF MOURNING", font=font(SANS_B, 10),
           fill=(220, 220, 220))
    d.text((x + w - 12, y + h - 26), "11 DEAD", font=font(SANS_B, 20),
           fill=(255, 120, 100), anchor="ra")


def ill_markets(x, y, w, h):
    panel(x, y, w, h, (16, 28, 52))
    # grid
    for gy in range(y + 16, y + h - 8, 22):
        d.line([x + 10, gy, x + w - 10, gy], fill=(50, 66, 96), width=1)
    for gx in range(x + 40, x + w - 10, 40):
        d.line([gx, y + 14, gx, y + h - 10], fill=(40, 56, 84), width=1)
    # candlesticks behind the lines
    for cx, ch, col in [(x + 30, 18, (150, 60, 55)), (x + 60, 24, (150, 60, 55)),
                        (x + 90, 14, (70, 150, 100)), (x + 120, 26, (150, 60, 55)),
                        (x + 150, 20, (150, 60, 55)), (x + 180, 30, (150, 60, 55)),
                        (x + 210, 16, (70, 150, 100)), (x + 240, 28, (150, 60, 55))]:
        cy = y + 40 + (cx - x) // 12
        d.line([cx, cy - ch - 6, cx, cy + 6], fill=col, width=1)
        d.rectangle([cx - 5, cy - ch, cx + 5, cy], fill=col)
    # crashing line (Kospi)
    pts = [(x + 16, y + 18), (x + 70, y + 30), (x + 120, y + 26),
           (x + 170, y + 58), (x + 210, y + 52), (x + 260, y + 88),
           (x + 300, y + 108)]
    d.line(pts, fill=(255, 80, 70), width=5, joint="curve")
    for px, py in pts[1:]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 80, 70))
    # second line: Sensex opened up, then swung (green, gentler)
    pts2 = [(x + 16, y + 44), (x + 70, y + 38), (x + 120, y + 44),
            (x + 170, y + 40), (x + 210, y + 48), (x + 260, y + 44)]
    d.line(pts2, fill=(120, 220, 160), width=3, joint="curve")
    # third line: Taiwan index, choppy then down (yellow)
    pts3 = [(x + 16, y + 64), (x + 70, y + 56), (x + 120, y + 66),
            (x + 170, y + 74), (x + 210, y + 70)]
    d.line(pts3, fill=(230, 200, 90), width=2, joint="curve")
    # small green futures arrow
    d.line([(x + w - 88, y + h - 22), (x + w - 30, y + h - 52)],
           fill=(80, 220, 130), width=4)
    d.polygon([(x + w - 30, y + h - 52), (x + w - 44, y + h - 50),
               (x + w - 32, y + h - 38)], fill=(80, 220, 130))
    d.text((x + 14, y + h - 34), "KOSPI -3.3%", font=font(SANS_B, 22),
           fill=(255, 90, 80))
    d.text((x + 14, y + 8), "TOKYO CLOSED", font=font(SANS_B, 10),
           fill=(150, 170, 210))
    d.text((x + w - 14, y + 10), "US FUTURES +2%", font=font(SANS_B, 11),
           fill=(120, 230, 160), anchor="ra")


def ill_democrats(x, y, w, h):
    panel(x, y, w, h, (26, 64, 128))
    # stars in the sky
    for sx, sy in [(x + 14, y + 40), (x + 40, y + 44), (x + 62, y + 36),
                   (x + 132, y + 8), (x + 172, y + 36)]:
        d.polygon([(sx, sy - 4), (sx + 1, sy - 1), (sx + 4, sy),
                   (sx + 1, sy + 1), (sx, sy + 4), (sx - 1, sy + 1),
                   (sx - 4, sy), (sx - 1, sy - 1)], fill=(255, 255, 255))
    # capitol dome silhouette, sized to fit the panel
    cx = x + w // 2 + 18
    base = y + h - 8
    d.rectangle([cx - 48, base - 14, cx + 48, base], fill=(240, 240, 235))
    d.rectangle([cx - 22, base - 28, cx + 22, base - 14], fill=(240, 240, 235))
    d.pieslice([cx - 26, base - 52, cx + 26, base - 6], 180, 360,
               fill=(240, 240, 235))
    d.rectangle([cx - 2, base - 60, cx + 2, base - 50], fill=(240, 240, 235))
    for i in range(5):
        colx = cx - 40 + i * 19
        d.line([colx, base - 12, colx, base - 2], fill=(26, 64, 128), width=3)
    # side wings, gold finial, flag on the left wing, crowd at the base
    d.rectangle([cx - 76, base - 10, cx - 48, base], fill=(225, 225, 220))
    d.rectangle([cx + 48, base - 10, cx + 76, base], fill=(225, 225, 220))
    d.ellipse([cx - 3, base - 64, cx + 3, base - 58], fill=(255, 210, 90))
    d.line([cx - 70, base - 26, cx - 70, base - 10], fill=(255, 255, 255),
           width=2)
    d.rectangle([cx - 70, base - 26, cx - 58, base - 19], fill=(200, 60, 50))
    d.rectangle([cx - 70, base - 26, cx - 63, base - 22], fill=(40, 80, 160))
    for hx in range(cx - 44, cx + 46, 9):
        d.ellipse([hx - 2, base - 5, hx + 2, base - 1], fill=(15, 40, 80))
    d.text((x + 8, y + 6), "258", font=font(SANS_B, 24), fill=(255, 255, 255))
    d.text((x + w - 8, y + 8), "HOUSE", font=font(SANS_B, 11),
           fill=(180, 210, 245), anchor="ra")


def ill_cikande(x, y, w, h):
    panel(x, y, w, h, (40, 32, 30))
    # factory + chimney
    d.rectangle([x + 18, y + h - 44, x + 120, y + h - 8], fill=(120, 116, 112))
    d.rectangle([x + 132, y + 22, x + 150, y + h - 8], fill=(140, 136, 132))
    # flames (orange outer, yellow inner) + embers
    for fx, fh, col in [(30, 30, (255, 140, 30)), (55, 42, (255, 90, 30)),
                        (82, 28, (255, 170, 40)), (105, 36, (255, 110, 30))]:
        d.polygon([(x + fx, y + h - 44), (x + fx + 10, y + h - 44 - fh),
                   (x + fx + 20, y + h - 44)], fill=col)
        d.polygon([(x + fx + 5, y + h - 44), (x + fx + 10, y + h - 44 - fh + 12),
                   (x + fx + 15, y + h - 44)], fill=(255, 220, 90))
    for ex, ey in [(x + 40, y + 6), (x + 66, y + 2), (x + 92, y + 8),
                   (x + 118, y + 4), (x + 78, y + 14)]:
        d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 180, 60))
    # smoke
    for sx, sy, sr in [(150, 18, 9), (162, 8, 12), (178, 14, 8),
                       (170, 26, 7), (186, 26, 6)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(150, 150, 150))
    # fire truck (foreground, left) + water jet arcing onto the flames
    d.rectangle([x + 6, y + h - 22, x + 52, y + h - 8], fill=(200, 40, 40))
    d.rectangle([x + 6, y + h - 22, x + 20, y + h - 14], fill=(220, 60, 60))
    d.line([x + 10, y + h - 30, x + 44, y + h - 22], fill=(220, 220, 220), width=2)
    d.ellipse([x + 12, y + h - 10, x + 20, y + h - 4], fill=(20, 20, 20))
    d.ellipse([x + 38, y + h - 10, x + 46, y + h - 4], fill=(20, 20, 20))
    for ti in range(11):
        t = ti / 10
        jx = int((1 - t) ** 2 * 46 + 2 * (1 - t) * t * 75 + t * t * 100)
        jy = int((1 - t) ** 2 * 44 + 2 * (1 - t) * t * 12 + t * t * 28)
        d.ellipse([x + jx - 2, y + jy - 2, x + jx + 2, y + jy + 2],
                  fill=(140, 200, 240))
    d.text((x + w - 10, y + h - 30), "24 DEAD", font=font(SANS_B, 17),
           fill=(255, 150, 80), anchor="ra")


def ill_merkury(x, y, w, h):
    panel(x, y, w, h, (18, 52, 84))
    # distant shoreline (Benghazi coast) + sea
    d.rectangle([x + 6, y + h - 52, x + w - 6, y + h - 46], fill=(30, 70, 105))
    for bx in (x + 70, x + 88, x + 150, x + 168):
        d.rectangle([bx, y + h - 60, bx + 10, y + h - 52], fill=(30, 70, 105))
    for wy in range(y + h - 26, y + h - 2, 8):
        d.line([x + 6, wy, x + w - 6, wy], fill=(120, 180, 220), width=2)
    # listing ship
    hull = [(x + 40, y + h - 40), (x + 150, y + h - 58), (x + 158, y + h - 44),
            (x + 150, y + h - 30), (x + 60, y + h - 22)]
    d.polygon(hull, fill=(200, 200, 200))
    d.rectangle([x + 88, y + h - 74, x + 116, y + h - 58], fill=(200, 200, 200))
    d.line([x + 102, y + h - 92, x + 102, y + h - 74], fill=(200, 200, 200),
           width=3)
    # explosion at the stern + fire
    ex, ey = x + 42, y + 32
    d.polygon([(ex, ey - 12), (ex + 4, ey - 4), (ex + 12, ey - 6),
               (ex + 6, ey), (ex + 12, ey + 6), (ex + 4, ey + 4),
               (ex, ey + 12), (ex - 4, ey + 4), (ex - 12, ey + 6),
               (ex - 6, ey), (ex - 12, ey - 6), (ex - 4, ey - 4)],
              fill=(255, 160, 40))
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 230, 120))
    # drones (sea-drone swarm) with wake trails
    for dx, dy in [(120, 12), (150, 20), (172, 10), (72, 12), (180, 30)]:
        d.line([x + dx - 14, y + dy + 6, x + dx - 4, y + dy + 2],
               fill=(255, 220, 80), width=1)
        d.ellipse([x + dx - 4, y + dy - 4, x + dx + 4, y + dy + 4],
                  fill=(255, 220, 80))
    # wake + debris
    d.line([x + 42, y + 52, x + 12, y + 62], fill=(200, 230, 250), width=2)
    d.line([x + 42, y + 52, x + 12, y + 44], fill=(200, 230, 250), width=2)
    for bx, by in [(x + 22, y + 60), (x + 32, y + 66), (x + 16, y + 68)]:
        d.rectangle([bx, by, bx + 6, by + 3], fill=(90, 90, 90))
    d.text((x + 8, y + 6), "SUNK", font=font(SANS_B, 17),
           fill=(255, 220, 80))


def ill_belgium(x, y, w, h):
    panel(x, y, w, h, (226, 230, 232))
    # clouds
    for cx, cy, cr in [(x + 70, y + 12, 8), (x + 88, y + 8, 10),
                       (x + 128, y + 16, 7)]:
        d.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2],
                  fill=(255, 255, 255))
    # terminal building + control tower behind the runway
    d.rectangle([x + 30, y + h - 34, x + 150, y + h - 18], fill=(180, 186, 190))
    for wx in range(x + 38, x + 146, 14):
        d.rectangle([wx, y + h - 30, wx + 8, y + h - 24], fill=(90, 110, 140))
    d.rectangle([x + 8, y + 36, x + 16, y + h - 18], fill=(160, 166, 170))
    d.rectangle([x + 5, y + 28, x + 19, y + 36], fill=(120, 130, 140))
    # runway
    d.rectangle([x, y + h - 18, x + w, y + h - 8], fill=(90, 90, 90))
    for rx in range(x + 8, x + w - 8, 20):
        d.line([rx, y + h - 13, rx + 10, y + h - 13], fill=(255, 255, 255),
               width=2)
    # plane silhouette on the ground
    px, py = x + 20, y + h - 42
    d.ellipse([px, py, px + 110, py + 16], fill=(60, 90, 140))
    d.polygon([(px + 40, py + 4), (px + 66, py - 16), (px + 78, py - 16),
               (px + 66, py + 6)], fill=(60, 90, 140))
    d.polygon([(px + 86, py + 2), (px + 112, py - 8), (px + 112, py + 2)],
              fill=(60, 90, 140))
    # landing gear + luggage cart on the apron
    for gx in (px + 30, px + 90):
        d.line([gx, py + 16, gx, y + h - 18], fill=(60, 90, 140), width=2)
        d.ellipse([gx - 3, y + h - 20, gx + 3, y + h - 14], fill=(30, 30, 30))
    d.rectangle([x + 142, y + h - 16, x + 170, y + h - 10], fill=(200, 180, 60))
    d.ellipse([x + 146, y + h - 11, x + 152, y + h - 7], fill=(30, 30, 30))
    d.ellipse([x + 160, y + h - 11, x + 166, y + h - 7], fill=(30, 30, 30))
    # no-entry sign
    cx, cy, r = x + w - 34, y + 28, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=5)
    d.line([cx - r + 4, cy + r - 4, cx + r - 4, cy - r + 4], fill=RED, width=5)
    d.text((x + 10, y + 8), "SHUT", font=font(SANS_B, 16), fill=RED)


def ill_wwc(x, y, w, h):
    panel(x, y, w, h, (22, 120, 70))
    # stadium stands: crowd dots along the top-left
    for cx in range(x + 8, x + 108, 8):
        for cy in (y + 5, y + 11):
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2],
                      fill=(255, 255, 255) if (cx + cy) % 16 == 0 else (200, 230, 200))
    # pitch lines: centre circle, halfway line, penalty boxes, goals
    d.ellipse([x + w // 2 - 34, y + h // 2 - 22, x + w // 2 + 34,
               y + h // 2 + 22], outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 6, x + w // 2, y + h - 6], fill=(255, 255, 255),
           width=2)
    d.rectangle([x + 2, y + h // 2 - 16, x + 16, y + h // 2 + 16],
                outline=(255, 255, 255), width=2)
    d.rectangle([x + w - 16, y + h // 2 - 16, x + w - 2, y + h // 2 + 16],
                outline=(255, 255, 255), width=2)
    d.rectangle([x + 1, y + h // 2 - 8, x + 5, y + h // 2 + 8],
                outline=(255, 255, 255), width=2)
    d.rectangle([x + w - 5, y + h // 2 - 8, x + w - 1, y + h // 2 + 8],
                outline=(255, 255, 255), width=2)
    # ball
    bx, by, br = x + 34, y + h - 30, 17
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
              outline=INK, width=1)
    d.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 6),
               (bx - 4, by + 6), (bx - 7, by - 2)], fill=INK)
    # players + trophy
    for px, py in [(x + 70, y + 50), (x + 120, y + 30), (x + 145, y + 54)]:
        d.ellipse([px - 3, py - 10, px + 3, py - 4], fill=(255, 255, 255))
        d.rectangle([px - 3, py - 4, px + 3, py + 4], fill=(255, 255, 255))
    tx, ty = x + 166, y + 56
    d.polygon([(tx - 6, ty), (tx + 6, ty), (tx + 4, ty + 8), (tx - 4, ty + 8)],
              fill=(255, 210, 90))
    d.rectangle([tx - 1, ty + 8, tx + 1, ty + 12], fill=(255, 210, 90))
    d.rectangle([tx - 5, ty + 12, tx + 5, ty + 15], fill=(255, 210, 90))
    d.text((x + w - 10, y + 8), "2035", font=font(SANS_B, 26),
           fill=(255, 255, 255), anchor="ra")
    d.text((x + w - 10, y + 38), "UK HOSTS", font=font(SANS_B, 11),
           fill=(200, 240, 210), anchor="ra")


# ---------------------------------------------------------------- leads (3)
LEADS = [
    ("GLOBAL · CLIMATE — CONFIRMED", "COP31 COLLAPSES: NO DEAL",
     "After a record ~49 hours of overtime, the Antalya summit ends with no "
     "agreement. The EU and ~130 countries reject a final text that never "
     "mentions fossil fuels.",
     "Reuters", ill_cop31),
    ("EUROPE · UKRAINE — CONFIRMED", "DYMER TOLL RISES TO 11",
     "Rescuers pull a boy, 7, alive from a flattened block hit by a Russian "
     "drone; a woman, 79, is found alive at 03:28. Fifteen dead across the "
     "Kyiv region; Monday is a day of mourning.",
     "BBC / Reuters", ill_dymer),
    ("ASIA · MARKETS — CONFIRMED", "AI ROUT HITS ASIA",
     "Seoul's Kospi falls 3.3% as the AI sell-off spreads; Taiwan bans short "
     "sales below the prior close and Seoul readies a stabilisation fund. "
     "US futures rebound 2%.",
     "Bloomberg / Reuters", ill_markets),
]
ly = 162
for i, (kick, head, deck, src, ill) in enumerate(LEADS):
    x = 16 + i * 336
    ill(x, ly, 322, 140)
    d.text((x, ly + 146), kick, font=font(SANS_B, 11), fill=RED)
    y = draw_lines(d, x, ly + 162, wrap(d, head, font(SERIF_B, 19), 322),
                   font(SERIF_B, 19), INK, 21)
    y = draw_lines(d, x, y + 3, wrap(d, deck, font(SANS, 12), 322),
                   font(SANS, 12), INK, 14)
    d.text((x, y + 2), "Source: " + src, font=font(SANS, 10), fill=GREY)
d.line([16, 418, 1008, 418], fill=INK, width=1)

# ---------------------------------------------------------------- tier 2 (5)
TIER2 = [
    ("AMERICAS — CONFIRMED", "DEMOCRATS CLINCH 258 HOUSE SEATS",
     "NC recount confirms Hubbard's win; biggest House majority since 1992.",
     "dpa / BBC", ill_democrats),
    ("ASIA — CONFIRMED", "24 DEAD IN CIKANDE FACTORY FIRE",
     "24 dead at a gutted candy factory in Banten; dozens still missing.",
     "Reuters", ill_cikande),
    ("AFRICA — CONFIRMED", "UKRAINE SINKS RUSSIAN CORVETTE",
     "Zelenskyy confirms sea drones sank the Merkury off Benghazi, Libya.",
     "CNN / Reuters", ill_merkury),
    ("EUROPE — OFFICIAL", "BELGIAN AIRPORTS SHUT MONDAY",
     "ATC stops 07:00-21:00 in a strike; 429 flights grounded.",
     "skeyes", ill_belgium),
    ("SPORT — OFFICIAL", "UK TO HOST 2035 WOMEN'S WORLD CUP",
     "FIFA confirms the bid: 48 teams, 104 matches, first UK finals since '66.",
     "FIFA / BBC", ill_wwc),
]
ty = 424
for i, (kick, head, deck, src, ill) in enumerate(TIER2):
    x = 17 + i * 200
    ill(x, ty, 190, 76)
    d.text((x, ty + 80), kick, font=font(SANS_B, 10), fill=RED)
    y = draw_lines(d, x, ty + 94, wrap(d, head, font(SERIF_B, 13), 190),
                   font(SERIF_B, 13), INK, 15)
    y = draw_lines(d, x, y + 2, wrap(d, deck, font(SANS, 10), 190),
                   font(SANS, 10), INK, 12)
    d.text((x, y + 1), "Source: " + src, font=font(SANS, 9), fill=GREY)
d.line([16, 594, 1008, 594], fill=INK, width=1)


# ---------------------------------------------------------------- map strip
MAP_X, MAP_Y, MAP_W, MAP_H = 16, 600, 620, 104


def ll2xy(lon, lat):
    return (MAP_X + (lon + 170) / 360 * MAP_W,
            MAP_Y + (75 - lat) / 130 * MAP_H)


d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
            outline=INK, width=1)
# graticule: light lat/lon lines under the land
for lon in range(-150, 181, 30):
    gx, _ = ll2xy(lon, 75)
    d.line([gx, MAP_Y, gx, MAP_Y + MAP_H], fill=(185, 205, 222), width=1)
for lat in (-40, -10, 20, 50):
    _, gy = ll2xy(0, lat)
    d.line([MAP_X, gy, MAP_X + MAP_W, gy], fill=(185, 205, 222), width=1)
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 62), (-55, 52), (-60, 45), (-75, 35), (-80, 25),
     (-90, 21), (-97, 16), (-105, 20), (-110, 25), (-120, 34), (-125, 40),
     (-125, 49), (-135, 57), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 11), (-60, 8), (-50, 0), (-35, -8), (-35, -20),
     (-40, -30), (-48, -28), (-52, -32), (-58, -38), (-62, -41), (-65, -45),
     (-68, -52), (-70, -55), (-73, -50), (-73, -40), (-73, -30), (-70, -20),
     (-75, -15), (-80, -5), (-80, 5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 53), (3, 58), (5, 60),
     (10, 57), (10, 59), (18, 56), (21, 55), (24, 58), (21, 65), (18, 69),
     (25, 71), (30, 70), (32, 66), (28, 60), (30, 55), (28, 50), (24, 46),
     (28, 44), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (32, 20),
     (38, 18), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -26), (28, -33), (20, -35), (17, -29), (15, -22), (12, -18),
     (13, -12), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 15), (-16, 20),
     (-10, 30)],
    # Asia
    [(30, 36), (35, 36), (44, 39), (48, 30), (52, 26), (56, 27), (58, 23),
     (60, 25), (66, 25), (67, 23), (72, 20), (76, 8), (80, 7), (80, 15),
     (85, 20), (88, 22), (91, 22), (92, 16), (94, 17), (97, 10), (100, 7),
     (103, 1), (104, 9), (106, 10), (109, 13), (108, 18), (105, 20),
     (110, 21), (120, 22), (122, 25), (120, 30), (122, 32), (126, 33),
     (127, 35), (129, 33), (130, 42), (132, 43), (135, 44), (137, 46),
     (140, 40), (141, 45), (142, 50), (137, 54), (135, 59), (140, 60),
     (150, 60), (158, 52), (160, 55), (162, 60), (170, 60), (178, 65),
     (178, 68), (170, 70), (160, 72), (150, 72), (140, 72), (130, 72),
     (120, 73), (110, 74), (100, 76), (90, 75), (80, 73), (70, 72),
     (60, 69), (55, 68), (50, 60), (45, 55), (40, 50), (35, 45), (32, 42),
     (30, 40)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -38),
     (150, -37), (153, -30), (153, -27), (150, -23), (146, -19), (142, -11),
     (142, -15), (140, -17), (136, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (117, -20)],
    # Indonesia (schematic)
    [(95, 5), (105, 0), (114, -3), (120, -7), (130, -3), (140, -8),
     (141, -2), (135, 0), (128, 2), (120, 1), (110, 2), (100, 5)],
]
for poly in CONTINENTS:
    d.polygon([ll2xy(lon, lat) for lon, lat in poly], fill=LAND,
              outline=(150, 142, 118))
# numbered dots: the 8 illustrated stories (dx, dy nudge the crowded
# European cluster apart so the numbers stay legible)
DOTS = [(1, 30.7, 36.9, 8, 3), (2, 30.5, 50.5, 5, -5), (3, 127, 37.5, 0, 0),
        (4, -77, 39, 0, 0), (5, 106.5, -6.2, 0, 0), (6, 20, 32.1, -3, 6),
        (7, 4.4, 50.8, 7, 7), (8, -0.1, 51.5, -7, -7)]
for n, lon, lat, dx, dy in DOTS:
    cx, cy = ll2xy(lon, lat)
    cx, cy = cx + dx, cy + dy
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy - 1), str(n), font=font(SANS_B, 11), fill=(255, 255, 255),
           anchor="mm")
# compass rose (South Pacific, empty water) + tiny ships
rx, ry = MAP_X + 585, MAP_Y + 82
d.ellipse([rx - 15, ry - 15, rx + 15, ry + 15], outline=(120, 140, 160),
          width=1)
d.polygon([(rx, ry - 13), (rx + 3, ry), (rx, ry + 13), (rx - 3, ry)],
          fill=(120, 140, 160))
d.polygon([(rx - 13, ry), (rx, ry - 3), (rx + 13, ry), (rx, ry + 3)],
          fill=(120, 140, 160))
d.text((rx, ry - 24), "N", font=font(SANS_B, 8), fill=(120, 140, 160),
       anchor="mm")
for sx, sy in [(258, 652), (447, 676)]:
    d.polygon([(sx - 8, sy), (sx + 8, sy), (sx + 5, sy + 4), (sx - 5, sy + 4)],
              fill=(90, 110, 130))
    d.line([sx, sy, sx, sy - 7], fill=(90, 110, 130), width=1)
d.text((MAP_X + 6, MAP_Y + 4), "WHERE IT HAPPENED", font=font(SANS_B, 10),
       fill=INK)
# Europe zoom inset (Atlas-format idea): the European pins crowd together
# on the main map, so show them enlarged. Covers empty Pacific + the
# western edge of North America; no pins there.
IX, IY, IW, IH = MAP_X + 8, MAP_Y + MAP_H - 76, 140, 70
d.rectangle([IX, IY, IX + IW, IY + IH], fill=(232, 240, 248),
            outline=INK, width=1)
d.text((IX + 5, IY + 3), "EUROPE — ZOOM", font=font(SANS_B, 8), fill=INK)


def eu2xy(lon, lat):
    return (IX + 4 + (lon + 12) / 47 * (IW - 8),
            IY + 14 + (72 - lat) / 42 * (IH - 18))


d.polygon([eu2xy(lon, lat) for lon, lat in CONTINENTS[2]], fill=LAND,
          outline=(150, 142, 118))
for n, lon, lat in [(1, 30.7, 36.9), (2, 30.5, 50.5), (6, 20, 32.1),
                    (7, 4.4, 50.8), (8, -0.1, 51.5)]:
    cx, cy = eu2xy(lon, lat)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy - 1), str(n), font=font(SANS_B, 8), fill=(255, 255, 255),
           anchor="mm")

# region key (right of map)
kx, ky = 652, 600
d.rectangle([644, 598, 1008, 708], outline=(180, 172, 152), width=1)
d.line([kx + 180, ky + 2, kx + 180, ky + 90], fill=(210, 205, 192), width=1)
d.line([kx, ky + 100, kx + 348, ky + 100], fill=(180, 172, 152), width=1)
d.polygon([(kx + 174, ky + 95), (kx + 179, ky + 100), (kx + 174, ky + 105),
           (kx + 169, ky + 100)], fill=RED)
d.text((kx, ky), "30 STORIES BY REGION", font=font(SANS_B, 12), fill=INK)
regions = [("EUROPE", 11), ("ASIA", 5), ("AMERICAS", 5), ("AFRICA", 4),
           ("MIDDLE EAST", 3), ("OCEANIA", 1), ("GLOBAL", 1)]
for i, (name, cnt) in enumerate(regions):
    ry = ky + 20 + i * 10
    d.text((kx, ry), name, font=font(SANS_B, 10), fill=INK)
    d.rectangle([kx + 146, ry - 1, kx + 170, ry + 11], fill=RED)
    d.text((kx + 158, ry), str(cnt), font=font(SANS_B, 10),
           fill=(255, 255, 255), anchor="ma")
d.text((kx + 190, ky), "Numbered dots on the map =", font=font(SANS, 10),
       fill=GREY)
d.text((kx + 190, ky + 13), "the 8 illustrated stories", font=font(SANS, 10),
       fill=GREY)
d.text((kx + 190, ky + 30), "1 COP31  2 Dymer", font=font(SANS, 10), fill=INK)
d.text((kx + 190, ky + 43), "3 Markets  4 House", font=font(SANS, 10),
       fill=INK)
d.text((kx + 190, ky + 56), "5 Cikande  6 Merkury", font=font(SANS, 10),
       fill=INK)
d.text((kx + 190, ky + 69), "7 Brussels  8 WWC", font=font(SANS, 10),
       fill=INK)

# ---------------------------------------------------------------- numbered list
d.line([16, 710, 1008, 710], fill=INK, width=1)
d.text((16, 715), "ALSO ON MONDAY 23 NOVEMBER — 22 MORE STORIES",
       font=font(SANS_B, 14), fill=INK)
LIST = [
    "9. Shuri Castle reopens — rebuilt hall opens at noon, 7 years after fire (NHK)",
    "10. US postpones any Iran strike — decision put off at least a week (Ynet)",
    "11. US ports face daily cyberattacks — hundreds of attempts a day (FT)",
    "12. UN, US condemn Khartoum drone strikes — 4 killed, UN building hit (AFP)",
    "13. Bolsonaro stable in intensive care — day 3, no discharge date (One Turn)",
    "14. Fighting traps Ebola teams in Congo hospital — staff sheltering 24h+ (WHO)",
    "15. California braces for record king tides — 8.1 ft Monday, 8.6 ft Wed (NWS)",
    "16. Gaza contamination report out — pollution signs across >99% (Oxfam)",
    "17. India gives Nepal NPR 24,000 crore package — Modi-Shah talks (MEA)",
    "18. NATO meets after Russian missiles fell in Poland — 3 Kh-101 (NATO)",
    "19. Wellington Test ends in a draw — New Zealand bat out 120 overs (Cricinfo)",
    "20. V4 + Austria meet in Bratislava — EU budget, Ukraine aid (Visegrad)",
    "21. Second group of sick Gaza children lands in UK for NHS care (GOV.UK)",
    "22. Kim: North Korea seeks security, not supremacy (KCNA / Yonhap)",
    "23. Libya oil output plunges 365,000 bpd — pipelines shut (NOC)",
    "24. Burnham sells 'landmark' EU deal to MPs — claims £17bn boost (BBC)",
    "25. Russia fires 153 drones overnight — 134 downed; Kharkiv hit (Air Force)",
    "26. Ukrainian drones hit 3 Russian oil sites — refinery halts (ASTRA)",
    "27. Trump urges Nvidia to rehire Huang — shares up 9% premarket (TipRanks)",
    "28. Bomb threats hit schools in Germany and Denmark — 450 schools (Reuters)",
    "29. Germany: NATO will defend 'every inch' — Wadephul in Berlin (DW)",
    "30. Saudi strike on Hodeida kills 6, Houthi media say — 18 hurt (AP)",
]
lf = font(SANS, 12)
d.line([510, 736, 510, 934], fill=(210, 205, 192), width=1)
for i, item in enumerate(LIST):
    col = 0 if i < 11 else 1
    row = i % 11
    x = 16 if col == 0 else 522
    y = 738 + row * 18
    if row % 2 == 0:
        d.rectangle([x - 4, y - 2, x + 486, y + 14], fill=(246, 242, 232))
    wpx = d.textlength(item, font=lf)
    if wpx > 486:
        print("WARN: list item too wide (%d px): %s" % (wpx, item))
    # bold the number
    num = item.split(".")[0] + "."
    d.text((x, y), num, font=font(SANS_B, 12), fill=RED)
    d.text((x + d.textlength(num + " ", font=font(SANS_B, 12)), y),
           item[len(num) + 1:], font=lf, fill=INK)

# ---------------------------------------------------------------- DATE CHECK footer
d.line([16, 936, 1008, 936], fill=(210, 205, 192), width=1)
d.rectangle([16, 942, 1008, 1016], fill=(255, 240, 238), outline=RED, width=1)
for dx, dy in [(22, 949), (1002, 949), (22, 1009), (1002, 1009)]:
    d.polygon([(dx, dy - 4), (dx + 4, dy), (dx, dy + 4), (dx - 4, dy)],
              fill=RED)
d.text((28, 947), "DATE CHECK — DELIBERATELY LEFT OUT (they happened earlier):",
       font=font(SANS_B, 11), fill=DARKRED)
d.text((28, 962),
       "Riemann proof — 20 Nov  ·  ICJ Myanmar ruling — 19 Nov  ·  Anthropic debut — 19 Nov ($83 was the IPO price; shares opened $111.50)  ·  El Chapo captured — Friday",
       font=font(SANS, 11), fill=INK)
d.text((28, 977),
       "S&P 500 -3.7% — Friday's close  ·  Nikkei -5.06% — Friday (Tokyo shut Monday)  ·  Verstappen, Las Vegas GP — Saturday  ·  Alcaraz, ATP Finals — Sunday",
       font=font(SANS, 11), fill=INK)
d.text((28, 992),
       "NOT YET KNOWN at press time: Wall Street's Monday close  ·  the final Cikande toll.",
       font=font(SANS_B, 11), fill=INK)

img.save("entry.png", optimize=True)
print("saved entry.png")
