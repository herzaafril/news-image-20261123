#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: a dense newspaper front-page dashboard
summing up Monday 23 November 2026. 1024x1024 PNG, drawn with PIL (no AI
image generation, so every letter is crisp). Run: python3 draw.py
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
d.rectangle([16, 58, 1008, 92], fill=INK)
d.text((W // 2, 62), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 24),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 97),
       "Every story on this page happened, or was first reported, on Monday 23 November 2026",
       font=font(SANS, 13), fill=GREY, anchor="ma")
d.line([16, 118, 1008, 118], fill=INK, width=2)
d.line([16, 121, 1008, 121], fill=INK, width=1)

# ---------------------------------------------------------------- stats strip
stats = [
    ("11", "DEAD IN DYMER"),
    ("15", "DEAD, KYIV REGION"),
    ("258", "HOUSE SEATS (D)"),
    ("365,000", "BPD OIL LOST"),
    ("-3.3%", "KOSPI, SEOUL"),
    ("24", "DEAD IN CIKANDE"),
]
sx, sw = 16, 992 // 6
for i, (num, lab) in enumerate(stats):
    cx = sx + i * sw + sw // 2
    d.text((cx, 126), num, font=font(SANS_B, 17), fill=RED, anchor="ma")
    d.text((cx, 146), lab, font=font(SANS_B, 9), fill=INK, anchor="ma")
    if i:
        d.line([sx + i * sw, 128, sx + i * sw, 160], fill=LIGHT_GREY, width=1)
d.line([16, 164, 1008, 164], fill=INK, width=1)

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
    # summit table with flags
    tx, ty = x + 150, y + h - 44
    d.rectangle([tx, ty, tx + 150, ty + 8], fill=(240, 230, 200))
    d.rectangle([tx + 12, ty + 8, tx + 20, ty + 28], fill=(240, 230, 200))
    d.rectangle([tx + 130, ty + 8, tx + 138, ty + 28], fill=(240, 230, 200))
    for i, col in enumerate([(30, 90, 180), (40, 160, 90), (230, 200, 40),
                             (200, 60, 40), (150, 80, 180)]):
        fx = tx + 14 + i * 28
        d.line([fx, ty - 22, fx, ty], fill=(255, 255, 255), width=2)
        d.rectangle([fx, ty - 22, fx + 18, ty - 12], fill=col)
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
    d.text((x + w - 12, y + h - 26), "11 DEAD", font=font(SANS_B, 20),
           fill=(255, 120, 100), anchor="ra")


def ill_markets(x, y, w, h):
    panel(x, y, w, h, (16, 28, 52))
    # grid
    for gy in range(y + 16, y + h - 8, 22):
        d.line([x + 10, gy, x + w - 10, gy], fill=(50, 66, 96), width=1)
    # crashing line
    pts = [(x + 16, y + 18), (x + 70, y + 30), (x + 120, y + 26),
           (x + 170, y + 58), (x + 210, y + 52), (x + 260, y + 88),
           (x + 300, y + 108)]
    d.line(pts, fill=(255, 80, 70), width=5, joint="curve")
    for px, py in pts[1:]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 80, 70))
    # small green futures arrow
    d.line([(x + w - 88, y + h - 22), (x + w - 30, y + h - 52)],
           fill=(80, 220, 130), width=4)
    d.polygon([(x + w - 30, y + h - 52), (x + w - 44, y + h - 50),
               (x + w - 32, y + h - 38)], fill=(80, 220, 130))
    d.text((x + 14, y + h - 34), "KOSPI -3.3%", font=font(SANS_B, 22),
           fill=(255, 90, 80))
    d.text((x + w - 14, y + 10), "US FUTURES +2%", font=font(SANS_B, 11),
           fill=(120, 230, 160), anchor="ra")


def ill_democrats(x, y, w, h):
    panel(x, y, w, h, (26, 64, 128))
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
    d.text((x + 8, y + 6), "258", font=font(SANS_B, 24), fill=(255, 255, 255))
    d.text((x + w - 8, y + 8), "HOUSE", font=font(SANS_B, 11),
           fill=(180, 210, 245), anchor="ra")


