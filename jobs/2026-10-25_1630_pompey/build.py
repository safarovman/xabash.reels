import json,sys
J='/home/claude/xabash.reels/jobs/2026-10-25_1630_pompey/'
ns={}; exec(open(J+'lines.py').read(),ns); L=ns['L']
st=json.load(open(J+'brief_style.json')); mu=json.load(open(J+'brief_music.json')); ge=json.load(open(J+'brief_gestures.json'))['elements']
def cap(w,at,color='yellow'): return {"type":"caption","words":w,"color":color,"y":1330,"size":92,"at":at}
def talk(name,img,side,label,lc,hl,motion='jump',moods=None):
    r=side=='right'
    c={"type":"char","img":img,"from":side,"x":810 if r else 270,"y":1440,"h":680,"at":0.1,"motion":motion,"talk":["vo"],"label":label,"label_bg":lc}
    if moods: c["moods"]=moods
    return [{"type":"bubble","speaker":name,"x":540,"y":330,"at":"start","hl":hl,"tail":"down","tail_x":0.75 if r else 0.25,"tag":lc,"w":880},c]
LA=lambda img,hl,moods=None: talk("LAYLO",img,"right","ARXEOLOG LAYLO","orange",hl,'jump',moods)
PL=lambda img,hl: talk("PLINIY",img,"left","KICHIK PLINIY, 17","crimson",hl,'wag')
spec=[
("01.jpg",[["01b.jpg","qochib"]],[cap(["NEGA","QOCHMADI?"],"ulgurmagan")]),
("01b.jpg",[["11.jpg","Lekin"]],[]),
("02.jpg",[],LA("c_laylo.jpg",{"nima o'ldirgan":"red"})),
("03.jpg",[["03b.jpg","Rim"]],[]),
("cover.jpg",[["04b.jpg","bitta soat"]],[]),
("04.jpg",[],[cap(["14 KM","TUTUN"],"Bir soatda","white")]),
("05.jpg",[],PL("c_pliniy.jpg",{"ulkan bulut":"red"})),
("05b.jpg",[],[]),
("06.jpg",[["06b.jpg","kul"]],[cap(["KUNDUZI","TUN"],"tun")]),
("06.jpg",[],PL("c_pliniy_anx.jpg",{"yostiq":"red"})),
("02.jpg",[],LA("c_laylo_surprised.jpg",{"Nega hamma":"red"})),
("06b.jpg",[["07.jpg","Ammo"]],[cap(["KO'PCHILIK","QOCHGAN"],"ko'pchilik","white")]),
("07.jpg",[["07b.jpg","Boshqalar"]],[]),
("08.jpg",[],PL("c_pliniy_anx.jpg",{"qulay":"red"})),
("09.jpg",[["09b.jpg","bo'shliqlarga"]],[]),
("01.jpg",[],LA("c_laylo_surprised.jpg",{"shakli":"red"},[["c_laylo_amazed.jpg","Lekin"]])),
("10.jpg",[],[cap(["ERTASI","TONG"],"ertasi")]),
("10b.jpg",[],[]),
("11.jpg",[["01b.jpg","shu bulut"]],[cap(["LAVA","EMAS!"],"lava","white")]),
("12.jpg",[],LA("c_laylo.jpg",{"o'tib ketdi":"red"})),
("12.jpg",[],[]),
]
sc=[]
for i,((v,tts,text,spk),(img,imgs,els)) in enumerate(zip(L,spec),1):
    els=els+ge.get(str(i),[])
    for e in els:
        a=e.get('at')
        if isinstance(a,str) and a!='start' and a.lower() not in text.lower(): print('ANCHOR MISSING',i,a)
        if e['type']=='bubble':
            for h in e['hl']:
                if h.lower() not in text.lower(): print('HL MISSING',i,h)
    for x in imgs:
        if x[1].lower() not in text.lower(): print('IMG ANCHOR MISSING',i,x[1])
    s={"n":i,"speaker":spk,"text":text,"tts":tts,"mood":mu['moods'][i-1],"img":img,"elements":els,"vo":f"vo_{i:02d}.mp3","voice_id":v}
    if imgs: s["imgs"]=imgs
    sc.append(s)
cv=dict(st['cover']); cv.pop('flow_prompt',None); cv.pop('cover_title',None); cv['char']='c_laylo.jpg'; cv['props']=[]
head={"title":"Pompeyda odamlar nega qochmagan","pace":"fast","music":mu['music'],"music_seed":mu['music_seed'],"music_gain":mu['music_gain'],
"cover_title":st['cover']['cover_title'],"cover_sub":"Lava emas, unda nima?","cover_scene":0,"cover":cv,"anim":"static","bright":True,
"theme":dict(st['theme'],bubble_radius=14),"end_hold":1.2,"scenes":sc}
json.dump(head,open(J+'scenes.json','w'),ensure_ascii=False,indent=1)
print(len(sc), sum(len(s['elements'])+len(s.get('imgs',[])) for s in sc))
