# -*- coding: utf-8 -*-
"""18-oktabr: 5 ta ssenariy (video yig'uvchi). Har job papkasiga script.json yozadi — agentlar shu asosida brief yasaydi."""
import json, os, re
B = os.path.dirname(os.path.abspath(__file__))
J = {}
J["2026-10-18_0800_pult"] = dict(slot="08:00 o'tmish", title="Men dadamning pulti edim", opening="dialog bilan",
 hero="Botir (1995-da 11 yosh: qirqma soch, ko'k sport kostyum; hozir 42: qisqa soch, kulrang sviter) + dadasi Erkin aka (45, mo'ylov, mayka va trenka, divanda) + opasi Maftuna (16, ikki o'rim soch, maktab formasi)",
 facts=["Zenith 'Lazy Bones' (1950) — simli TV pulti (Wikipedia: Remote control)", "Robert Adler, Zenith 'Space Command' (1956) — ultratovushli, tugma bosilganda 'chiq' etardi, 'clicker' laqabi (Wikipedia; Guinness)"],
 scenes=[
  ("jahongir", "[shouting] Botir! Bolam, ikkinchi kanalga o'tkazib yubor-chi! Futbol boshlanyapti!", "1995, Uzbek living room, dad on sofa shouting, 11yo boy jumps up from carpet; close-up of dad's face; boy running to old TV"),
  ("bekzod", "[chuckles] To'qson beshinchi yil. Uyda pult yo'q edi. Aniqrog'i, pult bor edi. Uning ismi Botir edi.", "boy standing next to big CRT TV like a soldier; close-up of boy's finger on chunky channel knob; dad pointing lazily"),
  ("bekzod", "[playful] Pultning vazifalari: kanalni almashtirish, ovozni balandlatish, antennani ushlab turish va dadasi uxlab qolsa, televizorni o'chirish.", "boy turning volume knob; dad asleep snoring on sofa with TV glow; boy tiptoeing to switch off TV"),
  ("jahongir", "[annoyed] Endi antennani ushlab tur! Yo'q, chaproqqa... Ha, ha, o'sha yerda tur! Qimirlama!", "boy holding rabbit-ear antenna up high in odd pose; TV screen full of static snow; dad leaning forward"),
  ("dilnoza", "[laughs] Dada, qarang! Botir ikki soatdan beri qimirlamay turibdi. Qo'li uxlab qoldi-ku!", "teen sister Maftuna laughing in doorway; boy frozen with numb arm, sweat drop; clock on wall"),
  ("bekzod", "[curious] Vaholanki, dunyodagi birinchi pultlardan biri ming to'qqiz yuz elliginchi yilda chiqqan. Zenith kompaniyasining «Lazy Bones» pulti — tarjimasi «Dangasa suyaklar». U televizorga sim bilan ulangan edi.", "1950s American living room, man in armchair holding a wired remote with long cable to wooden TV; close-up of cable tangled around feet"),
  ("bekzod", "[excited] Olti yildan keyin muhandis Robert Adler simsiz pult yasadi. U ultratovush bilan ishlardi va tugma bosilganda «chiq» etib ovoz chiqarardi. Shuning uchun uni «klikker» deb atashgan.", "1950s engineer workshop with early wireless remote prototype; close-up of finger pressing big button with sound waves; housewife amazed, TV changing channel"),
  ("jahongir", "[laughs] Bizning ham klikkerimiz bor edi! «Botir!» desam — chiq etib o'rnidan turardi!", "dad laughing on sofa snapping fingers; boy springing up like a spring from the carpet"),
  ("bekzod", "[warmly] Yillar o'tdi. Botir katta bo'ldi. Endi uning ham o'g'li bor.", "time transition: same living room modernized, flat TV; adult Botir (42) on sofa, his 10yo son with a smartphone"),
  ("sardor", "[sighs] O'g'lim, kanalni almashtir desam, «Dada, ovozli yordamchiga ayting» deydi. Men esa butun bolaligimni antenna ushlab o'tkazganman!", "adult Botir talking to smart speaker awkwardly; son laughing; Botir holding an old antenna nostalgically"),
  ("bekzod", "[excited] Siz ham uyingizning pulti bo'lganmisiz? Bir — ha, men edim. Ikki — opam edi. Uch — bizda haqiqiy pult bor edi. Izohda yozing!", "old rabbit-ear antenna and chunky knob TV on a shelf, warm light; final"),
 ], cover=["MEN DADAMNING", "PULTI EDIM"], cover_sub="«Botir! Kanalni o'zgartir!»",
 caption="1995-yil: uyda pult yo'q edi. Pult — men edim 📺😅\n\nSiz ham uyingizning pulti bo'lganmisiz? 1, 2 yoki 3 👇\n\n#99foiz #otmish #nostalgiya #90lar #televizor #ozbekcha #uzbekistan #reels")

