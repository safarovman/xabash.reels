# -*- coding: utf-8 -*-
"""16-oktabr: 12:30 hozir, 16:00 kelajak-trial, 18:30 urf-odat, 21:00 xatolar (08:00 — plan_2026-10-15_v3 da).
Davomiylik 75-80 s (egasi tasdiqlagan). Helperlar plan_2026-10-15_v3.py dan."""
import json, os, importlib.util
_s = importlib.util.spec_from_file_location("v3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_2026-10-15_v3.py"))
v3 = importlib.util.module_from_spec(_s); _s.loader.exec_module(v3)
S, note, stamp, sticker, pill, card, big, dark, final, VOICES = v3.S, v3.note, v3.stamp, v3.sticker, v3.pill, v3.card, v3.big, v3.dark, v3.final, v3.VOICES

JOBS = {}

JOBS["2026-10-16_1230_dadam-oyinda"] = dict(
    slot="2026-10-16T12:30+05:00", theme="hozirgi zamon", trial=False,
    title="Dadam o'yinga qo'shildi", music_seed=81,
    cover_title=["DADAM", "O'YINGA QO'SHILDI"], cover_sub="soat 02:00, «snayper chapda!»", cover_scene=0,
    hero="o'g'il Sardor (17) + dadasi Anvar aka (48, qorin, mo'ylov, uy xalati) + onasi Gulnora opa",
    opening="cold open",
    images={
        "01": "Night, dark Uzbek apartment bedroom lit only by a glowing computer monitor: a middle-aged Uzbek father Anvar, 48, mustache, round belly, striped home robe, wearing a big gaming headset, leaning toward the screen and shouting excitedly, holding a controller; his teenage son Sardor, 17, in pajamas, standing shocked in the doorway. Blue and orange glow.",
        "02": "Daytime one week earlier: Uzbek father Anvar, 48, mustache, striped home robe, standing in his teenage son's messy gaming room with arms crossed, lecturing strictly, the son Sardor in a black t-shirt sitting at the computer rolling his eyes.",
        "03": "Teenage Uzbek boy Sardor, 17, black t-shirt, handing a game controller to his skeptical father Anvar with mustache and striped robe, both sitting on a sofa in front of a TV, father holding the controller upside down.",
        "04": "Uzbek father Anvar with mustache and striped robe completely absorbed in a video game on TV, eyes wide, tongue out in concentration, surrounded by empty tea piyolas and sunflower seed shells, clock on the wall showing late night.",
        "04_b": "SMALL CHANGE: same picture, but now the father jumps up from the sofa with both arms raised in victory, mouth open shouting.",
        "05": "Illustration of a huge crowd of diverse people of all ages around the world playing games on phones, consoles and computers, a globe in the background, colorful and energetic, sense of scale.",
        "06": "Uzbek mother Gulnora, 45, headscarf tied back, apron, standing in the living room doorway with a ladle in hand and a stern face, the father and son both frozen holding controllers on the sofa, comic scene.",
        "07": "Next morning breakfast table in an Uzbek kitchen: father Anvar with dark circles under his eyes yawning over tea, teenage son grinning at him, mother serving non bread and shaking her head with a smile.",
        "08": "Evening: mother Gulnora in headscarf now sitting between father and son on the sofa holding a game controller herself, all three laughing and playing together, warm family light.",
    },
    scenes=[
        S("bekzod", "Kecha soat ikkida xonadan baqiriq eshitildi: «Snayper! Chap tomonda! Qopqoqni yop!» Bu men emasdim. Bu dadam edi.", "tense", "01.jpg",
          [pill("SOAT 02:00", bg="crimson", y=330, at="start"), note("Baqirgan men emas, dadam edi.", y=1500, at="dadam")]),
        S("charlie", "Bir hafta oldin hammasi boshqacha edi. Dadam har kuni: «O'yin — vaqtni o'ldirish, kitob o'qi!» derdi.", "groove", "02.jpg",
          [note("Bir hafta oldin hammasi boshqacha edi.", y=1520, at="bir hafta")]),
        S("bekzod", "Ha, aytganman! O'yin — bekorchilik. Biz sening yoshingda tashqarida to'p tepib, daraxtga chiqardik.", "groove", "02.jpg",
          [stamp("O'yin — bekorchilik!", at="bekorchilik", y=1560)]),
        S("charlie", "Keyin men unga shunchaki bir marta urinib ko'rishni taklif qildim. U pultni teskari ushladi, lekin baribir rozi bo'ldi.", "groove", "03.jpg",
          [sticker(["Pult teskari,", "lekin rozi!"], color="yellow", x=780, y=1450, at="teskari")]),
        S("bekzod", "Faqat bitta raund, o'g'lim. Yana bittasi. Bu oxirgisi, haqiqatan oxirgisi! Kim meni otdi?!", "tense", "04.jpg",
          [note("«Bu oxirgisi» — o'ninchi marta.", y=1500, at="oxirgisi")], img2="04_b.jpg", img2_at="Kim meni"),
        S("charlie", "Bilasizmi, Newzoo hisobiga ko'ra dunyoda uch yarim milliarddan ortiq odam o'yin o'ynaydi. Demak, har ikki odamdan biri. Dadam endi shu yarmida.", "mystery", "05.jpg",
          [dark(0.35), card("Newzoo, 2025", ["3,58 MLRD", "O'YINCHI"], "Har ikki odamdan biri o'ynaydi.", at="Newzoo")]),
        S("lily", "Ikkalangiz ham hozir o'chirasizlar! Osh sovidi, choy muzladi, qo'shnilar esa kim urishyapti deb qo'ng'iroq qilishyapti!", "tense", "06.jpg",
          [stamp("Osh sovidi!", at="osh sovidi", y=1560)]),
        S("bekzod", "Ertalab dadam ko'zini ochib, birinchi bo'lib so'radi: «Kecha bizni kim yutdi? Revansh qachon?»", "groove", "07.jpg",
          [note("«Revansh qachon?»", y=1500, at="revansh")]),
        S("charlie", "Endi oyim ham qo'shildi. Uyimizda kitob o'qiydigan odam qolmadi. Sizning uyingizda kim eng ko'p o'ynaydi?", "finale", "08.jpg",
          [final(["SIZDA KIM", "KO'P O'YNAYDI?"])]),
    ],
    caption=("Kecha soat 2 da: «Snayper! Chap tomonda!» 🎮 Bu men emasdim — bu dadam edi 😅\n\n"
             "Bir hafta oldin u «o'yin — bekorchilik» derdi. Bitta raund… yana bitta… va endi revansh so'raydi. Oyim ham qo'shildi!\n\n"
             "Fakt: Newzoo hisobiga ko'ra 2025-yilda dunyoda 3,58 milliard o'yinchi bor — har ikki odamdan biri.\n\n"
             "Sizning uyingizda kim eng ko'p o'ynaydi? 👇\n\n"
             "#99foiz #oyin #gamer #dadam #oila #pubg #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #kulgu #reels #reelsuz #uzbekreels"),
)