def ill_cikande(x, y, w, h):
    panel(x, y, w, h, (40, 32, 30))
    # factory + chimney
    d.rectangle([x + 18, y + h - 44, x + 120, y + h - 8], fill=(120, 116, 112))
    d.rectangle([x + 132, y + 22, x + 150, y + h - 8], fill=(140, 136, 132))
    # flames
    for fx, fh, col in [(30, 30, (255, 140, 30)), (55, 42, (255, 90, 30)),
                        (82, 28, (255, 170, 40)), (105, 36, (255, 110, 30))]:
        d.polygon([(x + fx, y + h - 44), (x + fx + 10, y + h - 44 - fh),
                   (x + fx + 20, y + h - 44)], fill=col)
    # smoke
    for sx, sy, sr in [(150, 18, 9), (162, 8, 12), (178, 14, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(150, 150, 150))
    d.text((x + w - 10, y + h - 30), "24 DEAD", font=font(SANS_B, 17),
           fill=(255, 150, 80), anchor="ra")


def ill_merkury(x, y, w, h):
    panel(x, y, w, h, (18, 52, 84))
    # sea
    for wy in range(y + h - 26, y + h - 2, 8):
        d.line([x + 6, wy, x + w - 6, wy], fill=(120, 180, 220), width=2)
    # listing ship
    hull = [(x + 40, y + h - 40), (x + 150, y + h - 58), (x + 158, y + h - 44),
            (x + 150, y + h - 30), (x + 60, y + h - 22)]
    d.polygon(hull, fill=(200, 200, 200))
    d.rectangle([x + 88, y + h - 74, x + 116, y + h - 58], fill=(200, 200, 200))
    d.line([x + 102, y + h - 92, x + 102, y + h - 74], fill=(200, 200, 200),
           width=3)
    # drones
    for dx, dy in [(120, 12), (150, 20), (172, 10)]:
        d.ellipse([x + dx - 4, y + dy - 4, x + dx + 4, y + dy + 4],
                  fill=(255, 220, 80))
    d.text((x + 8, y + 6), "SUNK", font=font(SANS_B, 17),
           fill=(255, 220, 80))


def ill_belgium(x, y, w, h):
    panel(x, y, w, h, (226, 230, 232))
    # runway
    d.rectangle([x, y + h - 18, x + w, y + h - 8], fill=(90, 90, 90))
    # plane silhouette on the ground
    px, py = x + 20, y + h - 42
    d.ellipse([px, py, px + 110, py + 16], fill=(60, 90, 140))
    d.polygon([(px + 40, py + 4), (px + 66, py - 16), (px + 78, py - 16),
               (px + 66, py + 6)], fill=(60, 90, 140))
    d.polygon([(px + 86, py + 2), (px + 112, py - 8), (px + 112, py + 2)],
              fill=(60, 90, 140))
    # no-entry sign
    cx, cy, r = x + w - 34, y + 28, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=5)
    d.line([cx - r + 4, cy + r - 4, cx + r - 4, cy - r + 4], fill=RED, width=5)
    d.text((x + 10, y + 8), "SHUT", font=font(SANS_B, 16), fill=RED)


def ill_wwc(x, y, w, h):
    panel(x, y, w, h, (22, 120, 70))
    # pitch lines
    d.ellipse([x + w // 2 - 34, y + h // 2 - 22, x + w // 2 + 34,
               y + h // 2 + 22], outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 6, x + w // 2, y + h - 6], fill=(255, 255, 255),
           width=2)
    # ball
    bx, by, br = x + 34, y + h - 30, 17
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
              outline=INK, width=1)
    d.polygon([(bx, by - 7), (bx + 7, by - 2), (bx + 4, by + 6),
               (bx - 4, by + 6), (bx - 7, by - 2)], fill=INK)
    d.text((x + w - 10, y + 8), "2035", font=font(SANS_B, 26),
           fill=(255, 255, 255), anchor="ra")
    d.text((x + w - 10, y + 38), "UK HOSTS", font=font(SANS_B, 11),
           fill=(200, 240, 210), anchor="ra")


# ---------------------------------------------------------------- leads (3)
LEADS = [
    ("GLOBAL · CLIMATE", "COP31 COLLAPSES: NO DEAL",
     "After a record ~49 hours of overtime, the Antalya summit ends with no "
     "agreement. The EU and ~130 countries reject a final text that never "
     "mentions fossil fuels.",
     "Reuters", ill_cop31),
    ("EUROPE · UKRAINE", "DYMER TOLL RISES TO 11",
     "Rescuers pull a boy, 7, alive from a flattened block hit by a Russian "
     "drone; a woman, 79, is found alive at 03:28. Fifteen dead across the "
     "Kyiv region; Monday is a day of mourning.",
     "BBC / Reuters", ill_dymer),
    ("ASIA · MARKETS", "AI ROUT HITS ASIA",
     "Seoul's Kospi falls 3.3% as the AI sell-off spreads; Taiwan bans short "
     "sales below the prior close and Seoul readies a stabilisation fund. "
     "US futures rebound 2%.",
     "Bloomberg / Reuters", ill_markets),
]
ly = 170
for i, (kick, head, deck, src, ill) in enumerate(LEADS):
    x = 16 + i * 336
    ill(x, ly, 322, 128)
    d.text((x, ly + 134), kick, font=font(SANS_B, 11), fill=RED)
    y = draw_lines(d, x, ly + 150, wrap(d, head, font(SERIF_B, 19), 322),
                   font(SERIF_B, 19), INK, 21)
    y = draw_lines(d, x, y + 3, wrap(d, deck, font(SANS, 12), 322),
                   font(SANS, 12), INK, 14)
    d.text((x, y + 2), "Source: " + src, font=font(SANS, 10), fill=GREY)
