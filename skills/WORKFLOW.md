# xabash.reels — to'liq ish tartibi (skill'lar saqlanmagan bo'lsa ham shu yetarli)

## 0c. TEZ, RASMLARI KO'P, AGENTLI VIDEO (2026-10-16, egasi — eng ustun)
- **Egasi tasdiqlagan namuna**: `media/test/tez_sinov_2026-10-16.mp4` ("juda yaxshi chiqibdi, bundan keyin shunday qilsin"). Hamma videolar shu tezlik va uslubda.
- **Davomiylik**: kamida 70 soniya; aniq uzunlikni mavzuga qarab o'zingiz tanlang. Ma'lumotlar zo'r va qiziqarli: 2-3 ta tekshirilgan fakt, hazil bilan.
- **ElevenLabs akkaunti almashtirildi**: yangi flow `qGgjoCYEgz4zhvjl3GCQ` (`config.json → elevenlabs.flow_id`). Eski flow'lar ishlatilmaydi. O'zbek ovozlari va kasting o'sha-o'sha.
- **Agentlar** (`agents/README.md`): mavzu tasdiqlangach har video uchun **Agent tool** bilan uslub (`style_director.md`), musiqa (`music_director.md`), imo-ishora (`gesture_director.md`) agentlarini parallel ishga tushiring; ular `brief_*.json` yozadi; siz (video yig'uvchi) shular asosida `scenes.json` qilasiz.
- **Rasm uslubi mavzuga qarab o'zgaradi** — hamma Flow promptlarida `brief_style.json` dagi prefikslar (config'dagi `style.*` faqat zaxira). Shrift/palitra ham shu briefdan. `topics_log.md` ga `uslub`, `shrift`, `musiqa` ustunlarini yozing.
- **Tezlik**: `"pace": "fast"` (qisqa pauzalar, gap boshida kamera turtkisi, tez kirish, whip/zoom/flash/slide o'tishlar). Har 1.5-2 soniyada ekranda yangi narsa. Sekin aylanadigan harakat (`spin`, sekin `float`) ishlatmang — `point`, `pulse`, `jump`, `wag`, `bounce`, `shake`.
- **Rasmlar ko'p (20-30 ta)**: har sahnada 2-3 kadr — `imgs: ["05b.jpg", ["05c.jpg", "ibora"], {"img": "05d.jpg", "fx": "flash"}]`; boshqa burchak, yaqin plan, reaksiya kadri, detal. Hammasi Flow'da, bitta uslubda, personaj namuna (ingredient) qilib.
- **Imo-ishoralar 15-25 ta**: `mark` (circle/arrow/underline/check/cross/burst/box + `label` qo'lyozma eslatma) va Flow'dan `p_g_*.jpg` ko'rsatgich/eslatma/reaksiya stikerlari (`prop` + `motion`). Kutubxona: `assets/gestures/`.
- **Musiqa mavzuga qarab**: `scenes.json → "music": {"genre": ..., "bpm": ..., "key": ..., "scale": ...}` (janrlar `reel/music.py` GENRES), oxirgi 3 videoda takrorlanmaydi; har videoda yangi `music_seed`. Egasi bergan trek: `"music": {"file": "music.mp3"}`.

## 0a. TRIAL REEL YO'Q (2026-10-15)
- Trial reel qilinmaydi. Hamma video, 16:00 dagisi ham, oddiy Reels: `schedulingType: automatic`, `shouldShareToFeed: true` — profilda ko'rinadi. `notification` ishlatilmaydi.

## 0. YANGI QOIDALAR (2026-10-14, egasi aytgan — eng ustun)
- Kuniga 5 ta video (Asia/Tashkent): **08:00 o'tmish** (ota-bobolar zamoni vs hozir) · **12:30 hozirgi zamon** (internet, o'yinlar, ish, pul) · **16:00 kelajak** (koinot, AI, 2050 — oddiy Reels, avtomatik) · **18:30 urf-odatlar** · **21:00 odamlardagi ko'p xatolar**. Hammasi hazil-mutoyibali + tekshirilgan qiziq fakt. `config.json` → `slots`, `video_rules`.
- Davomiylik ~60 s. 2–3 personaj gapiradi (masalan dadasi: «Ex bolam, mening vaqtimda...»), har biri boshqa ElevenLabs ovozida. Ovoz bo'laklari uzunroq (1–3 to'liq gap). Ekrandagi yozuvlar — to'liq, tugallangan gap.
- Uslub namunasi: bitta qahramonning kuni, holat ko'rsatkichi (SABR/ENERGIYA %), soat, tez almashuvchi sahnalar, oxirida hisob-kitob varag'i. Boshqa sahifalarning logotip/brendini ishlatmang.
- Qahramonni kesib qimirlatish YO'Q (`anim` default `static`). Har videoda faqat **1–2 sahnaga 2-kadr**: `img/NN_b.jpg` — Flow'da asl rasm tile menyusi → "Добавить в запрос" → "Edit the reference image: keep exactly the same ... Only one small change: ..." → yuborish (558,575). Dvigatel gap o'rtasida (yoki `img2_at` iborasida) 1-kadrdan 2-kadrga o'tadi.
- Flow rasmlarini to'liq o'lchamda olish: tile `img.src` ni fetch → yakuniy URL dagi `=s512-rw` ni `=s0` ga almashtirib fetch; hammasini bitta paket faylga yig'ib Downloads → stage. Mos sahnani rasm o'xshashligi bo'yicha toping.
- Render uzoq (~20 daq): sessiya bo'sh qolsa jarayon to'xtaydi — `sleep` bilan kutib turing.

