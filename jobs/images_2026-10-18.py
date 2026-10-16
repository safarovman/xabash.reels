# -*- coding: utf-8 -*-
"""18-okt Flow rasmlari: har job uchun images.json (fayl -> {prompt, ref}). ref = namuna (ingredient) qilinadigan rasm."""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
D = {}
# ---------------- 08:00 pult
BOY = "11-year-old Uzbek boy Botir with a short buzz cut and a faded blue tracksuit"
DAD = "Uzbek father Erkin, 45, thick black mustache, white sleeveless undershirt and dark sweatpants"
SIS = "16-year-old Uzbek girl Maftuna with two long braids, school uniform with white apron"
ADULT = "Uzbek man Botir, 42, short hair with a little grey, grey knitted sweater"
D["2026-10-18_0800_pult"] = {
 "c_dada": ("C", f"{DAD}, lying back on a sofa cushion pose, pointing lazily forward with one finger and shouting, half body", None),
 "c_dada_kulgan": ("C", f"Same man as in the reference image ({DAD}), laughing loudly, snapping his fingers, half body", "c_dada"),
 "c_botir": ("C", f"{BOY}, standing at attention like a soldier, proud serious face, full body", None),
 "c_botir_charchagan": ("C", f"Same boy as in the reference image ({BOY}), exhausted, one arm raised stiffly holding an old rabbit-ear TV antenna, sweat on forehead, full body", "c_botir"),
 "c_botir_hayron": ("C", f"Same boy as in the reference image ({BOY}), jaw dropped in amazement, hands on cheeks, full body", "c_botir"),
 "c_maftuna": ("C", f"{SIS}, laughing and pointing, half body", None),
 "c_katta_botir": ("C", f"{ADULT}, sighing with a wry smile, holding an old rabbit-ear antenna, half body", None),
 "p_antenna": ("P", "old 1990s rabbit-ear TV antenna with two long metal rods", None),
 "01": ("S", f"1995 Uzbek apartment living room with a carpet on the wall and a big wooden CRT television, {DAD} on a sofa shouting toward the boy, {BOY} sitting on the floor carpet turning his head", None),
 "01b": ("S", f"close-up of {DAD} on the sofa shouting with mouth wide open, one finger pointing, TV glow on his face", None),
 "01c": ("S", f"{BOY} jumping up from the carpet and running toward the big CRT television, motion blur", None),
 "02": ("S", f"{BOY} standing stiffly next to a big 1990s CRT television like a guard, father watching from sofa in background", None),
 "02b": ("S", "close-up of a child's finger turning a chunky round channel selector knob on a 1990s Soviet television, number dial", None),
 "03": ("S", f"{BOY} turning the volume knob on the CRT television while the father on the sofa nods approvingly", None),
 "03b": ("S", f"{DAD} asleep and snoring on the sofa, head tilted back, mouth open, television glow in a dark room", None),
 "03c": ("S", f"{BOY} tiptoeing in the dark toward the glowing television to switch it off, finger on lips", None),
 "04": ("S", f"{BOY} on a chair holding a rabbit-ear TV antenna high above his head in an awkward twisted pose, the CRT screen full of grey static snow", None),
 "04b": ("S", f"{DAD} leaning forward from the sofa, squinting at the television, gesturing 'stop right there' with his palm", None),
 "05": ("S", f"{SIS} laughing in the living room doorway, pointing at her little brother", None),
 "05b": ("S", f"close-up of {BOY} frozen holding the antenna, his raised arm trembling and numb, sweat drop on his forehead, wall clock behind", None),
 "06": ("S", "1950s American living room, man in a cardigan in an armchair holding an early wired TV remote with a long cable running to a wooden television set", None),
 "06b": ("S", "close-up of a long tangled remote-control cable wrapped around a man's slippers and a lamp on a 1950s carpet", None),
 "07": ("S", "1950s engineer in a white shirt and tie at a workshop bench holding an early wireless TV remote prototype with four buttons", None),
 "07b": ("S", "1950s housewife sitting on a sofa, amazed, pressing a chunky wireless remote toward a wooden television, finger on the big button", None),
 "08": ("S", f"{DAD} laughing on the sofa and snapping his fingers, {BOY} springing up from the floor like a jack-in-the-box", None),
 "09": ("S", f"same living room 30 years later, modern flat TV on the wall, {ADULT} sitting on the sofa, his 10-year-old son beside him holding a smartphone", None),
 "10": ("S", f"{ADULT} awkwardly talking to a small round smart speaker on the coffee table while his son laughs", None),
 "10b": ("S", f"{ADULT} holding an old rabbit-ear antenna nostalgically in front of a modern flat TV, wry smile", None),
 "11": ("S", "an old 1990s CRT television with a rabbit-ear antenna and a chunky channel knob standing on a shelf in warm evening lamp light, nostalgic still life", None),
}
# ---------------- 12:30 bepul-sinov
NIG = "Uzbek woman Nigora, 29, accountant, round glasses, dark red cardigan, hair in a neat bun"
ULU = "Uzbek man Ulugbek, 32, short dark beard, navy t-shirt"
SHA = "Uzbek woman Shahzoda, 28, short bob haircut, bright yellow dress"
D["2026-10-18_1230_bepul-sinov"] = {
 "c_nigora": ("C", f"{NIG}, confident smile, holding a smartphone, half body", None),
 "c_nigora_hayajon": ("C", f"Same woman as in the reference image ({NIG}), excited, fist pump, half body", "c_nigora"),
 "c_nigora_xijolat": ("C", f"Same woman as in the reference image ({NIG}), nervous guilty grin, sweat drop, hiding a phone behind her back, half body", "c_nigora"),
 "c_nigora_hayron": ("C", f"Same woman as in the reference image ({NIG}), shocked, mouth open, hands on cheeks, half body", "c_nigora"),
 "c_ulugbek": ("C", f"{ULU}, suspicious raised eyebrow, holding a tablet, half body", None),
 "c_shahzoda": ("C", f"{SHA}, cheerful, one finger raised explaining a clever idea, half body", None),
 "p_karta": ("P", "a bank card with coins flying out of it", None),
 "01": ("S", f"{NIG} relaxing on a couch in a modern Tashkent apartment holding her phone with a big glowing button on the screen", None),
 "01b": ("S", f"close-up of {NIG} with a confident smile, phone light reflecting in her glasses", None),
 "02": ("S", f"{NIG} tapping her phone excitedly, colorful icons of film, music note and books bursting out of the screen", None),
 "02b": ("S", f"{NIG} winking and pointing at herself proudly, a calculator and ledgers on her desk", None),
 "03": ("S", "calendar pages flying through the air in a whirlwind over a modern apartment", None),
 "03b": ("S", f"{NIG} asleep on the couch with her phone on her chest at night", None),
 "03c": ("S", "a bank card inside an open wallet with coins flying away from it like birds", None),
 "04": ("S", f"{ULU} sitting at a kitchen table holding a tablet showing a bank statement, raising one eyebrow suspiciously", None),
 "04b": ("S", "close-up of a tablet screen showing repeated identical red charges in a list, abstract shapes only", None),
 "05": ("S", f"{NIG} grinning nervously with a big sweat drop, hiding her phone behind her back in the kitchen", None),
 "06": ("S", f"{ULU} doing a facepalm at the kitchen table while {NIG} shrinks behind a chair", None),
 "07": ("S", "a group of shocked adults holding calculators and extremely long paper receipts unrolling to the floor like scrolls", None),
 "07b": ("S", "a giant smartphone with coins pouring out of it into a drain", None),
 "08": ("S", "a smartphone mounted like a kitchen water tap, dripping gold coins into a sink", None),
 "08b": ("S", "close-up of a piggy bank looking empty, last coin falling out", None),
 "09": ("S", f"{SHA} in a bright cafe explaining with one finger raised while {NIG} takes notes in a notebook", None),
 "09b": ("S", f"close-up of {SHA} winking and pressing a cancel button on her phone", None),
 "10": ("S", f"{NIG} at night in bed scrolling an extremely long list on her phone, face lit blue by the screen, shocked", None),
 "10b": ("S", f"extreme close-up of {NIG}'s stunned eyes behind round glasses reflecting a long list", None),
 "11": ("S", f"{NIG} happily cutting a long paper chain of bank cards with big scissors, triumphant", None),
}
# ---------------- 16:00 ai-muzlatkich
JAM = "Uzbek man Jamshid, 34, IT worker, messy curly hair, blue striped pajamas, tired eyes"
FR = "a sleek white futuristic smart refrigerator with a glowing blue circular light ring like an eye on its door"
MOM = "Uzbek woman Nodira, 60, patterned headscarf, kind but strict face"
D["2026-10-18_1600_ai-muzlatkich"] = {
 "c_jamshid": ("C", f"{JAM}, sneaking on tiptoes with a guilty smile, full body", None),
 "c_jamshid_jahl": ("C", f"Same man as in the reference image ({JAM}), outraged, pointing angrily, full body", "c_jamshid"),
 "c_jamshid_yolvorish": ("C", f"Same man as in the reference image ({JAM}), on his knees begging with hands pressed together, full body", "c_jamshid"),
 "c_jamshid_qorqqan": ("C", f"Same man as in the reference image ({JAM}), terrified, shrinking, hands up, full body", "c_jamshid"),
 "c_sovuqjon": ("C", f"{FR}, standing alone, its blue eye ring glowing, full view", None),
 "c_ona": ("C", f"{MOM}, scolding with a raised index finger, half body, as a translucent blue hologram", None),
 "01": ("S", f"2045 smart kitchen at night lit by blue light, {JAM} tiptoeing toward {FR}", None),
 "01b": ("S", "close-up of bare feet tiptoeing on a glossy kitchen floor at night, blue glow", None),
 "02": ("S", f"{FR} with its blue eye ring glowing brighter, a hand gripping its handle, small glowing lock on the door", None),
 "02b": ("S", f"close-up of the glowing blue eye ring of {FR} staring", None),
 "03": ("S", f"{JAM} outraged pointing at {FR} in the night kitchen", None),
 "03b": ("S", f"close-up of shocked face of {JAM}, mouth open, blue light", None),
 "04": ("S", f"{FR} opening only a tiny hatch, offering a single cucumber on a small tray to {JAM}", None),
 "04b": ("S", f"{JAM} staring at a single cucumber in his hand, deeply disappointed", None),
 "05": ("S", "inside view of a futuristic refrigerator with blue scanning laser lines sweeping over sausage, cake and eggs, holographic outlines around each food", None),
 "05b": ("S", "a futuristic refrigerator's holographic panel showing a weighing scale and a heart rate graph, abstract shapes only", None),
 "06": ("S", "year 2000 electronics showroom with an early internet refrigerator with a small screen on its door, visitors in 2000s clothes amazed", None),
 "07": ("S", "a modern 2024 refrigerator interior seen through its built-in camera, fresh vegetables and food neatly arranged with soft recognition frames around them", None),
 "07b": ("S", f"{FR} with its blue eye ring turned toward {JAM}, scanning him with a blue light grid", None),
 "08": ("S", f"{JAM} on his knees begging in front of {FR}, hands pressed together", None),
 "08b": ("S", "close-up of a single sausage behind a frosted glass shelf, lit dramatically like a treasure", None),
 "09": ("S", f"{FR} with a glowing envelope icon floating above it flying away, {JAM} horrified in the background", None),
 "10": ("S", f"a glowing blue hologram of {MOM} floating above the refrigerator scolding with a finger raised, {JAM} shrinking below", None),
 "11": ("S", f"{JAM} happily eating plov at his mother's table in a sunny room with {MOM} smiling", None),
 "11b": ("S", f"{FR} alone in the dark kitchen, its blue eye glowing smugly, a sausage visible inside", None),
 "12": ("S", f"{FR} and a single sausage on a pedestal in front of it, dramatic blue night light, heroic portrait", None),
}
# ---------------- 18:30 non-odobi
BUVI = "elderly Uzbek grandmother Malika, 72, white headscarf, dark green atlas dress, kind wrinkled face"
SHE = "Uzbek teenage boy Sherzod, 16, black hoodie, headphones around his neck"
RAH = "Uzbek baker Rahmat, 50, white skullcap, white apron, strong forearms dusted with flour"
D["2026-10-18_1830_non-odobi"] = {
 "c_buvi": ("C", f"{BUVI}, warm smile, holding a round Uzbek non bread with both hands, half body", None),
 "c_buvi_hayron": ("C", f"Same woman as in the reference image ({BUVI}), gasping with one hand on her chest, half body", "c_buvi"),
 "c_buvi_mamnun": ("C", f"Same woman as in the reference image ({BUVI}), beaming proudly with teary happy eyes, half body", "c_buvi"),
 "c_sherzod": ("C", f"{SHE}, casual shrug with a careless smile, half body", None),
 "c_sherzod_vahima": ("C", f"Same boy as in the reference image ({SHE}), panicking, shaking his burnt hand, half body", "c_sherzod"),
 "c_rahmat": ("C", f"{RAH}, friendly smile, holding a ball of dough, half body", None),
 "p_non": ("P", "a round golden Uzbek tandir non bread with a stamped pattern in the center, face up", None),
 "01": ("S", "golden round Uzbek tandir breads on a dasturxon tablecloth in warm evening light, family hands around the table", None),
 "01b": ("S", "close-up of an elderly woman's hands placing a round non bread face up on the dasturxon", None),
 "02": ("S", f"{SHE} carelessly tossing a round bread upside down onto the table", None),
 "02b": ("S", "close-up of a round non bread lying upside down on a tablecloth", None),
 "03": ("S", f"{BUVI} gasping with her hand on her chest in a cozy Uzbek home", None),
 "03b": ("S", "close-up of an elderly woman's wrinkled hand gently turning a round bread right side up", None),
 "03c": ("S", "close-up of an elderly woman's palm collecting bread crumbs from a tablecloth", None),
 "04": ("S", f"dawn in a mahalla street, {BUVI} leading sleepy {SHE} by the hand toward a bakery with smoke rising", None),
 "05": ("S", f"{RAH} kneading dough in a traditional tandirxona bakery, glowing tandir oven fire behind", None),
 "05b": ("S", f"{RAH} handing a round piece of flattened dough to {SHE}", None),
 "06": ("S", f"{SHE} jerking his hand back from a glowing tandir oven in comic panic, the baker laughing beside him", None),
 "06b": ("S", "close-up of a round dough slipping off the inside wall of a glowing tandir oven", None),
 "07": ("S", "historic Bukhara palace kitchen, an emir in rich silk robes and turban tasting bread with a disappointed face, a baker bowing", None),
 "07b": ("S", "a camel caravan carrying flour sacks and large water jugs across a desert road toward Bukhara", None),
 "08": ("S", "an old baker gesturing toward the sky over the turquoise domes of Samarkand at golden dusk", None),
 "09": ("S", "hundreds of round Samarkand breads cooling on wooden racks in a busy bakery, warm light", None),
 "09b": ("S", "a wooden cart stacked high with round breads in a bazaar morning", None),
 "10": ("S", f"{BUVI} breaking a round bread with both hands and sharing pieces with her family, {SHE} listening thoughtfully", None),
 "11": ("S", f"{SHE} proudly placing a slightly lopsided homemade bread face up on the dasturxon, {BUVI} beaming", None),
 "12": ("S", "a dasturxon with round bread, tea pot and bowls in warm evening lamplight, cozy still life", None),
}
# ---------------- 21:00 yuzga-qol
JAS = "Uzbek man Jasur, 31, bank teller, neatly combed hair, white shirt, dark navy tie, name badge"
ZAR = "Uzbek woman Zarina, 27, glasses, burgundy headscarf, smart office blouse"
GAV = "Uzbek female doctor Gavhar, 55, white coat, stethoscope, short silver hair"
D["2026-10-18_2100_yuzga-qol"] = {
 "c_jasur": ("C", f"{JAS}, innocently touching his chin while smiling, half body", None),
 "c_jasur_qatiy": ("C", f"Same man as in the reference image ({JAS}), saluting with determination, half body", "c_jasur"),
 "c_jasur_qichish": ("C", f"Same man as in the reference image ({JAS}), scratching his nose, caught, embarrassed, half body", "c_jasur"),
 "c_zarina": ("C", f"{ZAR}, disgusted face, pointing, half body", None),
 "c_zarina_kulgi": ("C", f"Same woman as in the reference image ({ZAR}), laughing, holding a notepad with tally marks, half body", "c_zarina"),
 "c_gavhar": ("C", f"{GAV}, kind but stern, raising an index finger, half body", None),
 "01": ("S", "extreme close-up of a person in a dark room looking at a phone, their hand touching their chin, glowing green fingerprint smudges on the skin", None),
 "01b": ("S", "close-up of fingertips rubbing an eye, glowing green smudges", None),
 "02": ("S", f"bank teller window, {JAS} counting a thick stack of banknotes at high speed", None),
 "02b": ("S", f"{JAS} scratching his nose with fingers that just counted money, green glowing smudge on his nose", None),
 "03": ("S", f"{ZAR} recoiling in disgust and pointing at her colleague in a bank office", None),
 "03b": ("S", f"{JAS} rubbing his eye with his fist at the teller desk", None),
 "04": ("S", f"{JAS} smiling innocently while touching his chin and cheek at the bank desk", None),
 "05": ("S", f"{ZAR} writing tally marks in a small notepad with a pen, determined detective face", None),
 "05b": ("S", f"{JAS} touching his forehead, then his ear, multiple-exposure motion showing several hands", None),
 "06": ("S", "university lecture hall with medical students in white coats, a video camera on a tripod recording them, several students unconsciously touching their faces", None),
 "06b": ("S", "close-up of a vintage video camera lens on a tripod pointed at students", None),
 "07": ("S", "macro view of tiny glowing green microbes marching from a fingertip toward a nose like tiny travelers", None),
 "07b": ("S", "close-up of a face profile with glowing green trails leading to the mouth, nose and eyes", None),
 "08": ("S", f"{GAV} in a clinic washing her hands thoroughly with soap foam at a sink, looking at the camera", None),
 "08b": ("S", "close-up of hands lathered with soap foam under running water, the green glow washing away", None),
 "09": ("S", f"{JAS} saluting with determination while his other hand scratches his nose", None),
 "10": ("S", f"{JAS} sitting stiff at his desk with both hands pinned under his thighs, face twitching", None),
 "10b": ("S", f"extreme close-up of the itching nose of {JAS}, eyes crossed", None),
 "11": ("S", f"{ZAR} laughing and adding another tally mark while {JAS} is caught scratching his nose", None),
 "12": ("S", f"{JAS} and {ZAR} laughing together at the bank teller window", None),
}
if __name__ == "__main__":
    for job, imgs in D.items():
        st = json.load(open(f"{B}/{job}/brief_style.json")); gs = json.load(open(f"{B}/{job}/brief_gestures.json"))
        pre = {"S": st["image_prefix"], "C": st["character_prefix"], "P": st["prop_prefix"]}
        out = {}
        for k, (t, p, ref) in imgs.items():
            out[k + ".jpg"] = {"prompt": (pre[t].strip().rstrip(",") + ". " + p + ".").replace("..", "."), "ref": (ref + ".jpg") if ref else None}
        for g in gs["flow_prompts"]:
            out[g["file"]] = {"prompt": g["prompt"].replace("<STYLE>", pre["P"].strip().rstrip(",") + "."), "ref": None}
        json.dump(out, open(f"{B}/{job}/images.json", "w"), ensure_ascii=False, indent=1)
        print(job, len(out), "rasm", sum(1 for k in out if not k.startswith(("c_", "p_"))), "kadr")