d.line([16, 414, 1008, 414], fill=INK, width=1)

# ---------------------------------------------------------------- tier 2 (5)
TIER2 = [
    ("AMERICAS", "DEMOCRATS CLINCH 258 HOUSE SEATS",
     "NC recount confirms Hubbard's win; biggest House majority since 1992.",
     "dpa / BBC", ill_democrats),
    ("ASIA", "24 DEAD IN CIKANDE FACTORY FIRE",
     "24 dead at a gutted candy factory in Banten; dozens still missing.",
     "Reuters", ill_cikande),
    ("AFRICA", "UKRAINE SINKS RUSSIAN CORVETTE",
     "Zelenskyy confirms sea drones sank the Merkury off Benghazi, Libya.",
     "CNN / Reuters", ill_merkury),
    ("EUROPE", "BELGIAN AIRPORTS SHUT MONDAY",
     "ATC stops 07:00-21:00 in a strike; 429 flights grounded.",
     "skeyes", ill_belgium),
    ("SPORT", "UK TO HOST 2035 WOMEN'S WORLD CUP",
     "FIFA confirms the bid: 48 teams, 104 matches, first UK finals since '66.",
     "FIFA / BBC", ill_wwc),
]
ty = 420
for i, (kick, head, deck, src, ill) in enumerate(TIER2):
    x = 17 + i * 200
    ill(x, ty, 190, 76)
    d.text((x, ty + 80), kick, font=font(SANS_B, 10), fill=RED)
    y = draw_lines(d, x, ty + 94, wrap(d, head, font(SERIF_B, 13), 190),
                   font(SERIF_B, 13), INK, 15)
    y = draw_lines(d, x, y + 2, wrap(d, deck, font(SANS, 10), 190),
                   font(SANS, 10), INK, 12)
    d.text((x, y + 1), "Source: " + src, font=font(SANS, 9), fill=GREY)
d.line([16, 590, 1008, 590], fill=INK, width=1)


# ---------------------------------------------------------------- map strip
MAP_X, MAP_Y, MAP_W, MAP_H = 16, 596, 620, 88


def ll2xy(lon, lat):
    return (MAP_X + (lon + 170) / 360 * MAP_W,
            MAP_Y + (75 - lat) / 130 * MAP_H)


d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
            outline=INK, width=1)
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
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy - 1), str(n), font=font(SANS_B, 10), fill=(255, 255, 255),
           anchor="mm")
d.text((MAP_X + 6, MAP_Y + 4), "WHERE IT HAPPENED", font=font(SANS_B, 10),
       fill=INK)

# region key (right of map)
kx, ky = 652, 596
d.text((kx, ky), "30 STORIES BY REGION", font=font(SANS_B, 12), fill=INK)
regions = [("EUROPE", 11), ("ASIA", 5), ("AMERICAS", 5), ("AFRICA", 4),
           ("MIDDLE EAST", 3), ("OCEANIA", 1), ("GLOBAL", 1)]
for i, (name, cnt) in enumerate(regions):
    ry = ky + 20 + i * 10
    d.text((kx, ry), name, font=font(SANS_B, 10), fill=INK)
    d.text((kx + 150, ry), str(cnt), font=font(SANS_B, 10), fill=RED)
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
d.line([16, 692, 1008, 692], fill=INK, width=1)
d.text((16, 697), "ALSO ON MONDAY 23 NOVEMBER — 22 MORE STORIES",
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
for i, item in enumerate(LIST):
    col = 0 if i < 11 else 1
    row = i % 11
    x = 16 if col == 0 else 522
    y = 720 + row * 20
    wpx = d.textlength(item, font=lf)
    if wpx > 486:
        print("WARN: list item too wide (%d px): %s" % (wpx, item))
    # bold the number
    num = item.split(".")[0] + "."
    d.text((x, y), num, font=font(SANS_B, 12), fill=RED)
    d.text((x + d.textlength(num + " ", font=font(SANS_B, 12)), y),
           item[len(num) + 1:], font=lf, fill=INK)

# ---------------------------------------------------------------- DATE CHECK footer
d.rectangle([16, 942, 1008, 1016], fill=(255, 240, 238), outline=RED, width=1)
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
