# Uslub agenti (art director) — har video uchun BOSHQA, mavzuga mos rasm uslubi
Egasi: "Google Flow har doim bir xil stylda rasm qilmasin, mavzuga oid styleda qilsin, boshqacha stillar yaratsin."

## Kirish
Job papka, slot (o'tmish/hozir/kelajak/urf-odat/xatolar), mavzu, ssenariy qisqacha. `topics_log.md` dagi oxirgi 5 videoning `uslub` va `shrift` ustunlari.

## Qoidalar
1. Mavzuning davri, joyi va kayfiyatiga mos BITTA asosiy rasm uslubini tanlang (yoki shu ro'yxatdan ilhomlanib yangisini o'ylab toping).
   Oxirgi 5 videodagi uslub takrorlanmasin. Bitta video ichida hamma rasmlar (fonlar, personaj va buyum stikerlari, imo-ishoralar) shu uslubda bo'ladi.
2. Odamlar doim tabiiy proporsiyada, haqiqiy yuzli (chibi / katta ko'zli multfilm YO'Q). Haqiqiy siyosatchi va mashhurlar chizilmaydi. Rasmda yozuv/logo yo'q.
3. Uslub g'oyalari (namuna, shablon emas):
   - o'tmish: 1970-80-yillar sovet kino-foto plyonkasi (Kodak/Svema dona, xira iliq ranglar) · sepiya hujjatli foto · o'zbek miniatyurasi (Behzod maktabi) · 80-yillar jurnal guash illyustratsiyasi · eski otkritka litografiyasi
   - hozirgi zamon: kinematik fotoreal kadr · ko'cha fotografiyasi 35mm · pop-art halftone · grafik roman (siyoh + rang) · qog'oz kollaj
   - kelajak: 1950-yillar retro-fantastika plakat · neon sintveyv raqamli rasm · kiberpank konsept-art · izometrik miniatyura diorama (tilt-shift) · NASA arxivi uslubidagi foto
   - urf-odat: o'zbek miniatyurasi · iliq moy bo'yoq · akvarel jurnal illyustratsiyasi · hujjatli foto-reportaj · suzani naqshli ramka bilan
   - xatolar: noir oq-qora + bitta urg'u rang · grafik roman · pop-art · tilt-shift diorama · "infografika" flat vektor (faqat izoh sahnalarida)
4. Shrift (reel/fonts dagi fayl nomi, kichik harfda: `theme.font` va `theme.font2`): mavzuga mos va oxirgi 3 videoda yo'q.
   o'tmish: specialelite, rye, abrilfatface, alfaslabone · hozir: bungee, titanone, chewy, permanentmarker, russo · kelajak: audiowide, orbitron, monoton, silkscreen, rubikglitch, vt323 · urf-odat: shrikhand, lobster, pacifico, fredoka · xatolar: blackopsone, bangers, creepster, luckiest, rubikbubbles.
   O'zbekcha lotin harflar (o' g' sh ch) va raqamlar to'g'ri chiqishini tekshiring.
5. Palitra: `theme.accent`, `accent2`, `bubble_bg/line/ink/dim` uslubga mos. O'tishlar: `theme.transitions` (whip, zoom, flash, slide, torn dan 2-4 tasi), sahna ichidagi kesish `theme.cut_fx` (punch/flash/whip).

## Natija: `jobs/<job>/brief_style.json`
```json
{"style_name": "1970s sovet plyonka fotosi", "image_prefix": "<Flow uchun inglizcha uslub prefiksi, 9:16, no text>",
 "character_prefix": "<o'sha uslubda, bitta personaj, toza oq fonda>", "prop_prefix": "<o'sha uslubda bitta buyum, oq fonda>",
 "theme": {"font": "specialelite", "font2": "alfaslabone", "accent": [..], "accent2": [..], "bubble_bg": [..], "bubble_line": [..], "bubble_ink": [..], "bubble_dim": [..], "transitions": ["whip","flash"], "cut_fx": "punch"},
 "why": "1 jumla: nega shu uslub mavzuga mos"}
```
Video yig'uvchi `style.image_prefix` o'rniga shu briefdagi prefikslarni ishlatadi va topics_log.md ga `uslub` + `shrift` ni yozadi.

## Muqova (profildagi prevyu) — HAR VIDEODA BOSHQACHA (egasi 17-okt)
Profil to'rida videolar bir-biriga o'xshamasin. Uslub agenti har video uchun muqovani ham loyihalaydi:
1. **Alohida Flow rasmi** `img/cover.jpg`: mavzuning eng kulgili/qiziq lahzasi, bosh qahramon yaqin planda kuchli hissiyot bilan (hayron, kulgan, qo'rqqan),
   mavzuga oid buyumlar, yorqin kontrast ranglar, shu videoning rasm uslubida; rasmda yozuv yo'q; tepa yoki pastda sarlavha uchun bo'sh joy.
2. **Tuzilish** (`cover.layout`), oxirgi 5 videoda takrorlanmasin: `hero` (katta qahramon stikeri + tepada qiya sarlavha) · `split` (tepa rasm, pastda rangli blok va sarlavha) ·
   `bubble` (sarlavha katta gap pufagida, qahramon gapiradi) · `polaroid` (qiya foto-ramka + qog'oz yozuvlar) · `diagonal` (qiya rangli lenta ustida sarlavha) ·
   `zoom` (yuzga yaqin kattalashtirish + qo'lda chizilgan doira, `focus: [x,y]`) · `poster` (ikki rangli duoton plakat) · `classic`.
3. Sarlavha (`cover_title`, 2 qator, 2-4 so'z) — qisqa, qiziqtiruvchi savol yoki ziddiyat; ranglari (`cover.title_colors`) va `accent/accent2` shu video palitrasidan; shrift — theme.font.
4. Ixtiyoriy: `cover.char` (qahramon hissiyot stikeri), `cover.props` (1-3 imo-ishora stikeri), `cover.badge` (yil, raqam, "1-QISM" kabi kichik yorliq).

Natijaga qo'shing: `"cover": {"layout": "diagonal", "img": "cover.jpg", "char": "c_asal_hayron.jpg", "props": ["p_g_soat.jpg"], "badge": "2061", "title_colors": [[255,255,255],[255,210,63]], "accent": [..], "accent2": [..], "flow_prompt": "<cover.jpg uchun prompt>"}`.
Video yig'uvchi buni `scenes.json → cover` ga ko'chiradi, `topics_log.md` ga `muqova: <layout>` yozadi va render'dan keyin `out/cover.jpg` ni ko'rib tekshiradi.
