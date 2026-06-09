#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""102_thumb.py — 영상_102 블로그 카드 썸네일 (PIL 직관, 106 스타일 미러)
- 1200x630 (OG 표준)
- hero 좌: "3.1%" 큰 숫자 + 부제 "5월 CPI" + "26개월 만 최고" 강조 박스
- hero 우: "휘발유 +23.1% / 경유 +33.3% / 등유 +21.7%" 석유류 분해 카드
- one-liner 하단: "석유류 +24.2% · 외생 사슬 한 줄"
- 푸터: ONGLE · cornbee.github.io
- 출력: /Users/seogihwan/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/102-5월물가-휘발유.png
- 정치 회피: 정파·인물 어휘 0건. 구조 신호(숫자)만 표시.
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
    "/sessions/determined-relaxed-albattani/.local/lib/python3.10/site-packages/koreanize_matplotlib/fonts/NanumGothic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def find_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


FONT = find_font()
print(f"[102_thumb] font: {FONT}")


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


# 102 팔레트 — deep documentary slate + amber pump glow (외생 충격 사슬 톤)
BG_TOP     = (16, 24, 36)     # documentary slate
BG_BOTTOM  = (8, 14, 22)
HI_AMBER   = (255, 178, 70)   # 3.1% hero (fuel pump glow)
HI_AMBER2  = (220, 140, 50)
HI_CREAM   = (248, 240, 222)
HI_HOT     = (255, 220, 150)  # "26개월 만 최고" highlight
HOT_BG     = (170, 60, 50)    # warm burgundy (warning)
DIESEL_RED = (235, 110, 95)   # 경유 33.3% — 가장 큰 자리
GASOLINE   = (255, 178, 70)   # 휘발유 23.1%
KEROSENE   = (200, 200, 220)  # 등유 21.7% (가장 작은 자리, soft)
WHITE      = (255, 255, 255)
SUB_GRAY   = (190, 195, 210)
PANEL      = (28, 38, 56)
DIVIDER    = (60, 78, 100)


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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #102", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 09"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left column — 3.1% hero
shadow(d, (50, 80), "5월 소비자물가", font(36), HI_CREAM)

# 3.1% hero — 매우 큰 숫자
hero_y = 130
shadow(d, (50, hero_y), "+3.1%", font(180), HI_AMBER)

# "26개월 만 최고" — burgundy highlight box (강조)
hot_y = 360
hot_text = "26개월 만 최고"
f_hot = font(54)
hot_bb = d.textbbox((50, hot_y), hot_text, font=f_hot)
d.rounded_rectangle([(hot_bb[0] - 24, hot_bb[1] - 6), (hot_bb[2] + 28, hot_bb[3] + 18)],
                    radius=18, fill=HOT_BG)
d.text((50, hot_y), hot_text, font=f_hot, fill=HI_HOT)

# 하단 sub — 석유류 24.2% · 외생 사슬 한 줄
shadow(d, (50, 470), "석유류 +24.2%", font(40), HI_CREAM)
shadow(d, (50, 525), "외생 사슬 한 줄 · 0.92%p 기여", font(24), SUB_GRAY)

# Right side panel — 석유류 분해 카드
box_x, box_y, box_w, box_h = 720, 90, 440, 460
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=(34, 46, 66, 255),
                    outline=HI_AMBER2, width=5)

# 카드 상단 label
shadow(d, (box_x + 28, box_y + 22), "석유류 분해 (전년동월비)", font(24), HI_AMBER2)

# 경유 33.3% — 가장 큰 자리 (먼저 박음)
shadow(d, (box_x + 28, box_y + 70), "경유", font(30), HI_CREAM)
shadow(d, (box_x + 28, box_y + 110), "+33.3%", font(72), DIESEL_RED)

# 휘발유 23.1%
shadow(d, (box_x + 28, box_y + 210), "휘발유", font(30), HI_CREAM)
shadow(d, (box_x + 28, box_y + 250), "+23.1%", font(64), GASOLINE)

# 등유 21.7%
shadow(d, (box_x + 28, box_y + 340), "등유", font(26), HI_CREAM)
shadow(d, (box_x + 28, box_y + 375), "+21.7%", font(52), KEROSENE)

# divider line
d.line([(box_x + 28, box_y + 435), (box_x + box_w - 28, box_y + 435)],
       fill=HI_AMBER2, width=3)

# (footnote 제거 — 카드 안에 분포만)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

OUT_DIR = os.path.expanduser(
    "~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "102-5월물가-휘발유.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
