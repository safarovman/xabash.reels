# -*- coding: utf-8 -*-
"""18-okt: script.json + brief_style/music/gestures + images.json -> scenes.json, post.json (video yig'uvchi)."""
import json, os, sys
B = os.path.dirname(os.path.abspath(__file__))
CAST = {"bekzod": "kGOig3GPePLxobJGHo2M", "dilnoza": "O72h9AUwisM6Zj4He72B", "zilola": "cyPun3bl9MxcpLBX6pT0",
        "nodira": "132QLQIkg1RJGmpicuhR", "shahnoza": "eggZu1Ffe4if51TKev2v", "jahongir": "xDwfBjUEPdIoQekNOXAX",
        "sardor": "UjuEL3hLLUaDED9iW4Yb", "malika": "VTN9ql0D5MshokKncKAy"}
def bubble(sp, tagc, hl=None, y=330, tail="down", tail_x=0.3, at="start"):
    return {"type": "bubble", "speaker": sp, "x": 540, "y": y, "at": at, "hl": hl or {}, "tail": tail, "tail_x": tail_x, "tag": tagc, "w": 880}
def char(img, side="right", x=None, y=1440, h=760, at=0.2, moods=None, label=None, lbg="green", talk=True, motion="idle", out=None, flip=False):
    if x is None: x = {"right": 790, "left": 290, "bottom": 540, "pop": 540}[side]
    d = {"type": "char", "img": img, "from": side, "x": x, "y": y, "h": h, "at": at, "motion": motion, "flip": flip}
    if talk: d["talk"] = ["vo"]
    if moods: d["moods"] = moods
    if label: d["label"] = label; d["label_bg"] = lbg
    if out: d["out"] = out
    return d
def prop(img, x=780, y=1250, h=380, at=0.3, motion="bounce", label=None):
    d = {"type": "prop", "img": img, "x": x, "y": y, "h": h, "at": at, "motion": motion, "from": "pop"}
    if label: d["label"] = label
    return d
def tag(head, text, x=170, y=210, color="red", at="start"): return {"type": "tag", "head": head, "text": text, "x": x, "y": y, "color": color, "at": at}
def pill(t, bg="navy", x=600, y=300, at="start", rot=-3): return {"type": "pill", "text": t, "bg": bg, "fg": "white", "x": x, "y": y, "rot": rot, "at": at}
def note(t, y=1560, at="start", size=66, rot=-2): return {"type": "note", "text": t, "y": y, "size": size, "rot": rot, "at": at}
def sticker(lines, color="yellow", x=760, y=420, w=420, at="start", rot=4, size=50): return {"type": "sticker", "lines": lines, "color": color, "x": x, "y": y, "w": w, "size": size, "rot": rot, "at": at}
def card(k, title, sub, at=0.3, y=1320): return {"type": "card", "kicker": k, "title": title, "sub": sub, "at": at, "y": y}
def clock(day, t): return {"type": "clock", "day": day, "time": t, "at": "start"}
def bars(rows, y=900, at=0.4): return {"type": "bars", "rows": rows, "x": 540, "y": y, "at": at}
def stamp(t, y=1500, at="end", rot=-5): return {"type": "stamp", "text": t, "y": y, "rot": rot, "at": at}
def final(lines): return {"type": "final", "lines": lines, "at": 0.4}
def dark(a=0.4): return {"type": "dark", "amount": a, "at": "start"}
def avatar(img, x=880, y=330, size=200, at="start"): return {"type": "avatar", "img": img, "x": x, "y": y, "size": size, "at": at}

