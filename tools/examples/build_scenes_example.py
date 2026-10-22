import json,sys,re
sys.path.insert(0,'/tmp/claude-0/-home-claude/c735f165-7f0b-530d-b2ad-fc95286466fc/scratchpad')
import lines22 as L
R='/home/claude/xabash.reels/jobs/'
def cap(w,at,color='yellow'): return {"type":"caption","words":w,"color":color,"y":1330,"size":92,"at":at}
def tag(h,t,color,at='start'): return {"type":"tag","head":h,"text":t,"x":540,"y":210,"color":color,"at":at}
def prop(img,at,x=880,y=640,motion='shake'): return {"type":"prop","img":img,"x":x,"y":y,"h":250,"from":"pop","motion":motion,"at":at}
def card(k,t,s,at): return {"type":"card","kicker":k,"title":t,"sub":s,"at":at,"y":1330}
def stamp(t,at): return {"type":"stamp","text":t,"y":1350,"rot":-6,"at":at}
def final(l): return {"type":"final","lines":l,"at":0.4}
def talk(name,img,side,label,lc,hl,motion='jump'):
    r=side=='right'
    return [{"type":"bubble","speaker":name,"x":540,"y":330,"at":"start","hl":hl,"tail":"down","tail_x":0.75 if r else 0.25,"tag":lc,"w":880},
            {"type":"char","img":img,"from":side,"x":810 if r else 270,"y":1440,"h":680,"at":0.1,"motion":motion,"talk":["vo"],"label":label,"label_bg":lc}]
def build(job,lines,spec,head):
    sc=[]
    for i,((v,tts,text,spk),(img,mood,els)) in enumerate(zip(lines,spec),1):
        for e in els:
            a=e.get('at')
            if isinstance(a,str) and a!='start' and a.lower() not in text.lower(): print('ANCHOR MISSING',job,i,a)
            if e['type']=='bubble':
                for h in e['hl']:
                    if h.lower() not in text.lower(): print('HL MISSING',job,i,h)
        sc.append({"n":i,"speaker":spk,"text":text,"tts":tts,"mood":mood,"img":img,"elements":els,"vo":f"vo_{i:02d}.mp3","voice_id":v})
    head['scenes']=sc
    json.dump(head,open(R+job+'/scenes.json','w'),ensure_ascii=False,indent=1)
    print(job,len(sc))
K=lambda hl:talk("KAMOLA","c_kamola.jpg","right","KAMOLA, 13","pink",hl)
U=lambda hl:talk("USTOZ","c_ustoz.jpg","left","PALEONTOLOG","navy",hl,'wag')
SIK=[("01.jpg","mystery",[tag("AFSONA","SIKLOP","crimson"),cap(["BITTA","KO'Z"],"bitta"),prop("p_g_koz.jpg","ko'z")]),
("02.jpg","mystery",[card("GOMER, «ODISSEYA»",["POLIFEM"],"bahaybat siklop","Polifem")]),
("03.jpg","tense",[cap(["G'ORGA","QAMALDI"],"g'origa","white")]),
("04.jpg","groove",K({"ertakmi":"red"})+[prop("p_g_savol.jpg","ertakmi",280,640)]),
("04.jpg","warm",U({"haqiqiy suyak":"red"})),
("05.jpg","warm",[tag("BO'YI","1 METRDAN PAST","royal"),cap(["MITTI","FILLAR"],"mitti")]),
("06.jpg","warm",[cap(["4 METRLIK","AJDOD"],"ajdodi","white"),prop("p_g_lupa.jpg","kichrayib",880,640,'float')]),
("07.jpg","tension",[cap(["BOSH","SUYAGI"],"suyagini")]),
("07.jpg","mystery",[prop("p_g_undov.jpg","teshik",880,560),stamp("BU — BURUN TESHIGI","burun")]),
("08.jpg","groove",K({"bitta ko'z":"red"})),
("09.jpg","warm",[card("1914-YIL",["OTENIO ABEL"],"avstriyalik paleontolog","Otenio")]),
("10.jpg","mystery",[tag("XIV ASR","BOKKACHCHO","purple"),cap(["POLIFEM","SUYAKLARI?"],"Polifemniki")]),
("04.jpg","warm",U({"taxmini":"red"})),
("11.jpg","mystery",[cap(["AFSONA","QAYERDAN?"],"afsonalar")]),
("11.jpg","finale",[final(["QAYSI AFSONA","HAQIQAT?"])])]
build('2026-10-22_0800_sikloplar',L.SIK,SIK,{"title":"Sikloplar bo'lganmi?","pace":"fast",
 "music":{"genre":"detective","bpm":92,"key":-2,"scale":"minor","progression":[0,5,3,4]},"music_seed":1914,"music_gain":0.7,
 "cover_title":["SIKLOPLAR","BO'LGANMI?"],"cover_sub":"Afsona ortidagi suyak","cover_scene":0,
 "cover":{"layout":"poster","img":"cover.jpg","char":"c_ustoz.jpg","props":["p_g_koz.jpg"],"badge":"1914","title_colors":[[250,235,200],[40,170,180]],"accent":[40,150,160],"accent2":[230,160,60]},
 "anim":"static","bright":True,
 "theme":{"font":"alfaslabone","font2":"caveat","accent":[40,150,160],"accent2":[230,160,60],"bubble_bg":[246,240,226],"bubble_line":[30,90,100],"bubble_ink":[25,30,35],"bubble_dim":[40,150,160],"bubble_radius":16,"transitions":["zoom","torn","flash"],"cut_fx":"flash"},"end_hold":1.2})
