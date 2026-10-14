"""v2 scripts: each video has its own protagonist and its own opening structure."""
import json, os
P = "Hand-drawn storybook illustration, fine ink crosshatching linework, rich painted gouache colors, vertical 9:16 composition, no text, no letters, no logos. "
DIL = "the same young Uzbek woman as in the reference image (about 22, long black braid, round face, oversized lilac hoodie)"
STU = "the same slim young Uzbek student as in the reference image (about 19, thin face, round glasses, short neat black hair, dark green hoodie)"
NOD = "the same young Uzbek woman as in the reference image (about 27, dark hair in a neat bun, white blouse, beige cardigan)"
J = {}

J["2026-10-15_0000_yana-bitta-video"] = dict(title="Yana bitta video…", cover_title=["YANA BITTA", "VIDEO…"], cover_sub="23:00 → 02:47", music_seed=23, scenes=[
 dict(vo="new", text="Soat ikki-yu qirq yetti. U hali ham «oxirgi video»ni ko'ryapti.", mood="tense",
      img=("NEW", P + "Night close-up: a young Uzbek woman, about 22, long black braid, round face, oversized lilac hoodie, lying in bed in a dark bedroom, face lit cold blue by the smartphone, wide tired eyes, a faint smile, messy blanket, deep blue darkness around."),
      el=[dict(type="clock", day="TUN", time="02:47", at="start"),
          dict(type="caption", words=["«OXIRGI", "VIDEO»"], color="yellow", y=1420, at="oxirgi"),
          dict(type="stamp", text="47-CHISI", y=1600, rot=-5, at="koryapti")]),
 dict(vo="new", text="To'rt soat oldin hammasi boshqacha edi.", mood="sad",
      img=("REF", P + DIL + " in the evening at 11 pm sitting on her bed in pajamas, hair neatly braided, putting a sleep mask on her forehead, determined proud face, warm lamp light, tidy cozy Uzbek bedroom with a carpet on the wall."),
      el=[dict(type="note", text="4 soat oldin…", size=110, y=1480, rot=-3, at=0)]),
 dict(vo="night_s2", text="Soat o'n bir. «Bugun erta yotaman». Telefon — faqat budilnik qo'yish uchun.", mood="groove",
      img=("REF", P + DIL + " lying in bed under a floral blanket at night, holding her phone above her face to set an alarm, confident face, dark blue window with city lights."),
      el=[dict(type="clock", day="TUN", time="23:00", at="start"),
          dict(type="note", text="«bugun erta yotaman»", size=80, y=1520, rot=-2, at="bugun erta")]),
 dict(vo="night_s3", text="Bitta video. Yana bitta. Bu ham qiziq ekan...", mood="groove",
      img=("REF", P + "Close-up: " + DIL + " in bed at night, face lit blue by the phone screen, eyes wide and hypnotized, giggling, dark room."),
      el=[dict(type="pill", text="1 VIDEO", bg="navy", fg="yellow", x=300, y=480, rot=-5, at="bitta video"),
          dict(type="pill", text="+1", bg="navy", fg="yellow", x=760, y=560, rot=5, at="yana bitta"),
          dict(type="pill", text="+1 +1 +1", bg="navy", fg="yellow", x=520, y=700, rot=-3, at="qiziq")]),
 dict(vo="night_s5", text="Ertalab — ko'z ochilmaydi, choy ham yordam bermaydi.", mood="groove",
      img=("REF", P + DIL + " at the breakfast table in the morning like a sleepy zombie, eyes half closed, braid messy, head about to drop, holding a piyola of tea, round bread on the table, bright morning light, her mother in the background shaking her head."),
      el=[dict(type="note", text="choy ham yordam bermaydi…", size=74, y=1540, rot=2, at="choy")]),
 dict(vo="night_s6", text="Olimlar buni «uxlashni kechiktirish» deb atashadi: hech narsa xalaqit bermasa ham, uyquni orqaga suramiz.", mood="mystery", anim="static",
      img=("REUSE:06", None),
      el=[dict(type="dark", amount=0.35, at="start"),
          dict(type="card", kicker="Psixologiya", title=["UXLASHNI", "KECHIKTIRISH"], sub="Kroese va boshq. · 2014", y=560, at=0.3),
          dict(type="note", text="hech narsa xalaqit bermasa ham", size=66, y=960, rot=1.5, at="hech narsa")]),
 dict(vo="night_s7", text="Sababi oddiy: kun bo'yi o'zimizga vaqt qolmaydi — uni kechasi o'g'irlab olamiz.", mood="mystery",
      img=("REF", P + "Playful scene at night: " + DIL + " tiptoeing like a cartoon thief in a dark hallway, carrying a sack and sneakily pulling the hands off a giant wall clock, dark blue tones, funny."),
      el=[dict(type="dark", amount=0.2, at="start"),
          dict(type="caption", words=["VAQTNI"], color="white", y=1330, at="vaqt"),
          dict(type="caption", words=["O‘G‘IRLAYMIZ"], color="yellow", y=1455, at="ogirlab")]),
 dict(vo="night_s8", text="Lekin har kecha bir soat kam uxlasangiz — haftasiga yetti soat. Bu bitta to'liq tun.", mood="warm",
      img=("REF", P + DIL + " sleeping peacefully and happily in a cozy bed hugging a pillow, the phone placed face-down far away on a shelf charging, soft moonlight, calm atmosphere."),
      el=[dict(type="note", text="1 soat × 7 kun", size=80, y=1250, rot=-1, at="har kecha"),
          dict(type="big", text="= 1 TUN", y=1450, rot=-2, at="bitta toliq")]),
 dict(vo="night_s9", text="Telefoningizni qo'ying. Hoziroq. ...Bu videodan keyin, albatta.", mood="finale",
      img=("REF", P + DIL + " in bed at night looking straight at the viewer with a sly smile, holding the glowing phone, one finger raised as if saying just one more, dark blue room."),
      el=[dict(type="caption", words=["TELEFONNI", "QO‘YING."], color="white", y=1320, at=0),
          dict(type="hide_captions", at="bu videodan"),
          dict(type="dark", amount=0.5, at="bu videodan"),
          dict(type="final", lines=["BU VIDEODAN", "KEYIN"], y=880, at="bu videodan")])])

