# -*- coding: utf-8 -*-
"""18-okt v2: script.json (joriy ssenariy) + brief_style/music/hooks/gestures + images.json -> scenes.json.

Ishlatish:  python3 jobs/build2_2026-10-18.py [job_dir_nomi ...] [--cut]   (argumentsiz — 7 ta job;
            --cut: rembg modelisiz oq fonni kesib img/*_cut.png stikerlarini oflayn yasaydi)

- Sahna matni/tartibi faqat script.json dan olinadi. Ovoz: `reuse` bo'lsa aud/<reuse>, aks holda aud/vo_NN.mp3.
- Eski brief_gestures.json dagi sahna raqamlari eskirgan: element faqat `at` iborasi yangi sahna matnida
  bo'lsa saqlanadi va o'sha sahnaga ulanadi (payoff raqami oldinroq chiqib qolmasligi tekshiriladi).
- Har videoda 15-25 ta imo-ishora (mark + prop) bo'lishi kafolatlanadi; har sahnada kamida bittadan.
- Narrator (bekzod) sahnalarida pastki 1/3 da caption, personaj sahnalarida stiker + gap pufakchasi.
- Fayllar (rasm/ovoz) hali bo'lmasa ham scenes.json yoziladi, faqat WARN chiqadi.
"""
import json, os, re, sys, subprocess

B = os.path.dirname(os.path.abspath(__file__))
CAST = {"bekzod": "kGOig3GPePLxobJGHo2M", "dilnoza": "O72h9AUwisM6Zj4He72B", "zilola": "cyPun3bl9MxcpLBX6pT0",
        "nodira": "132QLQIkg1RJGmpicuhR", "shahnoza": "eggZu1Ffe4if51TKev2v", "jahongir": "xDwfBjUEPdIoQekNOXAX",
        "sardor": "UjuEL3hLLUaDED9iW4Yb", "malika": "VTN9ql0D5MshokKncKAy"}
NARRATOR = "bekzod"
MAX_G, MIN_G, MAX_PER_SCENE = 25, 15, 3
DIRS = {"right": 0, "up": 90, "left": 180, "down": 270}   # engine: mark/prop `dir` MUST be numeric degrees


# ---------------------------------------------------------------- element helpers
def prop(img, x=880, y=760, h=240, at=0.4, motion="pulse", label=None, rot=0, dir=None, frm="pop"):
    d = {"type": "prop", "img": img, "x": x, "y": y, "h": h, "at": at, "motion": motion, "from": frm, "rot": rot}
    if label: d["label"] = label
    if dir is not None: d["dir"] = dir
    return d
def mark(shape, x=540, y=800, w=340, h=None, at=0.4, label=None, color="red", to=None, lx=None, ly=None):
    d = {"type": "mark", "shape": shape, "x": x, "y": y, "w": w, "at": at, "color": color}
    if h is not None: d["h"] = h
    if label: d["label"] = label
    if to: d["to"] = to
    if lx is not None: d["label_x"] = lx
    if ly is not None: d["label_y"] = ly
    return d
def tag(head, text, x=170, y=210, color="red", at="start"): return {"type": "tag", "head": head, "text": text, "x": x, "y": y, "color": color, "at": at}
def pill(t, bg="crimson", x=600, y=300, at="start", rot=-3): return {"type": "pill", "text": t, "bg": bg, "fg": "white", "x": x, "y": y, "rot": rot, "at": at}
def note(t, y=1560, at=0.4, size=62, rot=-2): return {"type": "note", "text": t, "y": y, "size": size, "rot": rot, "at": at}
def sticker(lines, color="yellow", x=540, y=1470, w=420, at=1.2, rot=-3, size=78): return {"type": "sticker", "lines": lines, "color": color, "x": x, "y": y, "w": w, "size": size, "rot": rot, "at": at}
def card(k, title, sub, at=0.3, y=1330): return {"type": "card", "kicker": k, "title": title, "sub": sub, "at": at, "y": y}
def clock(day, t): return {"type": "clock", "day": day, "time": t, "at": "start"}
def bars(rows, y=880, at=0.4): return {"type": "bars", "rows": rows, "x": 540, "y": y, "at": at}
def stamp(t, y=1450, at="end", rot=-5): return {"type": "stamp", "text": t, "y": y, "rot": rot, "at": at}
def final(lines): return {"type": "final", "lines": lines, "at": 0.4}
def dark(a=0.35): return {"type": "dark", "amount": a, "at": "start"}
def hero(img, side="right", at=0.2, label=None, lbg="royal", moods=None):
    """main character reacting in a NARRATOR scene: smaller, low in the corner (caption moves up)"""
    d = {"type": "char", "img": img, "from": side, "x": 820 if side == "right" else 260, "y": 1570, "h": 640, "at": at, "motion": "idle", "flip": False}
    if label: d["label"] = label; d["label_bg"] = lbg
    if moods: d["moods"] = moods
    return d
GESTURE = ("mark", "prop")


