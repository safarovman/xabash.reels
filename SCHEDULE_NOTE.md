# Jadval kelishuvi (boshqa sessiyalar uchun)
2026-10-16 — 5 ta slot ham Buffer'da (hammasi automatic, shouldShareToFeed true):
- 08:00 Xating hali pochtada (6ad0a5066742034cc4e7b95c)
- 12:30 Dadam o'yinga qo'shildi (6ad0a97802a4f4f292316de4)
- 16:00 Robotaksi bilan savdolashish (6ad0ab82b324123738c6075b)
- 18:30 Nahor oshi (6ad0fc2843886cbb07532faa)
- 21:00 Har kecha 100% gacha zaryad (6ad0fc2b00e152e7cd1ba82c)

2026-10-17 — 5 ta video TAYYOR (media/2026-10-17/*.mp4, egasi tasdiqlagan), lekin Buffer'ga hali QO'YILMAGAN
(24 soat qoidasi). 16-okt 19:00 dagi run ularni list_posts bilan tekshirib, jobs/2026-10-17_*/post.json dagi
caption + video_url + thumbnailOffset bilan automatic qilib qo'ysin; keyin 18-okt mavzularini taklif qilsin.
- 08:00 kasseta · 12:30 texnikum (egasining hikoyasi) · 16:00 mars-kechikish (2061) · 18:30 askiya · 21:00 koz-charchoq
- 16-okt 14:00-16:30: ovozsiz qatorlar (0800 #6,#9 · 1830 #3,#9 · 2100 #2,#8) YANGI ElevenLabs akkaunti bilan yozildi, 3 video qayta render qilinib media'da almashtirildi; post.json thumbnailOffset yangilandi. Endi 5 tasi ham to'liq ovozli.
  Rasmlar+ovozlar: media/2026-10-17/assets_1017.tar (repo ildizida tar -xf).

## 2026-10-15 18:35 — OVOZLAR (keyingi postlardan)
O'zbekcha matnga ingliz ovozlari (Sarah, Charlie, Bill, Lily, Jessica) ISHLATILMAYDI — past va tushunarsiz. Kasting: config.json → elevenlabs.cast (hikoyachi doim Bekzod). Har qatorda eleven_v4 hissiyot teglari. ElevenLabs flow: qGgjoCYEgz4zhvjl3GCQ (16-okt yangi akkaunt). Dvigatel ovozlarni -16 LUFS ga tenglaydi.

## 2026-10-16 19:00 run
- 17-okt Buffer: 08:00 6ad22d1c · 12:30 6ad22d21 · 16:00 6ad22d24 · 18:30 6ad22d27 (automatic, shouldShareToFeed). 21:00 koz-charchoq hali QO'YILMAGAN (24 soat oynasi) — 16-okt 21:00 dan keyin yoki 17-okt 19:00 run qo'ysin (jobs/2026-10-17_2100_koz-charchoq/post.json).
- 18-okt mavzulari egasiga taklif qilindi (19:00): pult · bepul-sinov · ai-muzlatkich · non-odobi · yuzga-qol.

## 2026-10-18 22:20 — egasi: "bugun qo'yilmagan videolarni ertangi shu vaqtlarga qo'y"
18-okt 08:00 pult, 10:30 gitler, 12:30 bepul — Buffer'da JOYLANDI (sent).
14:30 anqara, 16:00 muzlatkich, 18:30 non-odobi, 21:00 yuzga-qol yasalib ulgurmadi → 19-okt 14:30/16:00/18:30/21:00 ga ko'chirildi (post.json dueAt).
Bloklar: (1) egasining kompyuteri ulanmagan — Google Flow rasmlari va ElevenLabs mp3 yuklab olish imkonsiz; (2) ElevenLabs kreditlari 18-okt tunda tugagan (anqara 7/10 qator, muz qisman).
Avvalgi konteynerdagi rasm/ovoz fayllari yo'qolgan (repo'da yo'q) — kompyuter ulanganda Flow'dan qayta yig'ish kerak. 19-okt 08:00/10:30/12:30 uchun video yo'q.

## 19-okt (03:05 holati)
- Buffer'da: 14:30 anqara (6ad54213), 16:00 ai-muzlatkich (6ad54216), 18:30 non-odobi (6ad52a45), 21:00 yuzga-qol (6ad54219) — hammasi automatic, reel.
- Egasi so'rovi: 08:00 (o'tmish), 10:30 (jahon tarixi), 12:30 (hozirgi zamon) — ketma-ket yasalyapti.
- ElevenLabs kredit ~520 qoldi — yangi ovozlar uchun boshqa akkaunt kerak.

## 19-okt kunduzi
- 13:20 «Yiliga 36 kun» (Buffer 6ad5d13a). Egasi bugungi 5 ta video uchun yangi hook'li nusxalarni o'zi sinov (trial) rejimida joylaydi — jobs/*_hook; Buffer'dagilar o'zgarmadi.
- 20-okt: 08:00 «36 ta kadr» (6ad5e94a), 10:30 «Napoleon pakana emasdi» (6ad5edf3).
- ElevenLabs: yangi akkaunt, flow O1Xu6Si8vMxJc7g9SnrC.
