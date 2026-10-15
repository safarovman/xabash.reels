# -*- coding: utf-8 -*-
"""17-oktabr: 5 ta video (egasi tasdiqlagan). 12:30 — egasining o'z hikoyasi (texnikum, tekshiruvchi, ustoz).
16:00 — 2050 emas, 2061-yil. Yangi qoidalar: o'zbekcha cast, hissiyot teglari (tts), yarim-realistik rasmlar,
PNG stikerlar (char/prop + moods), bubble, har videoga o'z theme."""
import json, os

CAST = {"bekzod": "kGOig3GPePLxobJGHo2M", "dilnoza": "O72h9AUwisM6Zj4He72B", "zilola": "cyPun3bl9MxcpLBX6pT0",
        "nodira": "132QLQIkg1RJGmpicuhR", "shahnoza": "eggZu1Ffe4if51TKev2v", "jahongir": "xDwfBjUEPdIoQekNOXAX",
        "sardor": "UjuEL3hLLUaDED9iW4Yb", "malika": "VTN9ql0D5MshokKncKAy"}

def S(speaker, tts, mood, img, elements, **kw):
    import re
    text = re.sub(r"\[[^\]]*\]\s*", "", tts).strip()
    d = {"speaker": speaker, "text": text, "tts": tts, "mood": mood, "img": img, "elements": elements}
    d.update(kw); return d
def note(t, y=1560, at="start", size=70, rot=-2, x=None):
    d = {"type": "note", "text": t, "y": y, "size": size, "rot": rot, "at": at}
    if x: d["x"] = x
    return d
def stamp(t, y=1560, at="end", rot=-5): return {"type": "stamp", "text": t, "y": y, "rot": rot, "at": at}
def sticker(lines, color="yellow", x=760, y=420, w=400, at="start", rot=4, size=54):
    return {"type": "sticker", "lines": lines, "color": color, "x": x, "y": y, "w": w, "size": size, "rot": rot, "at": at}
def pill(t, bg="navy", x=540, y=300, at="start", rot=-3, fg="white"): return {"type": "pill", "text": t, "bg": bg, "fg": fg, "x": x, "y": y, "rot": rot, "at": at}
def card(kicker, title, sub, at=0.3, y=None):
    d = {"type": "card", "kicker": kicker, "title": title, "sub": sub, "at": at}
    if y: d["y"] = y
    return d
def dark(a=0.4): return {"type": "dark", "amount": a, "at": "start"}
def final(lines): return {"type": "final", "lines": lines, "at": 0.4}
def tag(head, text, x=170, y=210, color="red", at="start"): return {"type": "tag", "head": head, "text": text, "x": x, "y": y, "color": color, "at": at}
def clock(day, time, at="start"): return {"type": "clock", "day": day, "time": time, "at": at}
def bubble(speaker, y=330, at="start", hl=None, tail="down", tail_x=0.3, tagc="navy", text=None, until=None, w=880):
    d = {"type": "bubble", "speaker": speaker, "x": 540, "y": y, "at": at, "hl": hl or {}, "tail": tail, "tail_x": tail_x, "tag": tagc, "w": w}
    if text: d["text"] = text
    if until: d["until"] = until
    return d
def char(img, side="right", x=None, y=1430, h=780, at=0.2, talk=True, moods=None, out=None, label=None, motion="idle", flip=False, label_bg="green"):
    if x is None: x = {"right": 800, "left": 280, "bottom": 540, "pop": 540}[side]
    d = {"type": "char", "img": img, "from": side, "x": x, "y": y, "h": h, "at": at, "motion": motion, "flip": flip}
    if talk: d["talk"] = ["vo"]
    if moods: d["moods"] = moods
    if out: d["out"] = out
    if label: d["label"] = label; d["label_bg"] = label_bg
    return d
def prop(img, x=780, y=1300, h=420, at=0.3, label=None, motion="idle", side="pop", path=None, dur=3.0):
    d = {"type": "prop", "img": img, "x": x, "y": y, "h": h, "at": at, "motion": motion, "from": side}
    if label: d["label"] = label
    if path: d["path"] = path; d["dur"] = dur
    return d
def bars(rows, y=900, at=0.4): return {"type": "bars", "rows": rows, "x": 540, "y": y, "at": at}

JOBS = {}

