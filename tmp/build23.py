import json,sys,os
sys.path.insert(0,os.path.dirname(__file__)); import lines23 as L
R='/home/claude/xabash.reels/jobs/'
def cap(w,at,color='yellow'): return {"type":"caption","words":w,"color":color,"y":1330,"size":92,"at":at}
def tag(h,t,color,at='start'): return {"type":"tag","head":h,"text":t,"x":540,"y":210,"color":color,"at":at}
def card(k,t,s,at): return {"type":"card","kicker":k,"title":t,"sub":s,"at":at,"y":1330}
def stamp(t,at): return {"type":"stamp","text":t,"y":1350,"rot":-6,"at":at}
def final(l): return {"type":"final","lines":l,"at":0.4}
def talk(name,img,side,label,lc,hl,motion='jump',moods=None):
    r=side=='right'
    c={"type":"char","img":img,"from":side,"x":810 if r else 270,"y":1440,"h":680,"at":0.1,"motion":motion,"talk":["vo"],"label":label,"label_bg":lc}
    if moods: c["moods"]=moods
    return [{"type":"bubble","speaker":name,"x":540,"y":330,"at":"start","hl":hl,"tail":"down","tail_x":0.75 if r else 0.25,"tag":lc,"w":880},c]
def build(job,lines,spec,head,maxg=2):
    B=json.load(open(R+job+'/brief_gestures.json')); M=json.load(open(R+job+'/brief_music.json'))
    ok={p['file'] for p in B['props_to_generate']}&set(head.pop('props'))
    sc=[]
    for i,((v,tts,text,spk),(img,imgs,els)) in enumerate(zip(lines,spec),1):
        hasbubble=any(e['type']=='bubble' for e in els)
        g=[dict(x) for x in B['gestures'] if x['line']==i and (x['type']=='mark' or x.get('img') in ok)]
        if hasbubble: g=[x for x in g if x['type']=='mark'][:1]
        g=g[:maxg]
        for x in g: x.pop('line',None); x.setdefault('motion','pulse') if x['type']=='prop' else None
        els=els+g
        for e in els:
            a=e.get('at')
            if isinstance(a,str) and a not in('start','end') and a.lower() not in text.lower(): print('ANCHOR MISSING',job,i,a)
            if e['type']=='bubble':
                for h in e['hl']:
                    if h.lower() not in text.lower(): print('HL MISSING',job,i,h)
        s={"n":i,"speaker":spk,"text":text,"tts":tts,"mood":M['moods'][i-1],"img":img,"elements":els,"vo":f"vo_{i:02d}.mp3","voice_id":v}
        if imgs: s['imgs']=imgs
        sc.append(s)
    S=json.load(open(R+job+'/brief_style.json'))
    cov=dict(S["cover"]); cov["props"]=[head.get("cprop")] if head.get("cprop") else []; cov.pop('cover_prompt',None); cov.pop('flow_prompt',None)
    out={"title":head['title'],"pace":"fast","music":M['music'],"music_seed":M['music_seed'],"music_gain":M['music_gain'],
      "cover_title":head.get('cover_title',S['cover_title']),"cover_sub":head.get('cover_sub',S['cover_sub']),"cover_scene":0,"cover":cov,
      "anim":"static","bright":True,"theme":S['theme'],"end_hold":1.2,"scenes":sc}
    json.dump(out,open(R+job+'/scenes.json','w'),ensure_ascii=False,indent=1); print(job,len(sc),sum(len(s['elements']) for s in sc),'elements')
