#!/usr/bin/env python3
"""Compose the 24 November 2026 news front page (1024x1024) from hero.png.

Fresh build for competition news-image-20261124. All headlines were checked
against reports dated 24 November 2026. Output: entry.png (<= 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (247, 243, 234)
INK = (18, 18, 18)
ACCENT = (158, 32, 24)          # deep newspaper red
RULE = (120, 110, 96)
BAND = (24, 32, 48)             # dark navy for the IN BRIEF band

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill=INK, leading=1.25):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, y, weight=2, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    name_f = font(SERIF_B, 66)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=name_f)
    d.text(((W - nw) / 2, 26), name, font=name_f, fill=INK)

    rule(d, 108, weight=4)
    rule(d, 114, weight=1)

    meta_f = font(SANS_B, 18)
    d.text((MARGIN, 124), "TUESDAY 24 NOVEMBER 2026", font=meta_f, fill=ACCENT)
    right = "ONE IMAGE  |  WORLD NEWS"
    d.text((W - MARGIN - d.textlength(right, font=meta_f), 124),
           right, font=meta_f, fill=INK)

    # ---- Lead story: Nvidia ---------------------------------------------
    y = 158
    lead_f = font(SERIF_B, 46)
    lead = "HUANG BACK AS NVIDIA CHIEF"
    d.text((MARGIN, y), lead, font=lead_f, fill=INK)
    y += 58
    deck_f = font(SANS, 21)
    deck = ("Jensen Huang reinstated as CEO, 11 days after stepping down "
            "amid a 'spy' controversy, after Trump intervened.")
    y = draw_lines(d, wrap(d, deck, deck_f, W - 2 * MARGIN),
                   deck_f, MARGIN, y, leading=1.3)
    y += 6
    rule(d, y, weight=2)
    y += 12

    # ---- Hero photo: sea drones off Libya -------------------------------
    hero = Image.open("hero.png").convert("RGB")
    img_w, img_h = W - 2 * MARGIN, 280
    # Centre-crop the 1920x1280 hero to the 952x300 slot.
    scale = max(img_w / hero.width, img_h / hero.height)
    resized = hero.resize((round(hero.width * scale),
                           round(hero.height * scale)), Image.LANCZOS)
    left = (resized.width - img_w) // 2
    top = (resized.height - img_h) // 2
    page.paste(resized.crop((left, top, left + img_w, top + img_h)),
               (MARGIN, y))
    d.rectangle([MARGIN, y, W - MARGIN, y + img_h], outline=INK, width=1)
    y += img_h + 10

    photo_f = font(SERIF_B, 33)
    photo_head = "SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA"
    y = draw_lines(d, wrap(d, photo_head, photo_f, W - 2 * MARGIN),
                   photo_f, MARGIN, y, leading=1.15)
    y += 4
    cap_f = font(SANS, 19)
    cap = ("Ukraine says its sea drones sank the warship in a Benghazi "
           "operation that also destroyed a Ka-27 helicopter and hit "
           "cargo ship MV Angara.")
    y = draw_lines(d, wrap(d, cap, cap_f, W - 2 * MARGIN),
                   cap_f, MARGIN, y, leading=1.3)
    y += 10
    rule(d, y, weight=2)
    y += 12

    # ---- Two secondary stories ------------------------------------------
    col_w = (W - 2 * MARGIN - 24) // 2
    head_f = font(SERIF_B, 23)
    body_f = font(SANS, 17)

    secondaries = [
        ("NATO VOWS SPACE DEFENCE",
         "The alliance pledges to defend space after reports Russia may "
         "launch a nuclear space weapon next month, with a "
         "satellite-destroying launch planned within weeks."),
        ("AT LEAST 14 KILLED IN KYIV REGION",
         "Russian strikes kill at least 14 in the Kyiv region, "
         "Ukraine says."),
    ]
    col_y = y
    for i, (head, body) in enumerate(secondaries):
        x = MARGIN + i * (col_w + 24)
        yy = col_y
        yy = draw_lines(d, wrap(d, head, head_f, col_w), head_f, x, yy,
                        leading=1.15)
        yy += 2
        draw_lines(d, wrap(d, body, body_f, col_w), body_f, x, yy,
                   leading=1.3)
        if i == 0:
            d.line([(x + col_w + 12, col_y), (x + col_w + 12, col_y + 116)],
                   fill=RULE, width=1)
    y = col_y + 122
    rule(d, y, weight=2)
    y += 10

    # ---- IN BRIEF band ---------------------------------------------------
    band_top = y
    band_h = (H - 40) - band_top
    d.rectangle([MARGIN, band_top, W - MARGIN, band_top + band_h], fill=BAND)
    brief_f = font(SANS_B, 17)
    d.text((MARGIN + 14, band_top + 10), "IN BRIEF", font=brief_f,
           fill=(232, 196, 120))
    item_f = font(SANS, 14)
    briefs_left = [
        "More bodies recovered from Indonesia candy factory fire.",
        "Trump offers Philippines $2.4bn for self-defence.",
        "Mexico captures FBI most-wanted drug kingpin; US drone helped.",
        "GTA VI hacker Arion Kurtaj gets 7 years; free on time served.",
    ]
    briefs_right = [
        "US states sue Musk firms over sexualised Grok images.",
        "Storms and airline glitches threaten messy Thanksgiving travel.",
        "COP31 climate talks collapse with no deal in Antalya.",
        "Democrats clinch biggest House majority since 1992: 258 seats.",
    ]
    bx = MARGIN + 14
    by = band_top + 36
    for col in (briefs_left, briefs_right):
        yy = by
        for item in col:
            lines = wrap(d, "\u2022  " + item, item_f, col_w - 14)
            yy = draw_lines(d, lines, item_f, bx, yy, fill=(235, 235, 235),
                            leading=1.2)
            yy += 2
        bx += col_w + 24

    # ---- Footer ----------------------------------------------------------
    foot_f = font(SANS, 13)
    foot = ("All headlines checked against reports dated 24 November 2026  |  "
            "The World Today")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, H - 26), foot, font=foot_f, fill=RULE)

    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)


if __name__ == "__main__":
    main()