# ---------------------------------------------------------------- 08:00 O'TMISH
JOBS["2026-10-17_0800_kasseta"] = dict(
    slot="2026-10-17T08:00+05:00", theme_cat="o'tmish", title="Qalam bilan aylantirilgan kasseta", music_seed=171,
    cover_title=["QALAM BILAN", "AYLANGAN KASSETA"], cover_sub="«Ex bolam, mening vaqtimda...»", cover_scene=1,
    hero="Ravshan aka (50, mo'ylov, jigarrang jilet) + o'g'li Temur (17, quloqchin) + buvi Oydin (Ravshanning onasi)",
    opening="dialog bilan",
    design="retro 90-yillar: kasseta varag'i ranglari (to'q sariq, jigarrang, krem), russo + caveat shrift, krem pufakcha jigarrang chiziq; 1993 yorlig'i, kasseta stikeri",
    theme={"font": "russo", "font2": "caveat", "accent": [222, 96, 40], "accent2": [255, 196, 86], "bubble_bg": [252, 238, 210],
           "bubble_line": [120, 66, 30], "bubble_ink": [60, 32, 18], "bubble_dim": [200, 170, 140], "bubble_radius": 18},
    images={
        "c_ravshan": "CHAR: Uzbek man Ravshan, 50, neat black mustache with grey strands, short dark hair, brown knitted vest over a light blue shirt, laughing proudly with one hand raised as if telling a story, half body.",
        "c_ravshan_hayron": "CHAR: Same man as in the reference image (Ravshan, 50, mustache, brown knitted vest, light blue shirt), eyebrows raised in amazement, mouth open, half body.",
        "c_ravshan_xafa": "CHAR: Same man as in the reference image (Ravshan, 50, mustache, brown knitted vest), wistful nostalgic smile with slightly sad eyes, holding an old audio cassette to his chest, half body.",
        "c_temur": "CHAR: Uzbek teenage boy Temur, 17, modern haircut, oversized grey hoodie, white wireless earbuds, holding a smartphone, grinning, half body.",
        "c_buvi": "CHAR: Elderly Uzbek grandmother Oydin, 75, white headscarf tied at the back, colorful atlas-patterned dress, kind wrinkled face, laughing warmly with one hand on her chest, half body.",
        "p_kasseta": "PROP: an old 1990s audio cassette with a yellow pencil inserted into one spool, tape slightly loose, realistic.",
        "01": "SCENE: Modern cozy Uzbek living room in the evening, teenage boy Temur (17, grey hoodie, white earbuds) sitting on a sofa enthusiastically showing his smartphone to his father Ravshan (50, mustache, brown knitted vest, light blue shirt) who looks skeptical with a tea cup in hand. Characters on the left and center, calm wall space at top.",
        "02": "SCENE: 1993, sunny traditional Uzbek courtyard with a grape vine trellis, a young man of 18 with a mustache-free face, 1990s haircut and striped shirt (young Ravshan) sitting on a wooden tapchan carefully rewinding an audio cassette tape with a pencil, an old silver radio cassette player beside him, warm nostalgic light.",
        "03": "SCENE: Same modern living room, teenage boy Temur (grey hoodie, earbuds) staring in total disbelief, holding his phone, mouth open, sofa and lamp behind him.",
        "04": "SCENE: 1990s Uzbek bedroom with carpet on the wall, young Ravshan (18, striped shirt) crouched tensely in front of a silver radio cassette player, finger hovering over the record button, waiting for a song on the radio, focused face.",
        "04_b": "EDIT 04: Only one small change: the young man now grabs his head with both hands in despair, mouth open.",
        "05": "SCENE: 1990s Uzbek wedding in a courtyard at dusk, a lively woman of 50 in a headscarf and atlas dress (grandmother Oydin when younger) proudly holding up an audio cassette next to a big boombox, guests dancing behind her, string lights.",
        "06": "SCENE: 1963 European radio exhibition hall, vintage display table with an early portable cassette recorder and small cassettes under spotlight, curious visitors in 1960s suits in the background, no logos.",
        "07": "SCENE: Dusty home storage room, father Ravshan (mustache, brown vest) and son Temur (grey hoodie) opening an old cardboard box full of hand-labeled audio cassettes, the son amazed, warm light through a small window.",
        "08": "SCENE: Father Ravshan (mustache, brown vest) and son Temur (grey hoodie) sitting together on the sofa, the son wearing old foam headphones connected to a 1990s portable cassette player, both smiling, the father's arm around his shoulder, warm evening lamp light.",
    },
    scenes=[
        S("sardor", "[excited] Dada, qarang! Telefonimda o'n million qo'shiq bor. Xohlagan qo'shig'imni bir soniyada qo'yaman!", "groove", "01.jpg",
          [bubble("TEMUR", hl={"million": "red", "soniyada": "red"}, tagc="orange")]),
        S("jahongir", "[chuckles] Ex bolam, mening vaqtimda bitta qo'shiq eshitish uchun avval qalam topardik. Lenta chigallashsa, qalamga kiygizib, sekin-sekin aylantirardik.", "warm", "02.jpg",
          [tag("YIL", "1993"), char("c_ravshan.jpg", "right", at=0.3, label="DADA", label_bg="orange"), prop("p_kasseta.jpg", x=300, y=1330, at="qalamga", label="ENG ZO'R ASBOB")]),
        S("sardor", "[surprised] Qalam bilan? Qo'shiq eshitish uchun? Dada, bu qanaqa texnologiya o'zi?", "groove", "03.jpg",
          [bubble("TEMUR", hl={"Qalam": "red"}, tagc="orange"), char("c_ravshan.jpg", "left", at="texnologiya", talk=False, moods=[["c_ravshan_hayron.jpg", "texnologiya"]])]),
        S("jahongir", "[warmly] Radiodan sevimli qo'shig'ing chiqsa, yugurib borib yozish tugmasini bosarding. Lekin oxirida baribir diktor gapirib yuborardi!", "tense", "04.jpg",
          [pill("YOZISH TUGMASI TAYYOR", bg="orange", at="start"), stamp("DIKTOR GAPIRIB YUBORDI!", at="diktor")], img2="04_b.jpg", img2_at="diktor"),
        S("malika", "[elderly voice] [laughs] Voy, o'sha kassetalarni men to'yga olib borardim. Bitta kassetani butun mahalla qarzga olib, hech kim qaytarib bermasdi!", "warm", "05.jpg",
          [char("c_buvi.jpg", "right", at=0.2, label="BUVI", label_bg="purple"), sticker(["Kasseta qarzga ketdi,", "qaytmadi!"], color="pink", x=330, y=420, at="qarzga")]),
        S("bekzod", "Bilasizmi, bu ixcham kassetani Philips kompaniyasi bir ming to'qqiz yuz oltmish uchinchi yilda Berlin radio ko'rgazmasida taqdim etgan. Keyin u butun dunyoning cho'ntagiga sig'adigan musiqaga aylandi.", "mystery", "06.jpg",
          [dark(0.35), card("Philips, 1963", ["IXCHAM KASSETA", "1963-YILDA CHIQQAN"], "Berlin radio ko'rgazmasida taqdim etilgan.", at="Philips")]),
        S("sardor", "[laughs] Dada, sizning o'n million qo'shig'ingiz shu bitta qutida yotibdi-ku! Bularning hammasini qayerdan topgansiz?", "groove", "07.jpg",
          [bubble("TEMUR", hl={"qutida": "red"}, tagc="orange"), char("c_ravshan_xafa.jpg", "right", at=0.3, talk=False, moods=[["c_ravshan.jpg", "qayerdan"]])]),
        S("jahongir", "[sighs] Har bir kassetaning o'z hikoyasi bor, bolam. Mana bu qo'shiqni men oyingga birinchi marta sovg'a qilganman. Sening telefoningda shunaqa hikoya bormi?", "warm", "08.jpg",
          [note("Har bir kassetaning o'z hikoyasi bor.", at="hikoyasi"), sticker(["Birinchi sovg'a:", "bitta kasseta"], color="yellow", x=760, y=420, at="sovg'a")]),
        S("bekzod", "Siz kassetani qalam bilan aylantirganmisiz? Bir — ha, ikki — yo'q, uch — kasseta nima o'zi? Izohda yozing!", "finale", "08.jpg",
          [final(["QALAM BILAN", "AYLANTIRGANMISIZ?"]), sticker(["1 - HA", "2 - YO'Q", "3 - KASSETA NIMA?"], color="yellow", x=540, y=1500, w=460, at="Bir")]),
    ],
    caption="Ex bolam, mening vaqtimda bitta qo'shiq uchun avval qalam topardik! 📼✏️\n\nSiz kassetani qalam bilan aylantirganmisiz? 1, 2 yoki 3 👇\n\n#99foiz #otmish #kasseta #nostalgiya #90lar #ozbekcha #uzbekistan #reels",
)

