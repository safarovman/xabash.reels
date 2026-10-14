# -*- coding: utf-8 -*-
"""5 ta video: 15/16-oktabr, yangi slotlar (08:00 o'tmish, 12:30 hozir, 16:00 kelajak-trial, 18:30 urf-odat, 21:00 xatolar).
Har sahna = bitta gapiruvchi (speaker) -> o'z ElevenLabs ovozi. Rasm: Google Flow. 2-kadr faqat 1-2 sahnada (img2)."""
import json, os

VOICES = {  # ElevenLabs premade/workspace voices (creative_list_voices dan)
    "bekzod": "kGOig3GPePLxobJGHo2M",   # chuqur erkak (rovi/erkak qahramon)
    "bill": "pqHfZKP75CvOlQylNhV4",     # keksa erkak (bobo, ota)
    "charlie": "IKne3meq5aSn9XLyUdCD",  # yosh yigit
    "sarah": "EXAVITQu4vr4xnSDxMaL",    # yosh ayol
    "lily": "pFZP5JQG7iQjIQuC4Bku",     # o'rta yosh ayol (ona, buvi)
    "jessica": "r1KmysJdVYZjJCm4mL3b",  # quvnoq yosh qiz
}

def S(speaker, text, mood, img, elements=None, **kw):
    d = {"speaker": speaker, "text": text, "mood": mood, "img": img, "elements": elements or []}
    d.update(kw); return d

def note(t, y=1500, at="start", size=76, rot=-2): return {"type": "note", "text": t, "y": y, "size": size, "rot": rot, "at": at}
def stamp(t, y=1560, at="end", rot=-5, size=None):
    d = {"type": "stamp", "text": t, "y": y, "rot": rot, "at": at}
    if size: d["size"] = size
    return d
def sticker(lines, color="yellow", x=760, y=420, w=420, at="start", rot=4, size=58):
    return {"type": "sticker", "lines": lines, "color": color, "x": x, "y": y, "w": w, "size": size, "rot": rot, "at": at}
def pill(t, bg="navy", x=540, y=360, at="start", rot=-3, fg="white"): return {"type": "pill", "text": t, "bg": bg, "fg": fg, "x": x, "y": y, "rot": rot, "at": at}
def card(kicker, title, sub, at=0.3, y=None):
    d = {"type": "card", "kicker": kicker, "title": title, "sub": sub, "at": at}
    if y: d["y"] = y
    return d
def big(t, y=1450, at="end", color=None):
    d = {"type": "big", "text": t, "y": y, "at": at}
    if color: d["color"] = color
    return d
def dark(a=0.4): return {"type": "dark", "amount": a, "at": "start"}
def final(lines): return {"type": "final", "lines": lines, "at": 0.4}

JOBS = {}

