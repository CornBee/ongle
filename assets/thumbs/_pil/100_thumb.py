#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""100_thumb.py — 영상_100 블로그 카드 썸네일 (PIL 직관, anchor 스타일)
- 1200x630 (OG 표준)
- 헤드라인: "9년 사이 거꾸로"
- 좌측 hero: "19% → 11%" (중국 對미 수출 비중)
- 우측 hero: "10% → 35%" (반도체 자급률)
- 가운데/하단: "한국 자리?" 캡션
- 푸터: ONGLE · cornbee.github.io/ongle
- 출력: ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs/100-미중위상역전.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ─── 폰트 후보 — koreanize NanumGothic 우선 (Bold 별도 파일), AppleSDGothicNeo fallback
_FONT_CANDIDATES = [
    "/sessions/serene-beautiful-cori/.local/lib/python3.10/site-packages/koreanize_matplotlib/fonts/NanumGothic.ttf",
    "/sessions/serene-beautiful-cori/mnt/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc",
    os.path.expanduser("~/Desktop/Shorts_제작/영상_015_20260425_머스크SpaceX/fonts/AppleSDGothicNeo.ttc"),
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
]
_BOLD_CANDIDATES = [
    "/sessions/serene-beautiful-cori/.local/lib/python3.10/site-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf",
] + _FONT_CANDIDATES

FONT = next((p for p in _FONT_CANDIDATES if os.path.exists(p)), None)
FONT_BOLD = next((p for p in _BOLD_CANDIDATES if os.path.exists(p)), FONT)
print(f"[100_thumb] regular font: {FONT}")
print(f"[100_thumb] bold    font: {FONT_BOLD}")


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT
    if path is None:
        return ImageFont.load_default()
    try:
        if path.endswith(".ttc"):
            return ImageFont.truetype(path, size, index=4 if bold else 0)
        return ImageFont.truetype(path, size)
    except (TypeError, OSError):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            return ImageFont.load_default()


def shadow(d, xy, t, f, fill, shadow_color=(0, 0, 0, 200), offset=(3, 4)):
    d.text((xy[0] + offset[0], xy[1] + offset[1]), t, font=f, fill=shadow_color)
    d.text(xy, t, font=f, fill=fill)


# ─── 100 팔레트 — anchor / 위상 역전 = deep navy + slate gray + cyan hero + amber accent
BG_TOP    = (12, 20, 36)      # deep documentary navy
BG_BOTTOM = (6, 12, 22)
HI_CYAN   = (95, 215, 235)    # 19% / 10% (시작점)
HI_AMBER  = (255, 170, 85)    # 11% / 35% (끝점)
HI_RED    = (235, 110, 110)   # 한국 자리? 캡션
WHITE     = (255, 255, 255)
CREAM     = (240, 235, 220)
SUB_GRAY  = (185, 195, 210)
PANEL     = (24, 32, 50)
DIVIDER   = (60, 75, 100)


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

# ─── Top tag bar
d.rectangle([(0, 0), (W, 50)], fill=(0, 0, 0, 230))
shadow(d, (24, 10), "ONGLE · anchor #100 · 미중 위상 역전", font(24), (220, 220, 220, 255))

# 날짜 pill
date_text = "2026 · 05 · 14"
fdate = font(22)
bbox = d.textbbox((0, 0), date_text, font=fdate)
tw = bbox[2] - bbox[0]
d.rectangle([(W - tw - 50, 8), (W - 14, 42)], fill=(50, 50, 50, 230))
d.text((W - tw - 30, 13), date_text, font=fdate, fill=(240, 240, 240, 255))

# ─── 헤드라인 — "9년 사이 거꾸로"
shadow(d, (50, 80), "9년 사이", font(48, bold=True), CREAM)
shadow(d, (50, 140), "거꾸로", font(112, bold=True), HI_AMBER)

# 부캡션 — 트럼프 9년 만 방중
shadow(d, (50, 260), "트럼프 9년 만 방중 · 5/14 베이징", font(26), SUB_GRAY)

# ─── 좌측 hero 박스 — 19% → 11% (중국 對미 수출 비중)
box1_x, box1_y, box1_w, box1_h = 50, 320, 540, 200
d.rounded_rectangle([(box1_x, box1_y), (box1_x + box1_w, box1_y + box1_h)],
                    radius=20, fill=PANEL, outline=DIVIDER, width=2)