# ---------------------------------------------------------------- 12:30 EGASINING HIKOYASI
JOBS["2026-10-17_1230_texnikum"] = dict(
    slot="2026-10-17T12:30+05:00", theme_cat="hozirgi zamon (egasining hikoyasi)", title="10 daqiqa kechikish", music_seed=183,
    cover_title=["10 DAQIQA KECHIKDIM,", "3 SOAT NASIHAT"], cover_sub="texnikumdagi tekshiruvchi", cover_scene=1,
    hero="«men» — texnikum talabasi (oq ko'ylak, ryukzak) + tekshiruvchi (kal, yashil ko'z, qorin, ko'k Nexia) + ustoz (ozg'in, katta ko'zoynak, eski konspekt)",
    opening="birinchi shaxs (egasining xotirasi)",
    design="bo'r doska: to'q yashil pufakcha, oq bo'r yozuv, marker + fredoka shrift, qizil-sariq aksent; 1 sahna blueprint infografika (kechikish/nasihat chiziqlari), checklist stikeri, ko'k Nexia uchib o'tadi",
    theme={"font": "marker", "font2": "fredoka", "accent": [235, 80, 60], "accent2": [250, 232, 120], "bubble_bg": [34, 66, 50],
           "bubble_line": [236, 236, 222], "bubble_ink": [250, 250, 240], "bubble_dim": [110, 140, 120], "bubble_radius": 12},
    images={
        "c_men": "CHAR: Uzbek college student, 18, slim, short neat haircut, white shirt, black trousers, black backpack on one shoulder, cheerful confident smile, full body.",
        "c_men_xafa": "CHAR: Same young man as in the reference image (18, white shirt, black trousers, backpack), standing tired against an invisible wall, shoulders dropped, bored exhausted face, full body.",
        "c_men_kulgan": "CHAR: Same young man as in the reference image (white shirt, backpack) laughing out loud, holding his stomach, full body.",
        "c_tekshiruvchi": "CHAR: Uzbek college discipline inspector, 50, completely bald shiny head, striking bright green eyes, big round belly, tight grey suit jacket that barely buttons, dark tie, hands on hips, stern suspicious squint, holding car keys, full body.",
        "c_ustoz": "CHAR: Thin elderly Uzbek college teacher, 65, huge old-fashioned thick glasses, oversized faded brown suit, holding a yellowed old notebook close to his face, sleepy monotone expression, half body.",
        "p_nexia": "PROP: small blue 1990s four-door compact sedan car, side view, slightly dusty, realistic, no logos, no license plate text.",
        "01": "SCENE: Morning entrance hall of an old Uzbek technical college (texnikum), long empty corridor with green-painted walls, big round wall clock, sunlight from tall windows, worn parquet floor.",
        "02": "SCENE: Same college corridor, a bald college inspector (50, shiny bald head, bright green eyes, big belly, tight grey suit) blocking the way with hands on hips, staring down at a nervous student (18, white shirt, backpack) who just arrived, dramatic morning light.",
        "04": "SCENE: Same corridor, the bald green-eyed inspector with a big belly measuring the student's hair with a wooden ruler, the student (white shirt) standing stiffly against the green wall, other students peeking from a classroom door.",
        "04_b": "EDIT 04: Only one small change: the inspector now holds a big magnifying glass to the student's chin instead of the ruler.",
        "05": "SCENE: College parking lot, the bald inspector with a big belly squeezing into a small blue 1990s compact sedan, belly pressed against the steering wheel, proud face; in the background through a window the student stands against a wall.",
        "06": "SCENE: Old Soviet-era classroom with a green chalkboard, a thin elderly teacher with huge thick glasses and an oversized brown suit reading monotonously from a yellowed notebook, students half asleep at wooden desks, dust in the sunbeams.",
        "07": "SCENE: Close-up of an old teacher's grade journal and a piece of chalk on a wooden desk by the window, an empty classroom behind, soft afternoon light, melancholic.",
        "08": "SCENE: Modern bright classroom, young Uzbek students working actively in small groups around a whiteboard, discussing and laughing, a young teacher guiding them.",
        "09": "SCENE: The same old college corridor today, renovated, a grown man in his 30s (the former student, now with a short beard, casual jacket) walking past the wall where he once stood, smiling to himself.",
    },
    scenes=[
        S("bekzod", "[sighs] Texnikumda o'qigan paytlarim... O'n daqiqa kechikdim, xolos. Lekin eshik oldida meni bitta odam kutib turardi.", "mystery", "01.jpg",
          [clock("DUSHANBA", "08:10"), char("c_men.jpg", "left", at=0.4, talk=False, label="MEN", label_bg="royal")]),
        S("sardor", "[angry] Ha-a, keldingmi? O'n daqiqa kechikding! Otang kim? Bobong kim? Qaysi mahalladansan? Butun urug'-aymog'ingni aytib ber-chi!", "tense", "02.jpg",
          [bubble("TEKSHIRUVCHI", hl={"Otang": "red", "Bobong": "red", "urug'-aymog'ingni": "red"}, tagc="crimson"),
           char("c_tekshiruvchi.jpg", "right", at="Otang", label="TEKSHIRUVCHI", label_bg="crimson")]),
        S("bekzod", "U meni koridorda ikki soat ushlab turdi. Nasihati esa uch soatga cho'zildi. Oxirida u mening urug'imni mendan ham yaxshiroq bilib oldi.", "groove", None,
          [tag("HISOB", "DAQIQA", x=200, y=260), bars([["Kechikish", 10, "yellow"], ["Ushlab turdi", 120, "red"], ["Nasihat", 180, "red"]], y=820, at=0.3),
           char("c_men_xafa.jpg", "bottom", x=540, y=1500, h=700, at="urug'imni", talk=False)], bg="blueprint", bg_color=[30, 70, 55]),
        S("sardor", "[shouting] Konspekting qani? Yo'qmi? Unda uch para tik turasan! Soching nega uzun? Soqoling nega o'sib ketgan? Hammasini tekshiraman!", "tense", "04.jpg",
          [bubble("TEKSHIRUVCHI", hl={"uch": "red", "para": "red"}, tagc="crimson", until="Soching"),
           sticker(["SOCH - TEKSHIRILDI", "SOQOL - TEKSHIRILDI", "KONSPEKT - YO'Q!"], color="yellow", x=540, y=1480, w=520, at="Soching", rot=-3)],
          img2="04_b.jpg", img2_at="Soqoling"),
        S("bekzod", "[chuckles] Keyin u ko'k Nexiasiga o'tirdi, qornini rulga tirab, viqor bilan ketdi. Men esa uch para devor yonida tik turdim.", "groove", "05.jpg",
          [prop("p_nexia.jpg", x=700, y=1250, h=380, at="Nexiasiga", label="KO'K NEXIA", motion="fly", path=[-300, 1250], dur=1.6),
           note("Men esa uch para devor yonida tik turdim.", at="Men esa")]),
        S("jahongir", "[elderly voice] Bolalar, yozib olinglar. Sakson beshinchi yildagi konspekt, o'n ikkinchi bet. Savol bermanglar... men ham bilmayman.", "mystery", "06.jpg",
          [bubble("USTOZ", hl={"bilmayman": "red"}, tagc="purple", y=320), char("c_ustoz.jpg", "right", at=0.3, label="USTOZ", label_bg="purple")]),
        S("bekzod", "Intizom — besh. Soch-soqol — besh. Ilm-chi? Ilm o'sha kuni ham eshik oldida tik turib qolgan edi.", "sad", "07.jpg",
          [pill("INTIZOM: 5", bg="green", x=300, y=330, at="Intizom"), pill("SOCH-SOQOL: 5", bg="green", x=720, y=450, at="Soch-soqol", rot=3),
           note("Ilm eshik oldida tik turib qoldi.", at="Ilm-chi")]),
        S("bekzod", "Olimlar ham buni isbotlagan. Freeman va hamkasblarining ikki ming o'n to'rtinchi yilgi tadqiqotiga ko'ra, faqat ma'ruza tinglagan talabalar faol o'qiganlarga qaraganda bir yarim barobar ko'p yiqilgan.", "mystery", "08.jpg",
          [dark(0.4), card("PNAS, 2014 - Freeman va boshq.", ["FAQAT MA'RUZA:", "1,5 BAROBAR KO'P YIQILISH"], "Faol o'qish natijani yaxshilaydi.", at="Freeman")]),
        S("bekzod", "[laughs] Sizni ham kechikkaningiz uchun tik turg'izishganmi? Bir — ha, ikki — yo'q, uch — men o'zim tekshiruvchi edim. Izohda yozing!", "finale", "09.jpg",
          [final(["SIZNI HAM", "TURG'IZISHGANMI?"]), char("c_men_kulgan.jpg", "left", x=250, y=1500, h=640, at=0.3, talk=False)]),
    ],
    caption="10 daqiqa kechikdim — 2 soat ushlab turishdi, nasihat 3 soatga cho'zildi 😅🎒\n\nSizni ham kechikkaningiz uchun tik turg'izishganmi? 👇\n\n#99foiz #texnikum #talaba #kechikish #ustoz #ozbekcha #uzbekistan #reels",
)