# ---------------- 08:00 O'TMISH ----------------
JOBS["2026-10-16_0800_xating-pochtada"] = dict(
    slot="2026-10-16T08:00+05:00", theme="o'tmish", trial=False,
    title="Xating hali pochtada", music_seed=31,
    cover_title=["XATING HALI", "POCHTADA"], cover_sub="ikki hafta va bir soniya", cover_scene=1,
    hero="Rahim bobo (70, oq do'ppi, kulrang soqol) + nevarasi Shoxrux (15) + Oysha buvi",
    opening="savol bilan",
    images={
        "01": "Modern Uzbek living room, evening. A 15-year-old Uzbek boy Shoxrux with messy black hair, green hoodie, holding a smartphone toward the camera with an impatient face; behind him on a sofa his grandfather sits calmly drinking tea from a piyola. Warm lamp light, teal and orange palette.",
        "02": "Elderly Uzbek grandfather Rahim, about 70, white embroidered doppi skullcap, neat grey beard, brown cardigan over a white shirt, laughing kindly and holding up an old yellowed paper envelope with stamps, sitting on a sofa in a cozy Uzbek living room.",
        "03": "1970s Uzbek village street in summer: a mail carrier on a bicycle with a leather bag delivers a letter, children and neighbors in traditional clothes come out of wooden gates to look; poplar trees, adobe walls, golden nostalgic light, sepia and ochre palette.",
        "04": "Same elderly grandmother: an elderly Uzbek woman Oysha, about 68, white headscarf, atlas-patterned dress, sitting by a window holding a bundle of old letters tied with a ribbon, smiling with tears of joy. Soft morning light, warm pastel palette.",
        "05": "The 15-year-old Uzbek boy Shoxrux in a green hoodie typing extremely fast on his smartphone with both thumbs, cartoon emoji speech bubbles flying around him, comic energy, bright modern bedroom.",
        "06": "Close-up of a 1990s grey mobile phone with a tiny monochrome green screen glowing in the dark, on a wooden desk with an old desktop computer, dramatic spotlight, dark blue background.",
        "07": "Elderly Uzbek grandfather Rahim with white doppi and grey beard, reading glasses on the tip of his nose, holding a big smartphone at arm's length and pressing the screen with one finger very carefully, concentrated funny face, sitting on a sofa.",
        "07_b": "SMALL CHANGE: same picture, but now the grandfather lifts the phone to his mouth and is coughing into it, eyes squeezed shut.",
        "08": "Whole Uzbek family laughing together on a tapchan in a courtyard at evening: grandfather in white doppi, grandmother in white headscarf and the teenage boy in a green hoodie showing the phone, tea and bread on the dastarkhan, string lights, warm golden palette.",
    },
    scenes=[
        S("charlie", "Bobo, sizga ertalab yozgan edim-ku! Ikki soat o'tdi, nega hali ham javob yo'q?", "groove", "01.jpg",
          [note("Ikki soat o'tdi, javob yo'q!", y=1480, at="ikki soat")]),
        S("bill", "Ex bolam, mening vaqtimda xat yozardik. Javobini ikki hafta kutardik, va hech kim xafa bo'lmasdi!", "warm", "02.jpg",
          [stamp("IKKI HAFTA!", at="ikki hafta", y=1540)]),
        S("bekzod", "Ellik yil oldin Rahim bobo shahardan qishloqqa xat jo'natardi. Pochtachi velosipedda kelsa, butun mahalla ko'chaga chiqardi.", "warm", "03.jpg",
          [pill("ELLIK YIL OLDIN", bg="orange", y=330, at="start")]),
        S("lily", "O'sha xatlarni hali ham saqlab qo'yganman. Har biri bir hafta yo'l yurgan, lekin bir umr esda qoldi.", "warm", "04.jpg",
          [note("Har bir xat bir umr esda qoladi.", y=1500, at="bir umr")]),
        S("charlie", "Hozir xabar bir soniyada yetib boradi. Lekin baribir hech kim javob bermaydi!", "groove", "05.jpg",
          [pill("BIR SONIYADA YETADI", bg="royal", y=380, at="bir soniyada"), stamp("JAVOB YO'Q!", at="javob bermaydi")]),
        S("bekzod", "Bilasizmi, dunyodagi birinchi SMS ming to'qqiz yuz to'qson ikkinchi yil, uchinchi dekabrda yuborilgan. Unda atigi ikki so'z bor edi: «Merry Christmas».", "mystery", "06.jpg",
          [dark(0.35), card("Fakt · History.com", ["BIRINCHI SMS", "1992-YIL"], "Uni 22 yoshli muhandis Nil Papvort yuborgan.", at="birinchi SMS")]),
        S("bill", "Mayli, men ham yozay. Qaysi tugmani bossam, xat ketadi? Shu qizil tugmami, yo yashilimi?", "groove", "07.jpg",
          [sticker(["Qaysi tugma", "xat yuboradi?"], color="yellow", x=760, y=420, at="qaysi")], img2="07_b.jpg", img2_at="qizil"),
        S("charlie", "Bobo, siz menga ovozli xabar yubordingiz. Uch daqiqa! Faqat yo'talgansiz!", "groove", "07_b.jpg",
          [stamp("Uch daqiqa yo'tal keldi!", at="yo'talgansiz", y=1520)], no_img2=True),
        S("bekzod", "Xat ikki haftada kelardi, lekin sog'inch bilan o'qilardi. Siz oxirgi marta qachon qo'lda xat yozgansiz?", "finale", "08.jpg",
          [final(["OXIRGI XATNI", "QACHON YOZGANSIZ?"])]),
    ],
    caption=("«Bobo, nega javob yozmadingiz?» — «Ex bolam, mening vaqtimda bitta xatga ikki hafta javob kutardik!» ✉️😄\n\n"
             "Pochtachi velosipedda kelsa, butun mahalla ko'chaga chiqardi. Hozir xabar bir soniyada yetadi — lekin baribir hech kim javob bermaydi 😅\n\n"
             "Fakt: dunyodagi birinchi SMS 1992-yil 3-dekabrda yuborilgan — «Merry Christmas» (History.com).\n\n"
             "Siz oxirgi marta qachon qo'lda xat yozgansiz? 👇\n\n"
             "#99foiz #otmish #xat #pochta #bobom #nostalgiya #sms #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #reels #reelsuz #uzbekreels"),
)