JOBS["2026-10-16_1600_robotaksi"] = dict(
    slot="2026-10-16T16:00+05:00", theme="kelajak", trial=True,
    title="Haydovchisiz taksi bilan savdolashish", music_seed=92,
    cover_title=["ROBOTAKSI BILAN", "SAVDOLASHISH"], cover_sub="«Chorsugacha 15 ming bo'ladimi?»", cover_scene=1,
    hero="Muqaddas opa (55, gulli ro'mol, bozor sumkasi) + haydovchisiz taksi AI + qo'shnisi Dilfuza",
    opening="savol bilan",
    images={
        "01": "Near-future Tashkent street, 2035: a sleek white driverless robotaxi with no steering wheel and a glowing friendly light strip parked at the curb; an Uzbek woman Muqaddas opa, 55, colorful floral headscarf, cardigan, holding big market bags, peering into the empty driver seat suspiciously. Bright sunny day, green trees.",
        "02": "Inside the driverless robotaxi: Uzbek woman Muqaddas, 55, floral headscarf, sitting in the back seat with market bags, talking and gesturing to a small glowing screen with a cute digital face on the dashboard, no driver, no steering wheel.",
        "02_b": "SMALL CHANGE: same picture, but the woman now wags her finger at the screen and the screen face shows a confused expression.",
        "03": "Close-up of the robotaxi dashboard screen showing a cute glowing digital face with polite eyes and a fixed price tag icon, futuristic clean interior, soft blue light.",
        "04": "Infographic-style illustration: many white driverless robotaxis driving on a big American city street at dusk with glowing sensors on their roofs, calm and futuristic.",
        "05": "Uzbek woman Muqaddas, 55, floral headscarf, holding up a jar of homemade apricot jam toward the robotaxi screen, smiling cunningly, offering a deal, market bags beside her.",
        "06": "Robotaxi arriving at a busy Chorsu-like bazaar with a big blue dome market building; the Uzbek woman with floral headscarf getting out happily, her neighbor Dilfuza, 50, waiting with surprised face.",
        "07": "Two Uzbek women neighbors laughing together at the bazaar entrance, one with floral headscarf telling a story with big gestures, the robotaxi driving away with a tiny jar of jam on its roof.",
    },
    scenes=[
        S("lily", "Chorsugacha o'n besh mingga boramizmi, ukam? Ha, nega indamaysan? Rulda hech kim yo'q-ku!", "groove", "01.jpg",
          [pill("2035-YIL · TOSHKENT", bg="royal", y=330, at="start"), note("Rulda hech kim yo'q!", y=1500, at="hech kim")]),
        S("sarah", "Assalomu alaykum, men haydovchisiz taksiman. Chorsugacha narx — o'ttiz ikki ming so'm. Narx qat'iy.", "mystery", "02.jpg",
          [stamp("Narx qat'iy!", at="qat'iy", y=1560)], no_img2=True),
        S("lily", "Qat'iy? Bozorda hech narsa qat'iy emas, bolam. Yigirmaga bor, men doimiy mijozman!", "groove", "02.jpg",
          [sticker(["Bozorda hech narsa", "qat'iy emas!"], color="pink", x=760, y=1450, at="bozorda")], img2="02_b.jpg", img2_at="yigirmaga"),
        S("sarah", "Kechirasiz, savdolashish dasturimda yo'q. Lekin sizga musiqa qo'yib berishim mumkin.", "mystery", "03.jpg",
          [note("Savdolashish dasturda yo'q.", y=1500, at="savdolashish")]),
        S("bekzod", "Bu xayol emas. Amerikada haydovchisiz taksilar allaqachon haftasiga to'rt yuz mingdan ortiq pullik safar qilmoqda. Ertaga ular bizga ham keladi.", "mystery", "04.jpg",
          [dark(0.35), card("Waymo, 2026", ["400 000+", "SAFAR"], "Haftasiga haydovchisiz taksida.", at="Amerikada")]),
        S("lily", "Mayli, unda bunday qilamiz: men senga uy murabbosidan bir banka beraman, sen narxni tushirasan. Kelishdikmi?", "warm", "05.jpg",
          [note("Murabbo evaziga chegirma.", y=1500, at="murabbo")]),
        S("sarah", "Tizim xatosi. Murabbo qabul qilindi. Narx — yigirma besh ming. Bu qanday bo'ldi, o'zim ham tushunmadim.", "groove", "06.jpg",
          [stamp("Chegirma: 7 000 so'm!", at="yigirma besh", y=1560)]),
        S("lily", "Ko'rdingmi, Dilfuza? Robot ham o'zbek opasiga yutqazadi. Texnologiya qanchalik aqlli bo'lmasin, bozor qoidasi o'zgarmaydi!", "warm", "07.jpg",
          [note("Bozor qoidasi o'zgarmaydi.", y=1500, at="bozor qoidasi")]),
        S("bekzod", "Sizningcha, haydovchisiz taksi bilan savdolashish mumkinmi? Kim yutadi: robotmi yoki opa?", "finale", "07.jpg",
          [final(["ROBOTMI", "YOKI OPA?"])]),
    ],
    caption=("«Chorsugacha 15 mingga boramizmi, ukam?» — «Men haydovchisiz taksiman. Narx qat'iy.» 🚕🤖\n\n"
             "Kelajakda rulda hech kim bo'lmaydi. Lekin opalarimiz bilan savdolashishga hech qanday sun'iy intellekt tayyor emas 😄 Bir banka murabbo — va chegirma tayyor!\n\n"
             "Fakt: Waymo haydovchisiz taksilari AQShda haftasiga 400 mingdan ortiq pullik safar qilmoqda (2026).\n\n"
             "Kim yutadi: robotmi yoki opa? 👇\n\n"
             "#99foiz #kelajak #robotaksi #texnologiya #suniyintellekt #taksi #bozor #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #reels #reelsuz #uzbekreels"),
)

