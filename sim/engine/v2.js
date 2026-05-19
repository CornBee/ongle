/* ONGLE sim engine v2 — multi-route visual novel runtime
 *
 * Loads a script.json (schema = script_v_final.json) and renders the game.
 * Designed to be chapter-agnostic: engine knows the schema, not the content.
 *
 * Usage (chapterN/index.html):
 *   <link rel="stylesheet" href="/ongle/sim/engine/v2.css">
 *   <div id="sim-root"></div>
 *   <script src="/ongle/sim/engine/v2.js"></script>
 *   <script>
 *     OngleSimV2.mount({
 *       root: '#sim-root',
 *       scriptUrl: 'script.json',
 *       assetsBase: 'scenes/',
 *       characterSheetBase: 'character_sheets/',
 *       saveKey: 'ongle_chapter2_save',
 *     });
 *   </script>
 */
(function (global) {
  'use strict';

  // ---------- State ----------
  function makeState(script) {
    const sa = (script.game_config && script.game_config.start_affinity) || {
      sea: 30, harin: 30, seoyeon: 30, mirae: 30,
    };
    return {
      phase: 'cover',          // cover | scene | reply | ending
      block: 'common',         // common | route_sea | route_harin | route_seoyeon | route_mirae | bad_drift | ending
      idx: 0,                  // index within current block
      route: null,
      affinity: Object.assign({}, sa),
      flags: new Set(),
      replyText: null,
      replyChar: null,
      history: [],
      currentScene: null,
      lastChoiceIdx: null,
    };
  }

  // ---------- Trigger evaluator ----------
  function evalTrigger(trigger, state) {
    if (!trigger) return false;
    const orParts = trigger.split('||').map(s => s.trim());
    for (const orP of orParts) {
      const andConds = orP.split('&&').map(s => s.trim()).filter(Boolean);
      if (andConds.every(c => evalCond(c, state))) return true;
    }
    return false;
  }

  function evalCond(cond, state) {
    cond = cond.trim();
    if (cond.startsWith('!')) return !evalCond(cond.slice(1).trim(), state);
    let m;
    if ((m = cond.match(/^route\s*=\s*(\w+)$/))) return state.route === m[1];
    if (cond === 'all_cleared') return state.flags.has('all_four_cleared');
    if ((m = cond.match(/^aff\s*>=\s*(\d+)$/))) {
      if (!state.route || !state.affinity[state.route]) return false;
      return state.affinity[state.route] >= parseInt(m[1], 10);
    }
    if ((m = cond.match(/^all\s+aff\s*<\s*(\d+)$/))) {
      const t = parseInt(m[1], 10);
      return ['sea','harin','seoyeon','mirae'].every(k => (state.affinity[k] || 0) < t);
    }
    // default: flag name
    return state.flags.has(cond);
  }

  // ---------- Scene navigation ----------
  function getScenesForBlock(script, block) {
    if (block === 'common') return script.scenes_common || [];
    if (block === 'route_sea') return script.scenes_route_sea || [];
    if (block === 'route_harin') return script.scenes_route_harin || [];
    if (block === 'route_seoyeon') return script.scenes_route_seoyeon || [];
    if (block === 'route_mirae') return script.scenes_route_mirae || [];
    return [];
  }

  function getCurrentScene(script, state) {
    const list = getScenesForBlock(script, state.block);
    return list[state.idx] || null;
  }

  function advance(script, state) {
    const list = getScenesForBlock(script, state.block);
    if (state.idx + 1 < list.length) {
      state.idx += 1;
      state.currentScene = list[state.idx];
      return true;
    }
    // end of block → transition
    if (state.block === 'common') {
      // common ended without branch_rule? fallback to ending
      state.block = 'ending';
      return false;
    }
    if (state.block.startsWith('route_')) {
      // route ended → ending
      state.block = 'ending';
      return false;
    }
    state.block = 'ending';
    return false;
  }

  // ---------- Choice handling ----------
  function applyChoice(script, state, choiceIdx) {
    const scene = getCurrentScene(script, state);
    if (!scene || !Array.isArray(scene.choices)) return;
    const ch = scene.choices[choiceIdx];
    if (!ch) return;
    state.lastChoiceIdx = choiceIdx;
    // affinity delta
    if (ch.aff && typeof ch.aff === 'object') {
      for (const k of Object.keys(ch.aff)) {
        state.affinity[k] = clamp((state.affinity[k] || 0) + ch.aff[k], 0, 100);
      }
    }
    // flag
    if (ch.flag) state.flags.add(ch.flag);
    if (Array.isArray(ch.flags)) ch.flags.forEach(f => state.flags.add(f));
    // route branch
    if (scene.kind === 'route_branch') {
      const route = ch.route || (ch.flag && ch.flag.startsWith('route_') ? ch.flag.slice(6) : null);
      if (route === 'bad_drift' || route === 'cold') {
        state.route = null;
        state.flags.add('cold');
        state.block = 'ending';
      } else if (route) {
        state.route = route;
        state.block = 'route_' + route;
        state.idx = -1; // advance() will move to 0
      }
    }
    // reply popup
    state.replyText = ch.reply || null;
    state.replyChar = scene.speaker || null;
    state.history.push({ sceneId: scene.id, choice: choiceIdx, flag: ch.flag, route: state.route });
  }

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  // ---------- Ending selection ----------
  function selectEnding(script, state) {
    const endings = (script.endings || []).slice().sort((a, b) => (a.priority || 99) - (b.priority || 99));
    for (const e of endings) {
      if (evalTrigger(e.trigger, state)) return e;
    }
    // fallback
    return endings[endings.length - 1] || null;
  }

  // ---------- Renderer ----------
  function render(ctx) {
    const { root, script, state, opts } = ctx;
    root.innerHTML = '';
    if (state.phase === 'cover') return renderCover(ctx);
    if (state.phase === 'ending') return renderEnding(ctx);
    return renderScene(ctx);
  }

  function renderCover(ctx) {
    const { root, script, state, opts } = ctx;
    const cover = el('div', { class: 'cover' });
    cover.appendChild(el('h1', {}, script.title || '미연시'));
    if (script.subtitle) cover.appendChild(el('div', { class: 'subtitle' }, script.subtitle));

    const chars = script.characters || {};
    const cast = el('div', { class: 'cast' });
    for (const key of ['sea', 'harin', 'seoyeon', 'mirae']) {
      const c = chars[key];
      if (!c) continue;
      const card = el('div', { class: 'card' });
      const img = el('img', {
        src: opts.characterSheetBase + '_00_' + key + '_sheet_front.png',
        alt: c.name || key,
        loading: 'lazy',
      });
      card.appendChild(img);
      card.appendChild(el('div', { class: 'name' }, c.name || key));
      card.appendChild(el('div', { class: 'role' }, c.role || ''));
      cast.appendChild(card);
    }
    cover.appendChild(cast);

    const cta = el('button', { class: 'cta', type: 'button' }, '시작하기 →');
    cta.addEventListener('click', () => {
      state.phase = 'scene';
      state.block = 'common';
      state.idx = 0;
      state.currentScene = getCurrentScene(script, state);
      saveState(ctx);
      render(ctx);
      emitEvent(opts, 'sim_start_clicked', { chapter: script.chapter });
      emitEvent(opts, 'scene_view', { scene_id: state.currentScene && state.currentScene.id });
    });
    cover.appendChild(cta);

    const meta = el('div', { class: 'meta' }, '챕터 ' + (script.chapter || '?') + ' · ' + (script.meta && script.meta.duration_est ? script.meta.duration_est : '약 10~15분'));
    cover.appendChild(meta);

    // resume button if save exists
    const saved = loadSavedState(opts);
    if (saved && saved.phase && saved.phase !== 'cover') {
      const resume = el('button', { class: 'cta', type: 'button', style: 'margin-top:12px; background: rgba(255,255,255,0.12);' }, '이어 하기');
      resume.addEventListener('click', () => {
        Object.assign(state, saved);
        state.flags = new Set(Array.from(saved.flags || []));
        state.currentScene = getCurrentScene(script, state);
        render(ctx);
      });
      cover.appendChild(resume);
    }

    root.appendChild(cover);
  }

  function renderScene(ctx) {
    const { root, script, state, opts } = ctx;
    const scene = state.currentScene || getCurrentScene(script, state);
    if (!scene) {
      state.phase = 'ending';
      return render(ctx);
    }

    const sceneEl = el('div', { class: 'scene fade-in' });

    // bg-wrap: 16:9 image area + overlays
    const bgWrap = el('div', { class: 'bg-wrap' });
    if (scene.scene_asset) {
      const img = el('img', {
        class: 'bg-img',
        src: opts.assetsBase + scene.scene_asset + '.png',
        alt: scene.label || '',
      });
      bgWrap.appendChild(img);
    }
    bgWrap.appendChild(el('div', { class: 'bg-overlay' }));
    // status bar (overlay on top of bg)
    bgWrap.appendChild(renderStatusbar(script, state));
    // menu button (overlay)
    const menubar = el('div', { class: 'menubar' });
    const menuBtn = el('button', { type: 'button' }, '메뉴');
    menuBtn.addEventListener('click', () => {
      if (confirm('처음으로 돌아갈까요? (저장된 진행은 초기화됩니다)')) {
        clearSavedState(opts);
        Object.assign(state, makeState(script));
        state.phase = 'cover';
        render(ctx);
      }
    });
    menubar.appendChild(menuBtn);
    bgWrap.appendChild(menubar);
    // label (overlay at bottom)
    if (scene.label) bgWrap.appendChild(el('div', { class: 'scene-label' }, scene.label));
    sceneEl.appendChild(bgWrap);

    // dialog (below bg, natural flow)
    const dialog = el('div', { class: 'dialog' });

    // reply popup (post-choice) — inside dialog now
    if (state.replyText) {
      const rp = el('div', { class: 'reply-popup' });
      rp.textContent = (state.replyChar ? state.replyChar + ': ' : '') + state.replyText;
      dialog.appendChild(rp);
    }
    const speakerLabel = scene.speaker && scene.speaker !== 'narrator' ? scene.speaker : '·';
    const face = scene.face ? faceEmoji(script, scene.face) : '';
    const speaker = el('div', { class: 'speaker' });
    speaker.appendChild(el('span', { class: 'face' }, face));
    speaker.appendChild(document.createTextNode(' ' + speakerLabel));
    dialog.appendChild(speaker);
    dialog.appendChild(el('div', { class: 'text' }, scene.text || ''));

    // choices or next
    if (Array.isArray(scene.choices) && scene.choices.length > 0) {
      const choicesEl = el('div', { class: 'choices' });
      scene.choices.forEach((ch, i) => {
        const btn = el('button', { type: 'button', class: 'choice' });
        btn.textContent = ch.text || ('선택 ' + (i + 1));
        // requires_min_aff check
        let blocked = false;
        if (ch.requires_min_aff) {
          for (const k of Object.keys(ch.requires_min_aff)) {
            if ((state.affinity[k] || 0) < ch.requires_min_aff[k]) blocked = true;
          }
        }
        if (blocked) {
          btn.classList.add('disabled');
          btn.disabled = true;
          const lock = el('span', { class: 'lock' }, '🔒 호감도 부족');
          btn.appendChild(lock);
        } else {
          btn.addEventListener('click', () => {
            applyChoice(script, state, i);
            emitEvent(opts, 'choice_made', { scene_id: scene.id, choice_idx: i, flag: ch.flag });
            // route branch이면 advance가 이미 idx=-1로 세팅됨
            if (state.block === 'ending') {
              saveState(ctx);
              state.phase = 'ending';
              render(ctx);
              return;
            }
            const ok = advance(script, state);
            if (!ok && state.block === 'ending') {
              saveState(ctx);
              state.phase = 'ending';
              render(ctx);
              return;
            }
            state.currentScene = getCurrentScene(script, state);
            saveState(ctx);
            render(ctx);
            emitEvent(opts, 'scene_view', { scene_id: state.currentScene && state.currentScene.id });
          });
        }
        choicesEl.appendChild(btn);
      });
      dialog.appendChild(choicesEl);
    } else if (scene.next || true) {
      const nextBtn = el('button', { type: 'button', class: 'next-btn' }, '다음 →');
      nextBtn.addEventListener('click', () => {
        state.replyText = null;
        const ok = advance(script, state);
        if (!ok && state.block === 'ending') {
          saveState(ctx);
          state.phase = 'ending';
          render(ctx);
          return;
        }
        state.currentScene = getCurrentScene(script, state);
        saveState(ctx);
        render(ctx);
        emitEvent(opts, 'scene_view', { scene_id: state.currentScene && state.currentScene.id });
      });
      dialog.appendChild(nextBtn);
    }

    sceneEl.appendChild(dialog);
    root.appendChild(sceneEl);
  }

  function renderStatusbar(script, state) {
    const sb = el('div', { class: 'statusbar' });
    const chars = script.characters || {};
    for (const key of ['sea', 'harin', 'seoyeon', 'mirae']) {
      const c = chars[key] || {};
      const v = state.affinity[key] || 0;
      const pill = el('div', { class: 'aff-pill', 'data-c': key });
      pill.appendChild(el('div', { class: 'name' }, (c.name || key).slice(-2)));
      const bar = el('div', { class: 'bar' });
      const fill = el('div', { class: 'fill', style: 'width: ' + v + '%' });
      bar.appendChild(fill);
      pill.appendChild(bar);
      sb.appendChild(pill);
    }
    return sb;
  }

  function renderEnding(ctx) {
    const { root, script, state, opts } = ctx;
    const ending = selectEnding(script, state);
    const wrap = el('div', { class: 'ending fade-in' });
    if (ending) {
      wrap.appendChild(el('div', { class: 'tag' }, ending.tag || '엔딩'));
      wrap.appendChild(el('div', { class: 'mascot' }, ending.mascot || '🌸'));
      wrap.appendChild(el('h2', {}, ending.title || '엔딩'));
      wrap.appendChild(el('div', { class: 'body' }, ending.body || ''));

      // optional summary
      const sum = el('div', { class: 'summary' });
      const affLine = ['sea', 'harin', 'seoyeon', 'mirae']
        .map(k => ((script.characters && script.characters[k] && script.characters[k].name) || k) + ' ' + (state.affinity[k] || 0))
        .join(' · ');
      sum.textContent = '최종 호감도 — ' + affLine + (state.route ? ' · 루트: ' + state.route : '');
      wrap.appendChild(sum);

      emitEvent(opts, 'ending_reached', {
        ending_tag: ending.tag,
        route: state.route,
        aff_sea: state.affinity.sea,
        aff_harin: state.affinity.harin,
        aff_seoyeon: state.affinity.seoyeon,
        aff_mirae: state.affinity.mirae,
      });

      // mark cleared
      const ck = (script.game_config && script.game_config.cleared_localStorage_key) || ('ongle_' + script.chapter + '_cleared');
      try {
        const cleared = JSON.parse(localStorage.getItem(ck) || '[]');
        if (!cleared.includes(ending.tag)) cleared.push(ending.tag);
        localStorage.setItem(ck, JSON.stringify(cleared));
      } catch (e) {}
    } else {
      wrap.appendChild(el('h2', {}, '엔딩을 찾지 못했습니다'));
    }
    const actions = el('div', { class: 'actions' });
    const again = el('button', { type: 'button' }, '다시 하기');
    again.addEventListener('click', () => {
      clearSavedState(opts);
      Object.assign(state, makeState(script));
      state.phase = 'cover';
      render(ctx);
      emitEvent(opts, 'replay_started', {});
    });
    actions.appendChild(again);
    const home = el('button', { type: 'button', class: 'secondary' }, '시뮬 목록');
    home.addEventListener('click', () => {
      window.location.href = '/ongle/sim/list/';
    });
    actions.appendChild(home);
    wrap.appendChild(actions);

    root.appendChild(wrap);
  }

  function faceEmoji(script, key) {
    const fk = (script.face_keys || {})[key] || '';
    return (fk.split(' ')[0] || '');
  }

  // ---------- Save / Load ----------
  function saveState(ctx) {
    if (!ctx.opts.saveKey) return;
    try {
      const dump = Object.assign({}, ctx.state, {
        flags: Array.from(ctx.state.flags),
        currentScene: null,
      });
      localStorage.setItem(ctx.opts.saveKey, JSON.stringify(dump));
    } catch (e) {}
  }
  function loadSavedState(opts) {
    if (!opts.saveKey) return null;
    try {
      const raw = localStorage.getItem(opts.saveKey);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) { return null; }
  }
  function clearSavedState(opts) {
    if (!opts.saveKey) return;
    try { localStorage.removeItem(opts.saveKey); } catch (e) {}
  }

  // ---------- Analytics ----------
  function emitEvent(opts, name, params) {
    try {
      if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    } catch (e) {}
  }

  // ---------- DOM helpers ----------
  function el(tag, attrs, text) {
    const e = document.createElement(tag);
    if (attrs) for (const k of Object.keys(attrs)) {
      if (k === 'class') e.className = attrs[k];
      else if (k === 'style') e.setAttribute('style', attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    if (text !== undefined && text !== null) e.appendChild(document.createTextNode(text));
    return e;
  }

  // ---------- Public mount ----------
  function mount(opts) {
    const root = typeof opts.root === 'string' ? document.querySelector(opts.root) : opts.root;
    if (!root) { console.error('[OngleSimV2] root not found'); return; }
    const finalOpts = Object.assign({
      assetsBase: 'scenes/',
      characterSheetBase: 'character_sheets/',
      saveKey: null,
    }, opts);
    fetch(opts.scriptUrl, { cache: 'no-cache' })
      .then(r => r.json())
      .then(script => {
        const state = makeState(script);
        const ctx = { root, script, state, opts: finalOpts };
        state.currentScene = getCurrentScene(script, state);
        render(ctx);
      })
      .catch(err => {
        console.error('[OngleSimV2] script load failed', err);
        root.innerHTML = '<div style="padding:24px;color:#fff;text-align:center;">시뮬을 불러오지 못했습니다.<br>잠시 후 다시 시도해 주세요.</div>';
      });
  }

  global.OngleSimV2 = { mount: mount, evalTrigger: evalTrigger };
})(window);
