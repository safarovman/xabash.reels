# xabash.reels

Avtomatik o'zbekcha Reels zavodi: ssenariy → Google Flow rasmlari → ElevenLabs ovozi → motion dizayn + musiqa → Buffer orqali Instagram.

- `reel/engine.py JOB_DIR` — `scenes.json` + `img/` + `aud/` dan 1080×1920 video yig'adi (`out/video.mp4`, `out/cover.jpg`).
- `reel/music.py` — sahnalarga mos fon musiqasi (FluidSynth, General MIDI).
- `SCHEMA.md` — `scenes.json` formati.
- `jobs/` — har bir videoning ssenariysi (`scenes.json`, `post.json`).
- Tayyor videolar GitHub **Releases**'ga (har kun bitta release) yuklanadi; Buffer ularni o'sha yerdan oladi.
