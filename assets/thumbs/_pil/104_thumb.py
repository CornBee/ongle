#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""104_thumb.py — 영상_104 블로그 카드 썸네일 (PIL, 089/102/103 스타일)
- 1200x630 (OG 표준)
- hero 좌: "0.95" 큰 숫자 + 부제 "2026·1Q 합계출산율" + "7년 만 0.9" 강조 박스
- hero 우: "2019·1Q 1.02 / 2025·1Q 0.82 / 2026·1Q 0.95" 7년 곡선 3자리
- one-liner 하단: "+0.13 · 1월 단월 0.99 (월별 최고치) · 단일 분기 신호"
- 푸터: ONGLE · cornbee.github.io
- 출력: assets/thumbs/104-출산율-7년-곡선.png
- 정치 회피: 정파·인물 어휘 0건. 출산 권장·이념적 family framing 0건. 통계 숫자만.
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
print(f"[104_thumb] font: {FONT}")


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


# 104 팔레트 — warm cream beige + amber (인구·시계열 톤)
BG_TOP     = (32, 24, 18)     # warm deep brown
BG_BOTTOM  = (22, 16, 12)
HI_AMBER   = (255, 198, 100)  # 0.95 hero (warm amber)
HI_AMBER2  = (220, 160, 60)
HI_CREAM   = (248, 240, 222)
HI_HOT     = (255, 220, 150)  # "7년 만 0.9" highlight
HOT_BG     = (130, 70, 50)    # warm burgundy (시계열 신호)
PEAK_2019  = (200, 165, 120)  # 2019 1.02 (soft past peak)
PEAK_2026  = (255, 198, 100)  # 2026 0.95 (current — amber)
PEAK_2025  = (160, 145, 130)  # 2025 0.82 (recent low — neutral)
WHITE      = (255, 255, 255)
SUB_GRAY   = (200, 195, 185)
PANEL      = (52, 42, 32)
DIVIDER    = (100, 84, 60)


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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #104", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 09"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left column — 0.95 hero
shadow(d, (50, 80), "2026·1Q 합계출산율", font(36), HI_CREAM)

# 0.95 hero — 매우 큰 숫자
hero_y = 130
shadow(d, (50, hero_y), "0.95", font(180), HI_AMBER)

# "7년 만 0.9 회복" — burgundy highlight box
hot_y = 340
hot_text = "7년 만 0.9 자리"
f_hot = font(42)
hot_bb = d.textbbox((50, hot_y), hot_text, font=f_hot)
d.rounded_rectangle([(hot_bb[0] - 24, hot_bb[1] - 6), (hot_bb[2] + 28, hot_bb[3] + 18)],
                    radius=18, fill=HOT_BG)
d.text((50, hot_y), hot_text, font=f_hot, fill=HI_HOT)

# 하단 sub
shadow(d, (50, 440), "+0.13 · 출생아 +7.4%", font(36), HI_CREAM)
shadow(d, (50, 490), "1월 단월 0.99 — 월별 최고치", font(22), SUB_GRAY)
shadow(d, (50, 525), "단일 분기 신호 — 추세/노이즈 분기 자리", font(20), SUB_GRAY)

# Right side panel — 7년 곡선 3자리
box_x, box_y, box_w, box_h = 720, 90, 440, 460
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=(52, 42, 32, 255),
                    outline=HI_AMBER2, width=5)

# 카드 상단 label
shadow(d, (box_x + 28, box_y + 22), "7년 곡선 — 3자리", font(24), HI_AMBER2)

# 2019-1Q 1.02 (직전 0.9대 자리)
shadow(d, (box_x + 28, box_y + 70), "2019·1Q", font(24), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 105), "1.02", font(54), PEAK_2019)
shadow(d, (box_x + 215, box_y + 120), "직전 0.9대", font(20), SUB_GRAY)

# 2025-1Q 0.82 (1년 전 자리)
shadow(d, (box_x + 28, box_y + 190), "2025·1Q", font(24), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 225), "0.82", font(54), PEAK_2025)
shadow(d, (box_x + 215, box_y + 240), "1년 전", font(20), SUB_GRAY)

# 2026-1Q 0.95 (이번 분기 — 강조)
shadow(d, (box_x + 28, box_y + 310), "2026·1Q", font(24), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 345), "0.95", font(60), PEAK_2026)
shadow(d, (box_x + 215, box_y + 360), "+0.13", font(22), HI_AMBER)

# divider line
d.line([(box_x + 28, box_y + 435), (box_x + box_w - 28, box_y + 435)],
       fill=HI_AMBER2, width=3)

# Bottom footer
d.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 38), "ONGLE 블로그 — cornbee.github.io", font(24),
       (220, 220, 220, 255))

OUT_DIR = os.path.expanduser(
    "~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs")
# When running in sandbox, also try absolute mount path
if not os.path.isdir(OUT_DIR):
    OUT_DIR = "/sessions/determined-relaxed-albattani/mnt/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs"
os.makedirs(OUT_DIR, exist_ok=True)
# slug full match: 104-출산율-7년-곡선
OUT = os.path.join(OUT_DIR, "104-출산율-7년-곡선.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