S=lambda hl:talk("SARDOR","c_sardor.jpg","right","SARDOR, 12","orange",hl)
A=lambda hl:talk("AMAKI","c_amaki.jpg","left","OTBOQAR AMAKI","green",hl,'wag')
OT=[("01.jpg","mystery",[cap(["NEGA AYNAN","FARG'ONA?"],"Farg'onaning"),prop("p_g_savol.jpg","nega")]),
("02.jpg","epic",[tag("XAN SULOLASI","IMPERATOR U-DI","crimson"),cap(["2000 YIL","OLDIN"],"2000","white")]),
("03.jpg","tense",[cap(["XUNNLAR"],"xunnlar"),prop("p_g_qilich.jpg","tez")]),
("04.jpg","warm",[card("ELCHI",["CHJAN SZYAN"],"g'arbdan xabar","Chjan")]),
("05.jpg","groove",S({"zo'r":"red"})),
("05.jpg","warm",A({"samoviy otlar":"red"})),
("06.jpg","tension",[tag("SOVG'A","1000 BO'LAK OLTIN","orange"),cap(["SOTMADI!"],"sotmadi")]),
("07.jpg","tense",[stamp("OLTIN OT SINDI","sindirib")]),
("07.jpg","tension",[cap(["KECHIRMADI"],"kechirmadi","white"),prop("p_g_chaqmoq.jpg","kechirmadi")]),
("08.jpg","sad",[tag("MIL. AVV.","104-YIL","royal"),cap(["1-YURISH:","MAG'LUBIYAT"],"yengilib","white")]),
("09.jpg","epic",[tag("2-YURISH","60 000 ASKAR","crimson"),cap(["30 MING","OT"],"30")]),
("10.jpg","epic",[cap(["40 KUNLIK","QAMAL"],"40"),prop("p_g_soat.jpg","kundan")]),
("10.jpg","groove",S({"ot":"red"})),
("11.jpg","warm",[card("SULH",["~3000 OT"],"Xitoyga olib ketildi","3000")]),
("12.jpg","warm",A({"Buyuk ipak yo'lining":"red"})),
("12.jpg","finale",[final(["ARZIRMIDI?"])])]
build('2026-10-22_1030_otlar',L.OT,OT,{"title":"Farg'ona otlari","pace":"fast",
 "music":{"genre":"epic","bpm":96,"key":-3,"scale":"minor","progression":[0,5,3,4]},"music_seed":104,"music_gain":0.7,
 "cover_title":["FARG'ONA","OTLARI"],"cover_sub":"Xitoy nega urush qildi?","cover_scene":0,
 "cover":{"layout":"hero","img":"cover.jpg","char":"c_amaki.jpg","props":["p_g_savol.jpg"],"badge":"MIL. AVV. 104","title_colors":[[250,230,190],[230,180,60]],"accent":[200,50,40],"accent2":[230,180,60]},
 "anim":"static","bright":True,
 "theme":{"font":"abrilfatface","font2":"caveat","accent":[200,50,40],"accent2":[230,180,60],"bubble_bg":[250,242,226],"bubble_line":[140,40,30],"bubble_ink":[30,25,25],"bubble_dim":[200,50,40],"bubble_radius":14,"transitions":["slide","zoom","torn"],"cut_fx":"whip"},"end_hold":1.2})
