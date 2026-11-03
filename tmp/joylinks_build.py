#!/usr/bin/env python3
"""Joylinks IT Academy (Termiz) uchun 5 ta Reels: scenes.json, images.json, post.json, prompts."""
import json, os, re, shutil
ROOT = "/home/claude/xabash.reels"
LOGO = f"{ROOT}/brand/logo_joylinks_plate.png"
NOTXT = "vertical 9:16, no text, no letters, no numbers, no logos, no watermark, "
V = dict(n="sMpnELN3fdB8ZVjj6xa0", ustoz="rgK9zQmSATbqc0STi5u4", bobo="eD0k57hUAx0oDuThLFT9", boss="GcnlXfqDudh5dSQpZVll",
         mirzaev="RaNVfTYq3HYeFPLng6XN", sodiq="CBeZJ4EnTnrJmhtlMCNC", asil="fytsqG6MLzC2aCSw7MLa", shoh="u20lT5dpbOWoIKz6PpYb")
TEAL = [20, 146, 124]

def M(shape, x, y, w=320, h=220, at="start", label=None, color="red", to=None, out=None):
    e = dict(type="mark", shape=shape, x=x, y=y, w=w, h=h, at=at, color=color)
    if label: e.update(label=label, label_x=x, label_y=y - h // 2 - 50)
    if to: e["to"] = to
    if out: e["out"] = out
    return e
def G(img, x, y, at, h=300, motion="pulse", label=None):
    e = dict(type="prop", img=img, x=x, y=y, h=h, at=at, motion=motion)
    if label: e["label"] = label
    return e
def CARD(k, t, s, at="start", y=1290): return dict(type="card", kicker=k, title=t, sub=s, at=at, y=y)
def TAG(h, t, x=170, y=210, c="red"): return dict(type="tag", head=h, text=t, x=x, y=y, color=c, at="start")
def NOTE(t, y=1180, at="start", x=540, rot=-2): return dict(type="note", text=t, y=y, x=x, at=at, rot=rot, size=66)

def S(spk, text, tag, mood, img, cap=None, extra=(), els=(), hl=None):
    return dict(spk=spk, text=text, tag=tag, mood=mood, img=img, cap=cap, extra=list(extra), els=list(els), hl=hl or {})

VIDEOS = []
# ---------------------------------------------------------------------- 1
VIDEOS.append(dict(
 slug="kompyuter", title="Kompyuter savodxonligi: ikki tugma",
 prefix=NOTXT + "bold pop-art comic illustration, halftone dots, thick ink outlines, saturated yellow, cyan and magenta, Uzbek office in the 2020s, realistic adult human proportions, ",
 cprefix=NOTXT + "bold pop-art comic illustration, halftone shading, thick ink outlines, single person, half body, realistic adult proportions, isolated on a clean plain white background, ",
 pprefix=NOTXT + "bold pop-art comic illustration, thick ink outlines, single object, isolated on a clean plain white background, ",
 theme=dict(font="bungee", font2="patrickhand", accent=[230, 40, 110], accent2=[255, 214, 0], bubble_bg=[255, 250, 230], bubble_line=[20, 20, 30], bubble_ink=[15, 15, 25], bubble_dim=[150, 140, 120], bubble_radius=26, transitions=["whip", "zoom", "flash"], cut_fx="punch"),
 music=dict(genre="funk", bpm=108, key=5, scale="minor", progression=[0, 3, 5, 4]), seed=1983,
 cover=dict(layout="hero", img="cover.jpg", char="c_sanobar_voy.jpg", props=["p_g_tugma.jpg"], badge="CTRL + ?", title_colors=[[255, 255, 255], [255, 214, 0]], accent=[230, 40, 110], accent2=[255, 214, 0]),
 cover_title=["3 SOATLIK ISH", "QAYERGA KETDI?"], cover_sub="Ikki tugma hammasini qaytaradi",
 chars={
  "sanobar": ("Uzbek woman accountant Sanobar, 45, neat dark hair in a bun, reading glasses on a chain, burgundy cardigan", {"": "friendly worried smile", "voy": "shocked, hands on cheeks, mouth open", "kulgi": "laughing with relief, joyful"}),
  "boss": ("stern Uzbek office boss Karimov, 55, thick moustache, grey suit, tie", {"": "angry, pointing at his wristwatch"}),
  "jasur": ("young Uzbek office worker Jasur, 23, short hair, light blue shirt, lanyard", {"": "calm confident smile, one hand raised"}),
 },
 props={"p_g_tugma.jpg": "two big glossy computer keyboard keys side by side, blank key caps, glowing outline", "p_g_soat.jpg": "big red alarm clock ringing, motion lines", "p_g_qaychi.jpg": "old steel scissors and a small glue pot", "p_g_qogoz.jpg": "cut paper strips with blank printed lines, pasted on a sheet"},
 cover_img="close up of a shocked Uzbek woman accountant, 45, bun, reading glasses on a chain, burgundy cardigan, staring at a completely white computer monitor, papers flying, empty space at the top",
 scenes=[
  S("n", "Uch soatlik ish. Bitta tugma. Hammasi g'oyib bo'ldi.", "[tense]", "tense", "a computer monitor showing a completely blank white document, papers exploding through the air around it, dramatic office desk", "3 SOATLIK ISH G'OYIB BO'LDI!", [("a finger pressing one single keyboard key, extreme close up, impact lines", "Bitta tugma")], [M("circle", 540, 800, 620, 480, "Hammasi", "BO'SH!")]),
  S("sanobar", "Voy! Hisobot qani?! Hozirgina shu yerda edi-ku!", "[surprised] [sad]", "tense", "a messy accountant desk with a monitor and stacks of folders in an Uzbek office, warm light", extra=[("close up of a blank computer screen with a blinking cursor", "qani")]),
  S("boss", "Sanobar opa! Hisobot o'n daqiqadan keyin stolimda bo'lsin!", "[angry]", "tense", "long office corridor with a glass door, wall clock, dramatic perspective", els=[TAG("VAQT", "10 DAQ"), G("p_g_soat.jpg", 860, 700, "o'n daqiqadan", 320, "shake")]),
  S("n", "Yigirma yillik tajribali hisobchi. Lekin kompyuter oldida qo'li qaltiraydi.", "[chuckles]", "groove", "wooden shelves full of old paper ledgers and an abacus in an office", "20 YILLIK TAJRIBA, LEKIN KOMPYUTERDAN QO'RQADI", [("trembling hands of a woman hovering over a keyboard, comic motion lines", "qo'li qaltiraydi")], [M("underline", 540, 1400, 700, 40, "qo'li qaltiraydi")]),
  S("sanobar", "Bu kompyuter menga qasd qilyapti, vallohi!", "[angry] [sarcastic]", "groove", "an old beige office computer looking menacing under dramatic comic lighting, no face", els=[M("burst", 780, 850, 300, 300, "qasd", "QASD!")]),
  S("n", "Aslida ikki tugma hammasini qaytarardi. Ularni hozircha aytmayman.", "[whispers]", "mystery", "two mysterious glowing keys in the dark on a keyboard, covered by question-mark shaped shadows without any symbols", "IKKI TUGMA HAMMASINI QAYTARADI", els=[M("box", 540, 850, 560, 340, "ikki tugma", "QAYSI?"), G("p_g_tugma.jpg", 540, 1050, "hozircha", 300, "jump")]),
  S("n", "Avval bir sirni ochay. Nusxa ko'chirishni kim o'ylab topgan?", "[excited]", "mystery", "a computer screen with two identical document pages, a giant hand drawing a copy of it", "NUSXA KO'CHIRISH QAYERDAN CHIQQAN?", [("a 1970s research computer lab with a big CRT terminal, warm colours", "kim o'ylab topgan")]),
  S("n", "Bu g'oya muallifi Larri Tesler. Ilhomi esa oddiy qaychi va yelimdan kelgan.", "[warmly]", "groove", "a 1970s desk with printed paper, scissors and a glue pot under a lamp", extra=[("hands cutting a paragraph out of a printed page with steel scissors, close up", "qaychi")], els=[CARD("KIM O'YLAB TOPGAN", ["LARRI TESLER"], "Kesish, nusxa ko'chirish, joylash"), G("p_g_qaychi.jpg", 830, 720, "qaychi", 320, "wag")]),
  S("n", "Ha, odamlar matnni qog'ozdan kesib, boshqa joyga yopishtirgan.", "[laughs]", "groove", "an editor gluing a cut strip of printed paper on a page, 1970s office", "MATN QAYCHI BILAN KESILGAN!", els=[G("p_g_qogoz.jpg", 800, 700, "yopishtirgan", 320, "bounce")]),
  S("boss", "Besh daqiqa qoldi! Hisobot qani, Sanobar opa?", "[angry]", "tense", "a big wall clock over an Uzbek office, dramatic close up, red tint", els=[TAG("VAQT", "5 DAQ"), G("p_g_soat.jpg", 840, 720, "Besh daqiqa", 340, "shake")]),
  S("jasur", "Opa, qo'rqmang. Bir soniya bering, hozir ko'rsataman.", "[warmly]", "warm", "a bright Uzbek office with a young colleague's desk and laptop, sunlight"),
  S("n", "Yosh hamkasb yaqinlashdi. Klaviaturaga barmog'ini qo'ydi...", "[whispers] [pause]", "mystery", "a young man's hand reaching toward a keyboard in slow motion, tense comic composition", "ENDI DIQQAT QILING...", els=[M("arrow", 300, 780, 200, 120, "barmog'ini", to=[640, 1000])]),
  S("n", "Control va Z! Uch soatlik hisobot bir soniyada qaytib keldi!", "[excited]", "hero", "two fingers pressing control and Z keys on a keyboard, fireworks of colour, comic explosion", "CTRL + Z. HISOBOT QAYTDI!", [("a full computer screen with a complete document and charts, glowing with success, sparkles", "qaytib keldi")], [M("burst", 540, 820, 560, 420, "Control va Z", "CTRL + Z")]),
  S("sanobar", "Voy, shu ekanmi? Yigirma yil qo'rqib yurgan ekanman!", "[laughs] [surprised]", "warm", "happy Uzbek office with paper confetti falling over a tidy desk, warm comic colours"),
  S("n", "Joylinks IT Academy, Termiz. Kompyuter savodxonligi noldan o'rgatiladi.", "[warmly]", "hero", "a bright modern computer classroom with adults of different ages learning together, friendly teacher", els=["CTA:KOMPYUTER SAVODXONLIGI"]),
  S("n", "Kompyuterda qilgan eng alamli xatoingiz qaysi? Izohda yozing.", "[playful]", "finale", "a comic keyboard with one key popping out, bright yellow background", els=[dict(type="final", lines=["ENG ALAMLI", "XATOINGIZ?"], at=0.4)]),
 ]))
# ---------------------------------------------------------------------- 2
VIDEOS.append(dict(
 slug="suniy-intellekt", title="Sun'iy intellekt: bitta jumla",
 prefix=NOTXT + "neon synthwave digital painting, deep violet and electric cyan, glowing rim light, Uzbek university setting, realistic human proportions and faces, ",
 cprefix=NOTXT + "neon synthwave digital painting, cyan and magenta rim light, single person, half body, realistic proportions, isolated on a clean plain white background, ",
 pprefix=NOTXT + "neon synthwave digital painting, single glowing object, isolated on a clean plain white background, ",
 theme=dict(font="audiowide", font2="fredoka", accent=[255, 60, 170], accent2=[80, 235, 255], bubble_bg=[24, 16, 60], bubble_line=[80, 235, 255], bubble_ink=[255, 255, 255], bubble_dim=[120, 120, 190], bubble_radius=30, transitions=["zoom", "flash", "slide"], cut_fx="flash"),
 music=dict(genre="synthwave", bpm=104, key=9, scale="minor", progression=[0, 5, 3, 4]), seed=2026,
 cover=dict(layout="zoom", img="cover.jpg", focus=[540, 760], zoom=1.5, badge="2 yoki 5?", title_colors=[[255, 255, 255], [80, 235, 255]], accent=[255, 60, 170], accent2=[80, 235, 255]),
 cover_title=["BITTA JUMLA", "BAHONI O'ZGARTIRDI"], cover_sub="Sun'iy intellektga to'g'ri so'rov",
 chars={
  "temur": ("Uzbek university student Temur, 20, messy black hair, grey hoodie, holding a phone", {"": "embarrassed and confused", "voy": "amazed, mouth open, eyes wide"}),
  "sardor": ("Uzbek university student Sardor, 21, glasses, navy sweater, laptop under the arm", {"": "calm confident smile"}),
  "ustoz": ("Uzbek woman university lecturer, 42, dark blazer, short hair, holding a printed paper", {"": "strict disappointed look, one eyebrow raised"}),
  "bobo": ("Uzbek grandfather, 72, white beard, doppi skullcap, striped chapan", {"": "wise warm smile, raising a finger"}),
 },
 props={"p_g_robot.jpg": "friendly small glowing chat assistant orb with no face", "p_g_ikki.jpg": "red paper exam sheet with a large circle stamp mark, no writing", "p_g_chiroq.jpg": "glowing light bulb idea", "p_g_kalit.jpg": "golden key glowing"},
 cover_img="close up of an amazed Uzbek student, 20, grey hoodie, face lit by a phone screen in cyan light, sparks of neon around, empty space at the top",
 scenes=[
  S("n", "Bitta sun'iy intellekt. Bitta vazifa. Biri ikki oldi, biri besh.", "[excited]", "tense", "two students seated apart in a dark lecture hall lit by two phone screens, one red glow, one cyan glow", "BIR XIL DASTUR. BIRI 2, BIRI 5!", [("close up of a glowing chat window on a phone, abstract blurred lines", "Bitta vazifa")], [TAG("BAHO", "2 / 5"), M("cross", 300, 800, 220, 220, "ikki oldi"), M("check", 780, 800, 220, 220, "biri besh", color="green")]),
  S("ustoz", "Temur, bu referatni kim yozgan? Bitta ham fikr yo'q-ku!", "[angry]", "tense", "a university lecture room with neon-lit blackboard, stacks of papers on the desk", els=[G("p_g_ikki.jpg", 830, 740, "referatni", 340, "shake")]),
  S("temur", "Ustoz, men sun'iy intellektga yozdirdim. U aybdor!", "[sad]", "groove", "a phone on a desk with a glowing chat screen, dramatic neon reflections", els=[G("p_g_robot.jpg", 820, 760, "aybdor", 300, "wag")]),
  S("n", "Yonidagi Sardor ham aynan o'sha dasturni ishlatgan. Lekin u eng yuqori baho oldi.", "[surprised]", "mystery", "a confident student at a laptop glowing cyan in an evening library", "DASTUR BIR XIL. NATIJA BOSHQA!", [("a printed essay with a golden glow on a desk", "eng yuqori baho")], [M("circle", 540, 850, 520, 400, "o'sha dasturni", "O'SHA DASTUR")]),
  S("n", "Farq pulda emas. O'zbekistonlik talabalar uchun obuna endi bepul.", "[warmly]", "groove", "a wallet and phone on a table, neon light, a coin rolling away", "FARQ PULDA EMAS"),
  S("n", "Google AI Plus. Yiliga oltmish dollarlik obuna. Aileaders.uz orqali bepul.", "[excited]", "groove", "a student holding a glowing phone in the air in a neon-lit campus at night", els=[CARD("TALABALAR UCHUN", ["GOOGLE AI PLUS", "1 YIL BEPUL"], "Aileaders.uz · yillik qiymati $60"), TAG("NARX", "$60")]),
  S("temur", "Demak, dastur bir xil. Unda nega menga bema'ni javob beradi?", "[sad] [surprised]", "mystery", "a phone with a dull grey chat screen, rain on a neon window behind it"),
  S("bobo", "Ex bolam, domlaga ham noaniq savol bersang, noaniq javob olasan.", "[elderly voice] [warmly]", "warm", "a cosy Uzbek home with a low table, teapot and piala, a soft neon glow through the window"),
  S("n", "Bobo bir gapni topdi. Sir aynan shu gapning ichida yashiringan.", "[whispers]", "mystery", "an old man's hand holding a piala, a faint glowing key reflected in the tea", "SIR SHU GAPNING ICHIDA", els=[G("p_g_kalit.jpg", 540, 800, "Sir aynan", 320, "pulse")]),
  S("n", "Temur yozgan so'rov mana bu: referat yozib ber. Uch so'z.", "[sarcastic]", "groove", "a phone in a hand, a chat box glowing with a short blurred line, dull red light", "\"REFERAT YOZIB BER\" — 3 SO'Z", els=[M("underline", 540, 1400, 760, 40, "Uch so'z"), M("cross", 860, 820, 180, 180, "Uch so'z")]),
  S("sardor", "Men esa unga avval ish berdim. Kimligini aytdim, keyin nima kerakligini.", "[warmly]", "groove", "a laptop glowing with a long blurred paragraph in a chat box, cyan light, library at night", els=[G("p_g_chiroq.jpg", 840, 720, "ish berdim", 300, "pulse")]),
  S("n", "Mana o'sha jumla. Skrinshot qilib oling.", "[excited] [pause]", "mystery", "a giant glowing chat window floating in a dark room, a student looking up at it from behind", "SKRINSHOT QILIB OLING!", els=[M("arrow", 240, 760, 200, 120, "o'sha jumla", to=[520, 1000])]),
  S("n", "Sen o'qituvchisan. Besh bandli reja tuz. Har bandga misol keltir.", "[warmly]", "hero", "a laptop bursting with rays of cyan and magenta light, pages flying out in order", extra=[("a stack of perfect printed pages with golden glow", "misol keltir")], els=[CARD("TO'G'RI SO'ROV", ["SEN O'QITUVCHISAN.", "5 BANDLI REJA TUZ."], "Har bandga misol keltir.", y=1250), M("box", 540, 1290, 900, 320, "Sen o'qituvchisan", color="yellow", out="Har bandga")]),
  S("temur", "Voy! Bitta jumla butun referatni o'zgartirdimi?", "[surprised] [excited]", "warm", "a university corridor glowing with morning neon pink, a printed essay with a high mark circle"),
  S("n", "Buni prompt muhandisligi deyishadi. Joylinks Termiz'da shu kurs bor.", "[warmly]", "hero", "a modern classroom with young students at laptops, friendly mentor, neon accents", els=["CTA:PROMPT ENGINEERING"]),
  S("n", "Sun'iy intellektga bergan eng g'alati savolingiz qaysi? Izohda yozing.", "[playful]", "finale", "a glowing chat bubble shape floating over a neon grid horizon, no writing", els=[dict(type="final", lines=["ENG G'ALATI", "SAVOLINGIZ?"], at=0.4)]),
 ]))
# ---------------------------------------------------------------------- 3
VIDEOS.append(dict(
 slug="dasturlash", title="Dasturlash: yashiringan ism",
 prefix=NOTXT + "traditional Central Asian miniature painting style with gold leaf and lapis blue, delicate brush lines, modern objects painted in the same miniature style, natural human proportions, ",
 cprefix=NOTXT + "traditional Central Asian miniature painting style, delicate brush lines, single person, half body, natural proportions, isolated on a clean plain white background, ",
 pprefix=NOTXT + "traditional Central Asian miniature painting style, gold leaf, single object, isolated on a clean plain white background, ",
 theme=dict(font="alfaslabone", font2="patrickhand", accent=[200, 60, 40], accent2=[232, 186, 80], bubble_bg=[250, 240, 214], bubble_line=[28, 50, 110], bubble_ink=[24, 26, 44], bubble_dim=[150, 130, 100], bubble_radius=18, transitions=["slide", "torn", "zoom"], cut_fx="whip"),
 music=dict(genre="chiptune", bpm=112, key=2, scale="dorian", progression=[0, 3, 5, 3]), seed=825,
 cover=dict(layout="split", img="cover.jpg", band_y=1180, badge="IX ASR", title_colors=[[255, 248, 225], [232, 186, 80]], accent=[28, 50, 110], accent2=[232, 186, 80]),
 cover_title=["HAR ILOVADA", "BIR XORAZMLIK"], cover_sub="Bu ismni har kuni ishlatasiz",
 chars={
  "rustam": ("Uzbek teenage boy Rustam, 16, short black hair, green t-shirt, holding a laptop", {"": "frustrated, scratching his head", "voy": "excited, eyes wide, big smile"}),
  "ustoz": ("Uzbek woman programming mentor, 40, kind face, teal blouse, short hair", {"": "patient warm smile, pointing a finger"}),
 },
 props={"p_g_kapalak.jpg": "a small brown moth with open wings", "p_g_kod.jpg": "a laptop with abstract coloured lines on its screen", "p_g_choynak.jpg": "a blue and white Uzbek teapot and a piala", "p_g_kitob.jpg": "an old open manuscript book with geometric diagrams, no writing"},
 cover_img="a medieval scholar in a turban in a Khorezm observatory holding a glowing smartphone, stars and geometry around him, gold and lapis blue, empty space at the bottom",
 scenes=[
  S("n", "Telefoningizdagi har bir ilova ichida bir xorazmlikning ismi yashiringan.", "[whispers]", "mystery", "a smartphone lying on an ornamented carpet, a golden medieval geometric star glowing out of its screen", "HAR ILOVADA BIR ISM YASHIRINGAN", [("a medieval Khorezm city with blue domes at dusk seen through a window", "xorazmlikning")], [M("circle", 540, 820, 500, 500, "ismi yashiringan", "KIMNING?")]),
  S("n", "Ishonmaysizmi? O'n olti yoshli Rustam ham ishonmagan edi.", "[chuckles]", "groove", "a teenager's room with a desk, laptop and carpets, late evening", "RUSTAM, 16 YOSH", els=[TAG("YOSH", "16")]),
  S("rustam", "Ustoz, dasturim ishlamayapti! Kompyuter meni yomon ko'radi!", "[sad] [angry]", "tense", "a laptop on a carved wooden desk with a red warning glow, crumpled papers around it", els=[G("p_g_kod.jpg", 820, 760, "ishlamayapti", 300, "shake")]),
  S("ustoz", "Kompyuter seni yomon ko'rmaydi, Rustam. Unda shunchaki xato bor.", "[warmly] [chuckles]", "warm", "a tidy classroom with a low table, laptops and a blackboard painted in miniature style"),
  S("n", "Xato, ya'ni bag. Inglizchada hasharot degani. Bu so'z tasodifiy emas.", "[excited]", "mystery", "an enormous magnifying glass over a laptop keyboard, ornamental border", "BAG = HASHAROT. TASODIFIY EMAS!", els=[M("underline", 540, 1400, 640, 40, "hasharot degani"), G("p_g_kapalak.jpg", 820, 760, "hasharot", 260, "wag")]),
  S("n", "Bir ming to'qqiz yuz qirq yettinchi yil. Garvard. Kompyuter ichidan haqiqiy kapalak topiladi.", "[surprised]", "mystery", "a huge 1940s room-sized electromechanical computer with relay panels, engineers in the distance", None, [("tweezers pulling a small moth out of a metal relay, close up", "kapalak")], [TAG("YIL", "1947"), CARD("GARVARD, MARK II", ["HAQIQIY KAPALAK"], "Grays Xopper jamoasi", at="Garvard")]),
  S("n", "Uni daftarga yopishtirib yozib qo'yishadi: birinchi haqiqiy bag topildi.", "[laughs]", "groove", "an old logbook page with a small moth taped to it, no readable writing", "BIRINCHI HAQIQIY BAG TOPILDI", els=[M("circle", 540, 800, 420, 340, "yopishtirib")]),
  S("rustam", "Demak, mening kodimda ham kapalak bormi?", "[surprised]", "groove", "a boy peeking into the back of a laptop with a small lamp, funny composition", els=[G("p_g_kapalak.jpg", 820, 720, "kapalak", 240, "bounce")]),
  S("ustoz", "Yo'q, senda bitta vergul yetishmayapti. Eng qizig'i esa boshqa joyda.", "[laughs]", "mystery", "a giant golden comma shape floating in front of a laptop, ornamented background"),
  S("n", "Kompyuterga har bir ishni qadam-baqadam aytish kerak. Xuddi choy damlagandek.", "[warmly]", "groove", "a hand pouring hot water into a blue and white Uzbek teapot, steam, tray with pialas", "HAR ISH QADAM-BAQADAM", [("three neat stages of brewing tea arranged in a row on a tray", "Xuddi choy")], [G("p_g_choynak.jpg", 830, 720, "choy", 300, "jump")]),
  S("rustam", "Algoritm! Lekin bu qanaqa g'alati so'z o'zi?", "[excited]", "groove", "a laptop screen with colourful abstract lines arranged as steps"),
  S("n", "Eslaysizmi, ismi yashiringan xorazmlik? Mana u, to'qqizinchi asr olimi.", "[excited] [pause]", "hero", "a medieval Muslim scholar writing at a desk surrounded by astrolabes and geometric drawings, candlelight, seen from behind, face in shadow", "IX ASR. BAGDOD. BIR XORAZMLIK OLIM", els=[TAG("ASR", "IX"), G("p_g_kitob.jpg", 830, 740, "olimi", 320, "pulse")]),
  S("n", "Muhammad al-Xorazmiy. Yevropada ismi lotinchaga o'girilib, algoritm so'ziga aylangan.", "[excited]", "hero", "an old European monastery scriptorium copying a manuscript, then a golden light rising", None, [("a glowing golden word-shaped ribbon flying from an old manuscript toward a laptop, no letters", "algoritm")], [CARD("AL-XORAZMIY", ["AL-XORAZMIY = ALGORITM"], "Har bir dastur shu so'z bilan ishlaydi")]),
  S("n", "Joylinks Termiz'da kodni noldan boshlaysiz. Bitta dars xonasi ham al-Xorazmiy nomida.", "[warmly]", "hero", "a modern classroom with teenagers coding on laptops painted in miniature style, mentor helping, gold border", els=["CTA:DASTURLASH"]),
  S("n", "O'z ilovangizni yaratsangiz, u nima qilardi? Izohda yozing.", "[playful]", "finale", "a smartphone resting on an ornamented golden tray, sparkling screen without text", els=[dict(type="final", lines=["ILOVANGIZ", "NIMA QILARDI?"], at=0.4)]),
 ]))
# ---------------------------------------------------------------------- 4
VIDEOS.append(dict(
 slug="kiberxavfsizlik", title="Kiberxavfsizlik: Shokir akaning paroli",
 prefix=NOTXT + "high contrast black and white film noir illustration with one single accent colour: blood red, graphic novel ink, realistic human proportions, modern Uzbek city at night, ",
 cprefix=NOTXT + "high contrast black and white noir ink illustration, a touch of red, single person, half body, realistic proportions, isolated on a clean plain white background, ",
 pprefix=NOTXT + "high contrast black and white noir ink illustration with red accent, single object, isolated on a clean plain white background, ",
 theme=dict(font="russo", font2="marker", accent=[220, 25, 40], accent2=[245, 245, 245], bubble_bg=[14, 14, 16], bubble_line=[220, 25, 40], bubble_ink=[255, 255, 255], bubble_dim=[120, 120, 125], bubble_radius=8, transitions=["flash", "whip", "torn"], cut_fx="punch"),
 music=dict(genre="detective", bpm=92, key=7, scale="minor", progression=[0, 5, 0, 4]), seed=123456,
 cover=dict(layout="poster", img="cover.jpg", char="c_shokir_voy.jpg", badge="123456", duo_dark=[16, 16, 18], ink=[230, 30, 45], title_colors=[[255, 255, 255], [230, 30, 45]], accent=[230, 30, 45], accent2=[255, 255, 255]),
 cover_title=["PAROLINGIZ", "123456 EMASMI?"], cover_sub="Bir soniyaga bormay buziladi",
 chars={
  "shokir": ("Uzbek taxi driver Shokir, 48, stubble, flat cap, leather jacket, holding a phone", {"": "cheerful and confident", "voy": "terrified, mouth open, sweat drops"}),
  "mutaxassis": ("Uzbek woman cybersecurity specialist, 38, black turtleneck, short hair, calm gaze", {"": "serious calm look, one finger raised"}),
 },
 props={"p_g_quluf.jpg": "broken open padlock", "p_g_qalqon.jpg": "a shield with a red outline", "p_g_sms.jpg": "a phone with a red notification glow, no text", "p_g_ilgak.jpg": "a fishing hook with a small envelope on it"},
 cover_img="a terrified taxi driver in a flat cap in a dark car, face lit by a red phone glow, noir shadows, empty space at the top",
 scenes=[
  S("n", "Ikki ming yigirma beshinchi yil. O'zbekistonda deyarli har ikkinchi jinoyat kiberjinoyat bo'lgan.", "[serious]", "tense", "a lone figure on a night street in Termez lit only by a red phone screen, long noir shadows", "DEYARLI HAR 2-JINOYAT KIBERJINOYAT", [("a thief's gloved hand reaching out of a phone screen, red glow", "har ikkinchi")], [TAG("2025", "49,6%"), CARD("IIV MA'LUMOTI", ["49,6 FOIZ"], "Barcha jinoyatlar ichida kiberjinoyat ulushi", at="kiberjinoyat", y=1280)]),
  S("n", "Taksichi Shokir aka bundan bexabar edi. Toki shu xabar kelguncha.", "[whispers]", "mystery", "an old white sedan taxi parked in a quiet night street, noir", "SHU XABAR KELGUNCHA...", [("a phone buzzing on a car dashboard, red glow", "shu xabar")], [G("p_g_sms.jpg", 820, 760, "shu xabar", 300, "shake")]),
  S("firibgar", "Aka, rasmlaringizni ko'rdingizmi? Mana shu faylni oching.", "[whispers] [sarcastic]", "tense", "a dark room with a hooded figure from behind at glowing monitors, face unseen", els=[G("p_g_ilgak.jpg", 820, 740, "faylni", 300, "wag")]),
  S("shokir", "Voy, qanaqa rasm? Hozir ochib ko'raman.", "[surprised]", "tense", "a thumb approaching a red glowing file icon shape on a phone, extreme close up", els=[M("arrow", 240, 780, 200, 120, "ochib", to=[520, 1000])]),
  S("n", "To'xtang! Eng keng tarqalgan usul aynan shu. Kiberjinoyatlarning o'ttiz sakkiz foizi.", "[angry]", "tense", "a giant red stop hand silhouette over a phone screen, noir", "TO'XTANG! 38% SHU USUL", els=[dict(type="bars", rows=[["Zararli dastur", 38, "red"], ["Soxta sotuvchi", 18, "yellow"], ["Onlayn birja", 16, "yellow"]], x=540, y=620, at="o'ttiz sakkiz"), TAG("IIV", "38%")]),
  S("shokir", "Bay-bay! Parolim bor-ku, menga hech kim kirolmaydi!", "[laughs]", "groove", "inside a taxi at night, a proud driver's hand tapping his chest, dashboard lights", els=[G("p_g_quluf.jpg", 830, 740, "Parolim", 280, "bounce")]),
  S("n", "Parolingiz nima, aka?", "[sarcastic]", "mystery", "an interrogation lamp shining on an empty chair in a dark room, noir", "PAROLINGIZ NIMA?", els=[M("box", 540, 800, 560, 260, "Parolingiz")]),
  S("shokir", "Bir ikki uch to'rt besh olti! Hech kim topolmaydi!", "[excited]", "groove", "a phone password field with six glowing dots on a dark dashboard", els=[M("burst", 540, 900, 500, 300, "Bir ikki", "123456")]),
  S("n", "Bu dunyodagi eng mashhur parol. Uch milliondan ortiq odam ishlatgan.", "[sarcastic]", "tense", "thousands of tiny identical phones arranged in a noir grid, all lit red", els=[CARD("NORDPASS TADQIQOTI", ["123456", "3 MLN+ ODAMDA"], "Dunyodagi eng ko'p ishlatiladigan parol")]),
  S("n", "Eng ommabop parollarning yetmish sakkiz foizi bir soniyaga bormay buziladi.", "[serious]", "tense", "a padlock shattering into shards with a red flash, stopwatch in the background", "78% PAROL 1 SONIYADA BUZILADI", [("a stopwatch frozen at the very start, red flash", "bir soniyaga")], [G("p_g_quluf.jpg", 820, 700, "buziladi", 320, "shake")]),
  S("shokir", "Unda nima qilay? Telefonni suvga otaymi endi?", "[sad] [surprised]", "groove", "a taxi driver's silhouette standing on a bridge at night holding a phone over a river, funny noir"),
  S("mutaxassis", "Shoshmang, aka. Sizni bitta oddiy qoida qutqaradi.", "[warmly]", "warm", "a calm bright security operations room with screens, a red shield glow", els=[G("p_g_qalqon.jpg", 830, 740, "qoida", 320, "pulse")]),
  S("n", "Firibgarga sizning bitta harakatingiz kerak. O'sha harakatni qilmang.", "[whispers] [pause]", "mystery", "a chess board in noir light with a single red piece about to move", "UNGA BITTA HARAKATINGIZ KERAK"),
  S("mutaxassis", "Notanish faylni ochmang. SMS kodni hech kimga aytmang, bankdan deyishsa ham.", "[serious]", "hero", "a phone with a large red shield glowing over it, thumb pulled away, dark background", extra=[("a hand covering a phone keypad, noir", "SMS kodni")], els=[M("cross", 840, 780, 200, 200, "Notanish faylni"), M("check", 240, 1150, 180, 180, "bankdan", color="green")]),
  S("n", "Himoya sirlarini o'rganmoqchimisiz? Joylinks Termiz'da kiberxavfsizlik kursi bor.", "[warmly]", "hero", "a modern classroom of students at laptops, red accent lights, mentor at a whiteboard with abstract network shapes", els=["CTA:KIBERXAVFSIZLIK"]),
  S("n", "Sizga kelgan eng ayyor xabar qanday edi? Izohda yozing.", "[playful]", "finale", "a phone on a black table with a red notification glow", els=[dict(type="final", lines=["ENG AYYOR", "XABAR QANDAY EDI?"], at=0.4)]),
 ]))
# ---------------------------------------------------------------------- 5
VIDEOS.append(dict(
 slug="backend", title="Backend: to'y oshxonasi",
 prefix=NOTXT + "warm rich oil painting, visible brush strokes, golden hour light, Uzbek toy wedding and kitchen life, natural human proportions and faces, ",
 cprefix=NOTXT + "warm rich oil painting, visible brush strokes, single person, half body, natural proportions, isolated on a clean plain white background, ",
 pprefix=NOTXT + "warm rich oil painting, single object, isolated on a clean plain white background, ",
 theme=dict(font="shrikhand", font2="fredoka", accent=[196, 74, 30], accent2=[244, 196, 92], bubble_bg=[255, 244, 222], bubble_line=[120, 56, 24], bubble_ink=[50, 26, 14], bubble_dim=[170, 140, 110], bubble_radius=34, transitions=["zoom", "slide", "whip"], cut_fx="punch"),
 music=dict(genre="doira_folk", bpm=118, key=4, scale="hijaz", progression=[0, 3, 4, 3]), seed=2021,
 cover=dict(layout="polaroid", img="cover.jpg", tilt=-5, badge="6 SOAT", title_colors=[[120, 40, 16], [196, 74, 30]], accent=[196, 74, 30], accent2=[244, 196, 92]),
 cover_title=["OSHXONA TO'XTADI", "DUNYO O'CHDI"], cover_sub="Ilovaning ko'rinmas qismi",
 chars={
  "bobo": ("Uzbek master osh chef grandfather Hamro, 70, white beard, doppi skullcap, white apron over a striped chapan, holding a big kafgir ladle", {"": "wise warm smile"}),
  "nabira": ("Uzbek teenage grandson Ulug'bek, 15, short hair, red t-shirt, holding a phone", {"": "curious and puzzled", "voy": "amazed, wide eyes"}),
  "ona": ("Uzbek woman guest, 42, floral dress, embroidered headscarf", {"": "worried, hands raised"}),
 },
 props={"p_g_yurak.jpg": "a shiny red heart shape", "p_g_qozon.jpg": "a big black cast iron kazan with plov", "p_g_server.jpg": "a tall black data centre server rack with small lights", "p_g_kalit.jpg": "a broken network cable with sparks"},
 cover_img="a huge Uzbek wedding table laid with plov, and behind it a dark empty kitchen with a cold kazan, an old chef in a doppi looking shocked, warm oil painting",
 scenes=[
  S("n", "Olti soat. Milliardlab odam yozisha olmay qoldi. Sababi bitta buyruq edi.", "[tense]", "tense", "a crowd of people in a dusk city all looking confused at dark phones, oil painting", "OLTI SOAT. BITTA BUYRUQ.", [("one hand pressing a single key in a dark room with server lights", "bitta buyruq")], [TAG("VAQT", "6 SOAT"), M("underline", 540, 1400, 620, 40, "bitta buyruq")]),
  S("n", "Uni ekranda hech kim ko'rmagan. Chunki u ilovaning ko'rinmas qismida yashaydi.", "[whispers]", "mystery", "a brightly lit wedding hall door slightly open with a dark hidden kitchen corridor behind it", "ILOVANING KO'RINMAS QISMI", els=[M("arrow", 240, 760, 200, 120, "ko'rinmas", to=[560, 960])]),
  S("nabira", "Bobo, mana bu yurakchani bosdim. Qayoqqa ketdi u?", "[surprised]", "groove", "a teenager's phone on a wooden table in an Uzbek courtyard, afternoon sun", els=[G("p_g_yurak.jpg", 820, 740, "yurakchani", 280, "jump")]),
  S("bobo", "Ex bolam, oshni yeysan-u, oshxonaga kirmaysan-da.", "[elderly voice] [chuckles]", "warm", "a giant kazan of plov steaming over fire in an Uzbek outdoor kitchen, carrots and rice", extra=[("a master chef's kafgir ladle stirring plov, close up", "oshxonaga")]),
  S("n", "Bobo to'g'ri aytadi. Ilova bu to'y. Dasturxon ko'rinadi, oshxona esa yo'q.", "[warmly]", "groove", "a magnificent Uzbek wedding table with guests, flowers and golden light", "ILOVA — BU TO'Y", [("behind a curtain, a busy hidden kitchen with chefs and steam", "oshxona esa")]),
  S("n", "Ekrandagi dasturxon frontend. Orqadagi oshxona esa backend.", "[excited]", "hero", "a split view: bright banquet table on the left, steaming kitchen on the right, oil painting", els=[dict(type="pill", text="FRONTEND", bg="royal", x=280, y=620, at="frontend"), dict(type="pill", text="BACKEND", bg="crimson", x=800, y=620, at="backend"), M("arrow", 800, 720, 120, 80, "backend", to=[800, 980])]),
  S("nabira", "Demak, yurakcha oshxonagacha boradimi?", "[excited]", "groove", "a glowing red heart flying down a corridor toward a kitchen, magical realism oil painting"),
  S("n", "Bir soniyaga ham bormay. So'rov serverga boradi, baza yangilanadi, javob qaytadi.", "[excited]", "groove", "a long aisle of black server racks with warm amber lights, like a huge pantry", "SO'ROV, BAZA, JAVOB", [("waiters passing plates in a fast chain through a kitchen hatch", "javob qaytadi")], [G("p_g_server.jpg", 830, 740, "serverga", 340, "bounce")]),
  S("ona", "Oshpaz ketib qolsa-chi? To'y nima bo'ladi?", "[surprised]", "tense", "an empty kitchen with a cold kazan and no fire, wedding music stands silent, dusk light"),
  S("n", "Aynan shu narsa bir marta butun dunyoda yuz bergan. Kompaniyani ham aytaman.", "[whispers] [pause]", "mystery", "a globe in the dark with lights going out one by one, oil painting", "BU BUTUN DUNYODA YUZ BERGAN", els=[M("circle", 540, 820, 520, 520, "butun dunyoda")]),
  S("n", "Ikki ming yigirma birinchi yil. Facebook, Instagram, WhatsApp bir vaqtda o'chdi.", "[surprised]", "tense", "many dark smartphones scattered on a wooden table, people looking worried in the background", els=[TAG("2021", "4-OKT"), CARD("2021-YIL, 4-OKTABR", ["FACEBOOK", "INSTAGRAM, WHATSAPP"], "Taxminan 6 soat ishlamadi")]),
  S("n", "Muhandislar xizmat paytida bitta buyruq yuborgan. U markazlarni internetdan uzib qo'ygan.", "[serious]", "tense", "an engineer at a terminal in a dim room with a look of dawning horror, warm monitor light", "BITTA BUYRUQ HAMMASINI UZDI", [("a thick network cable pulled out with sparks in a server room", "uzib qo'ygan")], [G("p_g_kalit.jpg", 830, 720, "uzib", 300, "shake")]),
  S("n", "Ichki asboblar ham ishlamay qolgan. Muhandislar serverlar oldiga shaxsan borishgan.", "[surprised]", "tense", "engineers walking urgently down a long dark server hall with flashlights", "SERVERLAR OLDIGA SHAXSAN BORISHGAN", els=[M("arrow", 240, 800, 200, 120, "shaxsan", to=[600, 960])]),
  S("bobo", "Ana ko'rdingmi! Oshxona to'xtasa, butun to'y to'xtaydi.", "[elderly voice] [warmly]", "warm", "an old chef's kitchen with the fire lit again, kazan steaming, warm light", els=[G("p_g_qozon.jpg", 830, 760, "Oshxona", 300, "pulse")]),
  S("n", "Mana shu oshxonani quradiganlar backend dasturchilar. Joylinks Termiz'da noldan boshlanadi.", "[warmly]", "hero", "a modern classroom with students at laptops, warm oil painting, mentor helping one student", els=["CTA:BACKEND DASTURLASH"]),
  S("n", "Siz dasturxonni tanlaysizmi yoki oshxonani? Izohda yozing.", "[playful]", "finale", "a richly laid Uzbek table with a glowing kitchen door behind it", els=[dict(type="final", lines=["DASTURXONMI", "YOKI OSHXONA?"], at=0.4)]),
 ]))

LABEL = dict(sanobar="SANOBAR OPA", boss="KARIMOV", jasur="JASUR", temur="TEMUR", sardor="SARDOR", ustoz="USTOZ", bobo="BOBO", rustam="RUSTAM", shokir="SHOKIR AKA", mutaxassis="MUTAXASSIS", firibgar="NOTANISH", nabira="ULUG'BEK", ona="MEHMON")
VOICE = dict(sanobar="ustoz", boss="boss", jasur="sodiq", temur="asil", sardor="sodiq", ustoz="ustoz", bobo="bobo", rustam="sodiq", shokir="mirzaev", mutaxassis="ustoz", firibgar="shoh", nabira="sodiq", ona="ustoz", n="n")

def build(v):
    job = f"jobs/2026-11-04_joylinks_{v['slug']}"; d = f"{ROOT}/{job}"; os.makedirs(d + "/img", exist_ok=True); os.makedirs(d + "/aud", exist_ok=True)
    shutil.copy(LOGO, d + "/img/logo_joylinks.png")
    imgs = {}
    def add(name, prompt): imgs[name] = dict(prompt=prompt)
    for nm, (desc, moods) in v["chars"].items():
        for m, face in moods.items():
            add(f"c_{nm}{'_' + m if m else ''}.jpg", v["cprefix"] + desc + ", " + face)
    for f, p in v["props"].items(): add(f, v["pprefix"] + p)
    add("cover.jpg", v["prefix"] + v["cover_img"])
    scenes = []; side = 0; seen = {}
    for i, s in enumerate(v["scenes"], 1):
        s = dict(s); n = f"{i:02d}"; add(f"{n}.jpg", v["prefix"] + s["img"])
        sc = dict(n=i, speaker=s["spk"], text=s["text"], tts=f"{s['tag']} {s['text']}", mood=s["mood"], img=f"{n}.jpg", vo=f"vo_{n}.mp3", voice_id=V[VOICE[s["spk"]]], elements=[])
        ex = []
        for j, (p, ph) in enumerate(s["extra"]):
            f = f"{n}{'bcd'[j]}.jpg"; add(f, v["prefix"] + p); ex.append([f, ph])
        if ex: sc["imgs"] = ex
        if s["spk"] != "n":
            c = s["spk"]; k = seen.get(c, 0); seen[c] = k + 1
            moods = list(v["chars"].get(c, ("", {"": ""}))[1])
            m = moods[k % len(moods)] if c in v["chars"] else ""
            left = side % 2 == 0; side += 1
            if c in v["chars"]:
                sc["elements"].append(dict(type="char", img=f"c_{c}{'_' + m if m else ''}.jpg", **{"from": "left" if left else "right"}, x=290 if left else 790, y=1450, h=880, at=0.05, talk=["vo"], motion="bounce", label=LABEL[c]))
            sc["elements"].append(dict(type="bubble", speaker=LABEL[c], text=s["text"], x=540, y=340, at="start", tail="down", tail_x=0.25 if left else 0.75))
        elif s["cap"]:
            sc["elements"].append(dict(type="caption", words=s["cap"].split(), color="yellow", y=1340, size=84, at=0.1))
        for e in s["els"]:
            if isinstance(e, str) and e.startswith("CTA:"):
                sc["elements"] += [dict(type="prop", img="logo_joylinks.png", x=540, y=500, h=300, at=0.1, motion="pulse"),
                                   dict(type="card", kicker="JOYLINKS IT ACADEMY · TERMIZ", title=[e[4:]], sub="Qo'ng'iroq: +998 99 287 32 20", at=0.4, y=1240)]
            else: sc["elements"].append(e)
        if i == len(v["scenes"]):
            sc["elements"].append(dict(type="pill", text="JOYLINKS TERMIZ · 99 287 32 20", bg="green", x=540, y=1640, at=1.0))
        scenes.append(sc)
    cfg = dict(title=v["title"], pace="fast", music=v["music"], music_seed=v["seed"], music_gain=0.7, cover_title=v["cover_title"], cover_sub=v["cover_sub"], cover_scene=0, cover=v["cover"], anim="static", bright=True, logo=f"{ROOT}/brand/logo_joylinks_plate.png", theme=v["theme"], end_hold=1.4, scenes=scenes)
    json.dump(cfg, open(d + "/scenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(imgs, open(d + "/images.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return job, imgs, scenes

allp, allv = [], []
for v in VIDEOS:
    job, imgs, scenes = build(v)
    chars = sum(len(s["tts"]) for s in scenes)
    print(job, "sahna", len(scenes), "rasm", len(imgs), "belgi", chars, "taxmin_s", round(sum(len(s["text"]) for s in scenes) / 14.5, 1), "uzun:", [s["n"] for s in scenes if len(s["text"]) > 88])
    allp += [[f"{v['slug']}/{k}", x["prompt"]] for k, x in imgs.items()]
    allv += [dict(job=job, n=s["n"], voice_id=s["voice_id"], tts=s["tts"]) for s in scenes]
json.dump(allp, open(f"{ROOT}/tmp/joylinks_prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(allv, open(f"{ROOT}/tmp/joylinks_vo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("jami rasm", len(allp), "ovoz", len(allv), "belgi", sum(len(x["tts"]) for x in allv))
