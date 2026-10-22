// Google Flow tabida bir marta ishga tushiring: PQ (prompt ro'yxati) yuklanadi va yordamchilar paydo bo'ladi.
// Ishlatish: await initFast('<media commit sha>','tmp/prompts.json')  -> [[ "job/01.jpg", "prompt" ], ...]
window.initFast = async (sha, path) => {
  window.PQ = await fetch(`https://raw.githubusercontent.com/safarovman/xabash.reels/${sha}/${path}`).then(r => r.json());
  window.PI = 0; window.SUB = []; window.MM = window.MM || {}; return PQ.length;
};
// Keyingi promptni maydonga yozadi (keyin yuborish strelkasini bosing)
window.fillN = () => { const d = document.querySelector('[contenteditable=true]'); d.focus(); document.execCommand('selectAll'); document.execCommand('delete'); document.execCommand('insertText', false, PQ[PI][1]); SUB.push(PQ[PI][0]); PI++; return [PI, d.innerText.length]; };
// Tepadagi k ta plitkani oxirgi k ta yuborilgan kalitga moslaydi (eng yangisi birinchi)
window.collect = async (k) => { document.querySelectorAll('*').forEach(e => { if (e.scrollTop > 0) e.scrollTop = 0; }); await new Promise(r => setTimeout(r, 1200));
  const t = [...document.querySelectorAll('flow-grid-tile-container')]; const n = SUB.length; const res = [];
  for (let i = 0; i < k && i < n; i++) { const im = t[i].querySelector('img[data-media-id]'); const key = SUB[n - 1 - i];
    if (im) { MM[key] = im.src; res.push([key, 'ok']); } else res.push([key, /%/.test(t[i].innerText) ? 'pend' : 'ERR']); }
  return [Object.keys(MM).length, res]; };
// Bitta job rasmlarini bitta fayl qilib yuklab oladi (tools/unpack.py bilan oching)
window.packJob = async (job, name) => { const keys = Object.keys(MM).filter(k => k.startsWith(job)); const parts = [], idx = [], bad = [];
  for (const k of keys) { const r = await fetch(MM[k]); if (!r.ok) { bad.push(k); continue; } const b = new Uint8Array(await r.arrayBuffer()); parts.push(b); idx.push([k, b.length]); }
  return window.dl(parts, idx, name, bad); };
// URL ro'yxatini (masalan ElevenLabs audio) bitta fayl qilib yuklab oladi: [[ "job/vo_01.mp3", url ], ...]
window.packUrls = async (sha, path, name) => { const L = await fetch(`https://raw.githubusercontent.com/safarovman/xabash.reels/${sha}/${path}`).then(r => r.json()); const parts = [], idx = [], bad = [];
  for (const [k, u] of L) { try { const r = await fetch(u); if (!r.ok) { bad.push([k, r.status]); continue; } const b = new Uint8Array(await r.arrayBuffer()); parts.push(b); idx.push([k, b.length]); } catch (e) { bad.push([k, String(e)]); } }
  return window.dl(parts, idx, name, bad); };
window.dl = (parts, idx, name, bad) => { const hj = new TextEncoder().encode(JSON.stringify(idx)); const h = new Uint8Array(4); new DataView(h.buffer).setUint32(0, hj.length);
  const blob = new Blob([h, hj, ...parts]); const a = document.createElementNS('http://www.w3.org/1999/xhtml', 'a'); a.href = URL.createObjectURL(blob); a.download = name;
  (document.body || document.documentElement).appendChild(a); a.click(); a.remove(); return [idx.length, bad, blob.size]; };