J["2026-10-15_0600_ozing-izlab-top"] = dict(title="O'zing izlab top", cover_title=["«O‘ZING", "IZLAB TOP»"], cover_sub="daftaring qani?", music_seed=37, scenes=[
 dict(vo="new", text="«Daftaring qani?» Dasturlash darsida eshitgan birinchi savolim shu bo'ldi.", mood="tense",
      img=("NEW", P + "Classroom, dramatic low angle: a strict middle-aged teacher in a grey suit pointing sternly at an empty desk, while a slim young Uzbek student, about 19, thin face, round glasses, short neat black hair, dark green hoodie, holds up his open laptop with code on screen, confused. Green chalkboard, old desks, window light."),
      el=[dict(type="pill", text="DAFTARING QANI?", bg="crimson", size=70, x=540, y=430, rot=-3, at=0),
          dict(type="caption", words=["DASTURLASH", "DARSIDA"], color="white", y=1330, at="dasturlash"),
          dict(type="stamp", text="1-SAVOL", y=1520, rot=4, at="birinchi")]),
 dict(vo="new", text="Men rahbarga bordim: «Nega bu mavzuni o'tmaymiz?» Javob: «Ustozingdan so'ra».", mood="groove",
      img=("REF", P + STU + " standing in a formal university office asking a stern boss in a suit sitting behind a big desk piled with papers; the boss points to the door without looking up."),
      el=[dict(type="note", text="«nega bu mavzuni o‘tmaymiz?»", size=70, y=380, rot=-2, at="nega"),
          dict(type="stamp", text="USTOZINGDAN SO‘RA", size=88, y=1580, rot=4, at="ustozingdan")]),
 dict(vo="new", text="Ustozga bordim. Javob: «O'zing izlab top».", mood="groove",
      img=("REF", P + STU + " in a classroom asking a teacher standing by a green chalkboard; the teacher shrugs and waves his hand dismissively."),
      el=[dict(type="stamp", text="«O‘ZING IZLAB TOP»", size=92, y=1580, rot=-4, at="ozing izlab")]),
 dict(vo="new", text="Lekin... mavzuni o'tish — ustozning vazifasi emasmi?", mood="tense",
      img=("REF", P + STU + " sitting at a school desk scratching his head, puzzled face, big hand-drawn question marks floating around him, a laptop on the desk."),
      el=[dict(type="caption", words=["USTOZNING"], color="white", y=1330, at="ustozning"),
          dict(type="caption", words=["VAZIFASI?"], color="yellow", y=1455, at="vazifasi")]),
 dict(vo="new", text="Uyda ota-onam so'raydi: «Dasturlashdan nimani o'rganding?» Nima ko'rsataman — daftarnimi?", mood="groove",
      img=("REF", P + "Uzbek family dinner at home: proud parents asking expectantly, while " + STU + " awkwardly holds up a notebook full of handwritten notes, embarrassed smile. Warm lamp light, tea on the table."),
      el=[dict(type="note", text="«nimani o‘rganding?»", size=78, y=380, rot=-2, at="nimani"),
          dict(type="caption", words=["DAFTARNIMI?"], color="yellow", y=1455, at="daftarnimi")]),
 dict(vo="new", text="«Ustoz, qachon amaliyot qilamiz?» — «Avval daftaringdagini ko'rsat».", mood="groove",
      img=("REF", P + "A computer lab with all monitors switched off and covered with dust covers; " + STU + " eagerly pointing at a computer, while the strict teacher holds up a notebook and taps it."),
      el=[dict(type="note", text="«qachon amaliyot qilamiz?»", size=74, y=380, rot=-2, at=0),
          dict(type="stamp", text="DAFTARINGNI KO‘RSAT!", size=86, y=1580, rot=4, at="avval daftaringdagini")]),
 dict(vo="new", text="Tadqiqotlar ko'rsatadi: faqat ma'ruza tinglagan talabalar amaliyot qilganlarga qaraganda bir yarim baravar ko'proq yiqiladi.", mood="mystery", anim="static",
      img=("NEWBG", P + "Moody dark scene: an empty lecture hall at dusk with rows of desks and a big chalkboard full of text, one laptop glowing on a desk, deep blue shadows, lots of empty space at the top."),
      el=[dict(type="dark", amount=0.35, at="start"),
          dict(type="card", kicker="Tadqiqot", title=["AMALIYOT", "YUTADI"], sub="Freeman va boshq. · PNAS 2014", y=560, at=0.3),
          dict(type="big", text="1,5× KO‘P YIQILADI", size=110, y=1250, rot=-2, at="bir yarim")]),
 dict(vo="new", text="Dasturlash daftarda emas — kompyuterda o'rganiladi. Sizda ham shunaqa ustoz bo'lganmi?", mood="finale",
      img=("REF", P + STU + " at night happily coding on his laptop at home, the screen glowing, a notebook closed and pushed aside, confident smile, cozy room."),
      el=[dict(type="caption", words=["DAFTARDA", "EMAS —"], color="white", y=1320, at=0),
          dict(type="caption", words=["KOMPYUTERDA."], color="yellow", y=1445, at="kompyuterda"),
          dict(type="hide_captions", at="sizda ham"),
          dict(type="dark", amount=0.5, at="sizda ham"),
          dict(type="final", lines=["SIZDA HAM", "SHUNAQAMI?"], y=880, size=130, at="sizda ham")])])