# ---------------- 12:30 HOZIRGI ZAMON ----------------
JOBS["2026-10-15_1230_savatcha"] = dict(
    slot="2026-10-15T12:30+05:00", theme="hozirgi zamon", trial=False,
    title="Savatchada 47 ta narsa", music_seed=44,
    cover_title=["SAVATCHADA", "47 TA NARSA"], cover_sub="sotib olingani — nol", cover_scene=0,
    hero="Kamola (28, dizayner, sariq sviter, ko'zoynaksiz, qora soch turmak) + eri Bekzod + kuryer",
    opening="birinchi shaxs",
    images={
        "01": "Young Uzbek woman Kamola, 28, graphic designer, mustard-yellow knitted sweater, black hair in a messy bun, lying on a sofa holding a smartphone showing an online shopping cart full of items, guilty happy smile. Bright modern apartment, mint and mustard palette.",
        "02": "Close-up of a smartphone screen held by a woman's hand with a mustard sleeve, showing a shopping cart app with product thumbnails: a lamp, a dress, a plant, sneakers, a red badge with many items; cozy blurred background.",
        "03": "Uzbek man Bekzod, 30, short beard, grey t-shirt, standing in a doorway holding a cup of tea, raising one eyebrow skeptically, looking toward the sofa. Bright modern apartment, mint palette.",
        "04": "Young Uzbek woman Kamola in a mustard sweater, black hair bun, hugging her smartphone to her chest dramatically with closed eyes, like protecting a treasure, sitting on a sofa, comic expression.",
        "05": "Surreal night scene: dozens of empty abandoned shopping carts standing alone on an empty city street under streetlights, light fog, deep blue and violet palette, mysterious mood.",
        "06": "Apartment front door opened: a cheerful young Uzbek courier with a cap and orange jacket holding a big stack of delivery boxes, Kamola in a mustard sweater standing surprised in the doorway.",
        "06_b": "SMALL CHANGE: same picture, but the courier now winks and gives a thumbs up, the boxes slightly tilted.",
        "07": "Living room full of opened delivery boxes: Kamola in mustard sweater holding a new lamp with shocked joyful face, her husband with short beard and grey t-shirt grinning beside her holding an empty wallet turned upside down.",
        "08": "Evening, Kamola in a mustard sweater sitting on the sofa among the new things, secretly adding a new item to the cart on her phone with a sly smile, warm lamp light.",
    },
    scenes=[
        S("sarah", "Mening savatchamda qirq yetti ta narsa bor. Sotib olganim esa — nol. Lekin men ularni har kuni ko'rib, ko'nglimni ko'taraman.", "groove", "01.jpg",
          [big("47 TA", y=430, at="qirq yetti"), note("Sotib olinganlari — nol.", y=1500, at="nol")]),
        S("sarah", "Mana bu chiroq uch oydan beri shu yerda yotibdi. Ko'ylakni to'yga deb qo'shgandim, to'y ham o'tib ketdi.", "groove", "02.jpg",
          [note("To'y o'tib ketdi, ko'ylak savatda qoldi.", y=1480, at="to'y ham")]),
        S("bekzod", "Kamola, yana savatchaga nimadir qo'shdingmi? U yer allaqachon bizning ikkinchi uyimizga aylandi-ku!", "groove", "03.jpg",
          [sticker(["Savatcha —", "ikkinchi uyimiz!"], color="pink", x=300, y=420, at="ikkinchi")]),
        S("sarah", "Men sotib olmayapman, Bekzod. Men shunchaki saqlab qo'yyapman. Bu butunlay boshqa narsa!", "groove", "04.jpg",
          [stamp("Bu xarid emas!", at="boshqa narsa", y=1540)]),
        S("sarah", "Keyin bildimki, men yolg'iz emasman ekan. Hisob-kitoblarga ko'ra, onlayn xaridorlarning yetmish foizi savatchani to'ldiradi-yu, to'lamay ketadi.", "mystery", "05.jpg",
          [dark(0.35), card("Baymard Institute", ["70%", "SAVATCHA"], "Har o'nta savatchadan yettitasi to'lovsiz qoladi.", at="yetmish")]),
        S("sarah", "Bir kuni eshik qo'ng'irog'i chalindi. Men hech narsa buyurtma qilmagan edim-ku!", "tense", "06.jpg",
          [{"type": "ring", "x": 900, "y": 300, "at": "qo'ng'irog'i"}], no_img2=True),
        S("charlie", "Kamola opa, sizga buyurtma keldi! Eringiz savatchangizdagi hamma narsani to'lab qo'yibdi.", "hero", "06.jpg",
          [stamp("Hammasi to'landi!", at="to'lab", y=1540)], img2="06_b.jpg", img2_at="to'lab"),
        S("bekzod", "Endi ikkinchi uyimiz bo'shadi, azizim. Lekin kartam ham bo'shab qoldi.", "groove", "07.jpg",
          [note("Karta ham bo'shab qoldi.", y=1500, at="kartam")]),
        S("sarah", "Xavotir olmang, savatcham yana to'lyapti. Sizning savatchangizda nechta narsa yotibdi?", "finale", "08.jpg",
          [final(["SAVATCHANGIZDA", "NECHTA NARSA BOR?"])]),
    ],
    caption=("«Savatchamda 47 ta narsa bor. Sotib olganim — nol.» 🛒😅\n\n"
             "Chiroq uch oydan beri yotibdi, ko'ylak to'yga deb qo'shilgan — to'y ham o'tib ketdi. Bu xarid emas, bu… saqlab qo'yish!\n\n"
             "Fakt: Baymard Institute hisobiga ko'ra, onlayn xaridorlarning ~70% i savatchani to'lamay tashlab ketadi.\n\n"
             "Sizning savatchangizda nechta narsa bor? Izohda raqam yozing 👇\n\n"
             "#99foiz #onlaynxarid #savatcha #shopping #oila #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #kulgu #reels #reelsuz #uzbekreels #pul"),
)

