#!/usr/bin/env python3
"""Build the X-post image for the post-x-promote-make-your-own-bounty-01 bounty.

Pure PIL poster build (sharp text, readable at 480x480). The bounty is scored
on replies + reposts + quotes, NOT likes or views — so the image is a question,
not a joke to scroll past: a make.fun "bounty board" that asks every reader
what bounty THEY would post if they had $250 in USDC to pay an AI agent.

The three seed ideas are deliberately silly and beatable, so readers reply
with a better one instead of just liking. The call to action is explicit:
REPLY WITH YOUR BOUNTY IDEA, best idea gets a repost.

House style follows the v6 verdict poster (cream paper, navy frame, gold
rule, magenta accents, the real make.fun ghost in a magenta seal disc).
"""
from PIL import Image, ImageDraw, ImageFont

WORK = "/home/hatch/workspace/makefun/post-x-promote-01"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-v2/ghost-extracted.png"
SIZE = 1600

NAVY = (22, 35, 63)
NAVY_SOFT = (60, 75, 110)
MAGENTA = (214, 0, 120)
GOLD = (176, 132, 46)
INK = (25, 25, 25)
GRAY = (120, 118, 112)
CREAM = (250, 244, 229)
PINK_FILL = (253, 238, 245)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/dejavu/"
LDIR = "/usr/share/fonts/truetype/liberation/"


def bold(n):
    return ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", n)


def regular(n):
    return ImageFont.truetype(FDIR + "DejaVuSans.ttf", n)


def italic(n):
    return ImageFont.truetype(LDIR + "LiberationSerif-Italic.ttf", n)


def mono(n):
    return ImageFont.truetype(FDIR + "DejaVuSansMono.ttf", n)


def center(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def dots(draw, x0, x1, y, fill=GRAY):
    x = x0
    while x < x1:
        draw.ellipse((x, y - 3, x + 6, y + 3), fill=fill)
        x += 18


img = Image.new("RGB", (SIZE, SIZE), CREAM)
d = ImageDraw.Draw(img)

# Outer navy frame + inner gold frame (the series' house style).
d.rectangle((12, 12, SIZE - 12, SIZE - 12), outline=NAVY, width=8)
d.rectangle((30, 30, SIZE - 30, SIZE - 30), outline=GOLD, width=3)

# Header: make.fun, left; ghost seal, right.
d.text((92, 66), "MAKE.FUN", font=bold(62), fill=NAVY)
d.text((92, 142), "BOUNTY BOARD  ·  NO. 001", font=bold(38), fill=NAVY_SOFT)
d.text((92, 196), "ANYONE CAN POST A BOUNTY", font=regular(30), fill=GRAY)

seal_cx, seal_cy, seal_r = 1352, 148, 96
d.ellipse(
    (seal_cx - seal_r, seal_cy - seal_r, seal_cx + seal_r, seal_cy + seal_r),
    fill=MAGENTA,
    outline=GOLD,
    width=5,
)
ghost = Image.open(GHOST).convert("RGBA")
ghost.thumbnail((168, 168), Image.LANCZOS)
img.paste(ghost, (seal_cx - ghost.width // 2, seal_cy - ghost.height // 2 + 6), ghost)
d = ImageDraw.Draw(img)

# Gold rule under the header.
d.line((92, 268, SIZE - 92, 268), fill=GOLD, width=4)

# Title block: the question.
center(d, SIZE // 2, 296, "YOUR TURN", bold(150), NAVY)
center(d, SIZE // 2, 468, "TO POST A BOUNTY", bold(72), MAGENTA)
center(d, SIZE // 2, 566, "You have $250 in USDC.", bold(48), NAVY)
center(
    d, SIZE // 2, 628,
    "What do you pay an AI agent to build?",
    regular(44), NAVY_SOFT,
)

# Seed ideas: three open bounties, dotted leaders like a filing.
d.text((110, 736), "OPEN IDEAS — STEAL ONE OR BEAT IT", font=bold(40), fill=NAVY)
d.line((110, 792, SIZE - 110, 792), fill=NAVY, width=4)

ideas = [
    ("01", "A bot that answers my group chat for me"),
    ("02", "An app that finds my lost socks"),
    ("03", "A game where my cat is the final boss"),
]
y = 822
for num, idea in ideas:
    d.text((110, y), num, font=bold(40), fill=MAGENTA)
    d.text((210, y + 2), idea, font=regular(38), fill=INK)
    y += 66

# Call-to-action box.
d.rounded_rectangle((110, 1050, SIZE - 110, 1240), radius=28,
                    fill=PINK_FILL, outline=MAGENTA, width=4)
center(d, SIZE // 2, 1078, "REPLY WITH YOUR BOUNTY IDEA", bold(56), MAGENTA)
center(d, SIZE // 2, 1150, "BEST IDEA GETS A REPOST", bold(40), NAVY)

# Scoring line.
center(d, SIZE // 2, 1280, "REPLIES + REPOSTS + QUOTES DECIDE THE TOP 50",
       regular(30), GRAY)
center(d, SIZE // 2, 1324, "LIKES DON'T COUNT. YOUR IDEA DOES.",
       bold(30), NAVY_SOFT)

# Closer strip, full bleed.
d.rectangle((0, 1420, SIZE, SIZE), fill=NAVY)
center(d, SIZE // 2, 1448, "MAKE YOUR OWN BOUNTY ON MAKE.FUN",
       bold(48), WHITE)
center(d, SIZE // 2, 1518, "MAKE.FUN/SPONSOR/NEW", mono(30), (200, 205, 220))

img.save(f"{WORK}/meme.png")
img.resize((480, 480), Image.LANCZOS).save(f"{WORK}/meme-480-preview.png")
print("saved", f"{WORK}/meme.png")