JOBS["2026-10-16_1830_nahor-oshi"] = dict(
    slot="2026-10-16T18:30+05:00", theme="urf-odat", trial=False,
    title="Nahor oshi", music_seed=103,
    cover_title=["NAHOR", "OSHI"], cover_sub="soat 05:30, butun mahalla bir joyda", cover_scene=1,
    hero="oshpaz usta Hamid aka (60, oq xalat, do'ppi, katta kafgir) + yosh kuyov Javlon (27, kostyum) + mahalla oqsoqoli",
    opening="tomoshabinga murojaat",
    images={
        "01": "Pre-dawn Tashkent mahalla street at 5:30 am, dark blue sky with first light, many Uzbek men in doppi skullcaps and warm coats walking together toward a lit courtyard with steam rising, street lamps, peaceful and atmospheric.",
        "02": "Huge cast-iron kazan of plov over a wood fire in a courtyard before dawn, master oshpaz Hamid aka, 60, white apron, embroidered doppi, gray mustache, stirring with a giant kafgir ladle, golden steam and firelight, epic composition.",
        "02_b": "SMALL CHANGE: same picture, but the oshpaz lifts the giant ladle high showing golden rice and carrots, steam bursting up.",
        "03": "Young Uzbek groom Javlon, 27, dark suit and white shirt, sleepy but happy, standing at the courtyard gate greeting arriving guests with hand on heart, early morning blue light.",
        "04": "Long tables in a courtyard with white tablecloths, men in doppi sitting shoulder to shoulder, big round plates of plov with carrots, raisins and meat, non bread and green tea, warm lamp light at dawn.",
        "05": "Still life close-up: a large lagan plate of Uzbek plov with yellow carrots, chickpeas, quail eggs and slices of meat on top, steam rising, embroidered tablecloth, dramatic warm light, dark background.",
        "06": "Elderly Uzbek mahalla elder, 75, white beard, chapan robe, raising open hands in blessing (duo) at the head of the table, other men listening respectfully, morning sun rays.",
        "07": "Sunrise over the courtyard: the oshpaz, the young groom and the elder laughing together next to the empty kazan, guests leaving, warm golden light, feeling of togetherness.",
    },
    scenes=[
        S("bekzod", "Tasavvur qiling: soat besh yarim, hali qorong'i. Butun mahalla erkaklari bir tomonga shoshyapti. Sabab bitta — nahor oshi.", "hero", "01.jpg",
          [pill("SOAT 05:30", bg="navy", y=330, at="start"), note("Butun mahalla bir tomonga shoshyapti.", y=1500, at="shoshyapti")]),
        S("bill", "Osh tun bo'yi tayyorlanadi, o'g'lim. Zirvak sabr bilan pishadi, guruch esa ko'ngil bilan damlanadi.", "warm", "02.jpg",
          [stamp("Osh sabr bilan pishadi.", at="sabr", y=1560)], img2="02_b.jpg", img2_at="guruch"),
        S("charlie", "Men esa kecha to'y oldidan uxlolmadim. Hamid aka bo'lsa, «kuyov, sen mehmon kutib ol, oshni menga qo'y» dedi.", "groove", "03.jpg",
          [note("«Oshni menga qo'y», dedi usta.", y=1500, at="menga")]),
        S("bekzod", "Nahor oshi — to'yning birinchi duosi. Uni tong otmasdan, mahalla bilan birga yeyishadi. Bu yerda hamma teng: boy ham, kambag'al ham.", "warm", "04.jpg",
          [note("Bu yerda hamma teng.", y=1500, at="hamma teng")]),
        S("bekzod", "Bilasizmi, o'zbek oshi va uning an'analari ikki ming o'n oltinchi yilda YUNESKOning nomoddiy madaniy merosi ro'yxatiga kiritilgan.", "mystery", "05.jpg",
          [dark(0.35), card("YUNESKO, 2016", ["OSH —", "MADANIY MEROS"], "Palov madaniyati va an'analari.", at="YUNESKO")]),
        S("bill", "Osh yeyildi, endi duo qilamiz. Yoshlarga baxt, ota-onaga sabr, mahallaga tinchlik bersin.", "warm", "06.jpg",
          [note("Yoshlarga baxt, mahallaga tinchlik.", y=1500, at="baxt")]),
        S("charlie", "Quyosh chiqqanda qozon bo'sh edi. Hamid aka esa kulib: «Osh tugadi, lekin mehr tugamaydi» dedi.", "warm", "07.jpg",
          [stamp("Mehr tugamaydi.", at="mehr", y=1560)]),
        S("bekzod", "Nahor oshi — bu shunchaki ovqat emas, bu bir mahallaning bir yurak bo'lib urishi.", "warm", "07.jpg",
          [note("Bir mahalla — bir yurak.", y=1500, at="bir yurak")]),
        S("bekzod", "Siz oxirgi marta qachon nahor oshiga borgansiz? Izohda yozing.", "finale", "04.jpg",
          [final(["NAHOR OSHIGA", "QACHON BORGANSIZ?"])]),
    ],
    caption=("Soat 05:30. Hali qorong'i. Butun mahalla bir joyga shoshyapti — nahor oshi! 🍚🌅\n\n"
             "Osh tun bo'yi sabr bilan pishadi, tong otmasdan mahalla bilan birga yeyiladi. Bu yerda hamma teng ❤️\n\n"
             "Fakt: «Palov madaniyati va an'analari» 2016-yilda YUNESKO nomoddiy madaniy merosi ro'yxatiga kiritilgan.\n\n"
             "Siz oxirgi marta qachon nahor oshiga borgansiz? 👇\n\n"
             "#99foiz #urfodat #nahoroshi #osh #palov #toy #mahalla #ozbekcha #ozbekiston #uzbekistan #toshkent #reels #reelsuz #uzbekreels #madaniyat"),
)

