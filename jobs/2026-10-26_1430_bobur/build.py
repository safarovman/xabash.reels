import sys; sys.path.insert(0,'/tmp'); from buildlib import *
BV=lambda img,hl: talk("ESAN DAVLAT BEGIM",img,"right","BUVISI","purple",hl,'wag')
QB=lambda img,hl: talk("QOSIMBEK",img,"left","KEKSA BEK","green",hl,'wag')
SH=lambda img,hl: talk("SHAYBONIYXON",img,"left","SHAYBONIYXON","crimson",hl,'shake')
def ch(img,at,side='right',moods=None):
    c={"type":"char","img":img,"from":side,"x":810 if side=='right' else 270,"y":1440,"h":640,"at":at,"motion":"bounce","label":"SHAHZODA","label_bg":"orange"}
    if moods: c["moods"]=moods
    return c
spec=[
("01.jpg",[["01b.jpg","shoh"]],[]),
("03.jpg",[["02.jpg","Otasi"]],[]),
("04.jpg",[],BV("c_buvi.jpg",{"hech kim":"red"})),
("04.jpg",[],[]),
("05.jpg",[["05b.jpg","uniki"]],[ch("c_shahzoda.jpg","Samarqand")]),
("06.jpg",[],[ch("c_shahzoda_sad.jpg","Andijon")]),
("05.jpg",[],QB("c_qosimbek.jpg",{"Ikki taxtni":"red"})),
("07.jpg",[["05b.jpg","yana"]],[]),
("08.jpg",[],SH("c_shayboniy.jpg",{"meniki":"red"})),
("08.jpg",[["08b.jpg","ochlik"]],[]),
("09.jpg",[],[cap(["2-MARTA","YO'QOTDI"],"Ikkinchi","white")]),
("10.jpg",[],[]),
("11.jpg",[],[]),
("01b.jpg",[],[ch("c_shahzoda_sad.jpg","Bir yil")]),
("10.jpg",[],QB("c_qosimbek_warm.jpg",{"ochiladi":"red"})),
("12.jpg",[],[]),
("13.jpg",[["13b.jpg","1000 fil"]],[]),
("13b.jpg",[["14.jpg","saltanat"]],[]),
("14.jpg",[],[cap(["BOBUR!"],"Bobur")]),
("15.jpg",[],[]),
("15.jpg",[],[]),
]
build('2026-10-26_1430_bobur',spec,"Samarqandni 3 marta yo'qotgan shoh","Andijondan Agragacha","c_shahzoda.jpg")