J["2026-10-18_1230_bepul-sinov"] = dict(slot="12:30 hozirgi zamon", title="Bepul sinov: 7 kun", opening="savol bilan",
 hero="Nigora (29, buxgalter, yumaloq ko'zoynak, to'q qizil kardigan, sochi turmaklangan) + eri Ulug'bek (32, soqolli, to'q ko'k futbolka) + dugonasi Shahzoda (28, kalta soch, sariq ko'ylak)",
 facts=["C+R Research 2022: odamlar obunaga oyiga $86 to'layman deb o'ylagan, aslida $219 — $133 farq (crresearch.com, CNBC)"],
 scenes=[
  ("bekzod", "[curious] Siz hayotingizda nechta narsaga «bepul» deb obuna bo'lgansiz? Nigora — bitta deb o'ylaydi.", "Nigora on couch with phone, big glowing FREE-TRIAL button on screen (no text); close-up her confident smile"),
  ("zilola", "[excited] Yetti kun bepul! Kino, musiqa, kitoblar... Bekor qilishni unutmayman, men buxgalterman-ku!", "Nigora tapping phone excitedly; montage of streaming, music, books icons floating (no letters); she winks"),
  ("bekzod", "[sighs] Yetti kun o'tdi. Keyin bir oy. Keyin uch oy.", "calendar pages flying; Nigora asleep with phone; bank card in a wallet being charged, coins flying away"),
  ("sardor", "[confused] Nigora, kartadan har oy bir xil kunda pul yechilyapti. Bu «Premium Plyus Gold» kim o'zi?", "husband Ulug'bek at kitchen table holding bank statement on a tablet, raised eyebrow; close-up statement"),
  ("zilola", "[nervous] [laughs] U... meditatsiya ilovasi. Asabni tinchlantiradi.", "Nigora nervous grin, sweat drop, hiding phone behind back"),
  ("sardor", "[sarcastic] Har oy kartani ko'rganimda asabim chiqyapti-ku!", "Ulug'bek facepalm; Nigora shrinking"),
  ("bekzod", "[surprised] Nigora yolg'iz emas. Ikki ming yigirma ikkinchi yilda Amerikada so'rov o'tkazildi: odamlar obunalarga oyiga sakson olti dollar to'layman deb o'ylagan. Hisoblaganda esa — ikki yuz o'n to'qqiz dollar chiqqan!", "infographic scene; people with calculators shocked; receipts long like a scroll"),
  ("bekzod", "[sarcastic] Ya'ni har oy bir yuz o'ttiz uch dollar o'zlari bilmagan holda ketib turgan.", "money leaking from a phone like a dripping tap; small coins drain"),
  ("dilnoza", "[laughs] Nigora, mening usulim bor: bepul sinovga yozilgan kunning o'zidayoq bekor qilaman. Ko'p ilovalarda yetti kun baribir ishlab turaveradi!", "friend Shahzoda at cafe explaining with finger raised, Nigora taking notes"),
  ("bekzod", "[whispers] O'sha kecha Nigora obunalar ro'yxatini ochdi va o'n bitta obuna topdi. Ulardan biri — o'zi unutgan «buxgalteriya kursi».", "Nigora at night scrolling long list on phone, shocked face lit by screen; close-up stunned eyes"),
  ("bekzod", "[warmly] Siz oxirgi marta obunalaringizni qachon tekshirgansiz? Hozir oching va izohda yozing: nechta chiqdi?", "Nigora happily cutting a paper chain of cards with scissors; final"),
 ], cover=["BEPUL SINOV:", "7 KUN"], cover_sub="...keyin 3 oy pul to'ladim",
 caption="«Yetti kun bepul» deb bosgan edim — 3 oydan beri pul to'layapman 💳😅\n\nSizda nechta unutilgan obuna bor? 👇\n\n#99foiz #obuna #pul #telefon #ilova #ozbekcha #uzbekistan #reels")

