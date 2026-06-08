#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""106_thumb.py — 영상_106 블로그 카드 썸네일 (PIL 직관, 098 스타일 미러)
- 1200x630 (OG 표준)
- hero 좌: "26.2조" 큰 숫자 + 부제 "추경" + "국채 0원" 강조 박스
- hero 우: "초과세수 25.2조 + 기금 1조" 카드 (= 26.2조 합산 식)
- one-liner 하단: "빚 없이 짠 자리"
- 푸터: ONGLE · cornbee.github.io
- 출력: ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/106-추경구조.png
- 정치 회피: 정파·인물 어휘 0건. 구조 신호(숫자·식)만 표시.
"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleSDGothicNeo.ttc",
    os.path.expanduser(
        "~/Desktop/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc"),
    os.path.expanduser("~/Library/Fonts/NanumGothic.ttf"),
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    # Linux sandbox — koreanize-matplotlib bundles NanumGothic
    os.path.expanduser(
        "~/.local/lib/python3.10/site-packages/koreanize_matplotlib/fonts/NanumGothic.ttf"),
    "/sessions/blissful-brave-euler/.local/lib/python3.10/site-packages/koreanize_matplotlib/fonts/NanumGothic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def find_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


FONT = find_font()
print(f"[106_thumb] font: {FONT}")


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


# 106 팔레트 — warm amber + cream + soft burgundy (정파 회피 색조)
BG_TOP     = (38, 26, 18)     # warm dark brown
BG_BOTTOM  = (22, 14, 10)
HI_AMBER   = (255, 196, 90)   # 26.2조 hero
HI_AMBER2  = (220, 150, 60)
HI_CREAM   = (250, 240, 220)
HI_NODEBT  = (255, 230, 160)  # "국채 0원" highlight
NODEBT_BG  = (160, 50, 50)    # burgundy
GREEN_OK   = (170, 220, 130)  # "+" mark / 합산 식
WHITE      = (255, 255, 255)
SUB_GRAY   = (200, 195, 180)
PANEL      = (52, 36, 22)


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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #106", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 09"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left column — 26.2조 hero
shadow(d, (50, 80), "추가경정예산", font(36), HI_CREAM)

# 26.2조 hero — 매우 큰 숫자
hero_y = 130
shadow(d, (50, hero_y), "26.2조", font(180), HI_AMBER)

# "국채 0원" — burgundy highlight box (강조)
nd_y = 360
nd_text = "국채 0원"
f_nd = font(70)
nd_bb = d.textbbox((50, nd_y), nd_text, font=f_nd)
d.rounded_rectangle([(nd_bb[0] - 24, nd_bb[1] - 6), (nd_bb[2] + 28, nd_bb[3] + 18)],
                    radius=18, fill=NODEBT_BG)
d.text((50, nd_y), nd_text, font=f_nd, fill=HI_NODEBT)

# 하단 sub — "빚 없이 짠 자리"
shadow(d, (50, 475), "빚 없이 짠 자리", font(40), HI_CREAM)
shadow(d, (50, 530), "추가 국채 발행 0 · 구조 분해", font(24), SUB_GRAY)

# Right side panel — 합산 식 카드
box_x, box_y, box_w, box_h = 720, 90, 440, 460
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=(60, 42, 26, 255),
                    outline=HI_AMBER2, width=5)

# 카드 상단 label
shadow(d, (box_x + 28, box_y + 22), "자금 출처", font(26), HI_AMBER2)

# 초과세수 25.2조
shadow(d, (box_x + 28, box_y + 70), "초과세수", font(30), HI_CREAM)
shadow(d, (box_x + 28, box_y + 110), "25.2조", font(74), HI_AMBER)

# 화살표 + (가운데 +)
plus_y = box_y + 200
d.text((box_x + 180, plus_y), "+", font=font(58), fill=GREEN_OK)

# 기금 1조
shadow(d, (box_x + 28, box_y + 225), "기금", font(30), HI_CREAM)
shadow(d, (box_x + 28, box_y + 265), "1조", font(74), HI_AMBER)

# divider line
d.line([(box_x + 28, box_y + 365), (box_x + box_w - 28, box_y + 365)],
       fill=HI_AMBER2, width=4)

# 합산 결과 = 26.2조
shadow(d, (box_x + 28, box_y + 385), "= 추경 26.2조", font(36), HI_AMBER)

# (sub text 제거 — 카드 안에 = 추경 26.2조까지 다 들어감)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

OUT_DIR = os.path.expanduser(
    "~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "106-추경구조.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
