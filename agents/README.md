# Agentlar (2026-10-16, egasi so'radi)
Har video 4 ta mutaxassis agent + 1 yig'uvchi bilan yasaladi. Asosiy (rejalashtirilgan) sessiya mavzu tasdiqlangach
har bir video uchun **Agent tool** bilan uchta agentni PARALLEL ishga tushiradi (general-purpose, prompt: "Repo /home/claude/xabash.reels.
agents/<fayl>.md ni o'qib, unga amal qil. Video: <slot, mavzu, ssenariy qisqacha, job papka>"). Har agent o'z natijasini job papkasiga JSON qilib yozadi,
keyin asosiy sessiya (video yig'uvchi) shular asosida `scenes.json`, Flow promptlari va renderni qiladi.

| agent | fayl | nima qiladi | natija |
|---|---|---|---|
| Mavzu | topic_scout.md | 19:00 da 5 ta mavzu (xabash-topics skill) | egasiga xabar, topics_log.md |
| Uslub | style_director.md | mavzuga mos RASM USLUBI, shrift, palitra, o'tishlar | jobs/<job>/brief_style.json |
| Musiqa | music_director.md | mavzuga mos janr, kayfiyatlar xaritasi, tonallik | jobs/<job>/brief_music.json |
| Imo-ishora | gesture_director.md | ko'rsatgich, strelka, doira, eslatma, reaksiya belgilari | jobs/<job>/brief_gestures.json |
| Video yig'uvchi | (asosiy sessiya, xabash-reel-maker) | ssenariy + 3 brief → scenes.json, Flow, ovoz, render | out/video.mp4 |

Agentlar ham bir-biridan va oxirgi videolardan farq qilishi uchun `topics_log.md` dagi `uslub`, `musiqa`, `shrift` ustunlarini o'qiydi.