shadow(d, (box1_x + 24, box1_y + 18), "중국 → 미국 수출 비중", font(24), SUB_GRAY)

# 큰 숫자 — 19% → 11%
num_y = box1_y + 65
shadow(d, (box1_x + 24, num_y), "19%", font(90, bold=True), HI_CYAN)
# 화살표
arrow_x = box1_x + 200
arrow_y = num_y + 55
d.line([(arrow_x, arrow_y), (arrow_x + 70, arrow_y)], fill=HI_AMBER, width=8)
d.polygon([(arrow_x + 70, arrow_y - 18),
           (arrow_x + 100, arrow_y),
           (arrow_x + 70, arrow_y + 18)], fill=HI_AMBER)
shadow(d, (box1_x + 320, num_y), "11%", font(90, bold=True), HI_AMBER)
shadow(d, (box1_x + 24, box1_y + 165), "9년 사이 — Visual Capitalist · PIIE", font(20), SUB_GRAY)

# ─── 우측 hero 박스 — 10% → 35% (반도체 자급률)
box2_x, box2_y, box2_w, box2_h = 610, 320, 540, 200
d.rounded_rectangle([(box2_x, box2_y), (box2_x + box2_w, box2_y + box2_h)],
                    radius=20, fill=PANEL, outline=DIVIDER, width=2)
shadow(d, (box2_x + 24, box2_y + 18), "중국 반도체 장비 자급률", font(24), SUB_GRAY)

# 큰 숫자 — 10% → 35%
num2_y = box2_y + 65
shadow(d, (box2_x + 24, num2_y), "10%", font(90, bold=True), HI_CYAN)
arrow2_x = box2_x + 200
d.line([(arrow2_x, arrow_y), (arrow2_x + 70, arrow_y)], fill=HI_AMBER, width=8)
d.polygon([(arrow2_x + 70, arrow_y - 18),
           (arrow2_x + 100, arrow_y),
           (arrow2_x + 70, arrow_y + 18)], fill=HI_AMBER)
shadow(d, (box2_x + 320, num2_y), "35%", font(90, bold=True), HI_AMBER)
shadow(d, (box2_x + 24, box2_y + 165), "한 자릿수 → 2025·말 — SCMP", font(20), SUB_GRAY)

# ─── 하단 캡션 — "한국 자리?" (한 줄 핵심 question)
cap_y = 537
shadow(d, (50, cap_y), "그 사이 — 한국 자리?", font(34, bold=True), HI_RED)
shadow(d, (510, cap_y + 8), "반도체·자동차·화학 → 환율·물가·고용", font(20), CREAM)

# ─── Bottom footer (조금 더 얇게)
d.rectangle([(0, H - 32), (W, H)], fill=(0, 0, 0, 230))
shadow(d, (24, H - 26), "ONGLE 블로그 — cornbee.github.io/ongle", font(20),
       (220, 220, 220, 255))

# ─── Output — 다중 경로 fallback
_OUT_DIRS = [
    "/sessions/serene-beautiful-cori/mnt/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs",
    os.path.expanduser("~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo/assets/thumbs"),
]
OUT_DIR = next((p for p in _OUT_DIRS if os.path.isdir(p)), _OUT_DIRS[0])
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "100-미중위상역전.png")
img.save(OUT, "PNG", optimize=True)
print(f"OK → {OUT}  ({W}x{H}, {os.path.getsize(OUT)/1024:.1f} KB)")

# Also save into the work_dir/report/thumbnail.png so sync_card_thumbnail finds it
_REPORT_DIRS = [
    "/sessions/serene-beautiful-cori/mnt/Shorts_제작/영상_100_트럼프방중미중위상역전_20260608/report",
    os.path.expanduser("~/Desktop/Shorts_제작/영상_100_트럼프방중미중위상역전_20260608/report"),
]
RD = next((p for p in _REPORT_DIRS if os.path.isdir(p)), None)
if RD:
    OUT2 = os.path.join(RD, "thumbnail.png")
    img.save(OUT2, "PNG", optimize=True)
    print(f"OK → {OUT2}")