J["2026-10-15_1200_47-soniya"] = dict(title="8 soat ish = 47 soniya", cover_title=["8 SOAT ISH", "= 47 SONIYA"], cover_sub="diqqatingiz qayerda?", music_seed=41, scenes=[
 dict(vo="new", text="Qirq yetti soniya. Bu videoni ham taxminan shuncha ko'rasiz... agar omadim kelsa.", mood="tense", anim="static",
      img=("NEWBG", P + "Dramatic scene: a giant old stopwatch floating in a dark modern office at night, its hand near 47 seconds, many small glowing phone notification bubbles swirling around it, deep blue and gold light."),
      el=[dict(type="big", text="47 SONIYA", size=150, y=1300, rot=-3, at=0),
          dict(type="note", text="…agar omadim kelsa", size=78, y=1520, rot=2, at="agar")]),
 dict(vo="new", text="Bu Nodira. U bugun sakkiz soat ishladi. Aniqrog'i — qirq yetti soniyadan.", mood="sad",
      img=("NEW", P + "A young Uzbek woman office worker, about 27, dark hair in a neat bun, white blouse, beige cardigan, sitting at an office desk with a computer, smiling proudly at the camera, a cup of tea and papers on the desk, bright office."),
      el=[dict(type="caption", words=["8", "SOAT"], color="white", y=1330, at="sakkiz"),
          dict(type="stamp", text="…47 SONIYADAN", y=1520, rot=-4, at="aniqrogi")]),
 dict(vo="new", text="Soat to'qqiz. Ishni boshladi. Bildirishnoma: «Siz guruhga qo'shildingiz».", mood="groove",
      img=("REF", P + NOD + " at an office desk in the morning starting work on a computer, focused, then glancing at her buzzing smartphone."),
      el=[dict(type="clock", day="ISH KUNI", time="09:00", at="start"),
          dict(type="pill", text="+1 GURUH", bg="royal", x=760, y=640, rot=5, at="guruhga")]),
 dict(vo="new", text="Qarindoshlar guruhi: tug'ilgan kun tabrigi, ikki yuz ta stiker.", mood="groove",
      img=("REF", P + NOD + " at her desk scrolling the phone with an amused face, the phone screen bursting with dozens of colorful cartoon sticker bubbles flying out around her. Funny."),
      el=[dict(type="pill", text="TABRIK!", bg="orange", x=300, y=480, rot=-6, at="tugilgan"),
          dict(type="pill", text="+200 STIKER", bg="purple", x=740, y=620, rot=4, at="ikki yuz")]),
 dict(vo="new", text="Ishga qaytdi. «Qayerda edim?» ...Yana boshidan.", mood="groove",
      img=("REF", P + NOD + " staring at a computer screen full of spreadsheets with a confused face, hand on forehead, sticky notes everywhere, papers scattered."),
      el=[dict(type="note", text="«qayerda edim?»", size=84, y=420, rot=-2, at="qayerda"),
          dict(type="stamp", text="YANA BOSHIDAN", y=1580, rot=4, at="yana boshidan")]),
 dict(vo="new", text="Tushlik — telefon bilan. Tushlikdan keyin ham — telefon.", mood="groove",
      img=("REF", P + NOD + " eating lunch (a bowl of lagman) at the office kitchen with one hand while scrolling the phone with the other, noodles hanging, distracted."),
      el=[dict(type="clock", day="TUSHLIK", time="13:00", at="start"),
          dict(type="pill", text="YANA TELEFON", bg="navy", fg="yellow", x=540, y=1540, rot=-2, at="keyin ham")]),
 dict(vo="new", text="Olima Gloria Mark hisoblagan: ikki ming to'rtinchi yilda ekranga diqqatimiz ikki yarim daqiqa edi. Hozir — qirq yetti soniya.", mood="mystery", anim="static",
      img=("NEWBG", P + "Moody dark scene: a lone computer monitor and a smartphone glowing in a dark office at night, many small light rectangles like notifications floating in the air, deep blue darkness with empty space at the top."),
      el=[dict(type="dark", amount=0.35, at="start"),
          dict(type="card", kicker="Tadqiqot", title=["DIQQAT", "VAQTI"], sub="Gloria Mark · UC Irvine", y=540, at=0.3),
          dict(type="pill", text="2004: 2,5 DAQIQA", bg="royal", x=540, y=1050, rot=-2, at="ikki ming"),
          dict(type="big", text="HOZIR: 47 SONIYA", size=110, y=1280, rot=-2, at="hozir")]),
 dict(vo="new", text="Hamkasbi esa bildirishnomalarni o'chirib qo'ydi. Ishni ikki soat oldin tugatdi.", mood="warm",
      img=("NEWBG", P + "A calm young Uzbek man colleague, about 30, short beard, blue shirt, working focused at a tidy office desk, his phone placed face-down, a plant and a cup of tea, golden afternoon light, peaceful."),
      el=[dict(type="note", text="bildirishnomalar: O‘CHIQ", size=76, y=360, rot=-2, at="bildirishnomalarni"),
          dict(type="big", text="−2 SOAT", y=1450, rot=-2, at="ikki soat")]),
 dict(vo="new", text="Bildirishnomalarni o'chirishga jur'atingiz yetadimi?", mood="finale",
      img=("REF", P + NOD + " at her desk holding her phone, thumb hovering over a switch, looking at the viewer with a hesitant, funny expression, evening office light."),
      el=[dict(type="dark", amount=0.5, at=0.1),
          dict(type="final", lines=["JUR’ATINGIZ", "YETADIMI?"], y=880, size=130, at="jur")])])

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__)); allp = []
    for job, j in J.items():
        d = f"{base}/{job}"; os.makedirs(f"{d}/img", exist_ok=True); os.makedirs(f"{d}/aud", exist_ok=True)
        sc = []
        for s in j["scenes"]:
            x = dict(text=s["text"], mood=s["mood"], elements=s["el"])
            if s.get("anim"): x["anim"] = s["anim"]
            sc.append(x)
        json.dump(dict(title=j["title"], music_seed=j["music_seed"], cover_title=j["cover_title"], cover_sub=j["cover_sub"], scenes=sc),
                  open(f"{d}/scenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for k, s in enumerate(j["scenes"]):
            allp.append(dict(job=job, n=k + 1, kind=s["img"][0], prompt=s["img"][1], vo=s["vo"], text=s["text"]))
    json.dump(allp, open("/home/claude/xabash_prompts_v2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(allp))