# ---------------------------------------------------------------- 16:00 KELAJAK (2061)
JOBS["2026-10-17_1600_mars-kechikish"] = dict(
    slot="2026-10-17T16:00+05:00", theme_cat="kelajak", title="Marsda kech qolishning bahonasi", music_seed=196,
    cover_title=["MARSDA KECHIKISH", "BAHONASI"], cover_sub="2061-yil, Mars universiteti", cover_scene=0,
    hero="Asal (20, talaba, skafandr, ikki o'rim soch) + domla Saodat opa (55, qattiqqo'l, naqshli sharf) + robot-davomat",
    opening="cold open (Marsda yugurish, keyin «40 daqiqa oldin»)",
    design="Mars: zang-qizil va havorang neon, orbitron + rubikmono shrift, to'q jigarrang pufakcha neon-to'q sariq chiziq; 1 sahna protsedurali koinot (fakt), suzuvchi (float) stikerlar",
    theme={"font": "orbitron", "font2": "rubikmono", "accent": [255, 110, 60], "accent2": [120, 228, 255], "bubble_bg": [44, 22, 20],
           "bubble_line": [255, 140, 80], "bubble_ink": [255, 245, 236], "bubble_dim": [140, 100, 90], "bubble_radius": 34},
    images={
        "c_asal": "CHAR: Young Uzbek woman Asal, 20, two long dark braids, sleek white and orange futuristic spacesuit without helmet, holding a tablet, sheepish hopeful smile, full body.",
        "c_asal_hayron": "CHAR: Same young woman as in the reference image (Asal, two braids, white-orange spacesuit), shocked wide eyes, hand over mouth, full body.",
        "c_asal_xafa": "CHAR: Same young woman as in the reference image (Asal, two braids, white-orange spacesuit), sad disappointed face, shoulders down, holding the tablet loosely, full body.",
        "c_domla": "CHAR: Strict Uzbek woman professor Saodat, 55, short grey bob hair, elegant dark futuristic uniform with a traditional ikat-patterned scarf, arms crossed, raised eyebrow, half body.",
        "p_robot": "PROP: small friendly floating attendance robot drone, round white body, one glowing blue eye, holographic checklist panel, realistic sci-fi design.",
        "p_mars": "PROP: realistic planet Mars, rusty red with visible craters and a thin polar ice cap.",
        "01": "SCENE: Year 2061, corridor of a university on Mars, huge curved windows showing a red rocky desert and a pale sky, a young Uzbek woman (two braids, white-orange spacesuit) running fast with a tablet, motion blur, morning light.",
        "02": "SCENE: Small cozy dorm capsule on Mars, the young woman with two braids asleep in a bunk, a futuristic alarm clock glowing, red Martian sunrise through a round window.",
        "02_b": "EDIT 02: Only one small change: the young woman is now sitting bolt upright in bed in panic, eyes wide, hair messy.",
        "03": "SCENE: Lecture hall under a glass dome on Mars, rows of students in futuristic uniforms, a strict woman professor (55, short grey bob, dark uniform, ikat scarf) standing at the front with arms crossed looking at the door.",
        "04": "SCENE: Doorway of the Mars lecture hall, the young woman with two braids in a white-orange spacesuit standing breathless with both hands raised apologetically, students turning to look.",
        "06": "SCENE: The strict professor (grey bob, ikat scarf) smirking and holding a glowing holographic exam sheet, a large holographic clock floating behind her, Mars dome lecture hall.",
        "07": "SCENE: The young woman with two braids sitting alone at an exam desk in the Mars lecture hall, a small floating white robot with a blue eye hovering beside her, she smiles wryly, red desert through the window.",
        "08": "SCENE: Wide view of a Mars dome city at sunrise, blue-tinted Martian sunset sky, the young woman with two braids on a balcony setting a futuristic wrist device, calm and determined.",
    },
    scenes=[
        S("bekzod", "[excited] Ikki ming oltmish birinchi yil. Mars. Universitet koridorida bitta talaba skafandrda yugurib ketyapti. Uning ismi Asal va u yana kechikdi.", "tense", "01.jpg",
          [tag("YIL", "2061"), pill("MARS UNIVERSITETI", bg="orange", x=640, y=300, at="Mars")]),
        S("bekzod", "Qirq daqiqa oldin Asal yotoqxonada shirin uxlab yotgan edi. Chunki budilnigi hali ham Yer vaqtiga qo'yilgan edi.", "mystery", "02.jpg",
          [clock("YER VAQTI", "07:00"), note("Budilnik hali ham Yer vaqtida.", at="budilnigi")], img2="02_b.jpg", img2_at="Chunki"),
        S("shahnoza", "[angry] Asal! Yana kechikdingmi? Bu semestrda o'n birinchi marta! Bahonang tayyormi?", "tense", "03.jpg",
          [bubble("DOMLA", hl={"o'n": "red", "birinchi": "red"}, tagc="crimson"), char("c_domla.jpg", "right", at=0.3, label="DOMLA", label_bg="crimson")]),
        S("zilola", "[nervous] [laughs] Domla, men kechikmadim! Marsda bir kun Yernikidan qariyb qirq daqiqa uzun. Men shunchaki... Yer vaqtida yashayapman!", "groove", "04.jpg",
          [bubble("ASAL", hl={"qirq": "orange", "Yer": "orange"}, tagc="royal"),
           char("c_asal.jpg", "left", at=0.3, moods=[["c_asal_hayron.jpg", "Men shunchaki"]], label="ASAL", label_bg="royal")]),
        S("bekzod", "Va bu safar u haq edi. Marsdagi bir sutka, ya'ni sol, yigirma to'rt soat o'ttiz to'qqiz daqiqa davom etadi.", "mystery", None,
          [prop("p_mars.jpg", x=540, y=640, h=520, at=0.2, motion="float"), card("NASA", ["1 SOL =", "24 SOAT 39 DAQIQA"], "Marsdagi sutka Yernikidan uzunroq.", at="sol", y=1350)],
          bg="space", bg_seed=17),
        S("shahnoza", "[sarcastic] Zo'r. Unda imtihon ham Yer vaqtida bo'ladi. Ya'ni... u o'ttiz to'qqiz daqiqa oldin boshlangan.", "tense", "06.jpg",
          [stamp("IMTIHON BOSHLANGAN!", at="boshlangan"), char("c_asal_xafa.jpg", "left", x=240, h=640, at="Ya'ni", talk=False)]),
        S("zilola", "[sighs] Kelajakda raketalar uchadi, robotlar ovqat pishiradi... Lekin kechikish uchun bahona baribir ish bermas ekan.", "sad", "07.jpg",
          [prop("p_robot.jpg", x=800, y=560, h=360, at=0.3, motion="float", label="ROBOT-DAVOMAT"), sticker(["Kechikdi:", "11-marta"], color="blue", x=300, y=420, at="bahona")]),
        S("bekzod", "Xullas, Marsga ko'chsangiz ham, budilnikni Mars vaqtiga qo'ying. Kun uzun bo'lgani bilan, domla baribir kutmaydi.", "warm", "08.jpg",
          [note("Budilnikni Mars vaqtiga qo'ying!", at="budilnikni"), char("c_asal.jpg", "right", x=820, h=640, at="domla", talk=False)]),
        S("bekzod", "Sizga har kuni qo'shimcha qirq daqiqa berilsa, nimaga sarflardingiz? Bir — uyquga, ikki — choyga, uch — baribir kechikardim!", "finale", "08.jpg",
          [final(["QO'SHIMCHA 40 DAQIQA", "NIMAGA KETADI?"]), sticker(["1 - UYQU", "2 - CHOY", "3 - BARIBIR KECHIKAMAN"], color="blue", x=540, y=1500, w=500, at="Bir")]),
    ],
    caption="2061-yil, Mars: talaba yana kechikdi — lekin bahonasi ilmiy! 🚀⏰\n\nQo'shimcha 40 daqiqani nimaga sarflardingiz? 👇\n\n#99foiz #kelajak #mars #koinot #talaba #ozbekcha #uzbekistan #reels",
)

