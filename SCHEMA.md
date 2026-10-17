# scenes.json schema

```json
{
  "title": "Ertadan boshlayman",
  "music_seed": 7,              // any int: changes groove/key so videos don't sound identical
  "music_gain": 0.8,            // optional
  "end_hold": 1.4,              // optional seconds after last VO
  "scenes": [ { ...scene... } ] // 7–10 scenes, one image + one VO clip each
}
```

## Scene
| key | meaning |
|---|---|
| `text` | exact VO text sent to ElevenLabs (used to place elements by phrase) |
| `mood` | music mood: `hero`, `sad`, `groove`, `mystery`, `tense`, `warm`, `finale` (last scene) |
| `img` / `vo` | optional; default `NN.jpg` / `vo_NN.mp3` |
| `kb` | optional Ken-Burns `[zoom_from, zoom_to, pan_x, pan_y]` |
| `extra` | optional extra seconds of hold |
| `elements` | list of overlay elements |

## `at` (when an element appears)
- number → seconds after the scene's VO starts
- `"start"` → right at scene start, `"end"` → near scene end
- string phrase → found in `text`; time estimated from its position and snapped to the nearest pause in the VO

## Element types
| type | fields | look |
|---|---|---|
| `caption` | `words[]`, `color` (white/yellow), `y`, `size`=96, `gap` | big bold words popping one by one (lower third y≈1300–1460) |
| `stamp` | `text`, `y`, `rot`, `size` | red rubber stamp, slams in + screen shake + orchestra hit |
| `big` | `text`, `y`, `color` | huge red number on paper (e.g. `≈ 61 SOAT`), slams |
| `note` | `text`, `y`, `x`, `size`=78, `rot` | handwritten line on torn paper, slides up |
| `sticker` | `lines[]`, `color` (yellow/pink/blue/green), `x`,`y`,`w`,`size`,`rot` | sticky note pops |
| `pill` | `text`, `bg` (navy/crimson/royal/orange/purple/green), `fg`, `x`,`y`,`rot` | rounded label pops |
| `clock` | `day`, `time`, `y`=290 | glowing digital clock drops from top |
| `card` | `kicker`, `title[]`, `sub`, `y` | info card (science fact, source) |
| `xmark` | `x`,`y`,`size` | red X drawn over something |
| `ring` | `x`,`y`,`dur` | alarm rings + alarm sound |
| `dark` | `amount`, `fade` | darkens the background (for cards / ending) |
| `hide_captions` | – | fades out everything shown so far in this scene |
| `final` | `lines[]`, `y`, `size`=150 | closing question, big white/yellow, final music hit |

Layout rules: canvas 1080×1920. Keep text inside x 60–1020. Leave the character's face visible —
put stickers/pills on the side or top, captions in the lower third. Max ~3 overlay items visible at once.

