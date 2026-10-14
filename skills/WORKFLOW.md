# xabash.reels — to'liq ish tartibi (skill'lar saqlanmagan bo'lsa ham shu yetarli)

## 1. Mavzular (xabash-topics)
- `topics_log.md` dagi so'nggi 30 kun mavzularini takrorlamang.
- Har kuni 4 ta: **00:00** tun (telefon, uyqusizlik), **06:00** ertalab (nonushta, choy, ishga tayyorlanish), **12:00** tush (tushlik, ish, pul, tirbandlik), **18:00** kechqurun (oila, mehmon, to'y, qo'shnilar).
- O'zbekona, hajviy-ijtimoiy, bitta tanish odat/paradoks atrofida. Siyosat, din, millat masxarasi yo'q.
- Har biriga WebSearch bilan tekshirilgan 1 ta fakt. Topilmasa — mavzuni almashtiring, uydirma raqam yo'q.
- Egasiga SendUserMessage: har bir vaqt uchun nom, ilmoq jumla, g'oya, fakt manbasi. "hammasi ok" yoki almashtirishni so'rang.
- **Tasdiqsiz hech narsa yasamang va joylamang.**

## 2. Video (xabash-reel-maker)
Papka: `jobs/<YYYY-MM-DD>_<HHMM>_<slug>/` → `scenes.json`, `img/NN.jpg`, `aud/vo_NN.mp3`. Format: `SCHEMA.md`, namuna: `jobs/2026-10-14_ertadan/scenes.json`.
- **Ssenariy 8–9 sahna, 45–60 s:** 1 epik ilmoq + raqam + shtamp (hero) → 2 teskari burilish bitta jumla (sad) → 3–6 kundalik haqiqat: soat, stikerlar, ikkinchi shtamp (groove) → 7 ilmiy fakt `card` (mystery) → 8 kontrast + `big` hisob (warm) → 9 xulosa + `final` savol (finale). Ovoz matni sodda, raqamlar so'z bilan.
- **Rasmlar — Google Flow**, egasining kompyuteridagi ichki brauzerda (`anthropic-skills:built-in-browser` skill'ini o'qing). flow.google.com → yangi loyiha → Image, 9:16, x1, Nano Banana. Prompt boshiga `config.json` → `style.image_prefix`. 1-rasm qahramon; qolgan qahramonli sahnalarda **+** → qahramon rasmini namuna qilib qo'shing, prompt "Same man as in the reference image (...)". Yuklab olish: JS `fetch(img[src*=flow-content])` → `<a download>` → Downloads `.tmp` → `device_list_dir` (hajm bo'yicha moslash) → `device_stage_files` → `/mnt/user-data/uploads/Downloads/`.
- **Ovoz — ElevenLabs:** `creative_create_flow`, har sahnaga `creative_generate_speech` (voice `kGOig3GPePLxobJGHo2M`, `eleven_v4`, `generations_count: 1`, qayta urinmaslik). URL'lar storage.googleapis.com da — konteyner ololmaydi: ichki brauzerda bitta URL ni `preview_start` bilan oching, o'sha tabda JS bilan hammasini fetch → download → stage.
- **Render:** `pip install --break-system-packages pyfluidsynth opencv-python-headless pillow numpy` → `python3 reel/engine.py jobs/<job> --auto-preview` (`out/preview/sheet.jpg` ni ko'ring, yuz to'silmasin) → `python3 reel/engine.py jobs/<job>` (~7 daq). Natija `out/video.mp4` (max sifat, <95 MB), `out/cover.jpg`, `out/timing.json`.
- **Caption** `post.json` ga: ilmoq + 2–3 qator + savol + 12–15 heshteg (#ozbekcha #uzbekistan #toshkent #reels #reelsuzbekistan + mavzuga oid).

## 3. Joylash (xabash-publish)
- Releases yopiq → `media` tarmog'i: `git fetch --depth 1 origin media && git worktree add /tmp/media origin/media -B media`, faylni `/tmp/media/<date>/<HHMM>_<slug>.mp4` ga, commit, `git push origin media`. Havola: `https://raw.githubusercontent.com/safarovman/xabash.reels/media/<date>/<HHMM>_<slug>.mp4` (curl -sIL bilan 200).
- Buffer `create_post`: channelId `6acf32c0778b240e2f04fcdf`, `schedulingType: automatic`, `mode: customScheduled`, `dueAt: <date>T<HH:MM>:00+05:00` (kelajakda bo'lsin — `get_account.currentTime`), assets video url + `thumbnailOffset` = `timing.json` `cover_ms`, metadata `instagram: {type: reel, shouldShareToFeed: true, isAiGenerated: true}`.
- Bepul Buffer: bir vaqtda 10 ta rejalashtirilgan post limiti.
- `get_post` bilan holatni tekshiring, `post.json` va `topics_log.md` ni yangilab `main` ga push qiling, egasiga jadval yuboring.
- 14 kundan eski, `sent` bo'lgan media papkalarini tozalang.

## To'xtash
Kompyuter/brauzer ulanmasa, ElevenLabs bloki yoki kredit tugashi, Flow limiti, push rad etilishi — takrorlamang, egasiga sabab va yechimni ayting. Parol hech qachon kiritilmaydi.
