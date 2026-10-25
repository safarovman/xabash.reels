import sys; sys.path.insert(0,'/tmp'); from buildlib import *
AM=lambda img,hl: talk("AMIR NUH",img,"left","SOMONIY AMIR","navy",hl,'wag')
TB=lambda img,hl: talk("TABIB",img,"left","SAROY TABIBI","purple",hl,'wag')
US=lambda img,hl: talk("USTOZ",img,"right","USTOZ DILOROM","orange",hl,'jump')
spec=[
("01.jpg",[],[cap(["O'LIM","TO'SHAGI"],"yotardi","white")]),
("01b.jpg",[["02.jpg","17"]],[]),
("03.jpg",[],AM("c_amir.jpg",{"seniki":"red"})),
("06.jpg",[],[]),
("04.jpg",[["04b.jpg","Afshonada"]],[]),
("05.jpg",[],[cap(["TIB — QIYIN","FAN EMAS"],"Tib")]),
("05.jpg",[],TB("c_tabib.jpg",{"dars":"red"})),
("01.jpg",[],[]),
("01b.jpg",[["02.jpg","Saroyga"]],[]),
("07.jpg",[],[cap(["AMIR","TUZALDI!"],"oyoqqa")]),
("07.jpg",[],AM("c_amir_laugh.jpg",{"Oltinmi":"red"})),
("06.jpg",[["08.jpg","bitta bino"]],[]),
("08.jpg",[],US("c_ustoz.jpg",{"bitta fan":"red"})),
("08b.jpg",[],US("c_ustoz_amazed.jpg",{"hech kim":"red"})),
("09.jpg",[],[]),
("10.jpg",[["10b.jpg","Yevropa"]],[]),
("04b.jpg",[],TB("c_tabib_sigh.jpg",{"edi-ya":"red"})),
("12.jpg",[["cover.jpg","kutubxonasiga"]],[cap(["KUTUBXONA!"],"ruxsat")]),
("11.jpg",[["11b.jpg","Dushmanlari"]],[]),
("12.jpg",[],[]),
]
build('2026-10-25_1830_ibn-sino',spec,"Ibn Sino: oltin emas, kutubxona","Amir unga xazina va'da qildi",None)
