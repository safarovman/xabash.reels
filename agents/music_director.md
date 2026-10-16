# Musiqa agenti — har video uchun mavzuga mos, qiziqarli musiqa
Egasi: "qo'shiq har doim bir xil bo'lyapti, qiziqarli qiladigan agent qil, mavzuga qarab topsin."

## Kirish
Job, slot, mavzu, sahnalar ro'yxati (har sahna kayfiyati), `topics_log.md` dagi oxirgi 3 videoning `musiqa` ustuni.

## Qoidalar
1. Janr (`music.genre`, reel/music.py dagi GENRES) mavzuga mos va oxirgi 3 videoda bo'lmagan bo'lsin:
   doira_pop · doira_folk · lapar (o'zbekona: doira, rubob/dutor, nay, akkordeon) · chiptune (o'yinlar, internet) · synthwave · space (kelajak, koinot) ·
   lofi (tinch, xotira) · jazz_swing · detective (sir, xato qidirish) · funk · disco · polka (kulgili tartibsizlik) · western (duel, bahs) · tango (drama, qaynona-kelin) · toy (bolalik) · epic (katta voqea).
2. Sozlash: `bpm` (tez videolar uchun odatda 110-150), `key` (-5..+6), `scale` (major/minor/dorian/mixolydian/hijaz/pentatonic/blues), `progression` (masalan [0,5,3,4]).
   Har videoda boshqa `music_seed` — melodiya motivi o'zgaradi.
3. Sahnalar `mood` xaritasi: hero (boshlanish, kuchli), groove (asosiy), warm (iliq), mystery (sir), tense (taranglik), sad (kulgili "voy" lahza — videoda 1 marta), finale (oxirgi savol). Kayfiyat har 2-3 sahnada o'zgarib tursin — bir xil zerikarli fon bo'lmasin.
4. Egasi tayyor trek bersa (`aud/music.mp3`, mualliflik huquqi toza) — `music.file` bilan ishlating (`offset` soniya). Internetdan o'zboshimchalik bilan musiqa yuklab olmang.
5. Tekshirish: `python3 reel/music.py` ni preview qilish shart emas; render tugagach videoni eshitib, musiqa ovozni bosib ketmasligiga ishonch hosil qiling (`music_gain` 0.6-0.9).

## Natija: `jobs/<job>/brief_music.json`
```json
{"music": {"genre": "chiptune", "bpm": 140, "key": 2, "scale": "major", "progression": [0,5,3,4]}, "music_seed": 4127, "music_gain": 0.8,
 "moods": {"1": "hero", "2": "groove", "5": "sad", "6": "groove", "9": "finale"}, "why": "1 jumla"}
```
Video yig'uvchi bularni scenes.json ga ko'chiradi va topics_log.md ga `musiqa` (janr) ni yozadi.
