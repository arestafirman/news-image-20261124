#!/usr/bin/env python3
"""Render the news poster for Tuesday 24 November 2026.

Draws a 1024x1024 broadsheet poster from the story data written in this
file (36 stories verified for 24 Nov 2026: 3 heroes, 10 tiles, 23 briefs).
All artwork is procedural geometry drawn with PIL - no external assets,
no photos, no network. Deterministic: same input, same bytes out.
Run: python3 generate_image.py  ->  entry.png (1024x1024, <=1 MiB)
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


# ---- palette ---------------------------------------------------------------
PAPER = (247, 243, 232)
INK = (18, 18, 18)
MUTED = (90, 86, 76)
RULE = (30, 30, 30)
RED = (178, 34, 28)
BLUE = (24, 68, 128)
GOLD = (176, 132, 24)
TEAL = (14, 110, 110)
GREEN = (46, 110, 52)
PURPLE = (96, 60, 140)
ORANGE = (196, 96, 16)
SKY = (222, 232, 238)
MAP_BG = (214, 228, 236)
LAND = (232, 226, 205)
CARD = (255, 255, 255)

REGION_COLORS = {
    "Middle East": (178, 34, 28),
    "Europe": (24, 68, 128),
    "Americas": (14, 110, 110),
    "East Asia": (196, 96, 16),
    "South Asia": (96, 60, 140),
    "Africa": (46, 110, 52),
    "Oceania": (176, 132, 24),
    "Global": (90, 86, 76),
}

# ---- data: the 36 verified stories of Tuesday 24 November 2026 -----------
HEROES = [
    {
        "n": 1, "region": "Middle East",
        "headline": "HOUTHI DRONE HITS RIYADH'S PIF TOWER",
        "body": "11 wounded in the strike on the tallest tower in Riyadh - the second hit on the tower in under a week.",
        "source": "Reuters, 16:48 UTC  -  CONFIRMED",
        "scene": "riyadh",
    },
    {
        "n": 2, "region": "Europe",
        "headline": "RUSSIA'S 96-DRONE BARRAGE",
        "body": "Ukraine says 73 of 96 drones were downed overnight; 2 killed, 44 hurt in Zaporizhzhia, 13 sites hit.",
        "source": "Ukraine Air Force via Reuters/AP  -  CONFIRMED",
        "scene": "barrage",
    },
    {
        "n": 3, "region": "Americas",
        "headline": "HUAWEI CONVICTED ON 10 OF 12 COUNTS",
        "body": "Brooklyn jury finds bank fraud, wire fraud and sanctions violations; sentencing set for 14 Sep 2027.",
        "source": "Reuters, 20:16 UTC  -  CONFIRMED",
        "scene": "court",
    },
]

TILES = [
    (4, "Europe", "Sparta II hit confirmed",
     "Zelenskiy confirms Ukraine hit the Russian ship; the attack was 21 Nov.",
     "Reuters", "ship"),
    (5, "Americas", "Giuliani gets top US medal",
     "Trump awards the Medal of Freedom in a private Oval Office ceremony.",
     "Reuters", "medal"),
    (6, "Americas", "CIA, ODNI systems breached",
     "Unclassified OSINT systems hit; no classified data; now resolved.",
     "NYT / Reuters", "lock"),
    (7, "Europe", "Sarkozys to stand trial",
     "Witness-tampering case over 2007 campaign funds; trial Nov 2027.",
     "Reuters / AFP", "gavel"),
    (8, "Africa", "AFCON title back to Senegal",
     "CAS overturns the CAF ruling; the 1-0 final vs Morocco stands.",
     "Reuters / AP", "trophy"),
    (9, "Middle East", "Hamas security chief killed",
     "Israeli strikes kill Naeem Abu Nahel and six others in Gaza.",
     "Reuters", "map_pin"),
    (10, "Global", "COP31 backlash grows",
     "Calls to reshape climate talks after the collapse of 22 Nov.",
     "Politico", "globe"),
    (11, "East Asia", "Russian jets enter KADIZ",
     "Fighters scrambled as Russian aircraft fly inside the zone.",
     "AP", "jet"),
    (12, "East Asia", "China probes Chen Jining",
     "Shanghai party chief investigated for discipline violations.",
     "NewsSumm", "lens"),
    (13, "Oceania", "Australia's tech duty of care",
     "Bill would fine tech giants up to 5% of global revenue.",
     "AP", "shield"),
]

BRIEFS = [
    (14, "Germany first to access Ukraine's Delta battlefield system"),
    (15, "Latvian president: Ukraine war may hit 'tipping point' next year"),
    (16, "Heavy fighting in Ituri traps Ebola responders"),
    (17, "Iraq PM orders oil ministry to manage Kurdish oilfields"),
    (18, "UNAIDS: HIV cuts threaten progress; 1,600 lives/day"),
    (19, "Sheikh Hasina plans return to Bangladesh on Dec 16"),
    (20, "Japan PM: full 2027 ICC contribution paid by year-end"),
    (21, "US envoy 'not certain' Israel military aid ends this year"),
    (22, "Yemeni govt: Houthis won't seize Aden; ~60 km away"),
    (23, "UN mission urges probe into Benghazi port attacks"),
    (24, "Radar issue delays flights at Chicago O'Hare"),
    (25, "Dell lifts forecasts; Nvidia shares fall 7%"),
    (26, "Venezuela reports total public debt $237.5bn"),
    (27, "Hostages held in Cartagena supermarket after hijack bid"),
    (28, "Germans oppose military aid to Kyiv, 53% vs 46%"),
    (29, "Trump spares turkeys Freedom and Feathers"),
    (30, "Fort Hood shooter Hasan seeks stay of execution"),
    (31, "Iran: no talks with US until 7 conditions met"),
    (32, "Car bomb in Villavicencio hurts 23+ at governor's offices"),
    (33, "Rep. Jimmy Gomez to resign Dec 1 after ethics report"),
    (34, "M5.6 earthquake strikes Nepal near China border"),
    (35, "Russia's Duma approves 2027-29 budget; military soars"),
    (36, "China unveils Shenzhou-24 crew; Pakistani astronaut to fly"),
]

REGIONS = [
    ("Middle East", 6), ("Europe", 7), ("Americas", 11), ("East Asia", 4),
    ("South Asia", 2), ("Africa", 3), ("Oceania", 1), ("Global", 2),
]

BIG_NUMBERS = [
    ("36", "STORIES"), ("96", "DRONES"), ("11", "WOUNDED"),
    ("10 OF 12", "COUNTS"), ("44", "INJURED"), ("8", "REGIONS"),
]

TIMELINE = [
    ("06:00", "73 of 96 drones downed overnight"),
    ("11:00", "Iran: no talks until 7 conditions met"),
    ("16:00", "Australia duty of care bill moves"),
    ("16:48", "Houthi drone hits Riyadh PIF Tower"),
    ("18:35", "Sarkozy & Bruni ordered to stand trial"),
    ("18:49", "Giuliani awarded Medal of Freedom"),
    ("20:16", "Huawei convicted on 10 of 12 counts"),
]

STALE = [
    ("Trump dares Iran: \u201cbottom of the sea\u201d", "22 Nov"),
    ("IRGC: \u201cthree more tankers hit mines\u201d", "23 Nov"),
    ("Iran FM: \u201cuse all tools vs blockade\u201d", "23 Nov"),
    ("Russia warns Estonia of \u201copen war\u201d", "23 Nov"),
    ("NATO chief Rutte: defend in space", "23 Nov"),
    ("COP31 ends with no deal", "22 Nov"),
    ("Iran attacks US bases in Bahrain", "21 Nov"),
    ("Sparta II attacked", "21 Nov"),
    ("Kryvyi Rih", "20 Nov"),
    ("Peru quake M6.7", "20 Nov"),
    ("BepiColombo", "21 Nov"),
    ("\u2018El Chapo Isidro\u2019", "21 Nov"),
    ("Shenzhen summit", "19 Nov"),
    ("Russia 400-drone barrage", "19\u201320 Nov"),
    ("Wall Street AI sell-off", "20 Nov"),
    ("Las Vegas GP / ATP / Liverpool\u2013Man Utd / HK Election", "22 Nov"),
    ("14 countries back ICJ Rohingya ruling", "23 Nov"),
    ("Guterres calls for AI risk framework", "23 Nov"),
    ("7 countries letter limiting Russian travel in EU", "23 Nov"),
]

NOT_YET = [
    "No breakout of the 14 Kharg tankers confirmed; no convoy sailed.",
    "No COP31 follow-up deal announced.",
    "No new US strike on Iran reported on 24 Nov.",
]

# lon/lat of every story for the map (pins 1-13 numbered, 14-36 dots)
COORDS = {
    1: (46.7, 24.7), 2: (35.2, 47.8), 3: (-74.0, 40.7), 4: (33.0, 43.5),
    5: (-77.0, 38.9), 6: (-77.0, 38.9), 7: (2.3, 48.8), 8: (-17.4, 14.7),
    9: (34.5, 31.5), 10: (6.1, 46.2), 11: (127.0, 37.5), 12: (121.5, 31.2),
    13: (149.1, -35.3), 14: (30.5, 50.4), 15: (24.1, 56.9), 16: (29.5, 1.0),
    17: (44.4, 33.3), 18: (0.0, 10.0), 19: (90.4, 23.8), 20: (139.7, 35.7),
    21: (34.8, 32.1), 22: (45.0, 12.8), 23: (20.1, 32.1), 24: (-87.6, 41.9),
    25: (-97.7, 30.4), 26: (-66.9, 10.5), 27: (-75.5, 10.4), 28: (13.4, 52.5),
    29: (-77.0, 38.9), 30: (-97.8, 31.1), 31: (51.4, 35.7), 32: (-73.6, 4.1),
    33: (-118.2, 34.0), 34: (85.3, 28.0), 35: (37.6, 55.8), 36: (116.4, 39.9),
}

REGION_OF = {}
for _n, _r, *_ in [(h["n"], h["region"]) for h in HEROES]:
    REGION_OF[_n] = _r
for _n, _r, *_ in TILES:
    REGION_OF[_n] = _r
REGION_OF.update({14: "Europe", 15: "Europe", 16: "Africa", 17: "Middle East",
                  18: "Global", 19: "South Asia", 20: "East Asia",
                  21: "Middle East", 22: "Middle East", 23: "Africa",
                  24: "Americas", 25: "Americas", 26: "Americas",
                  27: "Americas", 28: "Europe", 29: "Americas",
                  30: "Americas", 31: "Middle East", 32: "Americas",
                  33: "Americas", 34: "South Asia", 35: "Europe",
                  36: "East Asia"})


# ---- text helpers ----------------------------------------------------------
def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def badge(draw, x, y, n, color, r=10):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color,
                 outline=(255, 255, 255), width=2)
    t = str(n)
    ft = f(FONTB, 11 if len(t) < 2 else 10)
    tw = draw.textlength(t, font=ft)
    draw.text((x - tw / 2, y - 6), t, font=ft, fill=(255, 255, 255))


# ---- hero scenes (procedural, full-bleed) ---------------------------------
def scene_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    for sx in range(x + 8, x + w - 8, 26):
        d.ellipse([sx, y + 8 + (sx % 30), sx + 2, y + 10 + (sx % 30)],
                  fill=(220, 220, 200))
    d.ellipse([x + w - 46, y + 12, x + w - 16, y + 42], fill=(238, 230, 200))
    # skyline
    for bx, bw, bh in [(0, 46, 52), (52, 34, 78), (92, 40, 60), (238, 44, 66),
                       (288, 36, 48)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 38, 70))
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(250, 210, 90))
    # PIF tower: tall, tapering, lit
    tx = x + w // 2 - 22
    d.polygon([(tx, y + h), (tx + 6, y + 26), (tx + 38, y + 26),
               (tx + 44, y + h)], fill=(58, 74, 120))
    d.polygon([(tx + 6, y + 26), (tx + 22, y + 6), (tx + 38, y + 26)],
              fill=(80, 100, 150))
    for wy in range(y + 40, y + h - 8, 12):
        d.rectangle([tx + 14, wy, tx + 30, wy + 5], fill=(250, 210, 90))
    # drone + blast at the tower top
    d.ellipse([x + w - 96, y + 30, x + w - 72, y + 54], fill=(255, 140, 40))
    d.ellipse([x + w - 90, y + 36, x + w - 78, y + 48], fill=(255, 220, 120))
    d.line([(x + w - 110, y + 60), (x + w - 84, y + 42)], fill=(255, 180, 80),
           width=3)
    d.ellipse([x + 30, y + 34, x + 52, y + 48], fill=(200, 200, 200))
    d.line([(x + 28, y + 41), (x + 54, y + 41)], fill=(200, 200, 200), width=2)


def scene_barrage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 20, 34))
    for sx in range(x + 10, x + w - 10, 22):
        d.ellipse([sx, y + 6 + (sx * 7 % 40), sx + 2, y + 8 + (sx * 7 % 40)],
                  fill=(220, 220, 200))
    # city blocks under attack
    for bx, bw, bh in [(0, 60, 46), (66, 44, 70), (116, 52, 56), (174, 40, 82),
                       (220, 48, 58), (274, 50, 66)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(44, 36, 52))
        for wy in range(y + h - bh + 8, y + h - 6, 14):
            for wx in range(x + bx + 6, x + bx + bw - 6, 12):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(250, 200, 90))
    # drone swarm: dots with trails
    import math
    for i in range(14):
        dx = x + 18 + (i * 23) % (w - 40)
        dy = y + 18 + (i * 17) % 70
        d.line([(dx - 14, dy + 8), (dx, dy)], fill=(180, 180, 180), width=1)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(230, 230, 230))
    # two blasts
    for cx, cy, r in [(x + 90, y + h - 58, 22), (x + 250, y + h - 74, 18)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 30))
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  fill=(255, 210, 110))
    d.text((x + 10, y + 8), "96 DRONES", font=f(FONTB, 13), fill=(255, 220, 120))


def scene_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
    # courthouse columns
    for cx in range(x + 14, x + w - 14, 52):
        d.rectangle([cx, y + 34, cx + 22, y + h - 26], fill=(210, 205, 190))
        d.rectangle([cx - 4, y + 26, cx + 26, y + 36], fill=(232, 228, 214))
        d.rectangle([cx - 4, y + h - 34, cx + 26, y + h - 26],
                    fill=(232, 228, 214))
    d.rectangle([x, y + 8, x + w, y + 26], fill=(232, 228, 214))
    # scales of justice
    cx, cy = x + w // 2, y + 62
    d.line([(cx, cy - 18), (cx, cy + 34)], fill=(250, 210, 90), width=4)
    d.line([(cx - 34, cy - 14), (cx + 34, cy - 14)], fill=(250, 210, 90),
           width=3)
    for s in (-1, 1):
        d.line([(cx + s * 34, cy - 14), (cx + s * 22, cy + 8)],
               fill=(250, 210, 90), width=2)
        d.polygon([(cx + s * 34 - 12, cy + 8), (cx + s * 34 + 12, cy + 8),
                   (cx + s * 34, cy + 20)], fill=(250, 210, 90))
    # verdict stamp, text centred in its box
    stamp = "10 OF 12"
    stw = d.textlength(stamp, font=f(FONTB, 15))
    d.rectangle([x + w - 96, y + h - 46, x + w - 8, y + h - 16],
                outline=(255, 220, 120), width=3)
    d.text((x + w - 52 - stw / 2, y + h - 40), stamp, font=f(FONTB, 15),
           fill=(255, 220, 120))


SCENES = {"riyadh": scene_riyadh, "barrage": scene_barrage,
          "court": scene_court}


# ---- tile icons (small procedural drawings) --------------------------------
def icon(d, x, y, w, h, kind, color):
    cx, cy = x + w // 2, y + h // 2
    if kind == "ship":
        d.polygon([(x + 6, cy + 8), (x + w - 6, cy + 8), (x + w - 16, cy + 18),
                   (x + 16, cy + 18)], fill=color)
        d.rectangle([cx - 4, cy - 14, cx + 4, cy + 8], fill=color)
        d.polygon([(cx + 4, cy - 14), (cx + 22, cy - 6), (cx + 4, cy - 2)],
                  fill=RED)
        d.line([(x, cy + 24), (x + w, cy + 24)], fill=BLUE, width=2)
    elif kind == "medal":
        d.ellipse([cx - 13, cy - 12, cx + 13, cy + 14], outline=color, width=4)
        d.text((cx - 4, cy - 8), "1", font=f(FONTB, 14), fill=color)
        d.polygon([(cx - 8, cy + 12), (cx - 2, cy + 26), (cx + 2, cy + 12)],
                  fill=RED)
        d.polygon([(cx + 2, cy + 12), (cx + 8, cy + 26), (cx + 12, cy + 12)],
                  fill=BLUE)
    elif kind == "lock":
        d.rectangle([cx - 14, cy - 4, cx + 14, cy + 18], fill=color)
        d.arc([cx - 10, cy - 18, cx + 10, cy + 2], 180, 360, fill=color,
              width=4)
        d.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=(255, 255, 255))
    elif kind == "gavel":
        d.rectangle([cx - 16, cy - 10, cx + 14, cy + 2], fill=color)
        d.line([(cx - 2, cy + 2), (cx + 12, cy + 20)], fill=color, width=5)
        d.rectangle([cx - 14, cy + 22, cx + 18, cy + 26], fill=GOLD)
    elif kind == "trophy":
        d.polygon([(cx - 10, cy - 14), (cx + 10, cy - 14), (cx + 6, cy + 8),
                   (cx - 6, cy + 8)], fill=GOLD)
        d.arc([cx - 20, cy - 14, cx - 6, cy + 2], 90, 270, fill=GOLD, width=3)
        d.arc([cx + 6, cy - 14, cx + 20, cy + 2], 270, 90, fill=GOLD,
              width=3)
        d.rectangle([cx - 8, cy + 8, cx + 8, cy + 12], fill=GOLD)
        d.rectangle([cx - 12, cy + 12, cx + 12, cy + 16], fill=GOLD)
    elif kind == "map_pin":
        d.ellipse([cx - 12, cy - 16, cx + 12, cy + 8], fill=color)
        d.polygon([(cx - 8, cy + 4), (cx + 8, cy + 4), (cx, cy + 18)],
                  fill=color)
        d.ellipse([cx - 5, cy - 9, cx + 5, cy + 1], fill=(255, 255, 255))
    elif kind == "globe":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=color,
                  width=3)
        d.ellipse([cx - 5, cy - 14, cx + 5, cy + 14], outline=color, width=2)
        d.line([(cx - 14, cy), (cx + 14, cy)], fill=color, width=2)
    elif kind == "jet":
        d.polygon([(cx - 18, cy), (cx + 16, cy - 6), (cx + 20, cy),
                   (cx + 16, cy + 6)], fill=color)
        d.polygon([(cx - 2, cy - 4), (cx + 6, cy - 16), (cx + 10, cy - 4)],
                  fill=color)
        d.polygon([(cx - 2, cy + 4), (cx + 6, cy + 16), (cx + 10, cy + 4)],
                  fill=color)
    elif kind == "lens":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=color,
                  width=4)
        d.line([(cx + 9, cy + 9), (cx + 18, cy + 18)], fill=color, width=4)
    elif kind == "shield":
        d.polygon([(cx - 13, cy - 14), (cx + 13, cy - 14), (cx + 13, cy + 2),
                   (cx, cy + 18), (cx - 13, cy + 2)], fill=color)
        d.text((cx - 4, cy - 8), "\u2713", font=f(FONTB, 13),
               fill=(255, 255, 255))


# ---- world map --------------------------------------------------------------
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG)
    d.text((x + 10, y + 6), "WHERE IT HAPPENED", font=f(FONTB, 13),
           fill=INK)
    d.text((x + 10, y + 24), "Pins 1-13 numbered  -  dots are stories 14-36",
           font=f(FONT, 10), fill=MUTED)

    def px(lon, lat):
        # wide strip map: latitude range -55..75 stretched over the band
        return (x + 14 + (lon + 180) / 360.0 * (w - 28),
                y + 40 + (75 - lat) / 130.0 * (h - 48))

    # stylised continents (rough polygons, lon/lat)
    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 72), (-60, 60),
         (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-115, 30),
         (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
        [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-55, -35),
         (-70, -40), (-73, -50), (-70, -18), (-77, -5), (-80, 10)],
        [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (18, 56),
         (21, 55), (28, 59), (30, 60), (30, 70), (18, 70), (12, 65),
         (5, 60), (-5, 58), (-10, 50), (-10, 36)],
        [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
         (51, 11), (44, -2), (40, -10), (35, -18), (32, -29), (20, -35),
         (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-17, 15),
         (-17, 21), (-10, 31), (-6, 35)],
        [(30, 70), (40, 68), (55, 69), (70, 72), (100, 77), (130, 72),
         (160, 70), (178, 66), (162, 60), (158, 52), (140, 40), (130, 33),
         (122, 30), (110, 20), (105, 8), (100, 8), (95, 16), (90, 22),
         (80, 8), (77, 8), (72, 20), (66, 25), (60, 25), (52, 28),
         (48, 30), (44, 39), (40, 42), (30, 36), (30, 70)],
        [(113, -22), (122, -14), (130, -12), (137, -12), (142, -11),
         (146, -19), (150, -22), (153, -27), (150, -37), (140, -38),
         (132, -32), (124, -33), (115, -35), (113, -22)],
    ]
    for poly in continents:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(180, 175, 155))
    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = px(lon, 0)
        d.line([(gx, y + 40), (gx, y + h - 8)], fill=(200, 214, 222), width=1)
    # pins 1-13 (numbered), dots 14-36
    # nudges keep crowded European / Middle East / Washington pins readable
    NUDGE = {1: (-10, 10), 2: (0, -15), 4: (12, 12), 5: (0, 0),
             6: (14, -10), 7: (-16, -8), 10: (14, -12), 14: (10, 12),
             15: (-10, -10), 29: (-14, 12), 31: (16, 8), 35: (2, 14)}
    for n in range(1, 37):
        lon, lat = COORDS[n]
        px_, py_ = px(lon, lat)
        dx, dy = NUDGE.get(n, (0, 0))
        px_ += dx
        py_ += dy
        color = REGION_COLORS[REGION_OF[n]]
        if n <= 13:
            d.ellipse([px_ - 9, py_ - 9, px_ + 9, py_ + 9], fill=color,
                      outline=(255, 255, 255), width=2)
            t = str(n)
            ft = f(FONTB, 10 if len(t) < 2 else 9)
            tw = d.textlength(t, font=ft)
            d.text((px_ - tw / 2, py_ - 6), t, font=ft, fill=(255, 255, 255))
        else:
            d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], fill=color,
                      outline=(255, 255, 255), width=1)


# ---- build ------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14  # margin

    # masthead
    d.rectangle([0, 0, W, 62], fill=INK)
    d.text((M, 6), "THE WORLD IN ONE DAY", font=f(SERIFB, 34),
           fill=(247, 243, 232))
    d.text((W - M - d.textlength("TUESDAY 24 NOVEMBER 2026", font=f(FONTB, 16)),
            22), "TUESDAY 24 NOVEMBER 2026", font=f(FONTB, 16),
           fill=(250, 210, 90))
    d.text((M, 44), "36 STORIES  \u00b7  8 REGIONS  \u00b7  EVERY ONE DATED "
           "TUESDAY 24 NOVEMBER 2026", font=f(FONTB, 11), fill=(200, 195, 180))
    # subtitle: the three hero headlines
    sub = ("RIYADH TOWER HIT  \u00b7  96 DRONES OVER UKRAINE  \u00b7  "
           "HUAWEI GUILTY ON 10 OF 12 COUNTS")
    d.text((M, 66), sub, font=f(FONTB, 12), fill=RED)

    # big numbers strip
    y0 = 84
    bw = (W - 2 * M - 5 * 6) // 6
    for i, (val, lab) in enumerate(BIG_NUMBERS):
        bx = M + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y0 + 30], fill=CARD,
                    outline=(200, 195, 180))
        d.text((bx + bw // 2 - d.textlength(val, font=f(FONTB, 17)) / 2,
                y0 + 2), val, font=f(FONTB, 17), fill=INK)
        d.text((bx + bw // 2 - d.textlength(lab, font=f(FONTB, 9)) / 2,
                y0 + 20), lab, font=f(FONTB, 9), fill=MUTED)

    # region strip
    y0 = 120
    d.text((M, y0), "BY REGION:", font=f(FONTB, 11), fill=INK)
    rx = M + 78
    for name, count in REGIONS:
        col = REGION_COLORS[name]
        d.ellipse([rx, y0 + 1, rx + 9, y0 + 10], fill=col)
        label = f"{name} {count}"
        d.text((rx + 13, y0), label, font=f(FONTB, 11), fill=INK)
        rx += 13 + d.textlength(label, font=f(FONTB, 11)) + 12

    # heroes: 3 full-bleed illustrated panels
    y0 = 140
    hw = (W - 2 * M - 2 * 8) // 3
    hh = 196
    for i, hero in enumerate(HEROES):
        hx = M + i * (hw + 8)
        d.rectangle([hx, y0, hx + hw, y0 + hh], fill=CARD, outline=RULE)
        SCENES[hero["scene"]](d, hx + 1, y0 + 1, hw - 2, 108)
        col = REGION_COLORS[hero["region"]]
        badge(d, hx + 16, y0 + 124, hero["n"], col, r=11)
        tx = hx + 32
        lines = wrap(d, hero["headline"], f(FONTB, 14), hw - 40)
        text_lines(d, tx, y0 + 114, lines[:2], f(FONTB, 14), INK, 16)
        by = y0 + 114 + 16 * len(lines[:2]) + 2
        blines = wrap(d, hero["body"], f(FONT, 11), hw - 16)
        text_lines(d, hx + 8, by, blines[:2], f(FONT, 11), (50, 48, 44), 13)
        d.text((hx + 8, y0 + hh - 14), hero["source"], font=f(FONTB, 9),
               fill=MUTED)

    # tiles: 10 illustrated panels, 5 x 2
    y0 = 344
    tw_ = (W - 2 * M - 4 * 8) // 5
    th = 104
    for i, (n, region, head, body, src, kind) in enumerate(TILES):
        row, col_i = divmod(i, 5)
        tx0 = M + col_i * (tw_ + 8)
        ty0 = y0 + row * (th + 8)
        d.rectangle([tx0, ty0, tx0 + tw_, ty0 + th], fill=CARD,
                    outline=(200, 195, 180))
        col = REGION_COLORS[region]
        d.rectangle([tx0, ty0, tx0 + tw_, ty0 + 44], fill=SKY)
        icon(d, tx0 + 6, ty0 + 2, 40, 40, kind, col)
        badge(d, tx0 + tw_ - 16, ty0 + 16, n, col, r=10)
        d.text((tx0 + 50, ty0 + 6), region.upper(), font=f(FONTB, 8),
               fill=col)
        hlines = wrap(d, head, f(FONTB, 10), tw_ - 12)
        text_lines(d, tx0 + 6, ty0 + 48, hlines[:2], f(FONTB, 10), INK, 12)
        by = ty0 + 48 + 12 * len(hlines[:2])
        blines = wrap(d, body, f(FONT, 9), tw_ - 12)
        # only as many body lines as fit above the source line - no overlap
        fit = max(1, (ty0 + th - 14 - by) // 11)
        text_lines(d, tx0 + 6, by, blines[:fit], f(FONT, 9), (60, 58, 52), 11)
        d.text((tx0 + 6, ty0 + th - 12), src, font=f(FONTB, 8), fill=MUTED)

    # map
    draw_map(d, M, 568, W - 2 * M, 150)

    # timeline strip (UTC, exact hours)
    y0 = 722
    d.rectangle([M, y0, W - M, y0 + 26], fill=INK)
    tx = M + 8
    d.text((tx, y0 + 6), "UTC", font=f(FONTB, 11), fill=(250, 210, 90))
    tx += 34
    seg_w = (W - 2 * M - 42 - 8) // 7
    for tm, label in TIMELINE:
        seg = f"{tm}  {label}"
        lines = wrap(d, seg, f(FONT, 9), seg_w - 6)
        text_lines(d, tx, y0 + 3, lines[:2], f(FONT, 9), (247, 243, 232), 11)
        tx += seg_w

    # ALSO ON TUESDAY: briefs 14-36, 3 columns x 8 rows
    y0 = 754
    d.text((M, y0), "ALSO ON TUESDAY 24 NOVEMBER \u2014 23 MORE STORIES",
           font=f(FONTB, 13), fill=INK)
    d.line([(M, y0 + 18), (W - M, y0 + 18)], fill=RULE, width=2)
    col_w = (W - 2 * M - 2 * 10) // 3
    for i, (n, txt) in enumerate(BRIEFS):
        col_i, row = divmod(i, 8)
        bx = M + col_i * (col_w + 10)
        by = y0 + 24 + row * 15
        col = REGION_COLORS[REGION_OF[n]]
        d.ellipse([bx, by, bx + 12, by + 12], fill=col)
        t = str(n)
        ft = f(FONTB, 8)
        d.text((bx + 6 - d.textlength(t, font=ft) / 2, by + 2), t, font=ft,
               fill=(255, 255, 255))
        line = txt
        while (d.textlength(line, font=f(FONT, 10)) > col_w - 18
               and len(line) > 10):
            line = line[:-4].rstrip() + "\u2026"
            if line.endswith("\u2026\u2026"):
                line = line[:-1]
        d.text((bx + 16, by + 1), line, font=f(FONT, 10), fill=INK)

    # DATE CHECK box
    y0 = 880
    d.rectangle([M, y0, W - M, y0 + 100], fill=(255, 252, 240),
                outline=RED, width=2)
    d.text((M + 8, y0 + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT",
           font=f(FONTB, 12), fill=RED)
    d.text((M + 8, y0 + 22), "TOO OLD FOR 24 NOVEMBER:",
           font=f(FONTB, 9), fill=INK)
    # stale items in 3 columns
    scol_w = 218
    for i, (label, date) in enumerate(STALE):
        col_i, row = divmod(i, 7)
        sx = M + 8 + col_i * scol_w
        sy = y0 + 34 + row * 9
        item = f"\u2022 {label} \u2014 {date}"
        while (d.textlength(item, font=f(FONT, 8)) > scol_w - 6
               and len(item) > 12):
            item = item[:-5].rstrip() + "\u2026"
        d.text((sx, sy), item, font=f(FONT, 8), fill=(60, 58, 52))
    nx = M + 8 + 3 * scol_w + 8
    d.line([(nx - 6, y0 + 22), (nx - 6, y0 + 92)], fill=(200, 195, 180))
    d.text((nx, y0 + 22), "NOT YET (per 24 Nov 23:59 UTC):",
           font=f(FONTB, 9), fill=INK)
    ny = y0 + 36
    for item in NOT_YET:
        lines = wrap(d, "\u2022 " + item, f(FONT, 8), W - M - nx - 8)
        ny = text_lines(d, nx, ny, lines, f(FONT, 8), (60, 58, 52), 10)

    # footer
    d.text((M, 988), "Every story here happened, or was first reported, on "
           "Tuesday 24 November 2026.", font=f(FONTB, 12), fill=INK)
    d.text((M, 1006), "Sources named beside each story  \u00b7  "
           "Original drawings  \u00b7  36 stories, 8 regions",
           font=f(FONT, 10), fill=MUTED)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    build()