X = {}
X["2026-10-18_0800_pult"] = {
 1: [tag("YIL", "1995"), bubble("DADA", "crimson", {"Botir!": "red", "Futbol": "red"}, y=420),
     char("c_dada.jpg", "left", x=280, h=700, at=0.1, label="ERKIN AKA", lbg="crimson", out="Futbol")],
 2: [char("c_botir.jpg", "right", x=800, h=820, at="pult bor edi", talk=False, label="PULT", lbg="orange")],
 3: [sticker(["PULT VAZIFALARI:", "kanal", "ovoz", "antenna", "o'chirish"], "yellow", x=780, y=430, w=440, at=0.2)],
 4: [bubble("DADA", "crimson", {"antennani": "red", "Qimirlama!": "red"}, y=330)],
 5: [bubble("MAFTUNA", "purple", {"ikki": "red", "soatdan": "red"}, y=330),
     char("c_botir_charchagan.jpg", "right", x=800, h=760, at="Qo'li", talk=False)],
 6: [card("ZENITH, 1950", ["«LAZY BONES»", "SIMLI PULT"], "Birinchi pultlardan biri televizorga sim bilan ulangan edi.", at="Zenith"), tag("YIL", "1950", color="navy")],
 7: [tag("YIL", "1956", color="navy"), card("ROBERT ADLER, ZENITH", ["SIMSIZ «KLIKKER»"], "Ultratovushli pult: tugma bosilganda «chiq» etardi.", at="klikker", y=1330)],
 8: [bubble("DADA", "crimson", {"klikkerimiz": "red", "chiq": "red"}, y=330),
     char("c_dada.jpg", "left", x=270, h=680, at=0.1, moods=[["c_dada_kulgan.jpg", "Botir!"]], talk=True)],
 9: [tag("YIL", "2026", color="green"), char("c_katta_botir.jpg", "right", x=800, h=760, at="Endi", talk=False, label="BOTIR, 42", lbg="royal")],
 10: [bubble("BOTIR", "royal", {"ovozli": "red", "antenna": "red"}, y=330),
      char("c_katta_botir.jpg", "left", x=270, h=700, at=0.1)],
 11: [final(["SIZ PULT", "BO'LGANMISIZ?"]), sticker(["1 — ha, men edim", "2 — opam edi", "3 — pult bor edi"], "pink", x=540, y=1450, w=640, at=1.2, rot=-2, size=52)],
}
X["2026-10-18_1230_bepul-sinov"] = {
 1: [pill("BEPUL!", "crimson", x=780, y=300, at="«bepul»"), char("c_nigora.jpg", "right", x=800, h=760, at="Nigora", talk=False, label="NIGORA", lbg="crimson")],
 2: [bubble("NIGORA", "crimson", {"Yetti": "red", "bepul!": "red", "buxgalterman-ku!": "red"}, y=330),
     char("c_nigora_hayajon.jpg", "left", x=270, h=700, at=0.1)],
 3: [tag("KUN", "7", x=170, y=210, color="red", at="Yetti"), tag("OY", "3", x=910, y=210, color="navy", at="uch")],
 4: [bubble("ULUG'BEK", "royal", {"Premium": "red", "Plyus": "red", "Gold»": "red"}, y=330),
     char("c_ulugbek.jpg", "right", x=810, h=740, at=0.1, label="ULUG'BEK", lbg="royal")],
 5: [bubble("NIGORA", "crimson", {"meditatsiya": "red"}, y=330), char("c_nigora_xijolat.jpg", "left", x=270, h=720, at=0.1)],
 6: [bubble("ULUG'BEK", "royal", {"asabim": "red"}, y=330)],
 7: [dark(0.35), bars([["O'YLAGANI", 86, "yellow"], ["ASLIDA", 219, "red"]], y=880, at="sakson"),
     card("C+R RESEARCH, 2022", ["$86 → $219"], "Odamlar obunaga sarfini qariyb 2,5 baravar kam deb o'ylagan.", at="Hisoblaganda", y=1330)],
 8: [stamp("-$133 / OY", y=1450, at="bir yuz", rot=-6), prop("p_karta.jpg", x=800, y=1050, h=360, at=0.2, motion="shake")],
 9: [bubble("SHAHZODA", "orange", {"o'zidayoq": "red", "bekor": "red"}, y=330), char("c_shahzoda.jpg", "right", x=800, h=740, at=0.1, label="SHAHZODA", lbg="orange")],
 10: [char("c_nigora_hayron.jpg", "left", x=270, h=700, at="o'n", talk=False), note("11 ta obuna. Biri — buxgalteriya kursi.", at="Ulardan")],
 11: [final(["OBUNALARINGIZNI", "TEKSHIRING!"]), sticker(["Izohda yozing:", "nechta chiqdi?"], "blue", x=540, y=1450, w=560, at=1.2, rot=-3)],
}
X["2026-10-18_1600_ai-muzlatkich"] = {
 1: [clock("2045", "02:14"), char("c_jamshid.jpg", "left", x=280, h=760, at="Jamshid", talk=False, label="JAMSHID", lbg="royal")],
 2: [bubble("SOVUQJON", "green", {"uchinchi": "red", "qulflandi.": "red"}, y=330), char("c_sovuqjon.jpg", "right", x=820, h=720, at=0.1, label="AI MUZLATKICH", lbg="green")],
 3: [bubble("JAMSHID", "royal", {"mening": "red", "pul": "red"}, y=330), char("c_jamshid_jahl.jpg", "left", x=270, h=740, at=0.1)],
 4: [bubble("SOVUQJON", "green", {"kredit": "red", "bodring": "red"}, y=330)],
 5: [pill("SKANER: YOQILGAN", "green", x=600, y=300, at=0.2)],
 6: [tag("YIL", "2000", color="navy"), card("LG, IYUN 2000", ["INTERNETGA ULANGAN", "BIRINCHI MUZLATKICH"], "Eshigida ekran, ichida kamera bor edi.", at="LG", y=1330)],
 7: [tag("YIL", "2024", color="navy"), card("SAMSUNG «AI VISION INSIDE»", ["33 XIL MAHSULOT"], "Ichki kamera mahsulotlarni ko'rib taniydi.", at="o'ttiz", y=1330)],
 8: [bubble("JAMSHID", "royal", {"bitta": "red", "kolbasa.": "red"}, y=330), char("c_jamshid_yolvorish.jpg", "left", x=280, h=700, at=0.1)],
 9: [bubble("SOVUQJON", "green", {"onangizga": "red"}, y=330)],
 10: [bubble("ONASI", "purple", {"ikkida": "red", "oshga": "red"}, y=330), avatar("c_ona.jpg", x=880, y=640, size=240, at=0.1),
      char("c_jamshid_qorqqan.jpg", "left", x=270, h=700, at=0.2, talk=False)],
 11: [note("Kolbasani muzlatkich o'zi saqlaydi.", at="Kolbasani")],
 12: [final(["KOLBASA", "KIMNIKI?"]), sticker(["1 — kerak, ozaman", "2 — kolbasa meniki!"], "green", x=540, y=1450, w=620, at=1.2, rot=-2, size=52)],
}
X["2026-10-18_1830_non-odobi"] = {
 1: [pill("UYIMIZ QOIDASI", "orange", x=620, y=300, at=0.3)],
 2: [bubble("SHERZOD", "royal", {"baribir": "red"}, y=330), char("c_sherzod.jpg", "right", x=800, h=740, at=0.1, label="SHERZOD", lbg="royal")],
 3: [bubble("BUVI", "crimson", {"teskari": "red", "rizqing": "red"}, y=330),
     char("c_buvi_hayron.jpg", "left", x=270, h=720, at=0.1, label="MALIKA BUVI", lbg="crimson")],
 4: [pill("TONG, 05:30", "navy", x=600, y=300, at="tongda")],
 5: [bubble("RAHMAT AKA", "green", {"kechasi": "red", "tandir": "red"}, y=330), char("c_rahmat.jpg", "right", x=810, h=740, at=0.1, label="NOVVOY", lbg="green")],
 6: [bubble("SHERZOD", "royal", {"issiq": "red"}, y=330), char("c_sherzod_vahima.jpg", "left", x=270, h=700, at=0.1)],
 7: [card("RIVOYAT", ["SAMARQAND NONI"], "Buxoro amiri un va suvni ham Samarqanddan keltirtiribdi.", at="Unni", y=1330)],
 8: [note("«Samarqandning havosini olib kelolmadim».", at="Amirim", size=62)],
 9: [card("2022-YIL", ["KUNIGA ~15 000 TA", "SAMARQAND NONI"], "Rivoyat — rivoyat, raqam esa haqiqiy.", at="o'n besh", y=1330)],
 10: [bubble("BUVI", "crimson", {"mehnat.": "red", "hurmat": "red"}, y=330), char("c_buvi.jpg", "left", x=270, h=720, at=0.1)],
 11: [char("c_buvi_mamnun.jpg", "right", x=810, h=700, at="to'ppa-to'g'ri", talk=False)],
 12: [final(["SIZNING UYINGIZDA", "QANDAY ODAT BOR?"]), prop("p_non.jpg", x=540, y=1450, h=360, at=1.2, motion="pulse")],
}
X["2026-10-18_2100_yuzga-qol"] = {
 1: [pill("SIZ, HOZIR", "crimson", x=600, y=300, at="To'xtang.")],
 2: [char("c_jasur.jpg", "right", x=810, h=760, at="Jasur", talk=False, label="JASUR, KASSIR", lbg="royal")],
 3: [bubble("ZARINA", "purple", {"pul": "red", "ko'zingizni": "red"}, y=330), char("c_zarina.jpg", "left", x=270, h=720, at=0.1, label="ZARINA", lbg="purple")],
 4: [bubble("JASUR", "royal", {"umuman": "red"}, y=330), char("c_jasur.jpg", "right", x=810, h=740, at=0.1)],
 5: [tag("SANOQ", "1 SOAT", color="red", at="Zarina")],
 6: [tag("YIL", "2015", color="navy"), card("KWOK VA BOSHQ., 2015", ["SOATIGA 23 MARTA"], "26 tibbiyot talabasi videoga olingan.", at="yigirma uch", y=1330)],
 7: [bars([["Og'iz", 36, "red"], ["Burun", 31, "yellow"], ["Ko'z", 27, "green"]], y=880, at="og'iz"), note("Tegishlarning 44 foizi — og'iz, burun, ko'z.", at="Mikroblar")],
 8: [bubble("GAVHAR OPA", "green", {"yuving.": "red", "to'xtang.": "red"}, y=330), char("c_gavhar.jpg", "right", x=810, h=740, at=0.1, label="SHIFOKOR", lbg="green")],
 9: [bubble("JASUR", "royal", {"umuman": "red"}, y=330), char("c_jasur_qatiy.jpg", "left", x=270, h=720, at=0.1)],
 10: [pill("VA'DA: 12 SONIYA", "crimson", x=600, y=300, at="o'n ikki")],
 11: [bubble("ZARINA", "purple", {"Yigirma": "red", "to'rtinchi!": "red"}, y=330), char("c_jasur_qichish.jpg", "right", x=810, h=700, at=0.1, talk=False)],
 12: [final(["NECHA MARTA", "TEGDINGIZ?"]), sticker(["Rostini", "izohda yozing!"], "green", x=540, y=1450, w=520, at=1.2, rot=-3)],
}

