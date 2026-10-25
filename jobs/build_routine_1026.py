import json,sys,importlib.util
R='/home/claude/xabash.reels/jobs/'
def load_lines(j):
    sp=importlib.util.spec_from_file_location('l'+j[-4:],R+j+'/lines.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m.L
def talk(name,img,side,label,lc,hl,motion='jump'):
    r=side=='right'
    return [{"type":"bubble","speaker":name,"x":540,"y":330,"at":"start","hl":hl,"tail":"down","tail_x":0.75 if r else 0.25,"tag":lc,"w":880},
            {"type":"char","img":img,"from":side,"x":760 if r else 270,"y":1440,"h":680,"at":0.1,"motion":motion,"talk":["vo"],"label":label,"label_bg":lc}]
def ch(img,at,side='right',label=None,lc='orange',moods=None,motion='bounce'):
    c={"type":"char","img":img,"from":side,"x":810 if side=='right' else 270,"y":1440,"h":620,"at":at,"motion":motion}
    if label: c["label"]=label; c["label_bg"]=lc
    if moods: c["moods"]=moods
    return c
def build(j,spec,head):
    L=load_lines(j); G=json.load(open(R+j+'/brief_gestures.json'))['elements']; M=json.load(open(R+j+'/brief_music.json'))
    moods=M.get('moods') or {}
    sc=[]
    for i,((v,tts,text,spk),(img,imgs,extra,drop)) in enumerate(zip(L,spec),1):
        g=[e for e in G.get(str(i),[]) if not drop] if drop is not True else []
        els=g+extra
        for e in els:
            a=e.get('at')
            if isinstance(a,str) and a!='start' and a.lower() not in text.lower(): print('ANCHOR MISSING',j,i,a)
            if e['type']=='bubble':
                for h in e['hl']:
                    if h.lower() not in text.lower(): print('HL MISSING',j,i,h)
            for ta,_ in [(x[1],0) for x in e.get('moods',[])]:
                if ta.lower() not in text.lower(): print('MOOD ANCHOR MISSING',j,i,ta)
        for x in imgs:
            a=x[1] if isinstance(x,list) else None
            if a and a.lower() not in text.lower(): print('IMG ANCHOR MISSING',j,i,a)
        md=moods.get(str(i)) if isinstance(moods,dict) else moods[i-1]
        s={"n":i,"speaker":spk,"text":text,"tts":tts,"mood":md,"img":img,"elements":els,"vo":f"vo_{i:02d}.mp3","voice_id":v}
        if imgs: s["imgs"]=imgs
        sc.append(s)
    head['scenes']=sc
    json.dump(head,open(R+j+'/scenes.json','w'),ensure_ascii=False,indent=1); print(j,len(sc))
def head(j,title,extra_cover):
    S=json.load(open(R+j+'/brief_style.json')); M=json.load(open(R+j+'/brief_music.json'))
    cov=dict(S['cover']); cov.pop('flow_prompt',None); cov.update(extra_cover)
    return {"title":title,"pace":"fast","music":M['music'],"music_seed":M['music_seed'],"music_gain":M['music_gain'],
            "cover_title":S['cover_title'],"cover_sub":S['cover_sub'],"cover_scene":0,"cover":cov,"anim":"static","bright":True,"theme":S['theme'],"end_hold":1.2}

# ---------- EMU ----------
MER=lambda img,hl,m='jump': talk("MAYOR MEREDIT",img,"left","MAYOR","green",hl,m)
FER=lambda img,hl,m='shake': talk("FERMER JIM",img,"right","FERMER","orange",hl,m)
E=[("01.jpg",[],[],False),
("02.jpg",[],[],False),
("03.jpg",[],FER("c_fermer.jpg",{"Askar yuboringlar":"red"}),False),
("04.jpg",[["04b.jpg","soatiga"]],[],False),
("05.jpg",[],[ch("c_meredit.jpg","Mayor",'left',"MAYOR MEREDIT","green")],False),
("05.jpg",[],MER("c_meredit.jpg",{"Bir haftada":"red"}),True),
("07.jpg",[["07b.jpg","Birinchi"]],[],False),
("08.jpg",[],[],False),
("09.jpg",[],[],False),
("10.jpg",[["10b.jpg","Qolganlari"]],[],False),
("11.jpg",[],MER("c_meredit_angry.jpg",{"yuk mashinasiga":"red"},'shake'),True),
("12.jpg",[["12b.jpg","Silkinishda"]],[],False),
("13.jpg",[],[],False),
("13.jpg",[],MER("c_meredit_hayron.jpg",{"tankdek":"red"},'wag'),False),
("15.jpg",[],[],False),
("16.jpg",[],FER("c_fermer_sad.jpg",{"qaytib keldi":"red"}),True),
("17.jpg",[],[ch("c_meredit_angry.jpg","Mayor",'left',"MAYOR MEREDIT","green")],False),
("18.jpg",[],[],False),
("19.jpg",[],[ch("c_meredit_hayron.jpg","kamaymadi",'left',"MAYOR MEREDIT","green")],False),
("20.jpg",[],[],False),
("21.jpg",[],[{"type":"final","lines":["SIZ NIMA","QILARDINGIZ?"],"at":"qanday"}],False)]
build("2026-10-26_1630_emu",E,head("2026-10-26_1630_emu","Emu urushi: armiya qushlarga yutqazdi",{"title_colors":[[40,32,24],[230,120,40]]}))
# ---------- OTRAR ----------
GOY=lambda img,hl,m='shake': talk("G'OYIRXON",img,"left","O'TRAR HOKIMI","crimson",hl,m)
SHO=lambda img,hl: talk("XORAZMSHOH MUHAMMAD",img,"right","XORAZMSHOH","purple",hl,'wag')
TUY=lambda img,hl: talk("TUYAKASH",img,"right","TUYAKASH","orange",hl,'jump')
O=[("01.jpg",[["01b.jpg","saltanat"]],[],False),
("02.jpg",[],[],False),
("03.jpg",[["03b.jpg","oltin"]],[],False),
("04.jpg",[],[],False),
("05.jpg",[],GOY("c_goyirxon.jpg",{"josuslar":"red"}),True),
("06.jpg",[],[],False),
("07.jpg",[["07b.jpg","mollari"]],[],False),
("08.jpg",[],[],False),
("09.jpg",[],TUY("c_tuyakash.jpg",{"o'z ko'zim":"red"}),True),
("10.jpg",[],[],False),
("11.jpg",[],[],False),
("12.jpg",[],SHO("c_shoh.jpg",{"hech kimga":"red"}),True),
("13.jpg",[],[],False),
("14.jpg",[],[],False),
("15.jpg",[],[],False),
("16.jpg",[],GOY("c_goyirxon_gazab.jpg",{"taslim bo'lmaydi":"red"}),True),
("17.jpg",[["17b.jpg","ichkaridan"]],[],False),
("18.jpg",[["18b.jpg","Rivoyat"]],[],False),
("19.jpg",[],[],False),
("20.jpg",[],[],False),
("21.jpg",[],[{"type":"final","lines":["HOKIMMI","YOKI SHOHMI?"],"at":"kim"}],False)]
build('2026-10-26_1830_otrar',O,head('2026-10-26_1830_otrar',"O'trar fojiasi",{}))