# ---------------- 16:00 KELAJAK (TRIAL) ----------------
JOBS["2026-10-15_1600_2050-yil"] = dict(
    slot="2026-10-15T16:00+05:00", theme="kelajak", trial=True,
    title="2050-yil: bir kunlik hayot", music_seed=58,
    cover_title=["2050-YIL:", "BIR KUNLIK HAYOT"], cover_sub="robot nonushta, uchuvchi taksi", cover_scene=1,
    hero="Akmal (40, 2050-yildagi ota, kumush kurtka) + otasi (75, do'ppi) + uy roboti",
    opening="tomoshabinga murojaat",
    images={
        "01": "Year 2050, futuristic bright Tashkent apartment at sunrise, smart glass windows showing Tashkent TV tower among green skyscrapers; a friendly white humanoid home robot opens the curtains while Uzbek man Akmal, 40, short black hair, neat stubble, wakes up in bed stretching. Clean white, mint and warm gold palette.",
        "02": "Year 2050 kitchen: friendly white humanoid robot with a soft blue face screen, wearing a colorful Uzbek atlas-pattern apron, serving breakfast with non bread, tea and a cup of coffee on a modern table, futuristic but cozy.",
        "02_b": "SMALL CHANGE: same picture, but the robot now winks with its screen face and gives a thumbs up.",
        "03": "Elderly Uzbek man, about 75, white embroidered doppi skullcap, grey mustache, modern grey cardigan, sitting at a futuristic breakfast table holding a round traditional non bread and frowning skeptically at a humanoid robot, year 2050, comic expression.",
        "04": "Wide illustration: a long row of many different humanoid robots silhouetted in a huge bright futuristic factory hall, assembly lights, blue and silver palette, sense of scale.",
        "05": "Year 2050, a sleek white electric air taxi with several rotors flying over Tashkent with the Tashkent TV tower and green parks below, morning sky; inside the window Uzbek man Akmal, 40, in a silver jacket, smiling; small delivery drones around.",
        "06": "Rooftop air-taxi pad in 2050 Tashkent: elderly Uzbek man in white doppi and grey cardigan raising his arm high and waving at the sky like stopping a street taxi, an air taxi hovering above, his son in a silver jacket laughing next to him.",
        "07": "Year 2050 family dinner in a modern Uzbek home: elderly father in white doppi proudly serving plov from a big kazan, son Akmal in a silver jacket, his wife and kids around a dastarkhan, a humanoid robot politely holding a plate, warm evening light, cozy.",
    },
    scenes=[
        S("bekzod", "Tasavvur qiling: ikki ming ellikinchi yil, ertalab soat yetti. Meni budilnik emas, uy roboti uyg'otadi.", "hero", "01.jpg",
          [pill("2050-YIL · 07:00", bg="royal", y=330, at="start"), note("Meni uy roboti uyg'otadi.", y=1500, at="robot")]),
        S("sarah", "Xayrli tong, Akmal aka! Nonushta tayyor, qahvangiz iliq. Otangiz esa ertalabdan beri men bilan bahslashyapti.", "groove", "02.jpg",
          [sticker(["Nonushta", "tayyor!"], color="blue", x=780, y=420, at="nonushta")], img2="02_b.jpg", img2_at="otangiz"),
        S("bill", "Ex bolam, mening vaqtimda nonni tandirdan o'zimiz uzardik! Bu temir bola non ushatishni ham bilmaydi-ya.", "groove", "03.jpg",
          [stamp("Mening vaqtimda boshqacha edi!", at="mening vaqtimda", y=1540)]),
        S("bekzod", "Bu shunchaki xayol emas. Morgan Stanley tahlilchilari ikki ming ellikinchi yilga borib dunyoda bir milliarddan ortiq insonsimon robot ishlashini taxmin qilishmoqda.", "mystery", "04.jpg",
          [dark(0.35), card("Morgan Stanley prognozi", ["1 MILLIARD", "ROBOT"], "2050-yilda insonsimon robotlar soni milliarddan oshishi mumkin.", at="Morgan")]),
        S("bekzod", "Ishga uchuvchi taksida boraman. Tirbandlik yo'q, faqat qo'shnining dronini aylanib o'tamiz. Aytgancha, Dubayda bunday taksilar allaqachon sinovdan o'tyapti.", "hero", "05.jpg",
          [pill("UCHUVCHI TAKSI", bg="green", y=330, at="uchuvchi"), note("Tirbandlik yo'q, faqat dronlar bor.", y=1500, at="tirbandlik")]),
        S("bill", "Mening vaqtimda taksini qo'l ko'tarib to'xtatardik. Endi qo'limni qayerga ko'taray, osmongami?!", "groove", "06.jpg",
          [note("Taksini osmondan to'xtataman!", y=1500, at="osmongami")]),
        S("sarah", "Ota, qo'lingizni tushiring. Taksi sizni yuzingizdan taniydi, pulini ham o'zi yechib oladi.", "groove", "06.jpg",
          [stamp("Taksi yuzingizni taniydi!", at="yuzingizdan", y=1540)]),
        S("bekzod", "Texnologiya qanchalik o'zgarmasin, kechqurun hammamiz baribir bitta dasturxonga yig'ilamiz. Oshni esa hali ham otam damlaydi.", "warm", "07.jpg",
          [note("Oshni hali ham otam damlaydi.", y=1500, at="oshni")]),
        S("bekzod", "Sizningcha, ikki ming ellikinchi yilda qaysi texnologiya hammadan oldin hayotimizga kiradi?", "finale", "07.jpg",
          [final(["2050-YILDA QAYSI", "TEXNOLOGIYA KELADI?"])]),
    ],
    caption=("Tasavvur qiling: 2050-yil, soat 07:00. Sizni budilnik emas, uy roboti uyg'otadi 🤖☕\n\n"
             "Nonushtani robot tayyorlaydi, ishga uchuvchi taksida borasiz, otangiz esa osmonga qo'l ko'tarib taksi to'xtatmoqchi 😄 Lekin oshni baribir otam damlaydi!\n\n"
             "Fakt: Morgan Stanley prognoziga ko'ra, 2050-yilga kelib dunyoda 1 milliarddan ortiq insonsimon robot ishlashi mumkin. Uchuvchi taksilar esa Dubayda allaqachon sinovdan o'tmoqda (Joby).\n\n"
             "Sizningcha, qaysi texnologiya birinchi keladi? 👇\n\n"
             "#99foiz #kelajak #2050 #robot #texnologiya #suniyintellekt #uchuvchitaksi #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #reels #reelsuz #uzbekreels"),
)

