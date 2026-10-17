// Flow sahifasida: await (0,eval)(await fetch(RAW+'tools/flow_helper.js').then(r=>r.text())); await initFlow(SHA)
window.initFlow = async (sha) => {
  const raw = `https://raw.githubusercontent.com/safarovman/xabash.reels/${sha}/jobs/`;
  const a = await fetch(raw + 'flow_2026-10-18.json').then(r => r.json());
  const b = await fetch(raw + 'flow_v2_2026-10-18.json').then(r => r.json());
  window.P = a; for (const j in b) { P[j] = P[j] || {}; Object.assign(P[j], b[j]); }
  window.M = JSON.parse(localStorage.getItem('xabM') || '{}');
  window.S = JSON.parse(localStorage.getItem('xabS') || '[]');
  window.U = JSON.parse(localStorage.getItem('xabU') || '{}');
  window.QL = []; for (const j of Object.keys(P)) for (const k of Object.keys(P[j])) if (!P[j][k].ref) QL.push(j + '/' + k);
  return { jobs: Object.keys(P).length, QL: QL.length, S: S.length, M: Object.keys(M).length };
};
window.save = () => { localStorage.setItem('xabM', JSON.stringify(M)); localStorage.setItem('xabS', JSON.stringify(S)); localStorage.setItem('xabU', JSON.stringify(U)); };
window.ed = () => document.querySelector('[contenteditable=true]');
window.fillP = (job, key) => { const d = ed(); d.focus(); document.execCommand('selectAll'); document.execCommand('delete'); document.execCommand('insertText', false, P[job][key].prompt); return d.innerText.length; };
window.fillNext = () => { const done = new Set([...S, ...Object.keys(M)]); const nk = QL.find(x => !done.has(x)); if (!nk) return 'DONE'; const [j, k] = nk.split('/'); fillP(j, k); S.push(nk); save(); return nk; };
window.ORD = () => ['2026-10-18_0800_pult/c_dada.jpg', ...S];
window.grabU = () => { document.querySelectorAll('img[data-media-id]').forEach(i => U[i.dataset.mediaId] = i.src); save(); return Object.keys(U).length; };
window.topAll = () => { document.querySelectorAll('*').forEach(e => { if (e.scrollTop > 0) e.scrollTop = 0; }); };
window.assign = () => { topAll(); const t = [...document.querySelectorAll('flow-grid-tile-container')]; const o = ORD(); const n = o.length; let added = 0, pend = 0, err = 0, bad = []; t.forEach((el, i) => { const key = o[n - 1 - i]; const im = el.querySelector('img[data-media-id]'); if (im) { if (!M[key]) { M[key] = im.dataset.mediaId; added++; } else if (M[key] != im.dataset.mediaId) bad.push(key); } else { if (/%/.test(el.innerText)) pend++; else { err++; } } }); grabU(); save(); return { tiles: t.length, n, added, pend, err, bad: bad.slice(0, 5), mapped: Object.keys(M).length }; };
window.errKeys = () => { topAll(); const t = [...document.querySelectorAll('flow-grid-tile-container')]; const o = ORD(); const n = o.length; return t.map((el, i) => [o[n - 1 - i], !!el.querySelector('img[data-media-id]'), /%/.test(el.innerText)]).filter(x => !x[1] && !x[2]).map(x => x[0]); };
window.refPos = (key) => { const [j, k] = key.split('/'); const rid = M[j + '/' + P[j][k].ref]; if (!rid) return 'NOREF'; const im = document.querySelector(`img[data-media-id="${rid}"]`); if (!im) return 'NOTILE'; im.scrollIntoView({ block: 'center' }); const r = im.getBoundingClientRect(); const s = 800 / innerWidth; return [Math.round((r.left + r.width / 2) * s), Math.round((r.top + r.height / 2) * s)]; };
window.addMenu = () => { const it = [...document.querySelectorAll('[role=menuitem], button')].find(e => /Добавить в запрос/.test(e.innerText)); if (!it) return 'NOMENU'; it.click(); return 'ok'; };
window.fillRef = (key) => { const [j, k] = key.split('/'); const d = ed(); d.focus(); document.execCommand('insertText', false, P[j][k].prompt); S.push(key); save(); return d.innerText.length; };
window.nextRef = () => { const done = new Set([...S, ...Object.keys(M)]); for (const j of Object.keys(P)) for (const k of Object.keys(P[j])) { const key = j + '/' + k; if (P[j][k].ref && !done.has(key) && M[j + '/' + P[j][k].ref]) return key; } return 'NONE'; };
window.pack = async (job, name) => { grabU(); const keys = Object.keys(P[job]).map(k => job + '/' + k).filter(k => M[k] && U[M[k]]); const parts = [], idx = []; for (const k of keys) { const r = await fetch(U[M[k]]); if (!r.ok) continue; const b = new Uint8Array(await r.arrayBuffer()); parts.push(b); idx.push([k.split('/')[1], b.length, M[k]]); } const hj = new TextEncoder().encode(JSON.stringify(idx)); const h = new Uint8Array(4); new DataView(h.buffer).setUint32(0, hj.length); const blob = new Blob([h, hj, ...parts]); const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); return [idx.length, Object.keys(P[job]).length, blob.size]; };
window.missing = (job) => Object.keys(P[job]).filter(k => !M[job + '/' + k]);