## Brend va muqova
- `cover_title`: `["1-qator", "2-qator"]` — video oxirida 1.8 s muqova kadri (xira qahramon rasmi + logotip + katta sarlavha). Instagram thumbnail shu kadrdan olinadi (`timing.json` → `cover_ms`). Profil to'rida markaziy 3:4 qism ko'rinadi — sarlavha markazda.
- `cover_sub`: muqova ostidagi qisqa qo'lyozma qator.
- `cover_scene`: muqova foni uchun sahna raqami (0 = 1-sahna).
- Logotip `brand/logo_99foiz.png` avtomatik o'ng pastki burchakka qo'yiladi (`"logo": false` bilan o'chiriladi).


## PNG stikerlar va gap pufakchalari (2026-10-15)
- `char` — PNG personaj stikeri (oq kontur + soya). `{"type":"char","img":"c_dada.jpg","from":"left|right|bottom|pop","x":780,"y":1450,"h":900,"at":0.5,"talk":["vo"] | [["ibora1","ibora2"]],"out":"ibora","flip":false,"label":"DADA"}`. `img` — oq fondagi rasm (rembg avtomatik kesadi, `_cut.png` kesh) yoki tayyor RGBA PNG. Chetdan sakrab kiradi, yengil tebranadi, `talk` oralig'ida gapirgandek qimirlaydi, `out` da chiqib ketadi.
- `prop` — buyum stikeri (default `from: pop`, `h: 420`), ixtiyoriy `label` (yashil yorliq).
- `bubble` — gap pufakchasi: `{"type":"bubble","speaker":"DADA","text":"...","x":540,"y":330,"at":"start","until":"ibora","hl":{"so'z":"crimson"},"tail":"down|up|none","tail_x":0.3,"tag":"navy"}`. So'zlar ovozga mos ravishda kulrangdan qoraga yonadi; `hl` dagi so'zlar rangli va tagiga chiziladi. `text` berilmasa sahna matni olinadi.
- `scenes.json` → `"bright": true` (default) — yengil vinyetka, ochiq ko'rinish.
- Sahna fonida `"bg": "blueprint"` (+ `bg_color`) — ko'k chizma (grid) fon, infografika sahnalari uchun.
- `tag` — yirtma kalendar yorlig'i: `{"type":"tag","head":"YIL","text":"2005","x":150,"y":190,"color":"red"}` (REJA, YOSH, NARX va h.k.).
- `bars` — taqqoslash chiziqlari (animatsiyali to'lib boradi): `{"type":"bars","rows":[["Qo'shni",40,"red"],["Rahim",50,"yellow"]],"x":540,"y":620}`.
- `avatar` — doira ichidagi portret (telefon qo'ng'irog'i, eslab qolish): `{"type":"avatar","img":"c_bobur.jpg","x":880,"y":300,"size":200}`.

## Har video uchun o'z dizayni (theme) va harakatlar
- `scenes.json` → `"theme": {"font":"orbitron","font2":"fredoka","accent":[120,230,255],"accent2":[255,120,220],"bubble_bg":[20,24,60],"bubble_line":[120,230,255],"bubble_ink":[255,255,255],"bubble_dim":[110,120,170],"bubble_radius":30}` — shriftlar: inter, bangers, luckiest, pixel, orbitron, lobster, fredoka, russo, rubikmono, marker, caveat. `accent` = qizil o'rniga, `accent2` = sariq o'rniga (stamp, final, captionlar).
- Sahna fonida `"bg": "space"` — protsedurali koinot (yulduzlar, tumanliklar), `"bg_seed"`.
- `char`/`prop` da `"motion"`: `idle` (default), `float` (vaznsizlik: sekin suzish va aylanish), `fly` (`"path":[x0,y0]` dan `x,y` ga `dur` s ichida uchib keladi), `bounce`, `shake`, `spin`.
- `char` da `"moods": [["c_bobur_xafa.jpg","ibora"], ["c_bobur_hayron.jpg","ibora2"]]` — personaj hissiyoti gapga qarab almashadi (kulgan → xafa → hayron), almashganda kichik "pop".

## 2026-10-16 qo'shimchalar
- `"pace": "fast"` (video darajasida) — qisqa pauzalar (LEAD 0.06, TAIL 0.12), kuchliroq Ken Burns, har yangi gapda kichik kamera turtkisi, tez kirish, o'tishlar whip/zoom/flash/slide.
- `theme.transitions`: `["whip","zoom","flash","slide","torn"]` dan ro'yxat (sahnalar navbat bilan oladi); sahnada `"transition": "zoom"` bilan aniq. `theme.cut_fx`: sahna ichidagi kesish turi (punch | flash | whip).
- Sahna `imgs`: shu sahnadagi qo'shimcha kadrlar, gap davomida tez almashadi:
  `"imgs": ["05b.jpg", ["05c.jpg", "ibora"], {"img": "05d.jpg", "at": 3.2, "fx": "flash", "kb": [1.0, 1.15, 0.2, 0]}]` — `at` bo'lmasa teng bo'lib almashadi.
- Element `mark` — qo'lda chizilgan belgi: `{"type":"mark","shape":"circle|arrow|underline|check|cross|burst|box","x":540,"y":900,"w":380,"h":260,"to":[x,y] (arrow),"color":"red","width":13,"at":"ibora","label":"MANA U!","label_x":..,"label_y":..,"out":"ibora"}`.
- `char`/`prop` yangi `motion`: `point` (rot/`dir` yo'nalishida turtadi), `pulse`, `jump`, `wag` (+ bounce, shake, fly). `spin` va sekin `float` tavsiya qilinmaydi.
- Stiker rasmi job `img/` da bo'lmasa `assets/gestures/` dan olinadi.
- `"music": {"genre": "chiptune|synthwave|space|doira_pop|doira_folk|lapar|lofi|jazz_swing|detective|funk|disco|polka|western|tango|toy|epic", "bpm":.., "key":.., "scale":.., "progression":[0,5,3,4]}` yoki `{"file": "music.mp3", "offset": 0}` (aud/ ichida).
- `theme.font`/`font2`: reel/fonts dagi istalgan fayl, nomi kichik harfda va "-Regular"siz (specialelite, bungee, audiowide, shrikhand, blackopsone, monoton, rye, chewy, titanone, abrilfatface, alfaslabone, vt323, silkscreen, permanentmarker, patrickhand, pacifico, creepster, righteous, rubikbubbles, rubikglitch, bungeeshade ...).
- `"cover": {"layout": "hero|split|bubble|polaroid|diagonal|zoom|poster|classic", "img": "cover.jpg", "char": "c_x.jpg", "char_h": 1050, "flip": false, "props": ["p_g_x.jpg"], "badge": "2061", "title_colors": [[r,g,b],[r,g,b]], "accent": [r,g,b], "accent2": [r,g,b], "size": 150, "focus": [x,y], "zoom": 1.6, "tilt": -5, "band_y": 1180, "duo_dark": [r,g,b], "ink": [r,g,b]}` — oxirgi muqova kadri (profil prevyusi). `layout` berilmasa music_seed bo'yicha aylanadi.
- `python3 reel/engine.py JOB --qa` — tekshiruv varaqlari: har element paydo bo'lgandan 0.45 s keyingi va har kadr almashgandagi kadr, yorliq bilan → `out/qa/sheet_*.jpg`, `out/qa/elements.json`.