M=lambda hl:talk("MADINA","c_madina.jpg","right","MADINA, 16","pink",hl)
O=lambda hl:talk("RESTAVRATOR","c_opa.jpg","left","RESTAVRATOR OPA","royal",hl,'wag')
AF=[("01.jpg","mystery",[cap(["1300 YILLIK","DEVOR"],"devorda"),prop("p_g_lupa.jpg","Koreyadan")]),
("02.jpg","warm",[tag("YIL","1965","royal"),cap(["AFROSIYOB","TEPALIGI"],"Afrosiyob","white")]),
("03.jpg","groove",[cap(["FIL, TUYA,","OTLAR"],"fillar")]),
("12.jpg","groove",M({"kim":"red"})),
("12.jpg","warm",O({"Varxuman":"red"})),
("04.jpg","warm",[card("SAROY ZALI",["4 DEVOR"],"4 xil dunyo","devorning")]),
("05.jpg","groove",[tag("SHIMOL","XITOY","crimson"),cap(["QAYIQDAGI","MALIKA"],"malika")]),
("06.jpg","groove",[tag("JANUB","SAMARQAND","orange"),cap(["SHARQDA —","HINDISTON"],"Hindiston","white")]),
("07.jpg","mystery",[cap(["G'ARBIY","DEVOR"],"G'arbiy"),prop("p_g_undov.jpg","boshqa")]),
("08.jpg","mystery",[card("SO'G'DCHA YOZUV",["CHAG'ONIYON"],"hozirgi Surxondaryo","Chag'oniyondan")]),
("09.jpg","tension",[cap(["IKKITA","PAT"],"pat"),prop("p_g_lupa.jpg","qalpoq")]),
("10.jpg","warm",O({"Koguryo":"red"})),
("11.jpg","groove",M({"Samarqandgacha":"red"})),
("11.jpg","warm",[cap(["DUNYO","CHORRAHASI"],"chorrahasi")]),
("12.jpg","warm",[tag("BUGUN","AFROSIYOB MUZEYI","royal")]),
("12.jpg","finale",[final(["QANDAY","SOVG'A?"])])]
build('2026-10-22_1230_afrosiyob',L.AF,AF,{"title":"Samarqanddagi Koreya elchilari","pace":"fast",
 "music":{"genre":"doira","bpm":90,"key":2,"scale":"hijaz","progression":[0,5,3,4]},"music_seed":648,"music_gain":0.72,
 "cover_title":["KOREYA","ELCHILARI"],"cover_sub":"Samarqand devoridagi sir","cover_scene":0,
 "cover":{"layout":"polaroid","img":"cover.jpg","char":"c_opa.jpg","props":["p_g_lupa.jpg"],"badge":"VII ASR","title_colors":[[250,240,215],[210,150,60]],"accent":[40,80,170],"accent2":[210,150,60]},
 "anim":"static","bright":True,
 "theme":{"font":"titanone","font2":"patrickhand","accent":[40,80,170],"accent2":[210,150,60],"bubble_bg":[248,242,230],"bubble_line":[30,60,130],"bubble_ink":[25,25,40],"bubble_dim":[40,80,170],"bubble_radius":18,"transitions":["zoom","slide","torn"],"cut_fx":"flash"},"end_hold":1.2})