def build(job):
    d = f"{B}/{job}"; s = json.load(open(d + "/script.json")); st = json.load(open(d + "/brief_style.json"))
    mu = json.load(open(d + "/brief_music.json")); ge = json.load(open(d + "/brief_gestures.json")); im = json.load(open(d + "/images.json"))
    acc = st["theme"]["accent"]; acc2 = st["theme"]["accent2"]
    scenes = []
    for sc in s["scenes"]:
        n = sc["n"]; nn = f"{n:02d}"
        frames = [k for k in sorted(im) if k.startswith(nn) and k != nn + ".jpg"]
        els = list(X[job].get(n, []))
        for g in ge["elements"].get(str(n), []):
            g = dict(g)
            if g["type"] == "mark":
                c = g.get("color"); g["color"] = acc2 if c == "yellow" else (acc if c in (None, "red") else c)
            els.append(g)
        x = {"speaker": sc["speaker"], "text": sc["text"], "tts": sc["tts"], "mood": mu["moods"].get(str(n), "groove"),
             "img": nn + ".jpg", "elements": els, "vo": f"vo_{nn}.mp3", "voice_id": CAST[sc["speaker"]]}
        if frames: x["imgs"] = frames
        scenes.append(x)
    theme = dict(st["theme"])
    out = {"title": s["title"], "pace": "fast", "music": mu["music"], "music_seed": mu["music_seed"], "music_gain": mu.get("music_gain", 0.75),
           "cover_title": s["cover"], "cover_sub": s["cover_sub"], "cover_scene": 0, "anim": "static", "bright": True, "theme": theme, "scenes": scenes}
    json.dump(out, open(d + "/scenes.json", "w"), ensure_ascii=False, indent=1)
    post = {"slot": "2026-10-18T" + job.split("_")[1][:2] + ":" + job.split("_")[1][2:] + "+05:00", "title": s["title"], "theme": s["slot"],
            "trial": False, "schedulingType": "automatic", "mode": "customScheduled", "caption": s["caption"], "status": "yasalmoqda"}
    if not os.path.exists(d + "/post.json"): json.dump(post, open(d + "/post.json", "w"), ensure_ascii=False, indent=1)
    ne = sum(len(x["elements"]) for x in scenes); ni = len(scenes) + sum(len(x.get("imgs", [])) for x in scenes)
    print(job, len(scenes), "sahna", ni, "kadr", ne, "element")
if __name__ == "__main__":
    for j in (sys.argv[1:] or sorted(X)): build(j)