JOBS["2026-10-16_2100_zaryad-100"] = dict(
    slot="2026-10-16T21:00+05:00", theme="ko'p uchraydigan xatolar", trial=False,
    title="Har kecha 100% gacha zaryad", music_seed=117,
    cover_title=["HAR KECHA", "100% ZARYAD"], cover_sub="telefonning yashirin iltimosi", cover_scene=1,
    hero="talaba Madina (20, sariq ro'mol, kitoblar) + telefonining o'zi (gapiradigan personaj) + ustaxonachi Rustam aka",
    opening="birinchi shaxs",
    images={
        "01": "Cozy student dorm room at night: Uzbek student girl Madina, 20, yellow headscarf, pajamas, lying in bed hugging her smartphone plugged into a charger, smiling as the screen shows a full battery, books on the nightstand, warm lamp light.",
        "02": "Cartoon personified smartphone with a cute tired face and droopy eyes lying on a nightstand plugged into a charger, sweating, with a small bandage, cozy dark room, funny and sympathetic.",
        "02_b": "SMALL CHANGE: same picture, but the phone now holds up a tiny white flag and its eyes are wide open in panic.",
        "03": "Uzbek student Madina, 20, yellow headscarf, in a university corridor looking in shock at her phone showing a red low battery icon at noon, friends walking past.",
        "04": "Small phone repair kiosk in a Tashkent market: repairman Rustam aka, 40, short beard, glasses on his forehead, apron, holding a phone battery with tweezers and explaining, shelves with phone parts, warm light.",
        "05": "Infographic-style illustration of a smartphone battery cut in half showing glowing cells, a green zone from 20 to 80 percent and red zones at 0 and 100 percent, dark blue background, clean and simple.",
        "06": "Uzbek student Madina with yellow headscarf at her desk turning on a battery-saving setting on her phone, the personified phone smiling happily, notebook and tea beside her.",
        "07": "Morning: Uzbek student Madina with yellow headscarf walking cheerfully to university, her happy cartoon phone peeking from her bag pocket and waving, sunny autumn street with plane trees.",
    },
    scenes=[
        S("jessica", "Men telefonim yuz foiz bo'lmasa uxlay olmayman. Har kecha zaryadga qo'yaman va ertalabgacha shundoq qoladi.", "groove", "01.jpg",
          [note("Yuz foiz bo'lmasa uxlay olmayman.", y=1500, at="uxlay")]),
        S("charlie", "Assalomu alaykum, men uning telefoniman. Iltimos, meni har kecha to'liq to'yintirmang. Men ham charchayman!", "groove", "02.jpg",
          [stamp("Men ham charchayman!", at="charchayman", y=1560)], img2="02_b.jpg", img2_at="Iltimos"),
        S("jessica", "Lekin nega bir yildan keyin telefonim tushgacha ham chidamay qoldi? Ertalab yuz foiz, tushda o'n besh!", "tense", "03.jpg",
          [big("15%", y=430, at="o'n besh")]),
        S("bill", "Qizim, batareya ham odamga o'xshaydi. Uni har doim to'liq to'ldirib, soatlab shu holatda ushlasang, tezroq qariydi.", "warm", "04.jpg",
          [note("Batareya ham charchaydi.", y=1500, at="qariydi")]),
        S("bill", "Shuning uchun Apple ham telefonlarga «optimal zaryadlash» funksiyasini qo'shgan. U batareyaning yuz foizda turadigan vaqtini qisqartirib, uni uzoqroq yashatadi.", "mystery", "05.jpg",
          [dark(0.35), card("Apple Support", ["OPTIMAL", "ZARYADLASH"], "Batareya to'liq turish vaqtini qisqartiradi.", at="Apple")]),
        S("jessica", "Bugun men optimal zaryadlashni yoqdim. Endi telefonim kechasi saksonda kutib turadi va ertalabga to'ladi.", "warm", "06.jpg",
          [sticker(["Optimal zaryadlash", "yoqildi!"], color="green", x=760, y=1450, at="yoqdim")]),
        S("charlie", "Rahmat, Madina! Endi men ham uxlay olaman. Va'da beraman, tushgacha o'chib qolmayman.", "warm", "07.jpg",
          [note("Telefon ham uxlay oladi.", y=1500, at="uxlay olaman")]),
        S("bill", "Esingizda bo'lsin: batareya uchun eng yaxshi oraliq — yigirmadan saksongacha. Har kecha yuz foiz shart emas.", "warm", "05.jpg",
          [stamp("Yigirmadan saksongacha.", at="yigirmadan", y=1560)]),
        S("jessica", "Sizning telefoningiz hozir necha foizda? Izohda yozing.", "finale", "07.jpg",
          [final(["TELEFONINGIZ", "NECHA FOIZDA?"])]),
    ],
    caption=("«Telefonim 100% bo'lmasa uxlay olmayman.» Telefon esa ichida: «Iltimos, meni tinch qo'y…» 🔋😴\n\n"
             "Har kecha to'liq zaryadlab, ertalabgacha qoldirish — eng ko'p uchraydigan xatolardan biri. Natija: bir yildan keyin telefon tushgacha ham chidamaydi.\n\n"
             "Fakt (Apple): «optimal zaryadlash» batareyaning to'liq zaryadda turish vaqtini qisqartirib, uning eskirishini kamaytiradi.\n\n"
             "Telefoningiz hozir necha foizda? 👇\n\n"
             "#99foiz #telefon #batareya #zaryad #maslahat #talaba #ozbekcha #ozbekiston #uzbekistan #toshkent #hazil #reels #reelsuz #uzbekreels #texnologiya"),
)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    pref = "Hand-drawn storybook illustration, fine ink crosshatching linework, rich painted gouache colors, vertical 9:16 composition, no text, no letters, no logos."
    for name, j in JOBS.items():
        d = os.path.join(base, name); os.makedirs(d + "/img", exist_ok=True); os.makedirs(d + "/aud", exist_ok=True)
        scenes = []
        for k, sc in enumerate(j["scenes"]):
            sc = dict(sc); sc["vo"] = f"vo_{k + 1:02d}.mp3"; sc["voice_id"] = VOICES[sc["speaker"]]; scenes.append(sc)
        out = {"title": j["title"], "music_seed": j["music_seed"], "cover_title": j["cover_title"], "cover_sub": j["cover_sub"],
               "cover_scene": j["cover_scene"], "anim": "static", "scenes": scenes}
        json.dump(out, open(d + "/scenes.json", "w"), ensure_ascii=False, indent=1)
        json.dump({"images": j["images"], "hero": j["hero"], "opening": j["opening"]}, open(d + "/images.json", "w"), ensure_ascii=False, indent=1)
        json.dump({"slot": j["slot"], "title": j["title"], "theme": j["theme"], "trial": j["trial"], "caption": j["caption"]}, open(d + "/post.json", "w"), ensure_ascii=False, indent=1)
        tag = "S" + name[11:15]
        msg = [f"New set. Generate these images one by one, each 9:16, x1, in exactly the same hand-drawn storybook style as before ({pref}). Keep the characters consistent: use the first image where each character appears as the character reference for the later ones. For names ending in _b, use the image with the same number as the reference and change only the described small detail, keeping everything else identical."]
        for k, v in j["images"].items(): msg.append(f"{tag}_{k}: " + v.replace("SMALL CHANGE: same picture", f"SMALL CHANGE: same picture as {tag}_{k[:2]}"))
        open(f"/tmp/claude-0/work/msg_{tag}.txt", "w").write(" ".join(msg))
        print(name, len(scenes), sum(len(s["text"].split()) for s in scenes), "words")
