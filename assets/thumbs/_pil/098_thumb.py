#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""098_thumb.py — 영상_098 블로그 카드 썸네일 (PIL 직관, 089 스타일)
- 1200x630 (OG 표준)
- hero 좌: "5년 → 3년"
- hero 우 큰 highlight: "월 50만 → 3년 2,197만"
- one-liner: "매칭은 두 배로"
- 푸터: ONGLE · cornbee.github.io
- 출력: ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/098-청년미래적금.png
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleSDGothicNeo.ttc",
    os.path.expanduser(
        "~/Desktop/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc"),
    os.path.expanduser("~/Library/Fonts/NanumGothic.ttf"),
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def find_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


FONT = find_font()
print(f"[098_thumb] font: {FONT}")


def font(s, bold_index=0):
    if FONT is None:
        return ImageFont.load_default()
    try:
        return ImageFont.truetype(FONT, s, index=bold_index)
    except (TypeError, OSError):
        try:
            return ImageFont.truetype(FONT, s)
        except OSError:
            return ImageFont.load_default()


def shadow(d, xy, t, f, fill, shadow_color=(0, 0, 0, 220), offset=(3, 4)):
    d.text((xy[0] + offset[0], xy[1] + offset[1]), t, font=f, fill=shadow_color)
    d.text(xy, t, font=f, fill=fill)


# 098 팔레트 — deep teal + cream + warm pink accent
BG_TOP     = (12, 36, 42)
BG_BOTTOM  = (8, 22, 28)
HI_PINK    = (255, 138, 161)     # 매칭 두 배 highlight
HI_BOX     = (240, 100, 130)
GOLD_HI    = (255, 220, 110)     # 2,197만 hero
GOLD_BOX   = (220, 180, 60)
WHITE      = (255, 255, 255)
CREAM      = (240, 235, 220)
SUB_GRAY   = (190, 200, 205)
PANEL      = (18, 50, 58)
GREEN_OK   = (140, 220, 160)


def gradient_bg(d, W, H):
    for y in range(H):
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * (y / H))
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * (y / H))
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * (y / H))
        d.line([(0, y), (W, y)], fill=(r, g, b))


W, H = 1200, 630
img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img, "RGBA")
gradient_bg(d, W, H)

# Top tag bar
d.rectangle([(0, 0), (W, 50)], fill=(0, 0, 0, 230))
shadow(d, (24, 10), "ONGLE · 시점성 분석 #098", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 07"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left column — 5년 → 3년 hero with strikethrough on 5년
shadow(d, (50, 90), "청년미래적금", font(40), CREAM)
shadow(d, (50, 145), "2026 · 06 · 22", font(28), SUB_GRAY)

# 5년 strike → 3년
sy = 220
fbig = font(150)
five_text = "5년"
five_bb = d.textbbox((50, sy), five_text, font=fbig)
d.text((50, sy), five_text, font=fbig, fill=(170, 170, 170, 255))
# red strike line
d.line([(five_bb[0] - 6, (five_bb[1] + five_bb[3]) // 2 + 6),
        (five_bb[2] + 6, (five_bb[1] + five_bb[3]) // 2 + 6)],
       fill=HI_BOX, width=10)

# arrow
arrow_x = five_bb[2] + 35
d.line([(arrow_x, sy + 70), (arrow_x + 60, sy + 70)], fill=GOLD_BOX, width=8)
d.polygon([(arrow_x + 60, sy + 50), (arrow_x + 90, sy + 70),
           (arrow_x + 60, sy + 90)], fill=GOLD_BOX)

# 3년 highlight
shadow(d, (arrow_x + 110, sy), "3년", fbig, GOLD_HI)

# 매칭은 두 배로 — pink highlight box
mb_y = 400
mb_text = "매칭은 두 배로"
f_mb = font(50)
mb = d.textbbox((50, mb_y), mb_text, font=f_mb)
d.rounded_rectangle([(mb[0] - 16, mb[1] + 6), (mb[2] + 22, mb[3] + 18)],
                    radius=14, fill=HI_PINK)
d.text((50, mb_y), mb_text, font=f_mb, fill=(50, 20, 30))

# 하단 — 단일 게이트 식 작은 sub
shadow(d, (50, 500), "6% / 12% 일률 매칭", font(28), SUB_GRAY)
shadow(d, (50, 545), "취급 11곳 → 15곳", font(26), SUB_GRAY)

# Right side panel — 큰 hero 박스
box_x, box_y, box_w, box_h = 720, 90, 440, 360
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=(20, 60, 70, 255),
                    outline=GOLD_BOX, width=5)
shadow(d, (box_x + 30, box_y + 24), "월 50만 → 3년", font(34), GOLD_BOX)
shadow(d, (box_x + 30, box_y + 90), "2,197만", font(130), GOLD_HI)
shadow(d, (box_x + 30, box_y + 240), "우대형 · 금리 6% 기준", font(26), CREAM)
shadow(d, (box_x + 30, box_y + 285), "정부 매칭 12% · 비과세", font(26), GREEN_OK)

# 단일형 sub
shadow(d, (box_x, box_y + box_h + 40), "1차 모집 단 2주", font(34), CREAM)
shadow(d, (box_x, box_y + box_h + 90), "6.22 ~ 7.3", font(28), SUB_GRAY)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

OUT_DIR = os.path.expanduser(
    "~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "098-청년미래적금.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