# ---------------------------------------------------------------- per-job design
# chars: speaker -> {name, img, tag, side}; "per" : {phrase: {img, moods}} overrides for a scene (phrase in its text)
# extra: [(phrase, [elements])] — anchored to the FIRST scene whose text contains the phrase (robust to renumbering)
# cap:   {phrase: [words]} caption overrides for narrator scenes;  forbid: payoff tokens not allowed before payoff
J = {}
J["2026-10-18_0800_pult"] = dict(
    chars={"jahongir": dict(name="DADA", img="c_dada.jpg", tag="crimson", side="left", label="ERKIN AKA"),
           "dilnoza": dict(name="MAFTUNA", img="c_maftuna.jpg", tag="purple", side="right", label="MAFTUNA, OPASI"),
           "sardor": dict(name="BOTIR", img="c_katta_botir.jpg", tag="royal", side="right", label="BOTIR, 42")},
    per={"klikkerimiz": dict(moods=[["c_dada_kulgan.jpg", "Botir!"]]), "O'g'lim kanalni": dict(side="left")},
    forbid=["KLIKKER", "CHIQ"], forbid_spoken=["klikker"],
    cover=dict(layout="polaroid", props=["p_g_pult.jpg"], badge="1995", tilt=-5),
    cap={"Bu bola": ["LAQABI", "OXIRIDA!"], "Kanal almashtirish": ["ENG", "QIYINI", "OLDINDA!"],
         "Endi diqqat": ["BIRINCHI", "PULT", "QANDAY", "EDI?"], "Tarjimasi": ["«DANGASA", "SUYAKLAR»"],
         "Ellik oltinchi": ["VA", "MANA", "ENG", "QIZIG'I..."], "Bir soat": ["BOTIR", "QIMIRLAMAYDI!"]},
    extra=[("Bu bola uyimizning", [pill("LAQABI: ???", "crimson", x=640, y=300, at=0.3), hero("c_botir.jpg", "right", 0.15, "BOTIR, 11", "orange")]),
           ("To'qson beshinchi", [tag("YIL", "1995")]),
           ("Uning ismi Botir", [hero("c_botir.jpg", "right", "Uning ismi", "PULT", "orange")]),
           ("Kanal almashtirish", [sticker(["PULT VAZIFALARI:", "kanal", "ovoz", "antenna"], "yellow", x=780, y=430, w=440, at=0.2, rot=4, size=68),
                                   prop("p_g_tovush.jpg", 200, 760, 230, "ovozni", "pulse")]),
           ("Bir soat o'tdi", [tag("O'TDI", "1 SOAT", color="navy"), hero("c_botir_charchagan.jpg", "right", 0.2), prop("p_g_ter.jpg", 220, 820, 200, "qimirlamaydi", "bounce")]),
           ("O'ttiz yil", [tag("YIL", "2026", color="green"), hero("c_katta_botir.jpg", "right", "O'ttiz", "BOTIR, 42"), prop("p_antenna.jpg", 220, 800, 300, "o'g'li", "wag")]),
           ("ovozli yordamchiga", [prop("p_g_tovush.jpg", 880, 760, 240, "ovozli", "pulse"), mark("cross", 220, 820, 200, at="almashtiradi", label="ANTENNA YO'Q!")]),
           ("Endi diqqat", [pill("DIQQAT!", "crimson", x=540, y=300, at=0.1), prop("p_g_undov.jpg", 880, 760, 260, "ko'pchilik", "shake")]),
           ("Ellikinchi yil", [tag("YIL", "1950", color="navy"), card("ZENITH, 1950", ["«LAZY BONES»"], "Birinchi pultlardan biri", at="Zenith"),
                               prop("p_g_pult.jpg", 200, 760, 240, "pulti", "wag")]),
           ("Tarjimasi", [prop("p_g_zzz.jpg", 860, 700, 220, "Dangasa", "pulse")]),
           ("Robert Adler", [tag("YIL", "1956", color="navy"), pill("ROBERT ADLER", "navy", x=640, y=330, at="Robert")]),
           ("deyishgan", [stamp("KLIKKER!", y=1400, at="klikker"), mark("burst", 540, 780, 360, at="klikker")]),
           ("butun bolaligimni", [mark("burst", 540, 760, 320, at="klikker", label="KLIKKER BOTIR!"), prop("p_g_prujina.jpg", 880, 820, 240, "bo'lib", "jump")]),
           ("Bolaligingizda uyda", [final(["SIZNIKI QAYSI", "ISH EDI?"]), sticker(["Izohda", "yozing!"], "pink", w=460)])],
)
J["2026-10-18_1230_bepul-sinov"] = dict(
    chars={"zilola": dict(name="NIGORA", img="c_nigora.jpg", tag="crimson", side="left", label="NIGORA, BUXGALTER"),
           "sardor": dict(name="ULUG'BEK", img="c_ulugbek.jpg", tag="royal", side="right", label="ULUG'BEK"),
           "dilnoza": dict(name="SHAHZODA", img="c_shahzoda.jpg", tag="orange", side="right", label="SHAHZODA")},
    per={"Yetti kun bepul!": dict(img="c_nigora_hayajon.jpg"), "meditatsiya": dict(moods=[["c_nigora_xijolat.jpg", "meditatsiya"]])},
    forbid=["219", "133", "86"], forbid_spoken=["ikki yuz o'n to'qqiz", "sakson olti"],
    cover=dict(layout="split", char="c_nigora_hayron.jpg", char_h=600, props=[], badge="7 KUN BEPUL", title_colors=[[255, 255, 255], [255, 220, 30]]),
    cap={"«Bepul» so'zi": ["«BEPUL»", "=", "OYIGA", "$", "?"], "Endi diqqat": ["HATTO", "AMERIKALIKLAR", "HAM!"],
         "Yigirma ikkinchi": ["OYIGA", "QANCHA", "TO'LAYSIZ?"], "Siz-chi?": ["RAQAMNI", "O'YLANG!"],
         "Shu kuni Nigora": ["OBUNALARNI", "SANADI..."], "O'n bitta obuna": ["O'N", "BITTA", "OBUNA!"],
         "Amerikaliklar o'ylagani": ["ASLIDA", "$219!"], "Ya'ni har oy": ["HAR", "OY", "KETGAN!"]},
    extra=[("«Bepul» so'zi", [pill("JAVOB OXIRIDA", "navy", x=640, y=300, at="Javob")]),
           ("Yetti kun o'tdi", [tag("O'TDI", "7 KUN", at="Yetti")]),
           ("Lekin bu hali", [pill("ENG QIZIG'I — TELEFONDA", "crimson", x=540, y=300, at="Eng"), hero("c_nigora_xijolat.jpg", "right", 0.2),
                              prop("p_g_lupa.jpg", 200, 820, 230, "telefonida", "point", rot=-15, dir=0)]),
           ("Endi diqqat", [pill("DIQQAT!", "crimson", x=540, y=300, at=0.1), prop("p_g_undov.jpg", 880, 760, 250, "amerikaliklar", "shake")]),
           ("tadqiqotchilar", [tag("YIL", "2022", color="navy"), card("C+R RESEARCH, 2022", ["OYIGA QANCHA?"], "Obunalarga oylik sarf so'raldi", at="obunalarga"),
                               prop("p_g_lupa.jpg", 880, 760, 240, "tadqiqotchilar", "point", rot=20, dir=180)]),
           ("Siz-chi?", [sticker(["SIZNING RAQAMINGIZ:", "$ ___ ?"], "blue", x=760, y=440, w=440, at=0.3, rot=4, size=62),
                         prop("p_g_tangalar.jpg", 220, 820, 260, "Raqamni", "jump")]),
           ("Shu kuni Nigora", [hero("c_nigora.jpg", "right", 0.2), prop("p_g_lupa.jpg", 220, 820, 230, "sanab", "pulse")]),
           ("O'n bitta obuna", [hero("c_nigora_hayron.jpg", "right", "O'n bitta")]),
           ("Amerikaliklar o'ylagani", [dark(0.35), bars([["O'YLAGANI", 86, "yellow"], ["ASLIDA", 219, "red"]], y=820, at="sakson"),
                                        prop("p_g_tangalar.jpg", 880, 520, 220, "ikki yuz", "jump")]),
           ("Ya'ni har oy", [stamp("-$133 / OY", y=1450, at="bir yuz"), prop("p_karta.jpg", 820, 760, 320, 0.3, "shake")]),
           ("Siz qaysi obunani", [final(["QAYSI OBUNANI", "UNUTGANSIZ?"]), sticker(["Izohda", "yozing!"], "blue", w=440)])],
    relabel={"-$133 / OY": "BILMASDAN!"},
)
J["2026-10-18_1600_ai-muzlatkich"] = dict(
    chars={"shahnoza": dict(name="SOVUQJON", img="c_sovuqjon.jpg", tag="green", side="right", label="AI MUZLATKICH"),
           "sardor": dict(name="JAMSHID", img="c_jamshid_jahl.jpg", tag="royal", side="left", label="JAMSHID, 34"),
           "nodira": dict(name="ONASI", img="c_ona.jpg", tag="purple", side="right", label="ONASI")},
    per={"bitta kolbasa": dict(img="c_jamshid_yolvorish.jpg")},
    forbid=["LG", "SAMSUNG", "33", "2000", "2024"], forbid_spoken=["ikki minginchi", "o'ttiz uch"],
    cover=dict(layout="diagonal", char="c_jamshid_qorqqan.jpg", props=["p_g_qulf.jpg", "p_g_kolbasa.jpg"], badge="2045", title_colors=[[255, 255, 255], [176, 232, 108]], accent=[20, 30, 56]),
    cap={"Muzlatkichingiz sizga": ["BU", "FANTASTIKA", "EMAS!"], "Qirq beshinchi": ["2045,", "TUNGI", "02:14"],
         "Bir soniya": ["ICHIDA", "KAMERA", "BOR!"], "U har bir": ["ENG", "DAHSHATLISI", "OLDINDA!"],
         "Jamshid endi": ["KOLBASA", "MUZLATKICHNIKI"], "Fantastika deysizmi": ["FANTASTIKA", "DEYSIZMI?"],
         "Yigirma yildan": ["U", "SIZNI", "HAM", "TANIYDI"]},
    extra=[("Muzlatkichingiz sizga", [hero("c_sovuqjon.jpg", "right", 0.2, "SOVUQJON", "green"), prop("p_g_ogohlantirish.jpg", 200, 760, 240, "yo'q", "shake")]),
           ("Qirq beshinchi", [clock("2045", "02:14"), hero("c_jamshid.jpg", "left", "Jamshid", "JAMSHID")]),
           ("Sovuqjon oddiy", [pill("SKANER: YOQILGAN", "green", x=600, y=300, at=0.2), prop("p_g_skaner.jpg", 540, 780, 380, "kamera", "pulse")]),
           ("Bu haqda onangizga", [prop("p_g_konvert.jpg", 260, 760, 240, "xabar", "point", rot=-10, dir=180)]),
           ("Jamshid endi", [hero("c_jamshid_qorqqan.jpg", "left", 0.2), prop("p_g_kolbasa.jpg", 860, 760, 260, "Kolbasani", "wag")]),
           ("Fantastika deysizmi", [pill("SHOSHMANG!", "crimson", x=600, y=300, at="Shoshmang"), prop("p_g_robot_koz.jpg", 860, 760, 240, 0.3, "pulse")]),
           ("LG internetga", [tag("YIL", "2000", color="navy"), card("LG, 2000", ["INTERNETGA ULANGAN", "BIRINCHI MUZLATKICH"], "", at="LG"),
                   mark("circle", 540, 780, 420, 320, at="birinchi", label="BIRINCHI!")]),
           ("Samsung", [tag("YIL", "2024", color="navy"), pill("SAMSUNG «AI VISION»", "navy", x=640, y=330, at="Samsung"), stamp("33 XIL!", y=1420, at="o'ttiz uch")]),
           ("Yigirma yildan", [tag("YIL", "2045", color="green"), hero("c_sovuqjon.jpg", "right", 0.2)]),
           ("Agar muzlatkichingiz", [final(["MUZLATKICHINGIZ", "NIMA DERDI?"]), sticker(["Izohda", "yozing!"], "green", w=440)])],
)
J["2026-10-18_1830_non-odobi"] = dict(
    chars={"sardor": dict(name="SHERZOD", img="c_sherzod.jpg", tag="royal", side="right", label="SHERZOD, 16"),
           "malika": dict(name="BUVI", img="c_buvi_hayron.jpg", tag="crimson", side="left", label="MALIKA BUVI"),
           "jahongir": dict(name="RAHMAT AKA", img="c_rahmat.jpg", tag="green", side="right", label="NOVVOY")},
    per={"Voy, qo'lim": dict(img="c_sherzod_vahima.jpg", side="left"), "Ol, to'g'rilab": dict(img="c_buvi.jpg"),
         "Non — mehnat": dict(img="c_buvi_mamnun.jpg")},
    forbid=["HAVO"], forbid_spoken=["havosini"],
    cover=dict(layout="bubble", char="c_buvi_hayron.jpg", ink=[58, 34, 22]),
    cap={"Nega o'zbek": ["NEGA", "TESKARI", "EMAS?"], "Sherzod kulib": ["SABABINI", "AYTMADI..."],
         "Ertasi kuni": ["ERTASI", "KUNI", "TONGDA..."], "Eshik ochildi": ["NONNING", "SIRI..."],
         "Endi diqqat": ["BIR", "RIVOYAT", "BOR"], "Buxoro amiri": ["BUXORO", "AMIRI", "CHAQIRTIRIBDI"],
         "Unni ham": ["UN", "HAM,", "SUV", "HAM!"], "Novvoy uzoq": ["ENG", "QIZIG'I..."],
         "O'sha kuni Sherzod": ["TO'PPA-TO'G'RI!"]},
    extra=[("Nega o'zbek", [pill("UYIMIZ QOIDASI", "orange", x=620, y=300, at=0.3)]),
           ("Sherzod kulib", [hero("c_sherzod.jpg", "right", 0.2), prop("p_g_undov.jpg", 220, 780, 240, "aytmadi", "shake")]),
           ("Ertasi kuni", [pill("TONG, 05:30", "navy", x=600, y=300, at="tongda")]),
           ("Eshik ochildi", [prop("p_g_bugli_non.jpg", 860, 780, 280, "sirini", "bounce")]),
           ("Yigirma ikkinchi", [tag("YIL", "2022", color="navy"), card("2022-YIL", ["KUNIGA ~15 000 TA", "SAMARQAND NONI"], "", at="o'n besh")]),
           ("Endi diqqat", [pill("RIVOYAT", "crimson", x=600, y=300, at="rivoyat"), prop("p_g_bugdoy_boshoq.jpg", 860, 780, 280, "Samarqand", "pulse")]),
           ("Buxoro amiri", [prop("p_g_korsatgich_qol.jpg", 200, 800, 240, "chaqirtiribdi", "point", dir=0)]),
           ("Novvoy uzoq", [prop("p_g_un_bulut.jpg", 860, 760, 260, "jim", "pulse")]),
           ("Novvoy aytibdi", [stamp("SAMARQAND HAVOSI!", y=1420, at="havosini")]),
           ("O'sha kuni Sherzod", [hero("c_sherzod.jpg", "right", 0.2), mark("check", 260, 800, 220, at="to'ppa", label="TO'G'RI!")]),
           ("Sizning buvingiz", [final(["BUVINGIZ NON", "HAQIDA NIMA DERDI?"]), sticker(["Izohda", "yozing!"], "yellow", w=440)])],
)
J["2026-10-18_2100_yuzga-qol"] = dict(
    chars={"dilnoza": dict(name="ZARINA", img="c_zarina.jpg", tag="purple", side="left", label="ZARINA"),
           "sardor": dict(name="JASUR", img="c_jasur.jpg", tag="royal", side="right", label="JASUR, KASSIR"),
           "nodira": dict(name="GAVHAR OPA", img="c_gavhar.jpg", tag="green", side="right", label="SHIFOKOR")},
    per={"Tushundim, opa": dict(img="c_jasur_qatiy.jpg", side="left"), "Yigirma to'rtinchi": dict(img="c_zarina_kulgi.jpg")},
    forbid=["23", "22", "24", "YIGIRMA"], forbid_spoken=["yigirma uch"],
    cover=dict(layout="zoom", focus=[540, 760], zoom=1.35, props=["p_g_mikrob.jpg", "p_g_koz.jpg"], title_colors=[[235, 235, 228], [57, 255, 120]]),
    cap={"Yuzingizga soatiga": ["SOATIGA", "NECHA", "MARTA?"], "Javobni oxirida": ["HOZIR", "HAM", "TEGDINGIZ-A?"],
         "Va har sanagandan": ["BURNINI", "QASHIYDI!"], "Lekin Jasur": ["KIMDIR", "KUZATARDI..."],
         "Zarina daftar": ["BUNI", "KO'PCHILIK", "BILMAYDI"], "Tegishlarning": ["OG'IZ,", "BURUN,", "KO'Z!"],
         "Mikroblar uchun": ["UCHTA", "ESHIK!"], "Bir ishora": ["O'NDAN", "OSHDI!"], "roppa-rosa": ["12", "SONIYA!"],
         "Xo'sh, mana": ["NECHTA", "CHIZIQ?"], "Yigirma uchta!": ["23", "MARTA!"]},
    extra=[("Yuzingizga soatiga", [pill("TAXMIN QILING!", "crimson", x=600, y=300, at="Taxmin"), prop("p_g_koz.jpg", 860, 760, 240, 0.3, "pulse")]),
           ("Javobni oxirida", [mark("arrow", 860, 1000, at="Hozir", to=[600, 780], label="SIZ!")]),
           ("Bu — Jasur", [hero("c_jasur.jpg", "right", "Jasur", "JASUR, KASSIR")]),
           ("Va har sanagandan", [hero("c_jasur_qichish.jpg", "right", "burnini")]),
           ("Lekin Jasur", [prop("p_g_koz.jpg", 220, 780, 240, "kuzatib", "pulse")]),
           ("Zarina daftar", [pill("DIQQAT!", "crimson", x=600, y=300, at="diqqat"), hero("c_zarina_kulgi.jpg", "left", "daftar", "ZARINA", "purple")]),
           ("Tegishlarning", [pill("44%", "crimson", x=540, y=300, at="qirq")]),
           ("Bir ishora", [tag("SANOQ", "10+", color="red"), prop("p_g_sanoq.jpg", 860, 780, 260, "chiziqlar", "pulse")]),
           ("roppa-rosa", [pill("VA'DA: 12 SONIYA", "crimson", x=600, y=300, at="va'dani"), hero("c_jasur_qichish.jpg", "right", "o'n ikki")]),
           ("Xo'sh, mana", [prop("p_g_lupa.jpg", 860, 780, 240, "daftarida", "point", rot=20, dir=180)]),
           ("Yigirma uchta!", [stamp("23 MARTA!", y=1400, at=0.15)]),
           ("O'n beshinchi yili", [tag("YIL", "2015", color="navy"), card("KWOK VA BOSHQ., 2015", ["SOATIGA 23 MARTA"], "26 tibbiyot talabasi videoga olingan", at="O'rtacha")]),
           ("Siz qaysi odatingizni", [final(["QAYSI ODATNI", "TASHLAY OLMAYSIZ?"]), sticker(["Izohda", "tan oling!"], "green", w=460)])],
)
J["2026-10-18_1030_gitler-moskva"] = dict(
    # history: no character sticker for Hitler (text-only mention), no nazi symbols; only Ergash (fictional) + objects
    chars={"jahongir": dict(name="TEMIRCHI", img=None, tag="navy", side="left"),
           "sardor": dict(name="ERGASH", img="c_ergash.jpg", tag="crimson", side="left", label="ERGASH, 19")},
    per={"Oyijon": dict(moods=[["c_ergash_sovqotgan.jpg", "Qish kelyapti"]])},
    forbid=["QISH", "SOVUQ", "TAYYOR EMAS", "AYOZ"], forbid_spoken=["qishga umuman"],
    cover=None,   # brief_style.json -> cover (poster)
    cap={"Gitler Moskvaga": ["NEGA", "OLOLMADI?"], "Uning rejasi": ["JAVOBI", "ENG", "OXIRIDA"],
         "Qirq birinchi": ["22-IYUN,", "1941"], "Chegaradan": ["4", "MILLIONGA", "YAQIN", "ASKAR"],
         "Reja ishlayotgandek": ["BITTA", "KATTA", "XATO"], "Har bir shahar": ["HAR", "BIR", "KO'PRIK", "UCHUN"],
         "Bir soniya": ["BU", "ORADA", "O'ZBEKISTONDA..."], "Yarim millionga": ["~500", "MING", "KISHI"],
         "O'zbekistondan bir yarim": ["~1,5", "MILLION", "FRONTGA"], "Endi diqqat. Frontda": ["YO'LLAR", "LOYGA", "AYLANDI"],
         "Dekabrga kelib": ["MOSKVA", "OSTIDA"], "Moskva juda yaqin": ["BIR", "NARSANI", "UNUTISHDI..."],
         "Beshinchi dekabr": ["500", "MINGDAN", "ORTIQ"], "Bosqinchilar uch": ["REJA", "BARBOD", "BO'LDI"]},
    extra=[("Gitler Moskvaga", [mark("circle", 540, 820, 380, 300, at="Moskvaga", label="MOSKVA"), prop("p_g_undov.jpg", 880, 620, 240, "Lekin", "shake")]),
           ("Uning rejasi", [prop("p_muzlagan_soat.jpg", 860, 760, 280, "Uning", "pulse"), pill("JAVOB OXIRIDA", "navy", x=600, y=300, at="Javobi")]),
           ("Qirq birinchi", [tag("1941", "22.06", color="red"), prop("p_g_kompas.jpg", 860, 760, 240, "Tong", "wag")]),
           ("Chegaradan", [pill("~4 000 000 ASKAR", "crimson", x=600, y=300, at="to'rt"), prop("p_g_strelka.jpg", 220, 780, 260, "bostirib", "point", dir=0)]),
           ("Reja ishlayotgandek", [mark("cross", 540, 800, 260, at="xato", label="XATO?"), prop("p_g_undov.jpg", 880, 640, 230, "katta", "jump")]),
           ("Har bir shahar", [mark("arrow", 220, 1000, at="ko'prik", to=[480, 820], label="KO'PRIK!", lx=220, ly=1090)]),
           ("Bir soniya", [pill("TOSHKENT, 1941", "navy", x=600, y=300, at=0.1), prop("p_g_kompas.jpg", 860, 780, 240, "O'zbekistonda", "pulse")]),
           ("Yarim millionga", [mark("circle", 540, 800, 420, 320, at="evakuatsiya", label="YARIM MILLION")]),
           ("Kelinglar, bolalar", [prop("p_g_chinnigul.jpg", 880, 780, 260, "uyingiz", "pulse")]),
           ("Shomahmudovlar", [note("Shomahmudovlar oilasi — 14 bola", y=1560, at="o'n to'rt"), mark("burst", 540, 760, 320, at="o'n to'rt", label="14 BOLA!")]),
           ("O'zbekistondan bir yarim", [tag("FRONTGA", "1,5 MLN", color="navy"), prop("p_uchburchak_xat.jpg", 860, 780, 240, "frontga", "bounce")]),
           ("Oyijon", [prop("p_uchburchak_xat.jpg", 860, 760, 240, "Oyijon", "bounce")]),
           ("to'rt yuz yigirma", [dark(0.3), note("420 000 kishi uyga qaytmadi", y=1450, at="to'rt yuz"), prop("p_g_chinnigul.jpg", 540, 820, 300, "qaytmadi", "pulse")]),
           ("Endi diqqat. Frontda", [pill("DIQQAT!", "crimson", x=540, y=300, at=0.1), mark("arrow", 860, 1000, at="loyga", to=[600, 820], label="LOY!", lx=860, ly=1090)]),
           ("Dekabrga kelib", [tag("1941", "DEKABR", color="navy"), mark("circle", 540, 780, 400, 300, at="Moskva", label="MOSKVA")]),
           ("Moskva juda yaqin", [prop("p_g_qor.jpg", 860, 700, 220, "bir narsani", "pulse")]),
           ("Va mana javob", [stamp("QISH!", y=1380, at="qish"), prop("p_g_termometr.jpg", 860, 760, 300, "tayyor", "shake")]),
           ("Beshinchi dekabr", [tag("1941", "5 DEKABR", color="red"), prop("p_g_strelka.jpg", 220, 780, 260, "qarshi hujumga", "point", dir=180)]),
           ("Bosqinchilar uch", [mark("arrow", 760, 760, at="orqaga", to=[300, 800], label="300+ KM ORQAGA", lx=540, ly=640)]),
           ("Oilangizda urushga", [final(["BOBONGIZ", "BORMI?"]), sticker(["Ismini yozing —", "xotirasi yashasin"], "yellow", w=520, size=64),
                                   prop("p_g_chinnigul.jpg", 880, 560, 240, 1.0, "pulse")])],
)
ANQARA_PORTRAITS = True   # Amir Temur / Boyazid (15th c. rulers) as miniature-style stickers; set False to drop all c_ stickers
J["2026-10-18_1430_anqara"] = dict(
    chars={"sardor": dict(name="BOYAZID", img="c_boyazid.jpg", tag="crimson", side="right", label="SULTON BOYAZID"),
           "jahongir": dict(name="AMIR TEMUR", img="c_temur_ayyor.jpg", tag="royal", side="left", label="AMIR TEMUR")},
    per={"O'z otliqlarim": dict(img="c_boyazid_hayron.jpg")},
    forbid=["SUV OMBORI", "SUVSIZ", "BURDI", "BURIB"], forbid_spoken=["suv omboriga"],
    cover=None,   # brief_style.json -> cover (hero)
    cover_fix={"props": ["p_g_qilich.jpg", "p_jang_fili.jpg"]},   # the stream prop would hint the payoff on the profile grid
    cap={"Amir Temur sultonni": ["QANDAY", "HIYLA?"], "Javob oxirida": ["KIM", "BILAN", "KIM?"],
         "Olti asr": ["CHUBUQ", "TEKISLIGI"], "Bir tomonda": ["~140", "MING", "QO'SHIN"],
         "Qarshisida": ["VA", "FILLAR!"], "Lekin jangdan": ["TEMUR", "NIMANI", "PAYQADI?"],
         "Temur qo'shini": ["ORQASIGA", "O'TDI!"], "Nega aynan": ["NEGA", "AYNAN", "SHU", "JOY?"],
         "Jang boshlandi": ["JANG", "BOSHLANDI"], "qora tatarlar": ["TATARLAR", "O'TIB", "KETDI!"],
         "Anadolu beyliklarining": ["SIPOHIYLAR", "HAM!"], "Bir ishora": ["BIR", "ISHORA..."],
         "Va mana eng": ["ASL", "HIYLA?"], "Suvsiz qolgan": ["BOYAZID", "ASIR!"]},
    extra=[("Amir Temur sultonni", [hero("c_temur.jpg", "right", 0.2, "AMIR TEMUR", "royal"), prop("p_g_qilich.jpg", 200, 760, 280, "hiyla", "shake")]),
           ("Javob oxirida", [pill("TEMUR — BOYAZID", "navy", x=600, y=300, at="kim"), prop("p_g_tug.jpg", 860, 760, 300, "to'qnashdi", "wag")]),
           ("Olti asr", [tag("YIL", "1402"), mark("circle", 540, 820, 380, 280, at="Anqara", label="ANQARA")]),
           ("Bir tomonda", [hero("c_temur.jpg", "left", "Amir", "AMIR TEMUR, 66"), pill("~140 000", "royal", x=640, y=300, at="Yuz"),
                            prop("p_g_tug.jpg", 860, 760, 300, "qo'shin", "wag")]),
           ("Qarshisida", [pill("~85 000 · 32 FIL", "crimson", x=600, y=300, at="Sakson"), prop("p_jang_fili.jpg", 820, 820, 320, "fillar", "bounce")]),
           ("Lekin jangdan", [pill("DIQQAT!", "crimson", x=540, y=300, at="diqqat"), mark("circle", 540, 820, 320, 260, at="payqadi", label="?")]),
           ("Temur qo'shini", [mark("arrow", 260, 1060, at="ortiga", to=[820, 700], label="ORQAGA!", lx=260, ly=1150)]),
           ("Nega aynan", [prop("p_g_undov.jpg", 860, 740, 240, "Nega", "shake")]),
           ("Jang boshlandi", [prop("p_g_qilich.jpg", 200, 760, 280, "tarix", "shake")]),
           ("qora tatarlar", [mark("arrow", 820, 900, at="birdan", to=[300, 760], label="O'TDI!", lx=820, ly=990), prop("p_g_tug.jpg", 200, 760, 280, "Temur", "wag")]),
           ("Anadolu beyliklarining", [mark("arrow", 820, 1000, at="qo'shildi", to=[300, 860], label="YANA!", lx=820, ly=1090)]),
           ("Bir ishora", [prop("p_soy_ariq.jpg", 860, 780, 260, "Chubuq", "pulse"), mark("circle", 540, 860, 380, 260, at="oqardi", label="SOY")]),
           ("Va mana eng", [hero("c_temur_ayyor.jpg", "right", 0.2), prop("p_g_undov.jpg", 220, 760, 240, "hiylasi", "jump")]),
           ("suv omboriga", [stamp("SUVNI BURDI!", y=1400, at="burib"), prop("p_g_tomchi.jpg", 860, 720, 240, "Chubuq", "pulse")]),
           ("Suvsiz qolgan", [prop("p_g_mesh.jpg", 220, 760, 280, "Suvsiz", "shake")]),
           ("Usmonli sultoni shaxsan", [card("ANQARA, 28.07.1402", ["YAGONA HOLAT"], "Usmonli sultoni shaxsan asir olingan", at="Usmonli"),
                                        mark("burst", 540, 760, 320, at="yagona", label="BIRINCHI VA OXIRGI!")]),
           ("Siz Temur o'rnida", [final(["SIZ QANDAY", "HIYLA ISHLATARDINGIZ?"]), sticker(["Izohda", "yozing!"], "yellow", w=440)])],
)


