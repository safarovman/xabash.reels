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
