#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""103_thumb.py — 영상_103 블로그 카드 썸네일 (PIL 직관, 089/102 스타일 미러)
- 1200x630 (OG 표준)
- hero 좌: "1,561원" 큰 숫자 + 부제 "원·달러 (2026-06-07)" + "17년 만" 강조 박스
- hero 우: "2009-03-06 1,597원 / 2026-06-07 1,561원 / 공항 1,624원" 17년 곡선 3자리
- one-liner 하단: "시장 vs 공항 63원 차이 · 외생 3축 한 줄"
- 푸터: ONGLE · cornbee.github.io
- 출력: /Users/seogihwan/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/103-원달러-17년곡선.png
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
print(f"[103_thumb] font: {FONT}")


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


# 103 팔레트 — deep documentary blue + dollar green (외환시장 톤)
BG_TOP     = (10, 18, 32)     # documentary deep blue
BG_BOTTOM  = (6, 12, 22)
HI_GOLD    = (255, 198, 100)  # 1,561원 hero (dollar amber)
HI_GOLD2   = (220, 160, 60)
HI_CREAM   = (248, 240, 222)
HI_HOT     = (255, 220, 150)  # "17년 만" highlight
HOT_BG     = (140, 50, 60)    # deep burgundy (시계열 신호)
PEAK_RED   = (235, 110, 95)   # 2009 봉우리 1,597
PEAK_GOLD  = (255, 198, 100)  # 2026 봉우리 1,561
AIRPORT    = (200, 200, 220)  # 공항 1,624 (soft)
WHITE      = (255, 255, 255)
SUB_GRAY   = (190, 195, 210)
PANEL      = (24, 36, 56)
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
shadow(d, (24, 10), "ONGLE · 시점성 분석 #103", font(24), (220, 220, 220, 255))

# Date pill top-right
date_text = "2026 · 06 · 09"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# Left column — 1,561원 hero
shadow(d, (50, 80), "원·달러 (장중)", font(36), HI_CREAM)

# 1,561원 hero — 매우 큰 숫자
hero_y = 130
shadow(d, (50, hero_y), "1,561원", font(150), HI_GOLD)

# "17년 만" — burgundy highlight box (강조)
hot_y = 320
hot_text = "17년 만 두 번째 봉우리"
f_hot = font(42)
hot_bb = d.textbbox((50, hot_y), hot_text, font=f_hot)
d.rounded_rectangle([(hot_bb[0] - 24, hot_bb[1] - 6), (hot_bb[2] + 28, hot_bb[3] + 18)],
                    radius=18, fill=HOT_BG)
d.text((50, hot_y), hot_text, font=f_hot, fill=HI_HOT)

# 하단 sub — 시장 vs 공항 63원 · 외생 3축 한 줄
shadow(d, (50, 440), "시장 vs 공항 63원 차이", font(38), HI_CREAM)
shadow(d, (50, 495), "외생 3축 한 줄 · 미국금리·중동·엔화", font(22), SUB_GRAY)
shadow(d, (50, 535), "2009-03-06 이후 17년 3개월 만", font(20), SUB_GRAY)

# Right side panel — 17년 곡선 3자리
box_x, box_y, box_w, box_h = 720, 90, 440, 460
d.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)],
                    radius=24, fill=(24, 36, 56, 255),
                    outline=HI_GOLD2, width=5)

# 카드 상단 label
shadow(d, (box_x + 28, box_y + 22), "17년 곡선 — 3자리", font(24), HI_GOLD2)

# 2009-03-06 1,597 (종전 봉우리)
shadow(d, (box_x + 28, box_y + 70), "2009-03-06", font(24), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 105), "1,597원", font(54), PEAK_RED)
shadow(d, (box_x + 230, box_y + 120), "금융위기", font(20), SUB_GRAY)

# 2026-06-07 1,561 (이번 봉우리)
shadow(d, (box_x + 28, box_y + 190), "2026-06-07", font(24), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 225), "1,561원", font(60), PEAK_GOLD)
shadow(d, (box_x + 230, box_y + 240), "장중", font(20), SUB_GRAY)

# 인천공항 환전소 1,624
shadow(d, (box_x + 28, box_y + 320), "인천공항 환전소", font(22), SUB_GRAY)
shadow(d, (box_x + 28, box_y + 355), "1,624원", font(48), AIRPORT)
shadow(d, (box_x + 230, box_y + 370), "+63원", font(22), HI_GOLD)

# divider line
d.line([(box_x + 28, box_y + 435), (box_x + box_w - 28, box_y + 435)],
       fill=HI_GOLD2, width=3)

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
OUT = os.path.join(OUT_DIR, "103-원달러-17년곡선.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")