# ---------------------------------------------------------------- utils
WARN = []
def warn(msg): WARN.append(msg)
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("‘", "'").replace("’", "'").replace("ʻ", "'").replace("'", ""))
def clamp(v, lo, hi): return max(lo, min(hi, v))
def el_texts(e):
    out = [str(e.get(k, "")) for k in ("label", "text", "sub", "kicker")]
    for k in ("lines", "title", "words"): out += [str(x) for x in e.get(k, [])]
    for r in e.get("rows", []): out += [str(x) for x in r[:2]]
    return " ".join(out).upper()
def leaks(e, forbid):
    t = el_texts(e)
    return [f for f in forbid if re.search(r"(?<![0-9A-Z])" + re.escape(f.upper()) + r"(?![0-9A-Z])", t)]
def is_gesture(e): return e["type"] in GESTURE
def colorize(e, acc, acc2):
    c = e.get("color")
    if isinstance(c, list): return
    e["color"] = acc2 if c in ("yellow", "accent2") else acc
def dur(p):
    if not os.path.exists(p): return None
    try: return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
    except Exception: return None

def auto_caption(text):
    sents = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text.strip()) if s.strip()]
    cands = [s for s in sents if 2 <= len(s.split()) <= 4]
    s = min(cands, key=lambda s: len(s.split())) if cands else sents[0]
    words = [w.strip("—").upper() for w in s.split() if w.strip("—")]
    if len(words) > 4: words = words[:4]; words[-1] = words[-1].rstrip(",.") + "..."
    return words, " ".join(s.split()[:2])

