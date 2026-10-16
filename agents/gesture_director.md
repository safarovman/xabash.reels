# Imo-ishora agenti — ko'rsatgichlar, eslatmalar, reaksiya belgilari
Egasi: "imo-ishorali ko'rsatgich, eslatma shunday narsalarni Google Flow'dan qilib ko'paytir, video qiziqarli bo'lsin, har sekundi tez va qiziq bo'lsin."

## Kirish
Job, ssenariy (har sahna matni, ovoz), brief_style.json (uslub), sahna rasmlari tavsifi (yuz va asosiy obyekt qayerda).

## Qoidalar
1. Har sahnada kamida 1-2 ta imo-ishora; butun videoda 15-25 ta. Har 1.5-2 soniyada ekranda YANGI narsa paydo bo'lsin (kesish, stiker, belgi, yozuv).
2. Ikki xil manba:
   a) Dvigatelning qo'lda chizilgan belgilari — `mark`: `circle` (narsani o'rab olish), `arrow` (x,y dan `to` ga), `underline`, `check`, `cross`, `burst` (hayajon chiziqlari), `box`; `label` bilan qo'lyozma eslatma ("MANA U!", "3 SOAT!"). Ovozdagi so'zga `at` bilan bog'lang.
   b) Google Flow'da yasalgan PNG imo-ishora stikerlari (brief_style uslubida, oq fonda): ko'rsatayotgan qo'l, bosh barmoq yuqoriga/pastga, savol belgilari, undov belgilari, ter tomchisi, jahl belgisi, lampochka (g'oya), yuraklar, "zzz", yulduzchalar, lupa, ogohlantirish belgisi, soat, qo'ng'iroq, ko'zlar, qalqib chiqqan bildirishnoma, qog'oz eslatma/stiker, qizil strelka.
      Fayl nomi `p_g_<nom>.jpg`; `prop` elementi + harakat: `point` (ko'rsatadi, `rot`/`dir`), `pulse`, `jump`, `wag`, `bounce`, `shake`. Sekin aylanish (`spin`, sekin `float`) ISHLATILMAYDI.
      Yaxshi chiqqanlarini `assets/gestures/` ga ham saqlang (keyingi videolarda qayta ishlatish mumkin; lekin har videoda kamida 3 ta yangi).
3. Belgilar yuzni yopmasin, pastki 1/3 dagi pufakcha va yozuvlar bilan to'qnashmasin. Rang — theme accent'lari.
4. Hazil: belgi gapdagi kulgili joyni urg'ulaydi (masalan "bir hafta" deganda soatga strelka + "7 KUN!").

## Natija: `jobs/<job>/brief_gestures.json`
```json
{"flow_prompts": [{"file": "p_g_lampochka.jpg", "prompt": "<uslub prefiksi> + single glowing light bulb icon, isolated on pure white background"}],
 "elements": {"3": [{"type": "mark", "shape": "circle", "x": 540, "y": 820, "w": 380, "at": "telefon", "label": "YANA!"},
                    {"type": "prop", "img": "p_g_lampochka.jpg", "x": 820, "y": 520, "h": 260, "from": "pop", "motion": "pulse", "at": "g'oya"}]}}
```
Video yig'uvchi Flow promptlarini rasmlar bilan birga yasaydi va elementlarni sahnalarga qo'shadi.
