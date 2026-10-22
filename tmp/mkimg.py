import json
R='/home/claude/xabash.reels/jobs/'
NIL="young Uzbek woman Nilufar, 20, archaeology student, dark hair in a low ponytail, khaki field shirt, small canvas bag, natural face"
DOM="Uzbek woman archaeology professor, 55, short grey hair, round glasses, linen shirt, warm wise face"
TR={
"01.jpg":"a giant wooden Trojan horse standing before the tall stone walls of Troy at night, torches, Greek warriors hiding, dramatic low angle",
"01b.jpg":"close-up of an ancient papyrus scroll of Homer's epic unrolled on a table beside an oil lamp and a laurel wreath",
"02.jpg":f"{NIL} sitting in an excavation camp tent with books and maps, astonished expression, warm lamp light",
"02b.jpg":f"{NIL} leaning on a folding table in the excavation camp tent, skeptical raised eyebrow, arms crossed",
"03.jpg":"ancient Trojans mourning at the funeral pyre of the hero Hector outside intact city walls, smoke rising, solemn",
"04.jpg":f"{DOM} standing at the edge of an excavation trench holding a trowel, calm smile, ancient walls behind",
"05.jpg":"1871 archaeological dig at Hisarlik mound, 19th-century workers with baskets and pickaxes cutting a deep trench, a bearded man in a hat directing",
"05b.jpg":"old sepia photograph look of the deep Schliemann trench cutting through the Hisarlik mound, ladders and wooden barrows",
"06.jpg":"aerial view of Hisarlik hill in northwest Turkey near the Dardanelles strait, green plain and sea, sunny",
"06b.jpg":"antique parchment map of the Aegean Sea with Greece on the left and Anatolia on the right, a small marked city near the Dardanelles, ships",
"07.jpg":"glittering ancient gold treasure: golden diadem with hanging chains, gold cups and earrings piled on cloth, dramatic light",
"08.jpg":"cross-section diagram of the excavation mound showing the gold treasure deep in a much older lower layer, labeled only with colored bands",
"09.jpg":"cut-away cross-section of the Troy mound with nine stacked city layers from bottom to top like a layer cake, tiny houses and walls in each layer",
"10.jpg":"the burning city of Troy at night, flames over houses and walls, people fleeing, smoke",
"10b.jpg":"close-up of an excavation trench wall with a dark black burnt ash layer, charred beams and pottery shards",
"11.jpg":"ancient Hittite clay tablet covered with cuneiform wedge marks held in hands, dusty archive",
"11b.jpg":"Hittite king on a throne in the stone palace of Hattusa dictating a letter to a scribe",
"12.jpg":"ancient Anatolian ruler of Wilusa in a fine robe on city walls, portrait in vase-painting style, proud",
"13.jpg":f"empty excavation trench at sunset with measuring rods and tools, no horse anywhere, {DOM} shrugging",
"14.jpg":"Greek warriors climbing down a rope from the belly of the wooden horse inside the city at night, vase painting scene",
"14b.jpg":"ancient clay storage jar with a relief of a wooden horse on wheels with warriors' heads in its windows, museum light",
"15.jpg":"huge wooden siege tower on wheels covered with horse hides rolling toward ancient city walls",
"15b.jpg":"powerful earthquake cracking the ancient walls of Troy, falling stones, dust",
"16.jpg":"silhouette of the wooden horse on a hill at golden sunset with a big empty sky, mysterious",
}
TRC={"c_nilufar.jpg":f"{NIL}, curious friendly expression","c_nilufar_hayron.jpg":f"{NIL}, jaw dropped in disbelief, eyes wide","c_nilufar_kulgan.jpg":f"{NIL}, excited big smile, pointing finger up","c_domla.jpg":f"{DOM}, gentle knowing smile, holding a trowel"}
TRP={"p_g_dubulgha.jpg":"bronze Corinthian hoplite helmet with red horsehair crest","p_g_lupa.jpg":"vintage brass magnifying glass","p_g_belkurak.jpg":"archaeologist's trowel and small shovel crossed","p_g_yogoch_ot.jpg":"small wooden toy horse on wheels"}
ULB="Timurid prince astronomer Ulugh Beg, about 35, short dark beard, white turban with gold band, rich blue silk robe, natural face"
MAD="Uzbek schoolgirl Madina, 14, two long braids, white blouse and dark vest, curious face"
UL={
"01.jpg":"a Timurid astronomer on a rooftop at night measuring stars with only a brass instrument, no telescope, huge starry sky",
"01b.jpg":"close-up of an hourglass and an old manuscript with a star table under candlelight, night",
"02.jpg":"panorama of 15th-century Samarkand at night under a glowing starry sky, turquoise domes",
"03.jpg":f"{MAD} standing in front of the Ulugh Beg observatory museum on a green hill in Samarkand today, daylight, curious",
"04.jpg":f"{ULB} seated on a throne in a Samarkand palace garden, holding a book about stars",
"04b.jpg":"Registan square of 15th-century Samarkand with the Ulugh Beg madrasa under construction, busy builders",
"05.jpg":"construction of a huge round three-storey observatory building on a hill in Samarkand, scaffolding, workers, 1420s",
"05b.jpg":"the finished round Timurid observatory on the hill at dusk, glazed tiles shining, stars appearing",
"06.jpg":"group of Timurid scholars around a table with astrolabes and manuscripts inside the observatory, one old, one middle-aged, one young",
"07.jpg":f"{ULB} at night inside the observatory pointing at a bright star while a young assistant writes in a book",
"08.jpg":"a large open manuscript star catalogue with columns of tables and gold star drawings, constellations above",
"09.jpg":"dark storm clouds gathering over the Samarkand observatory, ominous red sky",
"10.jpg":"sad empty throne room with a fallen turban and a broken astrolabe on the floor, dim light, 1449 tragedy without violence",
"11.jpg":"ruins of the destroyed observatory on the hill, scattered tiles, while a young scholar rides away on a horse carrying a bundle of books",
"12.jpg":f"{MAD} looking sad at the grassy empty hill, wind",
"13.jpg":"grassy hill overgrown with weeds for centuries, shepherd with sheep, nothing visible, seasons passing",
"14.jpg":"1908 archaeologist in a white suit and hat with local workers digging into the hill in Samarkand, finding a curved marble arc",
"14b.jpg":"view down into a deep trench revealing a giant curved marble and brick arc going underground, workers looking amazed",
"15.jpg":"the giant Fakhri sextant: an enormous curved marble arc descending deep into the hill, steps on both sides, sunlight beam falling on it",
"16.jpg":"diagram style: a beam of sunlight entering through a small opening and falling on the giant curved meridian arc with degree marks",
"17.jpg":"golden glowing circle of the year: sun path around the earth with twelve gold zodiac segments, lapis night background",
"18.jpg":f"{MAD} amazed holding a phone with a clock, gold stars around her, inside the museum",
"19.jpg":"the Ulugh Beg observatory hill in Samarkand at golden sunset, monument, peaceful",
}
ULC={"c_ulugbek.jpg":f"{ULB}, warm wise smile","c_ulugbek_hayajon.jpg":f"{ULB}, excited, raising a hand toward the stars","c_madina.jpg":f"{MAD}, curious friendly expression","c_madina_hayron.jpg":f"{MAD}, amazed, hands on cheeks","c_madina_gamgin.jpg":f"{MAD}, sad expression"}
ULP={"p_g_usturlob.jpg":"antique brass astrolabe with engraved star map","p_g_yulduz.jpg":"three bright golden stars","p_g_qumsoat.jpg":"wooden hourglass with golden sand","p_g_quyosh.jpg":"golden sun disc with rays"}
out=[]
for job,BG,C,P in [('2026-10-23_0800_troya-oti',TR,TRC,TRP),('2026-10-23_1030_ulugbek-yili',UL,ULC,ULP)]:
    s=json.load(open(R+job+'/brief_style.json')); im={}
    for k,v in BG.items(): im[k]=s['image_prefix']+' '+v
    for k,v in C.items(): im[k]=s['character_prefix']+' '+v
    for k,v in P.items(): im[k]=s['prop_prefix']+' '+v
    im['cover.jpg']=s['cover']['cover_prompt']
    json.dump({k:{"prompt":v} for k,v in im.items()},open(R+job+'/images.json','w'),ensure_ascii=False,indent=1)
    out+= [[job+'/'+k,v] for k,v in im.items()]
json.dump(out,open('/tmp/claude-0/-home-claude-xabash-reels/9d5f8380-2124-5bfe-bd0d-50b8a19fad6d/scratchpad/p_a23.json','w'),ensure_ascii=False)
print(len(out))