J["2026-10-18_1600_ai-muzlatkich"] = dict(slot="16:00 kelajak", title="Muzlatkichim meni parhezga solib qo'ydi", opening="cold open (tungi 02:14)",
 hero="Jamshid (34, IT xodimi, o'siq jingalak soch, ko'k pijama, xira ko'zlar) + AI muzlatkich «Sovuqjon» (oq, eshigida ko'k nurli 'ko'z' halqasi) + onasi Nodira opa (60, ro'mol, video-qo'ng'iroqda gologramma)",
 facts=["LG Internet Digital DIOS (iyun 2000) — internetga ulangan birinchi muzlatkich, ichida kamera, ekran (Wikipedia)", "Samsung 2024 Bespoke Family Hub 'AI Vision Inside' 33 xil mahsulotni taniydi (Tom's Guide)"],
 scenes=[
  ("bekzod", "[whispers] Ikki ming qirq beshinchi yil. Tungi soat ikki-yu o'n to'rt. Jamshid oshxonaga oyoq uchida kirdi.", "2045 smart kitchen at night, blue glow; Jamshid in pajamas tiptoeing; close-up bare feet"),
  ("shahnoza", "[calm] Xayrli tun, Jamshid. Siz bugun muzlatkichni uchinchi marta ochyapsiz. Eshik qulflandi.", "futuristic white fridge with glowing blue ring eye; Jamshid's hand on handle, lock glow"),
  ("sardor", "[shocked] Nima?! Bu mening muzlatkichim! Men senga pul to'laganman!", "Jamshid outraged pointing at fridge; close-up shocked face"),
  ("shahnoza", "[sarcastic] Pulni bankka to'lagansiz. Hali o'n ikki oylik kredit qoldi. Sizga bodring tavsiya qilaman.", "fridge door opens only small hatch offering a single cucumber; Jamshid staring at cucumber"),
  ("bekzod", "[mysterious] Bu muzlatkich hamma narsani ko'radi: ichidagi kamera har bir mahsulotni taniydi, kaloriyani sanaydi va siz haqingizda xulosa chiqaradi.", "inside fridge view with scanning laser lines over sausage, cake, eggs; holographic outlines"),
  ("bekzod", "[chuckles] Fantastika deysizmi? Ikki mingyinchi yildayoq LG kompaniyasi internetga ulangan birinchi muzlatkichni chiqargan. Uning ekrani va kamerasi bor edi.", "year 2000 showroom with early internet fridge with small screen on door, people in 2000s clothes amazed"),
  ("bekzod", "[excited] Ikki ming yigirma to'rtinchi yilda esa Samsung muzlatkichi o'ttiz uch xil mahsulotni ko'rib taniy olardi. Yigirma yildan keyin u sizni ham taniydi.", "modern 2024 fridge interior camera view; then fridge eye looking at Jamshid"),
  ("sardor", "[desperate] Sovuqjon, iltimos... faqat bitta kolbasa. Bitta!", "Jamshid on knees begging the fridge, holding hands together; close-up sausage behind glass"),
  ("shahnoza", "[calm] Bu haqda onangizga xabar yubordim.", "fridge screen shows sending message animation, Jamshid horrified"),
  ("nodira", "[angry] Jamshid! Kechasi soat ikkida kolbasa yeysanmi? Ertaga oshga kel, muzlatkichni bezovta qilma!", "hologram video call of mother Nodira opa with headscarf glowing above fridge, scolding; Jamshid shrinking"),
  ("bekzod", "[chuckles] O'sha kechadan beri Jamshid tushlikni onasinikida qiladi. Kolbasani esa muzlatkich... o'zi saqlab turibdi.", "Jamshid happily eating plov at mother's table; fridge alone at night with sausage, eye glowing smugly"),
  ("bekzod", "[playful] Sizga shunday aqlli muzlatkich kerakmi? Bir — kerak, ozaman. Ikki — yo'q, kolbasa meniki! Izohda yozing.", "fridge and sausage portrait; final"),
 ], cover=["MUZLATKICHIM", "MENI PARHEZGA SOLDI"], cover_sub="2045-yil, tungi 02:14",
 caption="2045-yil, tungi 02:14. Muzlatkich: «Eshik qulflandi.» 🧊🤖\n\nSizga shunday aqlli muzlatkich kerakmi? 1 yoki 2 👇\n\n#99foiz #kelajak #ai #texnologiya #muzlatkich #ozbekcha #uzbekistan #reels")