# ---------------------------------------------------------------- 18:30 URF-ODAT
JOBS["2026-10-17_1830_askiya"] = dict(
    slot="2026-10-17T18:30+05:00", theme_cat="urf-odat", title="Askiya: so'z bilan kurash", music_seed=204,
    cover_title=["BOBO VA NEVARA:", "ASKIYA JANGI"], cover_sub="qilich yo'q, faqat so'z", cover_scene=0,
    hero="Hoji bobo (75, oq soqol, chopon, do'ppi) + nevarasi Doniyor (16) + buvi Mehri (hakam)",
    opening="epik ilmoq",
    design="Farg'ona choyxonasi: oltin-indigo, atlas naqshi ruhi; lobster + fredoka shrift, oq pufakcha indigo chiziq; hisob tablosi (bars), 1-RAUND/2-RAUND pill'lari",
    theme={"font": "lobster", "font2": "fredoka", "accent": [200, 36, 96], "accent2": [255, 204, 64], "bubble_bg": [255, 250, 238],
           "bubble_line": [40, 52, 130], "bubble_ink": [30, 34, 70], "bubble_dim": [180, 180, 200], "bubble_radius": 40},
    images={
        "c_bobo": "CHAR: Elderly Uzbek grandfather Hoji bobo, 75, neat white beard, traditional striped chapan robe, black-and-white doppi skullcap, laughing heartily with a sly twinkle in his eyes, one finger raised, half body.",
        "c_bobo_dono": "CHAR: Same old man as in the reference image (white beard, striped chapan, doppi), calm wise warm smile, hand on heart, half body.",
        "c_bobo_hayron": "CHAR: Same old man as in the reference image (white beard, striped chapan, doppi), surprised eyebrows up, mouth open in a delighted 'oho!', half body.",
        "c_doniyor": "CHAR: Uzbek teenage boy Doniyor, 16, short hair, white shirt with an embroidered vest, cheeky confident grin, pointing forward, half body.",
        "c_buvi": "CHAR: Elderly Uzbek grandmother Mehri, 72, light green headscarf, dark velvet vest over a floral dress, laughing and clapping her hands, half body.",
        "01": "SCENE: Fergana teahouse (choyxona) at golden hour, wooden carved pillars, an old man with a white beard in a striped chapan and doppi sitting on a tapchan facing a teenage grandson in an embroidered vest, other men around watching with smiles, teapots and bread on the table.",
        "02": "SCENE: Close medium shot in the teahouse: the white-bearded grandfather in the striped chapan leaning forward with a sly grin, delivering a witty line, warm golden light, tea steam.",
        "03": "SCENE: The teenage grandson in an embroidered vest on the tapchan answering back with a cheeky grin, onlookers laughing behind him, teahouse at golden hour.",
        "04": "SCENE: Grandmother in a light green headscarf sitting at the edge of the tapchan clapping and laughing, the grandfather and grandson in the background, warm light.",
        "05": "SCENE: The white-bearded grandfather gently putting a hand on his grandson's shoulder and explaining something wisely, both on the tapchan, teahouse at sunset.",
        "06": "SCENE: Outdoor stage at a festival in Uzbekistan, two performers in chapans facing each other mid-joke, a large audience laughing, colorful lights, dusk.",
        "07": "SCENE: Grandson leaning in with a mischievous challenging smile, holding a stack of round Uzbek bread (non), the grandfather listening with a raised eyebrow, teahouse.",
        "08": "SCENE: Grandfather hugging his grandson and both laughing, grandmother pouring tea, teahouse onlookers applauding, golden sunset light.",
    },
    scenes=[
        S("bekzod", "[excited] Farg'onadagi choyxonada jang boshlandi. Qilich yo'q, musht yo'q... qurol faqat so'z. Bir tomonda Hoji bobo, bir tomonda nevarasi Doniyor.", "hero", "01.jpg",
          [pill("1-RAUND", bg="crimson", x=540, y=300, at="jang"), note("Qurol faqat so'z.", at="qurol")]),
        S("jahongir", "[elderly voice] [chuckles] Ha, nevaram, eshitdimki, bir kunda ming marta layk bosarkansan. Barmog'ing chiniqib, bolg'adek bo'lib qolibdi-yu!", "groove", "02.jpg",
          [bubble("HOJI BOBO", hl={"layk": "red", "bolg'adek": "red"}, tagc="navy"), char("c_bobo.jpg", "right", x=820, h=720, at=0.3, label="HOJI BOBO", label_bg="navy")]),
        S("sardor", "[laughs] Bobojon, kecha osh yeyishda shunaqa tez edingizki, qoshiq ortingizdan yetolmay qoldi!", "groove", "03.jpg",
          [bubble("DONIYOR", hl={"qoshiq": "red"}, tagc="royal"), char("c_bobo.jpg", "left", x=240, h=640, at="qoshiq", talk=False, moods=[["c_bobo_hayron.jpg", "yetolmay"]])]),
        S("malika", "[elderly voice] [laughs] Voy, ikkalangiz ham bir-biringizdan qolishmaysiz! Bitta ochko bobosiga, bitta ochko nevarasiga!", "groove", "04.jpg",
          [bars([["HOJI BOBO", 1, "yellow"], ["DONIYOR", 1, "red"]], y=520, at="ochko"), char("c_buvi.jpg", "right", x=810, h=700, at=0.2, label="HAKAM: BUVI", label_bg="purple")]),
        S("jahongir", "[elderly voice] [warmly] Bolam, askiyada yutish uchun tez gapirish kam. Avval tinglash kerak, keyin kulib javob qaytarish kerak.", "warm", "05.jpg",
          [char("c_bobo.jpg", "right", x=820, h=720, at=0.2, moods=[["c_bobo_dono.jpg", "Avval"]]), note("Avval tingla, keyin kulib javob qaytar.", at="Avval", x=430)]),
        S("bekzod", "Bu shunchaki o'yin emas, bu san'at. «Askiya — so'z san'ati» ikki ming o'n to'rtinchi yilda YUNESKO nomoddiy madaniy merosi ro'yxatiga kiritilgan.", "mystery", "06.jpg",
          [dark(0.35), card("YUNESKO, 2014", ["ASKIYA -", "SO'Z SAN'ATI"], "Nomoddiy madaniy meros ro'yxatida.", at="Askiya")]),
        S("sardor", "[excited] Unda oxirgi savol, bobojon: nega mehmon kelsa, eng shirin gapni siz aytasiz-u, eng og'ir nonni men tashiyman?", "tense", "07.jpg",
          [pill("2-RAUND", bg="crimson", x=540, y=300, at="start"), bubble("DONIYOR", y=470, hl={"shirin": "red", "nonni": "red"}, tagc="royal")]),
        S("jahongir", "[elderly voice] [laughs] Chunki askiyani men o'rgataman, nonni esa sen o'rgatasan! Ana, bugun ikkalamiz ham ustoz bo'ldik.", "warm", "08.jpg",
          [stamp("DURRANG!", at="ustoz", y=1500), char("c_bobo_hayron.jpg", "left", x=250, h=620, at=0.2, moods=[["c_bobo.jpg", "Chunki"]])]),
        S("bekzod", "Sizning oilangizda kim eng zo'r askiyachi? Bir — bobom, ikki — buvim, uch — o'zim! Izohda yozing.", "finale", "08.jpg",
          [final(["OILANGIZDA KIM", "ZO'R ASKIYACHI?"]), sticker(["1 - BOBOM", "2 - BUVIM", "3 - O'ZIM"], color="yellow", x=540, y=1500, w=420, at="Bir")]),
    ],
    caption="Choyxonada jang: qilich yo'q, musht yo'q — qurol faqat so'z! 🫖😄\n\nOilangizda eng zo'r askiyachi kim? 👇\n\n#99foiz #askiya #urfodat #choyxona #fargona #ozbekcha #uzbekistan #reels",
)