JOBS["2026-10-15_1830_yarim-piyola"] = dict(
    slot="2026-10-15T18:30+05:00", theme="urf-odatlar", trial=False,
    title="Nega piyolam yarim?", music_seed=67,
    cover_title=["NEGA PIYOLAM", "YARIM?"], cover_sub="choy odobi — mehr bilan", cover_scene=1,
    hero="amerikalik sayyoh Jon (30, malla soch, sepkil, ko'k kepka) + Karim ota (72, to'n, salla-do'ppi) + qizi Zarina (tarjimon)",
    opening="epik ilmoq",
    images={
        "01": "Samarkand courtyard at golden sunset with blue tiled domes in the distance, a vine-covered tapchan with a dastarkhan of bread, fruit and teapot; a tall American tourist John, 30, ginger hair, freckles, blue cap, sitting cross-legged awkwardly holding a piyola, wide-eyed. Warm gold and turquoise palette, epic composition.",
        "02": "Close-up of the American tourist John with ginger hair, freckles and blue cap looking sadly and confused at a blue-and-white cotton-pattern piyola only half full of green tea, Uzbek dastarkhan background.",
        "03": "Young Uzbek woman Zarina, 25, long black braid, burgundy atlas dress with a light cardigan, smiling warmly and explaining with an open hand gesture, sitting on a tapchan in a courtyard with vines.",
        "04": "Elderly Uzbek man Karim ota, 72, white beard, striped chapan robe and black-white doppi, pouring green tea from a piyola back into a ceramic teapot with a high thin stream, calm wise smile, sunlit courtyard.",
        "04_b": "SMALL CHANGE: same picture, but the old man now lifts the teapot higher and the tea stream is longer, he winks.",
        "05": "Still life close-up: blue-and-white Uzbek cotton-pattern teapot and several half-filled piyolas with green tea and steam on a red dastarkhan with non bread, dramatic warm light, dark background.",
        "06": "The American tourist with ginger hair and blue cap happily holding up an empty piyola while the old Uzbek man in striped chapan pours him more tea, both laughing, courtyard at dusk.",
        "07": "Night courtyard with string lights: the American tourist with ginger hair leaning back on cushions with a full belly surrounded by many empty piyolas, the old man and young woman laughing, cozy and funny.",
    },
    scenes=[
        S("bekzod", "Jon Amerikadan Samarqandga keldi. U hayotida birinchi marta haqiqiy o'zbek dasturxoniga o'tirdi.", "hero", "01.jpg",
          [pill("SAMARQAND", bg="royal", y=330, at="Samarqandga")]),
        S("charlie", "Kechirasiz, nega mening piyolam yarimta? Men sizlarga yoqmay qoldimmi?", "sad", "02.jpg",
          [note("Nega mening piyolam yarimta?", y=1500, at="yarimta")]),
        S("sarah", "Yo'q, Jon, aksincha! Yarim piyola — bu hurmat belgisi. To'la piyola esa «tezroq ichib, keting» degani bo'lib qolishi mumkin.", "warm", "03.jpg",
          [sticker(["Yarim piyola —", "hurmat belgisi."], color="green", x=760, y=420, at="hurmat")]),
        S("bill", "Choy avval uch marta qaytariladi, o'g'lim. Piyoladan choynakka, choynakdan piyolaga. Shunda choy damlanadi, unga mehr ham qo'shiladi.", "warm", "04.jpg",
          [stamp("Uch marta qaytariladi!", at="uch marta", y=1540)], img2="04_b.jpg", img2_at="choynakdan"),
        S("bekzod", "Bu odatning sababi oddiy: yarim piyola qo'lni kuydirmaydi, choy sovimaydi, mezbon esa har safar yangi choy quyib, e'tibor ko'rsatadi.", "mystery", "05.jpg",
          [dark(0.35), card("O'zbek choy odobi", ["YARIM", "PIYOLA"], "Mezbon har gal yangi choy quyib, hurmat ko'rsatadi.", at="sababi")]),
        S("charlie", "Demak, piyolam bo'shashi bilan yana quyib berasizmi? Bu ajoyib odat-ku!", "groove", "06.jpg",
          [note("Bo'shashi bilan yana quyiladi.", y=1500, at="yana quyib")]),
        S("bill", "Albatta! Faqat bitta qoida bor: choy tugamaydi, mehmon ham ketolmaydi!", "groove", "06.jpg",
          [stamp("Choy tugamaydi!", at="choy tugamaydi", y=1540)]),
        S("sarah", "Jon o'sha kechasi o'ttiz ikki piyola choy ichdi. Lekin baribir «yana bittagina» dedi.", "groove", "07.jpg",
          [big("32 PIYOLA", y=430, at="o'ttiz ikki")]),
        S("bekzod", "Choy o'zbek uchun shunchaki ichimlik emas, bu ochiq yurak. Sizning uyingizda choy necha marta qaytariladi?", "finale", "01.jpg",
          [final(["SIZDA CHOY NECHA", "MARTA QAYTARILADI?"])]),
    ],
    caption=("Amerikalik mehmon Jon xafa bo'ldi: «Nega menga choyni yarimta quyishdi?» 🫖😄\n\n"
             "Yarim piyola — hurmat belgisi: qo'l kuymaydi, choy sovimaydi, mezbon esa har gal yangi choy quyib, e'tibor ko'rsatadi. Choy avval uch marta qaytariladi ❤️\n\n"
             "Sizning uyingizda choy necha marta qaytariladi? 👇\n\n"
             "#99foiz #urfodat #choy #piyola #mehmondostlik #samarqand #dasturxon #ozbekcha #ozbekiston #uzbekistan #toshkent #reels #reelsuz #uzbekreels #madaniyat"),
)

