#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""101_thumb.py — 영상_101 블로그 카드 썸네일 (PIL 직관, 089 스타일)
- 1200x630 (OG 표준)
- hero 좌: "1,993조" (큰 시안)
- 부캡션: "GDP ≈ 89%" "사상 최대"
- 가운데: "은행 → 2금융" 화살표
- 우측 박스: "은행 -0.2조 vs 비은행 +13조"
- 푸터: ONGLE · cornbee.github.io
- 출력: ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/101-가계신용.png
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

_FONT_CANDIDATES = [
    "/sessions/vibrant-dreamy-gates/mnt/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc",
    os.path.expanduser("~/Desktop/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc"),
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
]
FONT = next((p for p in _FONT_CANDIDATES if os.path.exists(p)), None)
print(f"[101_thumb] font: {FONT}")


def font(s, bold_index=4):
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


# 101 팔레트 — 가계부채 = deep navy + cyan hero + orange 풍선효과 accent
BG_TOP     = (10, 16, 28)
BG_BOTTOM  = (6, 10, 18)
HI_CYAN    = (95, 215, 235)        # 1,993조 hero
HI_CYAN_BX = (60, 170, 200)
HI_ORANGE  = (255, 175, 95)        # 풍선효과 highlight
HI_RED     = (240, 120, 120)
WHITE      = (255, 255, 255)
CREAM      = (240, 235, 220)
SUB_GRAY   = (190, 200, 215)
PANEL      = (22, 30, 50)
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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #101", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 08"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Title small
shadow(d, (50, 80), "1Q26 가계신용", font(38), CREAM)
shadow(d, (50, 130), "사상 최대 · 24년 만", font(28), SUB_GRAY)

# Hero — 1,993조 큰 숫자
hero_y = 195
shadow(d, (50, hero_y), "1,993조", font(160), HI_CYAN)
# 부캡션 — GDP 89%
shadow(d, (50, hero_y + 175), "GDP ≈ 89%", font(40), HI_ORANGE)
shadow(d, (50, hero_y + 230), "통계 작성 2002 4Q 이후 최대", font(22), SUB_GRAY)

# 가운데 화살표 — 은행 → 2금융
arrow_y = 360
arrow_x_start = 670
arrow_x_end = 760
d.line([(arrow_x_start, arrow_y), (arrow_x_end, arrow_y)], fill=HI_ORANGE, width=10)
d.polygon([(arrow_x_end, arrow_y - 22),
           (arrow_x_end + 32, arrow_y),
           (arrow_x_end, arrow_y + 22)], fill=HI_ORANGE)

# 좌측 "은행" 라벨
shadow(d, (570, arrow_y - 40), "은행", font(36), HI_RED)
shadow(d, (560, arrow_y + 10), "-0.2조", font(28), HI_RED)

# 우측 "2금융" 라벨
shadow(d, (810, arrow_y - 40), "2금융", font(36), HI_ORANGE)
shadow(d, (810, arrow_y + 10), "+13조", font(28), HI_ORANGE)

# 우측 박스 — 큰 hero 박스 (풍선효과 강조)
box_x, box_y, box_w, box_h = 720, 90, 440, 200
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=PANEL,
                    outline=HI_ORANGE, width=4)
shadow(d, (box_x + 26, box_y + 22), "풍선효과", font(36), HI_ORANGE)
shadow(d, (box_x + 26, box_y + 78), "은행 막혔는데", font(28), CREAM)
shadow(d, (box_x + 26, box_y + 118), "2금융 주담대", font(28), CREAM)
shadow(d, (box_x + 26, box_y + 158), "한 줄 +10.6조", font(28), HI_CYAN)

# 하단 sub — 결론 hint
sub_y = 540
shadow(d, (50, sub_y), "사상 최대보다 — 빚이 어디로 옮겨가는지", font(28), CREAM)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

# Output — 다중 경로 fallback
_OUT_DIRS = [
    "/sessions/vibrant-dreamy-gates/mnt/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs",
    os.path.expanduser("~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs"),
]
OUT_DIR = next((p for p in _OUT_DIRS if os.path.isdir(p)), _OUT_DIRS[0])
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "101-가계신용.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
