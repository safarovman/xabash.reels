# Agentlar (2026-10-16, egasi so'radi)
Har video mutaxassis agentlar + 1 yig'uvchi bilan yasaladi. Asosiy (rejalashtirilgan) sessiya mavzu tasdiqlangach
har bir video uchun avval ilmoq agentini (ssenariy), so'ng **Agent tool** bilan uslub, musiqa, imo-ishora agentlarini PARALLEL ishga tushiradi (general-purpose, prompt: "Repo /home/claude/xabash.reels.
agents/<fayl>.md ni o'qib, unga amal qil. Video: <slot, mavzu, ssenariy qisqacha, job papka>"). Har agent o'z natijasini job papkasiga JSON qilib yozadi,
keyin asosiy sessiya (video yig'uvchi) shular asosida `scenes.json`, Flow promptlari va renderni qiladi.

| agent | fayl | nima qiladi | natija |
|---|---|---|---|
| Mavzu | topic_scout.md | 19:00 da 5 ta mavzu (xabash-topics skill) | egasiga xabar, topics_log.md |
| Uslub | style_director.md | mavzuga mos RASM USLUBI, shrift, palitra, o'tishlar | jobs/<job>/brief_style.json |
| Musiqa | music_director.md | mavzuga mos janr, kayfiyatlar xaritasi, tonallik | jobs/<job>/brief_music.json |
| Ilmoq (stop-time) | hook_director.md | ssenariyga ilmoq, re-hook, izohga chorlovchi yakuniy savol (ovozdan oldin) | jobs/<job>/brief_hooks.json |
| Tarix | history_scout.md | 10:30 jahon va 14:30 O'zbekiston tarixi mavzulari, faktlar, xarita bilan tasvirlash | mavzu + ssenariy qoidalari |
| Imo-ishora | gesture_director.md | ko'rsatgich, strelka, doira, eslatma, reaksiya belgilari | jobs/<job>/brief_gestures.json |
| Tekshiruvchi (QA) | qa_inspector.md | render'dan keyin: ovozni transkripsiya qilib matn bilan solishtiradi, rasm/imo-ishora vaqtlari (engine --qa), tuzilish | jobs/<job>/qa_report.json — xatoning aniq joyi va tuzatish ko'rsatmasi; yig'uvchi o'sha joyni tuzatadi, video tashlanmaydi |
| Video yig'uvchi | (asosiy sessiya, xabash-reel-maker) | ssenariy + 3 brief → scenes.json, Flow, ovoz, render | out/video.mp4 |

Agentlar ham bir-biridan va oxirgi videolardan farq qilishi uchun `topics_log.md` dagi `uslub`, `musiqa`, `shrift` ustunlarini o'qiydi.
