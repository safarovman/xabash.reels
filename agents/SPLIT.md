# Ikki akkaunt o'rtasida ish taqsimoti (egasi, 2026-10-22)

Sahifa bitta: Instagram **xabash.jonkam** (Buffer kanali 6acf32c0778b240e2f04fcdf). Mavzu: **faqat tarix**.

| Akkaunt | Slotlar (Toshkent) | Job papka nomi |
|---|---|---|
| **A** — 1-Claude (shu repo egasi bilan ishlaydigan asosiy sessiya) | **08:00, 10:30, 12:30** | `jobs/<sana>_0800_*`, `_1030_*`, `_1230_*` |
| **B** — 2-Claude akkaunt | **14:30, 16:30, 18:30** | `jobs/<sana>_1430_*`, `_1630_*`, `_1830_*` |

## Qoidalar (ikkalasi uchun)
1. Faqat **o'z slotlaringiz**ga video yasang va Buffer'ga qo'ying. Boshqa akkauntning postlariga, job papkalariga va media fayllariga tegmang.
2. Mavzu tanlashdan oldin `topics_log.md` va `plan_<sana>.md` ni o'qing — ikkinchi akkaunt o'sha kuni olgan mavzuni takrorlamang. Mavzu tanlangan zahoti `plan_<sana>.md` ga o'z bo'limingizga yozib, push qiling (A — "## A (08:00–12:30)", B — "## B (14:30–18:30)").
3. Ilmoq va o'tish gaplari har videoda boshqacha (`agents/hook_director.md`). Faktlar 2–3 manbadan; taxmin va rivoyat shunday deb aytiladi.
4. Git: push'dan oldin har doim `git pull --rebase`. Media: `media` tarmog'i, `<sana>/<HHMM>_<slug>.mp4`.
5. Buffer: `schedulingType: automatic`, Reels, `shouldShareToFeed: true`, `isAiGenerated: true`. Parol kiritilmaydi.
6. Tugagach `topics_log.md` ga qator qo'shing va egasiga qisqa xabar yozing.