# ---------------- 21:00 XATOLAR ----------------
JOBS["2026-10-15_2100_parolim-123456"] = dict(
    slot="2026-10-15T21:00+05:00", theme="ko'p uchraydigan xatolar", trial=False,
    title="Parolim 123456", music_seed=73,
    cover_title=["PAROLIM", "123456"], cover_sub="juda «murakkab» parol", cover_scene=1,
    hero="Bahodir aka (50, sartarosh, mo'ylov, oq xalat) + qizi Sevara (dasturchi, ko'zoynak) + mijoz",
    opening="dialog bilan",
    images={
        "01": "Small Uzbek barbershop interior: barber Bahodir, 50, thick black mustache, round belly, white barber coat, holding scissors and a comb; his daughter Sevara, 24, round glasses, ponytail, denim jacket, sitting with an open laptop beside the mirror. Mint green walls, retro barber chair, warm light.",
        "02": "Uzbek barber Bahodir, 50, thick black mustache, white barber coat, raising one finger proudly with a very confident grin, scissors in the other hand, barbershop mirror behind.",
        "03": "A young Uzbek man client sitting in a retro barber chair with a funny half-finished haircut, cape around his neck, laughing and pointing at himself, barbershop mirror.",
        "04": "Young Uzbek woman Sevara, 24, round glasses, ponytail, denim jacket, facepalming with one hand while holding a laptop, exasperated comic expression, barbershop background.",
        "04_b": "SMALL CHANGE: same picture, but she now peeks through her fingers with one eye open, shaking her head.",
        "05": "Dark dramatic illustration: a giant padlock made of the digits 1 2 3 4 5 6 cracking and breaking apart, a shadowy hooded figure with a laptop behind it, red and dark blue palette.",
        "06": "Uzbek barber Bahodir, 50, mustache, white coat, scratching his head while thinking hard, eyes looking up, a calendar with his birthday circled on the wall behind him, barbershop.",
        "07": "Young Uzbek woman Sevara with round glasses and denim jacket teaching her father, pointing at a notebook page where three doodles are drawn: scissors, a teapot and a rain cloud; father with mustache listening attentively.",
        "08": "Uzbek barber Bahodir with mustache and white coat proudly writing on a big paper poster taped to the barbershop wall with a marker, very satisfied smile, daughter in background horrified.",
    },
    scenes=[
        S("jessica", "Dada, telefoningizni yangilab qo'yay. Parolingizni ayting-chi, tez bitiraman.", "groove", "01.jpg",
          [note("Dada, parolingizni ayting-chi.", y=1500, at="parolingizni")]),
        S("bekzod", "Parolim juda murakkab, qizim. Hech kim topolmaydi: bir, ikki, uch, to'rt, besh, olti!", "groove", "02.jpg",
          [big("123456", y=430, at="bir, ikki")]),
        S("charlie", "Aka, meniki ham shunaqa! Faqat men oxiriga yettini qo'shib qo'yganman, xavfsizroq bo'lsin deb.", "groove", "03.jpg",
          [sticker(["Mening parolim:", "1234567"], color="yellow", x=760, y=420, at="yettini")]),
        S("jessica", "Voy, ikkalangiz ham dunyodagi eng mashhur parolni tanlabsiz-ku! Buni hamma biladi!", "tense", "04.jpg",
          [stamp("Eng mashhur parol shu!", at="eng mashhur", y=1540)], img2="04_b.jpg", img2_at="hamma"),
        S("jessica", "Tadqiqotlarga ko'ra, dunyoda eng ko'p ishlatiladigan parol aynan bir-ikki-uch-to'rt-besh-olti. Bunday parolni buzish uchun bir soniya ham kerak emas.", "mystery", "05.jpg",
          [dark(0.35), card("NordPass tadqiqoti", ["123456", "1 SONIYA"], "Eng mashhur parollar bir soniyadan tez buziladi.", at="eng ko'p")]),
        S("bekzod", "Unda boshqasini qo'yaman. Masalan, o'z ismim yoki tug'ilgan kunim. Buni hech kim o'ylamaydi!", "groove", "06.jpg",
          [note("Ism yoki tug'ilgan kun — xato!", y=1500, at="tug'ilgan")]),
        S("jessica", "Dada, ism ham, tug'ilgan kun ham bo'lmaydi. Uchta tasodifiy so'zni birlashtiring, masalan: qaychi, choynak, yomg'ir. Uzun parol — kuchli parol.", "warm", "07.jpg",
          [sticker(["Uchta tasodifiy so'z —", "kuchli parol."], color="green", x=540, y=380, w=520, at="uchta")]),
        S("bekzod", "Zo'r! Esdan chiqmasligi uchun uni katta qilib devorga yozib qo'yaman.", "groove", "08.jpg",
          [stamp("Parolni devorga yozmang!", at="devorga", y=1540)]),
        S("charlie", "Aka, endi butun mahalla parolingizni biladi. Sizning parolingiz qanchalik kuchli? Faqat izohda yozmang!", "finale", "03.jpg",
          [final(["PAROLINGIZ", "QANCHALIK KUCHLI?"])]),
    ],
    caption=("«Parolim juda murakkab: bir, ikki, uch, to'rt, besh, olti!» 🔐💈\n\n"
             "Mijoz esa «xavfsizroq» bo'lsin deb oxiriga 7 qo'shibdi 😅 Keyin ism, keyin tug'ilgan kun… va oxiri parol devorda!\n\n"
             "Fakt (NordPass): dunyodagi eng mashhur parol — 123456; eng mashhur parollar bir soniyadan tez buziladi. Maslahat: uchta tasodifiy so'zdan uzun parol qiling.\n\n"
             "Parolingiz qanchalik kuchli? (Faqat izohda yozmang! 😄) 👇\n\n"
             "#99foiz #parol #xavfsizlik #kiberxavfsizlik #telefon #sartarosh #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #kulgu #reels #reelsuz #uzbekreels"),
)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    for name, j in JOBS.items():
        d = os.path.join(base, name); os.makedirs(d + "/img", exist_ok=True); os.makedirs(d + "/aud", exist_ok=True)
        scenes = []
        for k, sc in enumerate(j["scenes"]):
            sc = dict(sc); sc["vo"] = f"vo_{k + 1:02d}.mp3"; sc["voice_id"] = VOICES[sc["speaker"]]; scenes.append(sc)
        out = {"title": j["title"], "music_seed": j["music_seed"], "cover_title": j["cover_title"], "cover_sub": j["cover_sub"],
               "cover_scene": j["cover_scene"], "anim": "static", "scenes": scenes}
        json.dump(out, open(d + "/scenes.json", "w"), ensure_ascii=False, indent=1)
        json.dump({"images": j["images"], "hero": j["hero"], "opening": j["opening"]}, open(d + "/images.json", "w"), ensure_ascii=False, indent=1)
        post = {"slot": j["slot"], "title": j["title"], "theme": j["theme"], "trial": j["trial"], "caption": j["caption"]}
        json.dump(post, open(d + "/post.json", "w"), ensure_ascii=False, indent=1)
        print(name, len(scenes), sum(len(s["text"].split()) for s in scenes), "words")
