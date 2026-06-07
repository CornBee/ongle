#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""097_thumb.py — 영상_097 블로그 카드 썸네일 (PIL 직관, 089 스타일)
- 1200x630 (OG 표준)
- hero: "74%" + "4곳 중 3곳"
- one-liner: "코스닥 새내기가 같은 문을 지났다"
- highlight: "단일 게이트"
- 푸터: ONGLE · cornbee.github.io
- 출력: ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/097-정책자금-단일게이트.png
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
print(f"[097_thumb] font: {FONT}")


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


# 097 팔레트 — deep navy + warm gold + orange accent
BG_TOP     = (16, 23, 42)        # deep navy
BG_BOTTOM  = (10, 16, 30)
GOLD_HI    = (255, 200, 60)
GOLD_BOX   = (220, 170, 40)
ORANGE     = (255, 107, 53)
WHITE      = (255, 255, 255)
CREAM      = (240, 235, 220)
SUB_GRAY   = (190, 200, 215)
PANEL      = (28, 38, 64)


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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #097", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 05 · 23"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left panel (hero number)
d.rectangle([(0, 50), (560, H)], fill=PANEL)
# Big "74%" hero
f_hero = font(260, bold_index=0)
shadow(d, (60, 90), "74%", f_hero, GOLD_HI)

# subtitle 한 줄 by 한 줄
shadow(d, (60, 360), "코스닥 새내기", font(46), WHITE)
shadow(d, (60, 415), "4곳 중 3곳", font(46), WHITE)

# 하단 배지 — 단일 게이트
badge_y = H - 110
badge_text = "단일 게이트"
f_bg = font(34, bold_index=0)
bb = d.textbbox((0, 0), badge_text, font=f_bg)
bw2 = bb[2] - bb[0]
d.rounded_rectangle([(50, badge_y), (50 + bw2 + 40, badge_y + 60)],
                    radius=14, fill=ORANGE)
d.text((70, badge_y + 10), badge_text, font=f_bg, fill=WHITE)

# Right column — one-line hook + corrected frame
rx = 600
shadow(d, (rx, 110), "코스닥 새내기가", font(40), SUB_GRAY)
shadow(d, (rx, 165), "같은 문을 지났다", font(46), CREAM)

# 분리선
d.rectangle([(rx, 240), (W - 60, 248)], fill=GOLD_BOX)

# 강조 — 단일 게이트 하이라이트
shadow(d, (rx, 280), "병목은 종목 X", font(38), SUB_GRAY)
shadow(d, (rx, 340), "구조 O", font(54), WHITE)

# 노란 highlight 박스 — "KVIC 모태 단일 게이트"
hb_y = 410
real_text = "KVIC 모태 단일 게이트"
f_real = font(36, bold_index=0)
rb = d.textbbox((rx, hb_y), real_text, font=f_real)
d.rounded_rectangle([(rb[0] - 12, rb[1] + 6), (rb[2] + 18, rb[3] + 18)],
                    radius=12, fill=GOLD_HI)
d.text((rx, hb_y), real_text, font=f_real, fill=BG_BOTTOM)

# 작은 설명
shadow(d, (rx, 490), "224곳 지원 → 21곳 통과", font(26), SUB_GRAY)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

OUT_DIR = os.path.expanduser(
    "~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "097-정책자금-단일게이트.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