def fit(e, zone, used):
    """keep re-anchored / generated gestures inside the free zone of the scene (no face-cover, no bubble/caption clash)"""
    y0, y1 = zone
    if e["type"] == "prop":
        e["x"] = clamp(e.get("x", 880), 160, 920); e["h"] = min(e.get("h", 240), 300)
        e["y"] = clamp(e.get("y", 760), y0 + 60, y1 - 60)
        e["x"] = 900 if e["x"] >= 540 else 180   # stickers hug the left/right edge: faces are usually in the middle
        e["h"] = min(e["h"], 260)
        if "dir" in e and isinstance(e["dir"], str): e["dir"] = DIRS.get(e["dir"], 0)
        for (ux, uy) in used:   # don't stack two stickers on the same spot
            if abs(ux - e["x"]) < 260 and abs(uy - e["y"]) < 220: e["y"] = e["y"] + 260 if e["y"] + 260 < y1 else e["y"] - 260
        used.append((e["x"], e["y"]))
    else:
        w = e.get("w", 340); h = e.get("h", w * 0.7)
        if e["shape"] in ("circle", "box", "cross", "check"):
            h = min(h, y1 - y0 - 80); w = min(w, 760); e["w"] = w; e["h"] = h
            e["y"] = clamp(e.get("y", 800), y0 + h / 2, y1 - h / 2)
            e["x"] = clamp(e.get("x", 540), 60 + w / 2, 1020 - w / 2)
        elif e["shape"] == "burst":
            e["y"] = clamp(e.get("y", 800), y0 + w / 2 + 60, y1 - 40); e["w"] = min(w, 420)
        elif e["shape"] == "underline":
            e["y"] = clamp(e.get("y", 800), y0, y1)
        if e["shape"] == "arrow":
            e["y"] = clamp(e.get("y", 900), y0 + 40, y1 - 40); e["x"] = clamp(e.get("x", 540), 120, 960)
            if e.get("to"): e["to"] = [clamp(e["to"][0], 120, 960), clamp(e["to"][1], y0 + 40, y1 - 40)]
            if e.get("label") and e.get("label_y") is not None: e["label_y"] = clamp(e["label_y"], y0, y1 + 20)
            if e.get("label") and e.get("label_y") is None and e.get("to") and e["to"][1] + 90 > y1 + 20: e["label_y"] = min(e["y"], e["to"][1]) - 70
        elif e.get("label"):
            ly = e.get("label_y", e["y"] - e.get("h", e.get("w", 340) * 0.7) / 2 - 70)
            if ly < y0 - 30: ly = e["y"] + e.get("h", e.get("w", 340) * 0.7) / 2 + 60
            e["label_y"] = clamp(ly, y0 - 30, y1 + 30)
            if e.get("label_x") is not None: e["label_x"] = clamp(e["label_x"], 200, 880)
        if e.get("label"): e["label"] = e["label"].replace("№", "#")
    return e