N=lambda hl,m=None:talk("NILUFAR","c_nilufar.jpg","right","NILUFAR, 20","orange",hl,moods=m)
D=lambda hl:talk("DOMLA","c_domla.jpg","left","ARXEOLOG DOMLA","navy",hl,'wag')
TR=[("01.jpg",[["01b.jpg","Iliada"]],[tag("GOMER","«ILIADA»","crimson"),cap(["OT","YO'Q?!"],"yo'q")]),
("02.jpg",None,N({"yo'q":"red"},[["c_nilufar_hayron.jpg","Qanaqasiga"]])),
("03.jpg",None,[cap(["HEKTOR","DAFNI"],"Hektorning","white")]),
("02b.jpg",None,N({"to'qima":"red"})),
("04.jpg",None,D({"Troyaning":"red"})),
("05.jpg",[["05b.jpg","Shliman"]],[tag("YIL","1871","royal")]),
("06.jpg",[["06b.jpg","Turkiyadagi"]],[cap(["HISARLIK","TEPALIGI"],"Hisarlik")]),
("07.jpg",None,[cap(["«PRIAM","XAZINASI»"],"Priam")]),
("07.jpg",None,N({"Troya":"red"},[["c_nilufar_kulgan.jpg","Topibdi"]])),
("08.jpg",None,D({"ming yildan":"red"})),
("09.jpg",None,[tag("QATLAMLAR","9 TA SHAHAR","crimson")]),
("10.jpg",[["10b.jpg","yonib"]],[tag("MIL. AVV.","~1180-YILLAR","crimson"),cap(["YONIB","KETGAN"],"yonib","white")]),
("10b.jpg",None,N({"urush":"red"},[["c_nilufar.jpg","Yong'in"]])),
("11.jpg",[["11b.jpg","podsholarining"]],[card("XET MAKTUBLARI",["VILUSA"],"Ilion (Troya) bilan bog'lanadi","Vilusa")]),
("12.jpg",None,[cap(["ALAKSANDU","= PARIS?"],"Aleksandros")]),
("12.jpg",None,N({"ot":"red"},[["c_nilufar_kulgan.jpg","Mana"]])),
("13.jpg",None,[stamp("DALIL YO'Q","dalil")]),
("14.jpg",[["14b.jpg","Eneida"]],[card("OT QAYERDAN?",["«ODISSEYA»","«ENEIDA»"],"keyingi dostonlarda","Odisseya")]),
("15.jpg",[["15b.jpg","zilzila"]],D({"taxmin":"red"})),
("16.jpg",None,[final(["OT ASLIDA","NIMA EDI?"])])]
build('2026-10-23_0800_troya-oti',L.TR,TR,{"title":"Troya oti bo'lganmi?","cprop":"p_g_yogoch_ot.jpg","props":["p_g_dubulgha.jpg","p_g_lupa.jpg","p_g_belkurak.jpg","p_g_yogoch_ot.jpg"]})
M_=lambda hl,m=None:talk("MADINA","c_madina.jpg","right","MADINA, 14","pink",hl,moods=m)
U=lambda hl,m=None:talk("ULUG'BEK","c_ulugbek.jpg","left","ULUG'BEK","royal",hl,'wag',m)
UL=[("01.jpg",[["01b.jpg","Soat"]],[]),
("02.jpg",None,[cap(["600 YIL","OLDIN"],"600","white")]),
("03.jpg",None,M_({"tepalikda":"red"})),
("04.jpg",[["04b.jpg","nevarasi"]],[tag("XV ASR","ULUG'BEK","royal")]),
("04.jpg",None,U({"Yulduzlarni":"red"})),
("05.jpg",[["05b.jpg","rasadxona"]],[tag("YIL","1420-YILLAR","royal")]),
("06.jpg",None,[card("OLIMLAR",["QOZIZODA RUMIY","KOSHIY · ALI QUSHCHI"],"Samarqand rasadxonasi","Qozizoda")]),
("07.jpg",None,U({"yulduzni":"red"},[["c_ulugbek_hayajon.jpg","kecha"]])),
("08.jpg",None,[cap(["1018 TA","YULDUZ"],"1018")]),
("09.jpg",None,[cap(["LEKIN..."],"Lekin","white")]),
("10.jpg",None,[tag("YIL","1449","crimson")]),
("11.jpg",None,[cap(["ASARLAR","SAQLANDI"],"saqlab")]),
("12.jpg",None,M_({"yo'qolib":"red"},[["c_madina_gamgin.jpg","Voy"]])),
("13.jpg",None,[cap(["450+ YIL","UNUTILDI"],"450","white")]),
("14.jpg",[["14b.jpg","yoy"]],[tag("YIL","1908","royal")]),
("15.jpg",None,[card("FAXRIY SEKSTANTI",["RADIUSI ~36 M"],"yer ostiga tushgan marmar yoy","Faxriy")]),
("16.jpg",None,[cap(["SIR —","KATTALIKDA"],"Sir")]),
("17.jpg",None,[{"type":"big","text":"365 KUN 6:10:08","y":1000,"at":"365"}]),
("18.jpg",None,M_({"58 soniya":"red"},[["c_madina_hayron.jpg","Bugungi"]])),
("19.jpg",None,[final(["SIZGA NIMA","DEYISHGAN?"])])]
build('2026-10-23_1030_ulugbek-yili',L.UL,UL,{"title":"Ulug'bek yilni qanday o'lchagan?","cprop":"p_g_usturlob.jpg","props":["p_g_usturlob.jpg","p_g_yulduz.jpg","p_g_qumsoat.jpg","p_g_quyosh.jpg"],"cover_title":["ULUG'BEK","SIRI"],"cover_sub":"Teleskopsiz yil hisobi"})
