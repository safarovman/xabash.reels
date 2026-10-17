# -*- coding: utf-8 -*-
"""18-okt v2: tarix videolari rasmlari + 7 ta muqova (cover.jpg) -> images.json ga qo'shadi; flow_v2.json (faqat yangi rasmlar)."""
import json, os, re
B = os.path.dirname(os.path.abspath(__file__))
def clean(f): return re.sub(r";?\s*(on-screen|question in big|fast camera|slow push-in|punch-in|hard cut:|sudden reveal:|motion).*?($|;)", "", f).strip(" ;,")
EXTRA = {
 "2026-10-18_1030_gitler-moskva": {
  "01b": ("S", "close-up of an old military map with a circled city and dark arrows, frost creeping over the paper"),
  "04b": ("S", "close-up of heavy tank tracks crushing summer wheat, dust, no insignia"),
  "15b": ("S", "soldiers in plain greatcoats without badges trudging through a blizzard toward a distant city, seen from behind"),
  "17b": ("S", "close-up of a frost-covered soldier's glove and frozen buttons, breath steam, icy wind"),
  "18b": ("S", "Soviet soldiers in white winter camouflage advancing through a snowy forest at dawn"),
  "c_ergash": ("C", "young Uzbek soldier Ergash, 19, kind face, plain 1941 greatcoat and fur ushanka without badges, holding a folded triangle letter, gentle smile, full body"),
  "c_ergash_sovqotgan": ("C", "young Uzbek soldier Ergash, 19, plain frost-covered greatcoat and fur ushanka without badges, shivering, eyes wide from cold, breath steaming, full body"),
  "p_muzlagan_soat": ("P", "a frozen pocket watch covered in frost and ice crystals"),
  "p_uchburchak_xat": ("P", "a folded triangle-shaped WWII front letter, worn paper"),
  "p_g_qor": ("P", "a single large snowflake"),
  "p_g_termometr": ("P", "an old glass thermometer frozen with frost, mercury very low"),
  "p_g_strelka": ("P", "a bold brick-red map arrow bending sharply"),
  "p_g_chinnigul": ("P", "two red carnation flowers"),
  "p_g_kompas": ("P", "an old brass military compass"),
  "p_g_undov": ("P", "a bold exclamation mark shape"),
 },
 "2026-10-18_1430_anqara": {
  "05b": ("S", "close-up of an armored war elephant with a howdah, trumpeting, dust"),
  "11b": ("S", "Timurid archers releasing a volley of arrows, close view, gold sky"),
  "17b": ("S", "close-up of clear blue water rushing into a newly dug channel, shovels, Timurid soldiers smiling"),
  "18b": ("S", "exhausted Ottoman soldiers kneeling by a dry stream bed with empty water skins under burning sun"),
  "c_temur": ("C", "Amir Temur, 66, white beard, gilded armor and turban-helmet, calm wise face, standing with a hand on his sword, full body"),
  "c_temur_ayyor": ("C", "Amir Temur, 66, white beard, gilded armor and turban-helmet, sly knowing smile with one raised eyebrow, pointing behind him, full body"),
  "c_boyazid": ("C", "Sultan Bayezid, 42, black beard, golden helmet and rich red caftan over armor, proud confident pose, full body"),
  "c_boyazid_hayron": ("C", "Sultan Bayezid, 42, black beard, golden helmet and red caftan over armor, shocked face, hands raised, full body"),
  "p_soy_ariq": ("P", "a small sparkling blue stream flowing in a dug channel"),
  "p_jang_fili": ("P", "an armored war elephant"),
  "p_g_tomchi": ("P", "a single glistening blue water drop"),
  "p_g_mesh": ("P", "an empty deflated leather water skin"),
  "p_g_qilich": ("P", "a curved sword with a gold hilt"),
  "p_g_tug": ("P", "a Timurid horse-tail standard banner on a pole"),
  "p_g_undov": ("P", "a bold gilded exclamation mark shape"),
 },
}
COVER = {
 "2026-10-18_0800_pult": "funny close-up of an 11-year-old Uzbek boy in a faded blue tracksuit standing on a chair holding a rabbit-ear TV antenna high above his head with a strained face, his father on the sofa pointing at him, 1995 living room with a carpet on the wall, empty wall space at the top",
 "2026-10-18_1230_bepul-sinov": "close-up of Uzbek woman Nigora, 29, round glasses, dark red cardigan, shocked with mouth open, holding a smartphone from which gold coins are flying out, explosive comic background, empty space at the bottom",
 "2026-10-18_1600_ai-muzlatkich": "a futuristic white smart fridge with a glowing blue eye ring refusing to open, a man in blue striped pajamas hugging it and begging for a sausage behind the glass, night kitchen, empty space in the middle band",
 "2026-10-18_1830_non-odobi": "warm close-up of a kind elderly Uzbek grandmother in a white headscarf gently holding a golden round tandir bread with both hands, her teenage grandson in a black hoodie smiling beside her, glowing tandir fire behind, empty space at the top",
 "2026-10-18_2100_yuzga-qol": "extreme close-up of a bank teller's face touching his nose with fingers covered in glowing acid-green germs, magnifying glass reflection, dramatic noir light, face centered",
}
if __name__ == "__main__":
    flow = {}
    for job in sorted(set(EXTRA) | set(COVER)):
        d = f"{B}/{job}"; st = json.load(open(d + "/brief_style.json")); pre = {"S": st["image_prefix"], "C": st["character_prefix"], "P": st["prop_prefix"]}
        P = lambda t, p: (pre[t].strip().rstrip(",") + ". " + p + ".").replace("..", ".")
        ip = d + "/images.json"; im = json.load(open(ip)) if os.path.exists(ip) else {}
        new = {}
        if job in EXTRA:
            s = json.load(open(d + "/script.json"))
            for x in s["scenes"]:
                k = f"{x['n']:02d}.jpg"; new[k] = {"prompt": P("S", clean(x["frames"])), "ref": None}
                x["img"] = k; x["imgs"] = []
            for k, (t, p) in EXTRA[job].items():
                new[k + ".jpg"] = {"prompt": P(t, p), "ref": None}
                if k[:2].isdigit():
                    for x in s["scenes"]:
                        if f"{x['n']:02d}" == k[:2]: x["imgs"] = [k + ".jpg"]
            json.dump(s, open(d + "/script.json", "w"), ensure_ascii=False, indent=1)
        cp = st.get("cover", {}).get("flow_prompt") or P("S", COVER[job] + ", strong high contrast, no text")
        new["cover.jpg"] = {"prompt": cp, "ref": None}
        im.update(new); json.dump(im, open(ip, "w"), ensure_ascii=False, indent=1)
        flow[job] = new; print(job, len(new), "yangi rasm")
    json.dump(flow, open(f"{B}/flow_v2_2026-10-18.json", "w"), ensure_ascii=False)