# ---------------------------------------------------------------- build
def build(job):
    d = f"{B}/{job}"; spec = J[job]
    s = json.load(open(d + "/script.json", encoding="utf-8")); st = json.load(open(d + "/brief_style.json", encoding="utf-8"))
    mu = json.load(open(d + "/brief_music.json", encoding="utf-8")); hk = json.load(open(d + "/brief_hooks.json", encoding="utf-8"))
    im = json.load(open(d + "/images.json", encoding="utf-8")); imgs_known = set(im)
    ge = json.load(open(d + "/brief_gestures.json", encoding="utf-8")) if os.path.exists(d + "/brief_gestures.json") else {"elements": {}}
    theme = dict(st["theme"]); acc, acc2 = theme["accent"], theme["accent2"]
    SC = s["scenes"]; N = len(SC); texts = [norm(x["text"]) for x in SC]
    def scene_of(ph, after=0):
        p = norm(ph)
        for k in range(after, N):
            if p and p in texts[k]: return k
        return None
    # payoff = first scene that SPEAKS a payoff token (fallback: brief_hooks payoff_scene)
    pay = [scene_of(t) for t in spec.get("forbid_spoken", [])]; pay = [p for p in pay if p is not None]
    payoff = min(pay) if pay else (hk.get("payoff_scene", N) - 1)
    forbid = spec.get("forbid", [])
    els = {k: [] for k in range(N)}

    # 1) designed overlays + own gestures (phrase-anchored)
    for ph, lst in spec["extra"]:
        k = scene_of(ph)
        if k is None: warn(f"{job}: extra phrase '{ph}' not in any scene"); continue
        for e in lst:
            e = json.loads(json.dumps(e))
            if e["type"] == "char" and job.endswith("anqara") and not ANQARA_PORTRAITS: continue
            if k < payoff and leaks(e, forbid): warn(f"{job}: S{k + 1} payoff leak dropped {leaks(e, forbid)} in {e['type']}"); continue
            e["_own"] = True; els[k].append(e)
    # 2) old gesture brief, re-anchored by `at` phrase (first scene that contains it without leaking the payoff)
    kept = dropped = 0
    for old_n, lst in ge.get("elements", {}).items():
        for e in lst:
            e = json.loads(json.dumps(e)); at = e.get("at")
            if not isinstance(at, str) or at in ("start", "end"): dropped += 1; continue
            if e.get("label") in spec.get("relabel", {}): e["label"] = spec["relabel"][e["label"]]
            k = scene_of(at)
            while k is not None and k < payoff and leaks(e, forbid): k = scene_of(at, k + 1)
            if k is None: dropped += 1; continue
            if e["type"] == "prop" and e["img"] not in imgs_known: dropped += 1; continue
            e["_old"] = True; els[k].insert(0, e); kept += 1

    # 3) per-scene assembly
    out_scenes = []; n_hero = 0
    for k, sc in enumerate(SC):
        n = sc["n"]; nn = f"{n:02d}"; spk = sc["speaker"]; text = sc["text"]
        lst = els[k]; is_final = any(e["type"] == "final" for e in lst)
        has_hero = any(e["type"] == "char" for e in lst)
        has_card = any(e["type"] in ("card", "stamp", "bars", "note") and e.get("y", 1400) > 1200 for e in lst)
        char_scene = spk != NARRATOR
        if char_scene:
            ch = dict(spec["chars"].get(spk, {"name": spk.upper(), "img": None, "tag": "navy", "side": "left"}))
            for ph, ov in spec.get("per", {}).items():
                if norm(ph) in texts[k]: ch.update(ov)
            side = ch["side"]
            hl = {}
            for w in text.split():
                if w.endswith(("!", "?")) and len(hl) < 2 and len(norm(w)) > 3: hl[w] = "red"
            bub = {"type": "bubble", "speaker": ch["name"], "x": 540, "y": 330, "at": "start", "hl": hl, "tail": "down",
                   "tail_x": 0.25 if side == "left" else 0.75, "tag": ch["tag"], "w": 880}
            front = [bub]
            if ch.get("img") and not (job.endswith("anqara") and not ANQARA_PORTRAITS):
                c = {"type": "char", "img": ch["img"], "from": side, "x": 270 if side == "left" else 810, "y": 1440, "h": 700, "at": 0.1,
                     "motion": "idle", "flip": False, "talk": ["vo"]}
                if ch.get("moods"): c["moods"] = ch["moods"]
                if ch.get("label") and not any(o["type"] == "char" and o.get("label") == ch["label"] for sc_ in out_scenes for o in sc_["elements"]):
                    c["label"] = ch["label"]; c["label_bg"] = ch["tag"]
                front.append(c); n_hero += 1
            lst = front + lst
            zone = (600, 1060)
        elif is_final:
            zone = (450, 780)
        else:
            zone = (520, 1120) if not has_hero else (520, 1080)
            if not has_card:
                hits = [(ph, w) for ph, w in spec.get("cap", {}).items() if norm(ph) in texts[k]]
                cp = max(hits, key=lambda h: len(h[0]))[::-1] if hits else None   # longest key wins ("bir yarim" vs "yarim")
                words, at = cp if cp else auto_caption(text)
                if k < payoff and leaks({"words": words}, forbid): words, at = auto_caption(text)
                lst.append({"type": "caption", "words": words, "color": "yellow" if k % 2 else "white", "y": 1200 if has_hero else 1330,
                            "size": 84 if has_hero else 96, "at": at})
            n_hero += has_hero
        # gestures: fit into the free zone, cap per scene
        used = []; g = 0; final_list = []
        for e in lst:
            if is_gesture(e):
                if g >= MAX_PER_SCENE: continue
                if e["type"] == "mark": colorize(e, acc, acc2)
                fit(e, zone, used); g += 1
            final_list.append(e)
        x = {"n": n, "speaker": spk, "text": text, "tts": sc.get("tts", text), "mood": "groove", "img": sc["img"], "elements": final_list,
             "vo": sc["reuse"] or f"vo_{nn}.mp3", "voice_id": CAST.get(spk, CAST[NARRATOR])}
        if sc.get("imgs"): x["imgs"] = list(sc["imgs"])
        out_scenes.append(x)

    # 4) top up: every scene >= 1 gesture, video total within [MIN_G, MAX_G]
    def gcount(): return sum(1 for x in out_scenes for e in x["elements"] if is_gesture(e))
    pg = sorted(k for k in imgs_known if k.startswith("p_g_")) or ["p_g_undov.jpg"]
    for k, x in enumerate(out_scenes):
        if any(is_gesture(e) for e in x["elements"]): continue
        if any(e["type"] == "final" for e in x["elements"]):
            e = prop(pg[k % len(pg)], 880, 560, 230, 1.0, "pulse")
        elif x["speaker"] != NARRATOR:
            side_left = any(e["type"] == "char" and e["x"] < 540 for e in x["elements"])
            e = prop(pg[k % len(pg)], 860 if side_left else 220, 760, 230, "end" if len(x["text"]) < 40 else 1.2, ["pulse", "jump", "wag", "bounce"][k % 4])
            fit(e, (600, 1060), [])
        else:
            capy = next((c["y"] for c in x["elements"] if c["type"] == "caption"), None)
            e = mark("underline", 540, (capy + 80) if capy else 1100, 480, at="end" if capy is None else 1.0)
            colorize(e, acc, acc2)
        x["elements"].append(e)
    if gcount() < MIN_G:   # second gesture in the longest-text scenes
        for k in sorted(range(N), key=lambda k: -len(out_scenes[k]["text"])):
            if gcount() >= MIN_G: break
            x = out_scenes[k]
            if x["speaker"] == NARRATOR and not any(e["type"] == "final" for e in x["elements"]):
                e = prop(pg[(k + 3) % len(pg)], 220 if k % 2 else 860, 640, 220, 1.5, "pulse"); fit(e, (520, 1080), [(o["x"], o["y"]) for o in x["elements"] if o["type"] == "prop"])
                x["elements"].append(e)
    while gcount() > MAX_G:   # trim from the busiest scenes, old brief items first
        k = max(range(N), key=lambda k: sum(is_gesture(e) for e in out_scenes[k]["elements"]))
        el = out_scenes[k]["elements"]; cand = [e for e in el if is_gesture(e)]
        el.remove(next((e for e in cand if e.get("_old")), cand[-1]))
    for x in out_scenes:
        for e in x["elements"]: e.pop("_own", None); e.pop("_old", None)

    # 5) music moods: old brief keys are per OLD scene numbers -> stretch over the new scene list
    mk = sorted(mu.get("moods", {}), key=int); mv = [mu["moods"][q] for q in mk if mu["moods"][q] != "finale"] or ["groove"]
    for k, x in enumerate(out_scenes):
        x["mood"] = mv[round(k * (len(mv) - 1) / max(1, N - 2))] if k < N - 1 else "finale"
    if 0 <= payoff < N - 1: out_scenes[payoff]["mood"] = "hero"

    # 6) cover
    lay = s.get("cover_layout") or (st.get("cover") or {}).get("layout", "classic")
    cv = dict(st.get("cover") or {}); cv.pop("flow_prompt", None)
    if spec.get("cover"): cv.update(spec["cover"])
    cv.update(spec.get("cover_fix", {}))
    cv.setdefault("layout", lay); cv.setdefault("img", "cover.jpg"); cv.setdefault("accent", acc); cv.setdefault("accent2", acc2)
    if job.endswith("anqara") and not ANQARA_PORTRAITS: cv.pop("char", None)
    title = list(s["cover"])
    if job.endswith("yuzga-qol"): title = ["SOATIGA", "NECHA MARTA?"]
    for t in title + [s.get("cover_sub", ""), str(cv.get("badge", ""))]:
        if leaks({"label": t}, forbid): warn(f"{job}: cover text leaks payoff: {t}")

    out = {"title": s["title"], "pace": "fast", "music": mu["music"], "music_seed": mu["music_seed"], "music_gain": mu.get("music_gain", 0.75),
           "cover_title": title, "cover_sub": s.get("cover_sub", ""), "cover_scene": 0, "cover": cv, "anim": "static", "bright": True,
           "theme": theme, "end_hold": 1.2, "scenes": out_scenes}
    json.dump(out, open(d + "/scenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # 7) report: files, gesture count, rough timing of re-hooks / payoff
    need = set()
    for x in out_scenes:
        need.add("img/" + x["img"]); need |= {"img/" + i for i in x.get("imgs", [])}; need.add("aud/" + x["vo"])
        for e in x["elements"]:
            if e.get("img"): need.add("img/" + e["img"])
            for m_ in e.get("moods", []): need.add("img/" + m_[0])
    need.add("img/" + cv["img"]); need |= {"img/" + p for p in cv.get("props", [])}
    if cv.get("char"): need.add("img/" + cv["char"])
    missing = sorted(p for p in need if not os.path.exists(f"{d}/{p}"))
    unknown = sorted(p for p in need if p.startswith("img/") and p[4:] not in imgs_known)
    if unknown: warn(f"{job}: images not in images.json: {unknown}")
    if missing:
        mi = [p for p in missing if p.startswith("img/")]; ma = [p for p in missing if p.startswith("aud/")]
        warn(f"{job}: MISSING {len(mi)} images, {len(ma)} audio" + (f" (e.g. {(mi + ma)[:4]})" if mi or ma else ""))
    ds = [dur(f"{d}/aud/{x['vo']}") for x in out_scenes]
    tline = ""
    if all(v is not None for v in ds):
        st_ = 0; starts = []
        for v in ds: starts.append(st_); st_ += v + 0.18
        tot = st_ + 1.2
        long_ = [f"S{k + 1}:{v:.1f}s" for k, v in enumerate(ds) if v > 6.0]
        tline = f" | ~{tot:.0f}s, payoff S{payoff + 1}@{starts[payoff]:.0f}s ({starts[payoff] / tot:.0%})" + (f", VO>6s: {' '.join(long_)}" if long_ else "")
        if tot < 70: warn(f"{job}: estimated duration {tot:.0f}s < 70s")
    print(f"{job}: {N} sahna, {gcount()} imo-ishora (eski brief: {kept} saqlandi, {dropped} tashlandi), {n_hero} personaj stikeri, "
          f"stamp={sum(e['type'] in ('stamp', 'big') for x in out_scenes for e in x['elements'])}, muqova={cv['layout']}{tline}")


def make_cutouts(job):
    """offline fallback for stickers (no rembg model download): key out the plain white background connected to the border
    and cache it as <name>_cut.png, which reel/engine.py load_rgba() uses as-is."""
    import numpy as np, cv2
    from PIL import Image
    d = f"{B}/{job}"; sc = json.load(open(d + "/scenes.json", encoding="utf-8")); names = set()
    for x in sc["scenes"]:
        for e in x["elements"]:
            if e["type"] in ("char", "prop", "avatar"): names.add(e["img"]); names |= {m[0] for m in e.get("moods", [])}
    cv = sc.get("cover", {}); names |= set(cv.get("props", [])); names |= {cv["char"]} if cv.get("char") else set()
    made = 0
    for nm in sorted(names):
        p = f"{d}/img/{nm}"; out = p.rsplit(".", 1)[0] + "_cut.png"
        if not os.path.exists(p) or os.path.exists(out): continue
        rgb = np.asarray(Image.open(p).convert("RGB")); hh, ww = rgb.shape[:2]
        mask = np.zeros((hh + 2, ww + 2), np.uint8); sm = cv2.GaussianBlur(rgb, (5, 5), 0)
        edges = cv2.dilate(cv2.Canny(cv2.cvtColor(sm, cv2.COLOR_RGB2GRAY), 30, 90), np.ones((3, 3), np.uint8), iterations=2)
        mask[1:-1, 1:-1] = (edges > 0).astype(np.uint8)   # outlines act as walls: the fill can't leak into white shirts / faces
        seeds = [(x, 0) for x in range(0, ww, 16)] + [(0, y) for y in range(0, int(hh * 0.8), 16)] + [(ww - 1, y) for y in range(0, int(hh * 0.8), 16)]
        for (sx, sy) in seeds:   # floating-range flood fill from top/left/right edges: follows flash falloff on off-white walls
            if mask[sy + 1, sx + 1] == 0 and sm[sy, sx].min() > 110:
                cv2.floodFill(sm.copy(), mask, (sx, sy), 0, (6, 6, 6), (6, 6, 6), 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
        fg = (mask[1:-1, 1:-1] != 255).astype(np.uint8)
        fg = cv2.erode(fg, np.ones((3, 3), np.uint8), iterations=2)   # drop the edge-wall halo outside the subject
        n_, lab, stats, _ = cv2.connectedComponentsWithStats(fg, connectivity=8)
        if n_ > 1:
            big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])); keep = [i for i in range(1, n_) if stats[i, cv2.CC_STAT_AREA] > 0.08 * stats[big, cv2.CC_STAT_AREA]]
            fg = np.isin(lab, keep).astype(np.uint8)
        a = fg * 255
        Image.fromarray(np.dstack([rgb.astype(np.uint8), a])).save(out); made += 1
    print(f"{job}: {made} ta stiker kesildi (oq fon, oflayn)")


if __name__ == "__main__":
    cut = "--cut" in sys.argv
    jobs = [a for a in sys.argv[1:] if not a.startswith("--")] or sorted(J)
    for j in jobs: build(os.path.basename(j.rstrip("/")))
    if cut:
        for j in jobs: make_cutouts(os.path.basename(j.rstrip("/")))
    for w in WARN: print("WARN", w)
