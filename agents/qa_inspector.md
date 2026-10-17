# Tekshiruvchi agent (QA) — tayyor videoni OXIRIDA to'liq tekshiradi, Buffer'ga qo'yishdan OLDIN
Egasi (17-okt): "video oxirida olib, mazmunini, gaplarni to'liq tekshirsin — ElevenLabs xato qilmaganmi; rasmlar va imo-ishoralar vaqti to'g'rimi."
Natija `jobs/<job>/qa_report.json`; **"pass": false bo'lsa video Buffer'ga QO'YILMAYDI** — xato tuzatilib, qayta render qilinadi (ko'pi bilan 2 marta; yana o'tmasa egasiga ayting).

## 1. Ovoz — gaplar to'g'ri aytilganmi (ElevenLabs xatolari)
1. `ffmpeg -i out/video.mp4 -vn -ac 1 -b:a 96k out/qa_audio.mp3` → `media` tarmog'iga `tmp/qa/<job>.mp3` qilib push qiling.
2. ElevenLabs: `creative_attach_reference_file` (raw.githubusercontent URL) → `creative_transcribe_audio` (`eleven_scribe_v1`, `connect_from` = qaytgan node) → `creative_get_flow_run_status` dan matn va so'z vaqtlari.
3. Har sahna uchun (`out/timing.json` starts/scene_len oralig'idagi so'zlar) `scenes.json → text` bilan solishtiring (apostrof va katta-kichik harfni hisobga olmay). Belgilang:
   - tushib qolgan / qo'shilgan / buzilgan so'zlar, noto'g'ri raqam yoki ism, inglizcha talaffuz, bir xil bo'g'inning takrorlanishi, kesilib qolgan oxiri;
   - so'z mosligi < 90% bo'lgan sahna = XATO → o'sha qatorni qayta yozdiring (matnni biroz soddalashtirib), aud/vo_NN.mp3 ni almashtirib, qayta render.
   - Hissiyot teglari ([laughs] va h.k.) so'z bo'lib o'qilib qolgan bo'lsa — XATO.
4. Ovoz balandligi: `ffmpeg -af ebur128` — har sahna ovozi -19…-13 LUFS; musiqa ovozni bosmasin; 1 soniyadan uzun jimlik yo'q (oxiridagi muqovadan tashqari).

## 2. Rasm va imo-ishoralar vaqti
1. `python3 reel/engine.py jobs/<job> --qa` → `out/qa/sheet_*.jpg` (har element paydo bo'lgandan 0.45 s keyingi kadr, yorliq bilan) va `out/qa/elements.json`.
2. Har varaqni ko'ring (Read) va tekshiring:
   - kadr shu paytda aytilayotgan gapga mosmi (masalan "budilnik" deganda budilnik ko'rinadimi);
   - `mark` doira/strelka to'g'ri narsani ko'rsatyaptimi, kadr almashganda eski belgi qolib ketmaganmi;
   - stiker va pufakchalar yuzni, asosiy narsani yoki bir-birini yopmaydi; yozuvlar ekrandan chiqmaydi va o'qiladi; shriftda yo'q belgi (□) yo'q;
   - bo'sh/qora kadr, cho'zilgan yoki xira rasm yo'q; bir personaj hamma rasmda bir xil ko'rinadi;
   - muqova (`MUQOVA`) toza, sarlavha o'qiladi.
3. Xato bo'lsa `scenes.json` dagi `x/y/at/out/h` ni tuzating va qayta render.

## 3. Mazmun va ushlab qolish
- Boshidagi ilmoqda va'da qilingan ma'lumot/javob videoning OXIRGI 20% qismida beriladi (o'rtada emas) — `agents/hook_director.md` → "Javobni oxiriga". Aks holda — ssenariy XATO.
- Davomiylik ≥ 70 s; har 8-12 s da qayta ilmoq bor; yakuniy savol ochiq (1-2-3 ovoz berish yo'q); faktlar `card` da manbasi bilan.
- Caption: 1 ilmoq + 1 ochiq savol + 6-8 heshteg.

## Natija: `jobs/<job>/qa_report.json`
```json
{"pass": true, "audio": [{"scene": 4, "match": 0.97, "issues": []}], "visual": [{"t": 18.4, "issue": "stiker yuzni yopyapti", "fixed": true}],
 "structure": {"hook_payoff_at": 0.86, "rehooks": 3, "duration": 78.2}, "rerenders": 1}
```
Video yig'uvchi `post.json → status` ga "QA o'tdi" yozadi; keyin `tmp/qa/` ni media tarmog'idan o'chiradi.
