# 발행 메모 — 111 만화 리포트 (첫 시범편)

생성: 2026-06-13 (ONGLE Comic Report SKILL v1 첫 시범편)

## 현재 상태
- 만화 6컷: **PLACEHOLDER** (sandbox outbound 차단으로 nano banana 미실행)
- 차트 2개: FINAL
- HTML/SEO 본문/meta: FINAL (사용자 review 대기)

## 진짜 nano banana 컷으로 교체
```bash
cd ~/Desktop/Shorts_제작/영상_111_환율22.9원시민자리_20260609/report_comic
python3 ../../_tools/imagegen.py \
  --prompts prompts.json \
  --out-dir assets/comics \
  --aspect-ratio 1:1
# 생성 완료 후 placeholder 자리에 덮어쓰기
cp assets/comics/panel_*.png \
   ../../Shorts_업로드/_blog_repo/comic/111-환율-22.9원/assets/comics/
# cover.png 도 다시 합성
python3 -c "
from PIL import Image
from pathlib import Path
src = Path('assets/comics')
cw, ch = 1200, 1800
cell_w, cell_h = (cw-60)//2, (ch-80)//3
cover = Image.new('RGB', (cw, ch), (252,248,240))
fs = ['panel_01_hook.png','panel_02_point.png','panel_03_positive_loop.png',
      'panel_04_negative_loop.png','panel_05_split.png','panel_06_mirror.png']
for i,f in enumerate(fs):
    p = Image.open(src/f).convert('RGB').resize((cell_w,cell_h), Image.LANCZOS)
    col, row = i%2, i//2
    cover.paste(p, (20+col*(cell_w+20), 20+row*(cell_h+20)))
cover.save(src/'cover.png','PNG',quality=92)
"
cp assets/comics/cover.png ../../Shorts_업로드/_blog_repo/comic/111-환율-22.9원/assets/comics/
```

## GitHub Pages 발행 (수동)
```bash
cd ~/Desktop/Shorts_제작/Shorts_업로드/_blog_repo
git add comic/111-환율-22.9원/
git commit -m "comic: 111 환율 22.9원 첫 시범편 — 만화 6컷 + SEO 본문 + 차트"
git push origin main
```
→ URL: https://cornbee.github.io/ongle/comic/111-환율-22.9원/

## YouTube description 첫 줄 (영상 111 설명 update 시)
```
📌 만화로 보기 → https://cornbee.github.io/ongle/comic/111-환율-22.9원
📌 깊이 분석 → https://cornbee.github.io/ongle/r/111-환율-22.9원-시민자리
```

## 핀댓글 (만화 포맷용)
```
영상에 다 못 담은 부분 — 만화로 정리해 봤습니다.

📌 만화: 같은 22.9원이 두 자리에 어떻게 적히는가
검색: 'cornbee ongle' / 채널 설명 첫 줄 링크

(자세한 분석·차트·출처는 같은 페이지에서 분석 리포트로 이어집니다)
```