# ---------------------------------------------------------------- 21:00 XATOLAR
JOBS["2026-10-17_2100_koz-charchoq"] = dict(
    slot="2026-10-17T21:00+05:00", theme_cat="ko'p uchraydigan xatolar", title="Ko'zim qizardi, seriya tugamadi", music_seed=219,
    cover_title=["KO'Z QIZARDI,", "SERIYA TUGAMADI"], cover_sub="20 - 20 - 20 qoidasi", cover_scene=0,
    hero="Farhod (26, dasturchi, ko'zoynaksiz, qora futbolka) + singlisi Nilufar (19) + ko'z shifokori Dilorom opa (50)",
    opening="tomoshabinga murojaat",
    design="klinik toza: oq va zangori (teal), sariq ogohlantirish; inter + russo shrift, oq pufakcha zangori chiziq; ko'rish jadvali uslubidagi yozuvlar, 1 sahna blueprint (20-20-20), taymer stikeri",
    theme={"font": "inter", "font2": "russo", "accent": [0, 150, 140], "accent2": [255, 226, 80], "bubble_bg": [255, 255, 255],
           "bubble_line": [0, 140, 132], "bubble_ink": [20, 40, 46], "bubble_dim": [170, 200, 200], "bubble_radius": 24},
    images={
        "c_farhod": "CHAR: Young Uzbek programmer Farhod, 26, messy black hair, black t-shirt, hoodie around shoulders, tired red eyes, holding a laptop, grinning stubbornly, half body.",
        "c_farhod_hayron": "CHAR: Same young man as in the reference image (Farhod, messy black hair, black t-shirt), shocked face, eyes wide, pointing at himself, half body.",
        "c_farhod_kulgan": "CHAR: Same young man as in the reference image (Farhod, messy black hair, black t-shirt), refreshed happy smile, clear eyes, giving a thumbs up, half body.",
        "c_dilorom": "CHAR: Uzbek woman ophthalmologist Dilorom, 50, white doctor's coat, stethoscope, reading glasses pulled down to the tip of her nose, kind but strict look, half body.",
        "c_nilufar": "CHAR: Uzbek young woman Nilufar, 19, ponytail, pastel pajamas, worried face with hands on her cheeks, half body.",
        "p_taymer": "PROP: a round white kitchen timer, realistic, simple.",
        "01": "SCENE: Evening home office, young Uzbek programmer (26, messy black hair, black t-shirt) staring at three bright monitors with lines of code, red tired eyes, an empty energy drink can and a cold cup of tea on the desk.",
        "02": "SCENE: 2 AM, the same young man on a sofa with a laptop on his knees and a phone in his hand at the same time, screen light on his face, blanket, dim lamp.",
        "02_b": "EDIT 02: Only one small change: his eyes are now very red and one eyelid is twitching, comic exaggeration.",
        "03": "SCENE: Doorway of the living room, his younger sister (19, ponytail, pastel pajamas) pointing at him in shock, the young man on the sofa with laptop, dim night light.",
        "04": "SCENE: Bright clean ophthalmologist's office, an eye chart on the wall (abstract shapes, no readable text), a woman doctor of 50 in a white coat lowering her glasses to the tip of her nose looking at the young man sitting in the patient chair.",
        "07": "SCENE: The young man in the doctor's office looking stunned, the woman doctor holding up a small round kitchen timer, bright clinic light.",
        "08": "SCENE: Bright day, the young man standing at an open window, looking far away and smiling, on the opposite balcony a fluffy cat sits in the sun among flower pots, city trees.",
    },
    scenes=[
        S("bekzod", "Ha, siz. Hozir shu videoni ko'rayotgan siz. Oxirgi marta qachon ko'zingizni qirpdingiz? Farhod ham buni eslay olmaydi.", "mystery", "01.jpg",
          [pill("KO'Z ENERGIYASI: 12%", bg="crimson", x=540, y=300, at="qirpdingiz"), char("c_farhod.jpg", "right", x=820, h=700, at="Farhod", talk=False, label="FARHOD", label_bg="royal")]),
        S("sardor", "[tired] [laughs] Yana bitta qism, keyin uxlayman. Kodni tugataman, keyin seriyani tugataman, keyin... qaysi seriya edi o'zi?", "groove", "02.jpg",
          [clock("SESHANBA", "02:40"), bubble("FARHOD", y=620, hl={"Yana": "red", "bitta": "red"}, tagc="royal")], img2="02_b.jpg", img2_at="keyin..."),
        S("dilnoza", "[worried] Aka, ko'zingiz quyonnikidek qizarib ketibdi-ku! Ertaga shifokorga boramiz, gap tamom!", "tense", "03.jpg",
          [bubble("NILUFAR", hl={"quyonnikidek": "red"}, tagc="purple"), char("c_nilufar.jpg", "left", x=260, h=680, at=0.2, label="SINGLISI", label_bg="purple")]),
        S("bekzod", "Ertasi kuni ko'z shifokori Dilorom opa uni ko'rib, ko'zoynagini sekin burnining uchiga tushirdi.", "mystery", "04.jpg",
          [char("c_dilorom.jpg", "right", x=810, h=720, at="Dilorom", talk=False, label="DILOROM OPA", label_bg="green")]),
        S("nodira", "[sighs] O'g'lim, ekranga tikilganda odam kamroq qirpadi va ko'z quriydi. Har yigirma daqiqada yigirma soniya uzoqqa qarab turish kerak.", "warm", "04.jpg",
          [bubble("DILOROM OPA", hl={"yigirma": "red"}, tagc="green"), char("c_dilorom.jpg", "right", x=810, h=720, at=0.1)]),
        S("bekzod", "Bu shifokorning o'ylab topgani emas. Amerika Oftalmologiya Akademiyasi ham «yigirma-yigirma-yigirma» qoidasini tavsiya qiladi.", "mystery", None,
          [prop("p_taymer.jpg", x=540, y=560, h=380, at=0.2, motion="bounce"),
           card("Amerika Oftalmologiya Akademiyasi", ["20 - 20 - 20", "QOIDASI"], "Har 20 daqiqada 20 soniya 6 metr uzoqqa qarang.", at="Akademiyasi", y=1300)],
          bg="blueprint", bg_color=[0, 92, 96]),
        S("sardor", "[surprised] Yigirma daqiqada bir marta? Opa, men yigirma daqiqada faqat bitta reels ko'rib ulguraman-ku!", "groove", "07.jpg",
          [char("c_farhod_hayron.jpg", "left", x=250, h=660, at=0.1), bubble("FARHOD", y=330, hl={"reels": "red"}, tagc="royal")]),
        S("bekzod", "[chuckles] Bir haftadan keyin Farhod derazadan uzoqqa qaradi va qo'shnisining mushugini birinchi marta ko'rdi. Mushuk u yerda uch yildan beri yasharkan.", "warm", "08.jpg",
          [note("Mushuk uch yildan beri o'sha yerda ekan.", at="Mushuk"), char("c_farhod_kulgan.jpg", "left", x=240, h=600, at="birinchi", talk=False)]),
        S("bekzod", "Endi navbat sizga: hozir yigirma soniya uzoqqa qarang. Keyin izohda yozing — nimani ko'rdingiz?", "finale", "08.jpg",
          [final(["20 SONIYA", "UZOQQA QARANG!"])]),
    ],
    caption="Uch soatdan beri ekranga tikilib, bir marta ham ko'z qirpmagan odam — bu siz 👀😅\n\nHozir 20 soniya uzoqqa qarang — nimani ko'rdingiz? 👇\n\n#99foiz #salomatlik #koz #maslahat #telefon #ozbekcha #uzbekistan #reels",
)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    for name, j in JOBS.items():
        d = os.path.join(base, name); os.makedirs(d + "/img", exist_ok=True); os.makedirs(d + "/aud", exist_ok=True)
        scenes = []
        for k, sc in enumerate(j["scenes"]):
            sc = dict(sc); sc["vo"] = f"vo_{k + 1:02d}.mp3"; sc["voice_id"] = CAST[sc["speaker"]]
            if sc["img"] is None: sc.pop("img")
            scenes.append(sc)
        out = {"title": j["title"], "music_seed": j["music_seed"], "cover_title": j["cover_title"], "cover_sub": j["cover_sub"],
               "cover_scene": j["cover_scene"], "anim": "static", "bright": True, "theme": j["theme"], "scenes": scenes}
        json.dump(out, open(d + "/scenes.json", "w"), ensure_ascii=False, indent=1)
        json.dump({"images": j["images"], "hero": j["hero"], "opening": j["opening"], "design": j["design"]}, open(d + "/images.json", "w"), ensure_ascii=False, indent=1)
        json.dump({"slot": j["slot"], "title": j["title"], "theme": j["theme_cat"], "trial": False, "schedulingType": "automatic",
                   "mode": "customScheduled", "caption": j["caption"]}, open(d + "/post.json", "w"), ensure_ascii=False, indent=1)
        words = sum(len(s["text"].split()) for s in scenes)
        print(name, len(scenes), "sahna", words, "so'z ~", round(words / 2.3), "s", len(j["images"]), "rasm")