## 0b. DIZAYN QOIDALARI (2026-10-15, egasi + reference video)
- **Dizaynni har mavzu uchun O'ZINGIZ o'ylab toping.** Egasining misollari (koinot, o'yin va h.k.) faqat misol — shablon emas. Reference videolarni nusxalamang. Har videoda `theme` (shrift, palitra, pufakcha, harakat) mavzudan kelib chiqib boshqacha; `topics_log.md` ga yozing.
- **Butun videoga bitta umumiy fon qo'yib tashlamang.** Har sahna foni mavzuga mos, Flow'da yaratiladi. Protsedurali `space`/`blueprint` fonlar faqat ataylab tanlangan 1–2 sahnada.
- **Qahramon hissiyotlari**: bosh qahramon PNG stiker bo'lib 2–3 sahnada chiqadi va har xil reaksiya qiladi — bir gapda kulib turadi, keyingisida kayfiyati tushadi, keyin hayron qoladi. Har hissiyot uchun alohida Flow rasmi (o'sha personajni namuna qilib): `img/c_<nom>_<hissiyot>.jpg`; `char` elementida `moods` bilan gapga qarab almashadi.
- Mavzuga kerakli qo'shimcha rasmlarni (personajlar, buyumlar, fonlar) Google Flow'da o'zingiz yarating.
- **Rasm uslubi: tabiiy, yarim-realistik** (jurnal illyustratsiyasi) — haqiqiy odam proporsiyalari va yuzlari, iliq kinematik yorug'lik, tabiiy ranglar. **Multfilm/chibi/katta ko'zli uslub YO'Q** (`style.image_prefix`, `character_prefix`). Qorong'i sahna faqat syujet talab qilsa. Haqiqiy siyosatchi va mashhurlarni chizmang.
- **PNG stikerlar ko'p**: har videoda 3–6 marta personaj yoki buyum oq konturli stiker bo'lib chetdan/pastdan chiqadi va gapirganda qimirlaydi (`char`, `prop`). Personajlar Flow'da alohida, oq fonda (`style.character_prefix`) → `img/c_<nom>.jpg`; buyumlar `style.prop_prefix` → `img/p_<nom>.jpg`. Fon rasmlari personajsiz ham bo'lishi mumkin.
- **Dialog**: `bubble` — gapiruvchi nomi (DADA, OYI, BOBUR...) va so'zlar ovozga qarab yonadi, kalit so'zlar rangli.
- **Stikerlar xilma-xil**: pill, yorliq, sticky, soat, checklist/daftar varag'i, karta, emoji-buyumlar, ovoz berish (1-2-3). Katta qizil `stamp`/`big` — videoda ko'pi bilan 1 marta.
- Bir xil raqam/motivni takrorlamang ("47" endi yo'q).
- **Caption qisqa**: 1 ilmoq jumla + 1 savol + 6–8 heshteg. Mavzuni to'liq yozib tashlamang.
- Infografika sahnalari: `bg: blueprint` fon + `tag` (YIL 1995 → 2005 → 2025), `bars` (taqqoslash), `avatar` (qo'ng'iroq qilayotgan odam). Bir personaj yillar davomida o'zgarishi mumkin (yosh → keksa) — har yosh uchun alohida stiker rasmi.
- Yakunda tomoshabinni faollashtiruvchi savol/ovoz berish ("Siz nechanchi farzandsiz? 1·2·3 — izohda yozing").

## 1. Mavzular (xabash-topics)
- `topics_log.md` dagi so'nggi 30 kun mavzularini takrorlamang.
- Har kuni 4 ta: **00:00** tun (telefon, uyqusizlik), **06:00** ertalab (nonushta, choy, ishga tayyorlanish), **12:00** tush (tushlik, ish, pul, tirbandlik), **18:00** kechqurun (oila, mehmon, to'y, qo'shnilar).
- O'zbekona, hajviy-ijtimoiy, bitta tanish odat/paradoks atrofida. Siyosat, din, millat masxarasi yo'q.
- Har biriga WebSearch bilan tekshirilgan 1 ta fakt. Topilmasa — mavzuni almashtiring, uydirma raqam yo'q.
- Egasiga SendUserMessage: har bir vaqt uchun nom, ilmoq jumla, g'oya, fakt manbasi. "hammasi ok" yoki almashtirishni so'rang.
- **Tasdiqsiz hech narsa yasamang va joylamang.**

## 2. Video (xabash-reel-maker)
Papka: `jobs/<YYYY-MM-DD>_<HHMM>_<slug>/` → `scenes.json`, `img/NN.jpg`, `aud/vo_NN.mp3`. Format: `SCHEMA.md`, namuna: `jobs/2026-10-14_ertadan/scenes.json`.
- **Ssenariy 8–9 sahna, 45–60 s — HAR SAFAR BOSHQACHA.** Bitta shablonni takrorlamang. Har video uchun:
  - **yangi bosh qahramon** (jinsi, yoshi, kasbi, kiyimi farq qilsin; ism bering: Dilnoza, Nodira, talaba, bobo, kelin…) — oldingi 3 videodagi qahramonga o'xshamasin (`topics_log.md` da qahramon ustuni);
  - **yangi ochilish turi** — navbat bilan: epik ilmoq / «cold open» (voqea o'rtasidan, keyin «4 soat oldin» flashback) / tomoshabinga murojaat («47 soniya…») / birinchi shaxs hikoyasi («Daftaring qani?») / dialog bilan ochilish / savol bilan ochilish. Oxirgi ishlatilganni `topics_log.md` ga yozing;
  - yangi ikkinchi darajali personajlar (qo'shni, hamkasb, ustoz, ota-ona…), yangi joy va rang palitrasi;
  - fakt (`card`) va yakuniy savol (`final`) qoladi, lekin joyi va shakli o'zgarishi mumkin.
  Musiqa kayfiyatlari: hero / sad / groove / mystery / tense / warm / finale — sahnaga mos tanlang. Ovoz matni sodda, raqamlar so'z bilan.
- **Animatsiya (majburiy):** rasmlardan keyin `pip install --break-system-packages "rembg[cpu]"` va `python3 reel/cutout.py jobs/<job>` — qahramonni kesib `NN_fg.png` + `NN_bg.jpg` yasaydi; dvigatel qahramonni qimirlatadi (nafas, chayqalish, sakrab kirish, parallaks, zarbada kamera turtkisi). Qahramonsiz yoki qayta ishlatilgan rasm uchun sahnada `"anim": "static"`.
- **Brend:** `brand/logo_99foiz.png` har kadr burchagida avtomatik. `scenes.json` da `cover_title` (2 qator, KATTA) va `cover_sub` bo'lishi shart — oxirida 1.8 s muqova kadri, Instagram setkasida shu ko'rinadi (`thumbnailOffset = cover_ms`). 1% / BIR FOIZ brendini ishlatmang.
- **Rasmlar — Google Flow**, egasining kompyuteridagi ichki brauzerda (`anthropic-skills:built-in-browser` skill'ini o'qing). flow.google.com → yangi loyiha → Image, 9:16, x1, Nano Banana. Prompt boshiga `config.json` → `style.image_prefix`. 1-rasm qahramon; qolgan qahramonli sahnalarda **+** → qahramon rasmini namuna qilib qo'shing, prompt "Same person as in the reference image (...)". Avtomatlash: JS bilan `[aria-label="Добавить ингредиенты в окно запроса"]` ni bosing → oxirgi `input[placeholder="Поиск"]` ga nom yozing → natija (172,150) → textarea ga prompt → yuborish tugmasi koordinata (558,575) bilan bosiladi (JS .click ishlamaydi). browser_batch max 25 amal. «Ошибка» chiqsa — refresh tugmasi. Higgsfield ISHLATILMAYDI. Yuklab olish: JS `fetch(img[src*=flow-content])` → `<a download>` → Downloads `.tmp` → `device_list_dir` (hajm bo'yicha moslash) → `device_stage_files` → `/mnt/user-data/uploads/Downloads/`.
- **Ovoz — ElevenLabs:** flow `qGgjoCYEgz4zhvjl3GCQ` (2026-10-16 yangi akkaunt; eski flow'lar ishlatilmaydi), har sahnaga `creative_generate_speech` (`eleven_v4`, `generations_count: 1`, qayta urinmaslik). **Kasting `config.json` → `elevenlabs.cast`**: hikoyachi DOIM Bekzod `kGOig3GPePLxobJGHo2M`; qiz — Dilnoza/Zilola; ona — Nodira/Shahnoza; ota/bobo — Jahongir (+`[elderly voice]`); yigit/oshna — Sardor; buvi — Malika. O'zbekcha matnga INGLIZ ovozlari taqiqlangan (`banned_voices`) — past va tushunarsiz chiqadi. Har qatorda 1–2 hissiyot tegi ([excited] [laughs] [sighs] [sad] [angry] [surprised] [warmly] [sarcastic] ...), tabiiy so'zlashuv ('Voy', 'Ex bolam', 'Qo'ysang-chi'), AI ekani bilinmasin. Dvigatel har bo'lakni -16 LUFS ga tenglaydi (`vo_lufs`). URL'lar storage.googleapis.com da — konteyner ololmaydi: ichki brauzerda bitta URL ni `preview_start` bilan oching, o'sha tabda JS bilan hammasini fetch → BITTA paket fayl (4 bayt uzunlik + JSON indeks + mp3'lar ketma-ket) qilib download → stage → konteynerda bo'lib `aud/vo_NN.mp3`. URL ro'yxatini vaqtincha `media` tarmog'iga `tmp/vo_urls.json` qilib qo'yish mumkin (raw.githubusercontent CORS ochiq). "Free Tier disabled" ba'zan bitta jumlaga qayta-qayta chiqadi — jumlani biroz boshqacha yozib bir marta urinib ko'ring; yana chiqsa egasiga ayting.
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