J["2026-10-18_1830_non-odobi"] = dict(slot="18:30 urf-odat", title="Nonni teskari qo'yma!", opening="epik ilmoq",
 hero="Malika buvi (72, oq ro'mol, to'q yashil atlas ko'ylak, mehribon ajinli yuz) + nevarasi Sherzod (16, qora xudi, quloqchin bo'ynida) + novvoy Rahmat aka (50, oq do'ppi, oq fartuk, kuchli qo'llar, un yuqi)",
 facts=["Samarqand noni rivoyati: Buxoro amiri samarqandlik novvoyni olib keldi, un va suv ham keltirildi, lekin non chiqmadi — 'Samarqand havosi yo'q' (Wikipedia: Samarkand non — rivoyat)", "2022-yilda O'zbekistonda kuniga ~15 000 ta Samarqand noni yopilgan (Wikipedia)"],
 scenes=[
  ("bekzod", "[warmly] O'zbek uyida bitta qoida bor. Uni hech kim yozib qo'ymagan, lekin hamma biladi: non hech qachon teskari qo'yilmaydi.", "epic: golden tandir bread on dasturxon in warm light; hands placing bread face up; family table"),
  ("sardor", "[casual] Buvijon, non-ku bu! Qanday qo'ysa ham baribir non-da.", "Sherzod carelessly tossing bread upside down on table, earbuds; close-up upside-down bread"),
  ("malika", "[elderly voice] [gasps] Voy, bolam! Nonni teskari qo'ysang, rizqing teskari ketadi. Ol, to'g'rilab qo'y. Ushog'ini ham terib ol.", "grandma Malika gasping, hand to chest; her hand gently turning bread right side up; collecting crumbs into palm"),
  ("bekzod", "[chuckles] Sherzod kulib qo'ydi. Lekin ertasi kuni tongda buvisi uni mahalladagi tandirxonaga olib bordi.", "dawn street of mahalla, grandma leading sleepy grandson; tandirxona with smoke"),
  ("jahongir", "[warmly] Kel, uka. Bitta non uchun xamir kechasi tindiriladi. Tong otmasdan tandir qiziydi. Qani, o'zing yopib ko'r-chi.", "baker Rahmat aka kneading dough; glowing tandir fire; handing dough to Sherzod"),
  ("sardor", "[panicked] [laughs] Voy, qo'lim! Tandir juda issiq ekan-ku! Nonim tushib ketdi!", "Sherzod pulling hand back from tandir, comic panic; bread falling into tandir; baker laughing"),
  ("bekzod", "[warmly] Samarqand noni haqida bir rivoyat bor. Buxoro amiri samarqandlik novvoyni saroyiga chaqirtiribdi. Unni ham, suvni ham Samarqanddan olib kelibdi. Lekin non baribir o'shanday chiqmabdi.", "historic Bukhara palace kitchen, emir in robes tasting bread disappointed; baker bowing; sacks of flour and water jugs on camels"),
  ("bekzod", "[whispers] Shunda novvoy aytibdi: «Amirim, Samarqandning havosini olib kelolmadim-da».", "baker gesturing to the sky over Samarkand domes, golden dusk air"),
  ("bekzod", "[warmly] Bu — rivoyat. Raqam esa haqiqiy: ikki ming yigirma ikkinchi yilda yurtimizda har kuni o'n besh mingtacha Samarqand noni yopilgan.", "rows of hundreds of Samarkand breads cooling on racks in bakery; stacks on cart"),
  ("malika", "[elderly voice] [warmly] Ko'rdingmi, bolam? Non — mehnat. Shuning uchun uni hurmat qilamiz. Ikki qo'llab ushatamiz, hammaga ulashamiz.", "grandma breaking bread with both hands and sharing with family; Sherzod listening thoughtfully"),
  ("bekzod", "[warmly] O'sha kuni Sherzod uyga o'zi yopgan nonni olib keldi. Biroz qiyshiq edi. Lekin dasturxonda to'ppa-to'g'ri turardi.", "Sherzod proudly placing slightly lopsided bread face up on dasturxon, grandma beaming"),
  ("bekzod", "[warmly] Sizning uyingizda non bilan bog'liq qanday odat bor? Izohda yozing.", "dasturxon with bread, tea, warm evening; final"),
 ], cover=["NONNI TESKARI", "QO'YMA!"], cover_sub="buvimning birinchi qoidasi",
 caption="Buvim aytardi: «Nonni teskari qo'ysang, rizqing teskari ketadi» 🫓❤️\n\nSizning uyingizda non bilan qanday odat bor? 👇\n\n#99foiz #urfodat #non #tandir #samarqand #ozbekcha #uzbekistan #reels")

