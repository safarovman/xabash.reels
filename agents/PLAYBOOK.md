# Tez va tejamkor ish tartibi (limitni kam sarflash uchun)

Bu tartib bilan 3 video ~2 soatda, ozgina token bilan tayyor bo'ladi. Har qadamni qaytadan "kashf qilmang".

## Tejash qoidalari
- **Skrinshot kam oling.** Har skrinshot qimmat. Flow'da hamma ishni `tools/fast_flow.js` dagi JS bilan qiling; skrinshot faqat birinchi marta tugma joyini topish uchun (0.5 masshtab).
- **Katta natijalarni kontekstga o'qimang.** ElevenLabs `get_flow_run_status` ni 20 ta session_id bilan chaqiring — natija faylga saqlanadi, uni `python3`/`jq` bilan o'qing.
- **Bir nechta amalni bitta chaqiruvda bajaring:** `browser_batch` (fill → click → wait ×3 → collect), bir xabarda 5–6 ta parallel TTS chaqiruvi.
- **Fayllarni to'liq o'qimang** — kerakli qismini `head`/`python -c` bilan.
- **Render fonda:** `run_in_background`, timeout 7200000, natijani kutib boshqa ish qiling. Bir vaqtda bitta engine.
- **Tekshiruv — bitta kontakt varaq** (`ffmpeg -vf fps=1/7,scale=216:-1,tile=8x2`), har kadrni alohida emas.
- Sabab topmasdan qayta-qayta urinmang; xato bo'lsa bir marta tuzating.

## Qadamlar (bitta job uchun)
1. **Ssenariy:** `tools/examples/lines_example.py` namunasidek ro'yxat (ovoz, tts, matn, speaker). Raqamlar tts'da so'z bilan.
2. **Ovoz:** har qatorga `creative_generate_speech` (flow O1Xu6Si8vMxJc7g9SnrC, eleven_v4, generations_count 1). session_id'larni darhol JSON faylga yozing.
3. **Audio yuklash:** status faylidan URL'larni olib `[[job/vo_01.mp3, url],...]` qilib media tarmog'iga `tmp/*.json` push → storage.googleapis.com tabida `fast_flow.js` ni yuklab `await packUrls(sha,'tmp/x.json','aud.bin')` → `device_list_dir C:\Users\user\Downloads` → `device_stage_files` → `python3 tools/unpack.py /mnt/user-data/uploads/Downloads/<fayl>.tmp`.
4. **Rasmlar:** `images.json` (12 fon + 2 personaj, bitta uslub prefiksi) → `[[job/01.jpg, prompt],...]` ni tmp ga push → Flow tabida `(0,eval)(await fetch(RAW+'tools/fast_flow.js').then(r=>r.text())); await initFast(sha,'tmp/p.json')` → har batch: `fillN()`, strelka (494,559), wait 2 — 3 marta, so'ng ~25 s kutib `await collect(6)` → hammasi "ok" bo'lgach `await packJob(job,'img.bin')` → unpack.
5. **scenes.json:** `tools/examples/build_scenes_example.py` dagi `build()` bilan (ankerlarni avtomatik tekshiradi). Proplar `jobs/*/img/p_g_*.jpg` dan — nomiga ishonmang, rasmini ko'ring (p_g_koz aslida telefon!).
6. **Render → kontakt varaq → media push → curl 200 → Buffer create_post → post.json + topics_log → git pull --rebase, push.**