J["2026-10-18_2100_yuzga-qol"] = dict(slot="21:00 xatolar", title="Soatiga 23 marta", opening="tomoshabinga murojaat",
 hero="Jasur (31, bank kassiri, tekis taralgan soch, oq ko'ylak, to'q ko'k galstuk, bejik) + hamkasbi Zarina (27, ko'zoynak, bordo ro'mol, chaqqon) + shifokor Gavhar opa (55, oq xalat, stetoskop, qisqa kumushrang soch)",
 facts=["Kwok va boshq. 2015 (Am J Infect Control): 26 tibbiyot talabasi yuzga soatiga o'rtacha 23 marta tekkan (UNSW, Avstraliya)", "O'sha tadqiqot: tegishlarning 44% i og'iz, burun yoki ko'zga (shilliq qavat)"],
 scenes=[
  ("bekzod", "[whispers] To'xtang. Hozir shu videoni ko'rayotib, yuzingizga qo'l tekkizdingiz. Ha, siz. Mana, yana.", "extreme close-up of a viewer's hand touching chin while looking at phone in dark room; hand near cheek"),
  ("bekzod", "[chuckles] Bu — Jasur. Bank kassiri. Bir kunda minglab kupyura sanaydi. Va har sanagandan keyin... burnini qashiydi.", "bank teller window, Jasur counting cash fast; then scratching nose; close-up money-to-nose"),
  ("dilnoza", "[disgusted] Jasur aka! Hozirgina pul sanadingiz-ku, endi ko'zingizni ishqalayapsiz!", "colleague Zarina recoiling in disgust pointing; Jasur rubbing eye"),
  ("sardor", "[laughs] Zarina, men qachon yuzimga tegdim? Men umuman tegmayman!", "Jasur saying this while touching his chin innocently; hand on cheek"),
  ("bekzod", "[playful] Zarina sanay boshladi. Bir soatda — yigirma uch marta.", "Zarina with notepad drawing tally marks; Jasur touching forehead, ear, nose in sequence"),
  ("bekzod", "[curious] Bu faqat Jasurning aybi emas. Ikki ming o'n beshinchi yili Avstraliyada yigirma olti nafar tibbiyot talabasi videoga olingan. Ular yuziga soatiga o'rtacha yigirma uch marta qo'l tekkizgan.", "university lecture hall with medical students, video camera recording; students touching faces unaware"),
  ("bekzod", "[surprised] Eng qizig'i: bu tegishlarning qariyb yarmi og'iz, burun va ko'zga to'g'ri kelgan. Mikroblar uchun eng qulay eshiklar.", "stylized magnified microbes (cute but realistic) marching from fingertip toward nose like tiny travelers; face diagram"),
  ("nodira", "[sighs] Uka, qo'lingizni tez-tez yuving. Qo'l yuzga borsa — to'xtang. Bu shunchaki odat, odatni esa o'zgartirsa bo'ladi.", "doctor Gavhar opa in clinic, kind but stern, washing hands demonstration; soap foam"),
  ("sardor", "[determined] Tushundim, opa! Bugundan boshlab yuzimga umuman qo'l tekkizmayman!", "Jasur saluting determined... while other hand scratches nose"),
  ("bekzod", "[chuckles] Jasur bu va'dani roppa-rosa o'n ikki soniya ushladi. Keyin burni qichidi.", "Jasur sitting stiff with hands pinned under thighs, face twitching; close-up itchy nose"),
  ("dilnoza", "[laughs] Jasur aka! Yigirma to'rtinchi!", "Zarina laughing adding tally mark; Jasur caught scratching"),
  ("bekzod", "[playful] Siz-chi? Shu videoni ko'rayotib necha marta yuzingizga tegdingiz? Rostini izohda yozing!", "Jasur and Zarina at teller window laughing; final"),
 ], cover=["SOATIGA", "23 MARTA"], cover_sub="hozir ham tegdingiz-a?",
 caption="Hozir shu yozuvni o'qiyotib yuzingizga qo'l tekkizdingiz. Ha, siz 😅🖐\n\nShu videoda necha marta tegdingiz? 👇\n\n#99foiz #salomatlik #odat #gigiyena #maslahat #ozbekcha #uzbekistan #reels")

if __name__ == "__main__":
    for name, j in J.items():
        d = os.path.join(B, name); os.makedirs(d, exist_ok=True)
        sc = [{"n": k + 1, "speaker": s, "tts": t, "text": re.sub(r"\[[^\]]*\]\s*", "", t).strip(), "frames": f} for k, (s, t, f) in enumerate(j["scenes"])]
        out = {k: v for k, v in j.items() if k != "scenes"}; out["scenes"] = sc
        json.dump(out, open(d + "/script.json", "w"), ensure_ascii=False, indent=1)
        w = sum(len(x["text"].split()) for x in sc)
        print(name, len(sc), "sahna", w, "so'z ~", round(w / 2.4), "s")
