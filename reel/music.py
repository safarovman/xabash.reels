"""Scene-aware background score rendered with FluidSynth + General MIDI soundfont.
Moods: hero, sad, groove, mystery, warm, finale, tense
usage: python3 music.py plan.json out.npy
"""
import sys, json, random, numpy as np, fluidsynth, os
SR = 48000
SF = next(p for p in ["/usr/share/sounds/sf2/FluidR3_GM.sf2", "/usr/share/sounds/sf2/TimGM6mb.sf2", "/usr/share/sounds/sf2/default-GM.sf2"] if os.path.exists(p))
plan = json.load(open(sys.argv[1])); out = sys.argv[2]
TOTAL = plan["total"]; rnd = random.Random(plan.get("seed", 1))
TR = rnd.choice([0, 0, 2, -3, 5])  # transpose for variety
if (plan.get("music") or {}).get("genre"): TR = 0

ev = []
def note(t, ch, n, v, d): ev.append((t, 1, ch, n + (TR if ch not in (9, 1, 2) else 0), v)); ev.append((t + d, 0, ch, n + (TR if ch not in (9, 1, 2) else 0), 0))
def drum(t, n, v, d=0.2): ev.append((t, 1, 9, n, v)); ev.append((t + d, 0, 9, n, 0))
BRASS, TIMP, HIT, TROMB, MAR, PIZZ, TUBA, VIB, STR, PIANO, CEL, XYL, BASSOON = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13
PROG = {BRASS: 61, TIMP: 47, HIT: 55, TROMB: 57, MAR: 12, PIZZ: 45, TUBA: 58, VIB: 11, STR: 48, PIANO: 0, CEL: 8, XYL: 13, BASSOON: 70}
VOL = {BRASS: 100, TIMP: 110, HIT: 105, TROMB: 110, MAR: 105, PIZZ: 100, TUBA: 90, VIB: 95, STR: 80, PIANO: 100, CEL: 80, XYL: 85, BASSOON: 90}

# ---------------- genre engine (music agent picks a genre per topic: plan["music"]["genre"]) ----------------
MUS = plan.get("music") or {}
GLEAD, GCHORD = 14, 15
SCALES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
          "hijaz": [0, 1, 4, 5, 7, 8, 10], "pentatonic": [0, 2, 4, 7, 9, 12, 14], "blues": [0, 3, 5, 6, 7, 10, 12], "phrygian": [0, 1, 3, 5, 7, 8, 10]}
# drum patterns: 16 steps per bar; K kick, S snare, H hat, O open hat, R ride, D doira dum, T doira tak, J jingle/tambourine, C clap, W woodblock
DRUMS = {
    "backbeat": dict(K="x.......x.x.....", S="....x.......x...", H="x.x.x.x.x.x.x.x."),
    "four": dict(K="x...x...x...x...", S="....x.......x...", H="..x...x...x...x.", O="..x...x...x...x."),
    "chip": dict(K="x.....x.x.......", S="....x.......x..x", H="xxxxxxxxxxxxxxxx"),
    "funk": dict(K="x..x..x...x..x..", S="....x..x.x..x...", H="xxxxxxxxxxxxxxxx"),
    "lofi": dict(K="x......x..x.....", S="....x.......x...", H="x.x.x.x.x.x.x.x."),
    "swing": dict(K="x.......x.......", S="....x.......x...", R="x..xx..xx..xx..x"),
    "doira": dict(D="x.....x...x.....", T="...x.x.....x.x.x", J="x.x.x.x.x.x.x.x."),
    "doira_fast": dict(D="x..x..x...x..x..", T="..x...x.x...x.xx", J="xxxxxxxxxxxxxxxx"),
    "oompah": dict(K="x...x...x...x...", S="..x...x...x...x."),
    "train": dict(K="x.......x.......", S="..x.x.x...x.x.xx", H="x.x.x.x.x.x.x.x."),
    "tango": dict(K="x..x..x.x.......", S="........x..x....", W="x..x..x.x..x..x."),
    "epic": dict(K="x.....x.x.....x.", S="....x.......x...", C="....x.......x..."),
    "sparse": dict(K="x...............", H="........x.......", J="....x.......x...")}
DN = dict(K=36, S=38, H=42, O=46, R=51, D=64, T=63, J=54, C=39, W=76)
GENRES = {
    "doira_pop":   dict(bpm=112, scale="hijaz", lead=104, chord=24, bass=33, drums="doira_fast", dens=.62, oct=0, swing=0),
    "doira_folk":  dict(bpm=96, scale="hijaz", lead=73, chord=104, bass=32, drums="doira", dens=.5, oct=12, swing=0),
    "lapar":       dict(bpm=124, scale="minor", lead=21, chord=24, bass=32, drums="doira_fast", dens=.7, oct=0, swing=0),
    "chiptune":    dict(bpm=150, scale="major", lead=80, chord=80, bass=38, drums="chip", dens=.75, oct=12, swing=0, arp=True),
    "synthwave":   dict(bpm=100, scale="minor", lead=81, chord=89, bass=38, drums="backbeat", dens=.45, oct=0, swing=0, bass8=True),
    "lofi":        dict(bpm=82, scale="dorian", lead=4, chord=4, bass=33, drums="lofi", dens=.4, oct=0, swing=.14),
    "jazz_swing":  dict(bpm=140, scale="mixolydian", lead=65, chord=0, bass=32, drums="swing", dens=.55, oct=0, swing=.3, walk=True),
    "funk":        dict(bpm=108, scale="dorian", lead=61, chord=7, bass=36, drums="funk", dens=.5, oct=0, swing=.05),
    "polka":       dict(bpm=132, scale="major", lead=21, chord=21, bass=58, drums="oompah", dens=.7, oct=0, swing=0, oompah=True),
    "space":       dict(bpm=88, scale="pentatonic", lead=98, chord=89, bass=38, drums="sparse", dens=.35, oct=12, swing=0, arp=True),
    "western":     dict(bpm=120, scale="minor", lead=105, chord=25, bass=32, drums="train", dens=.6, oct=0, swing=.1),
    "disco":       dict(bpm=120, scale="minor", lead=48, chord=27, bass=33, drums="four", dens=.5, oct=0, swing=0, bass8=True),
    "toy":         dict(bpm=126, scale="major", lead=9, chord=12, bass=32, drums="sparse", dens=.65, oct=12, swing=0),
    "tango":       dict(bpm=116, scale="minor", lead=21, chord=0, bass=32, drums="tango", dens=.55, oct=0, swing=0),
    "epic":        dict(bpm=110, scale="minor", lead=61, chord=48, bass=58, drums="epic", dens=.45, oct=0, swing=0),
    "detective":   dict(bpm=96, scale="blues", lead=65, chord=0, bass=32, drums="swing", dens=.4, oct=0, swing=.28, walk=True),
}
GEN = None
if MUS.get("genre") in GENRES:
    GEN = dict(GENRES[MUS["genre"]]); GEN.update({k: v for k, v in MUS.items() if k in ("bpm", "scale", "lead", "chord", "bass", "drums", "dens", "swing")})
    PROG[TUBA] = GEN["bass"]; PROG[GLEAD] = GEN["lead"]; PROG[GCHORD] = GEN["chord"]; VOL[GLEAD] = 100; VOL[GCHORD] = 78
    ROOT = 48 + MUS.get("key", rnd.choice([0, 2, 5, 7, -3]))
    SC = SCALES.get(GEN["scale"], SCALES["major"])
    DEG = MUS.get("progression") or rnd.choice([[0, 5, 3, 4], [0, 3, 4, 4], [0, 6, 5, 4], [0, 4, 5, 3], [0, 0, 3, 4], [0, 5, 0, 4]])
    def sdeg(d, octv=0): return ROOT + SC[d % len(SC)] + 12 * (d // len(SC)) + 12 * octv
    # one motif per video (seeded) + variation -> catchy but not the same tune every time
    MOT = [[rnd.choice([0, 1, 2, 3, 4, 5, 7]) if rnd.random() < GEN["dens"] else None for _ in range(8)] for _ in range(2)]
def genre_section(a, b, energy=1.0):
    B = 60 / GEN["bpm"]; st = B / 4; t = a; bar = 0; pat = DRUMS[GEN["drums"]]
    drum(a, 49, int(80 + 30 * energy), 1.5)
    while t < b - .05:
        d0 = DEG[bar % len(DEG)]; chord = [sdeg(d0 + k) for k in (0, 2, 4)]
        for step in range(16):
            tt = t + step * st + (GEN["swing"] * st if step % 2 else 0)
            if tt >= b: break
            for key, ptn in pat.items():
                if ptn[step] == "x" and (energy > .5 or key in ("K", "D", "J", "H")):
                    v = {"K": 112, "S": 100, "H": 62, "O": 70, "R": 70, "D": 110, "T": 96, "J": 64, "C": 90, "W": 86}[key]
                    drum(tt, DN[key], int(v * (0.7 + 0.3 * energy) * (1.0 if step % 4 == 0 else 0.85)), .08)
            # bass
            if GEN.get("walk"):
                if step % 4 == 0: note(tt, TUBA, sdeg(d0 + [0, 2, 4, 5][step // 4], -1), 100, B * .9)
            elif GEN.get("oompah"):
                if step % 8 == 0: note(tt, TUBA, sdeg(d0 + (0 if step == 0 else 4), -1), 108, B * .6)
                if step % 8 == 4: [note(tt, GCHORD, n, 82, B * .35) for n in chord]
            elif GEN.get("bass8"):
                if step % 2 == 0: note(tt, TUBA, sdeg(d0, -1) + (12 if step % 4 == 2 else 0), 98, st * 1.6)
            elif step in (0, 6, 8, 11): note(tt, TUBA, sdeg(d0 + (4 if step == 11 else 0), -1), 104, st * 2.5)
            # chords / arps
            if GEN.get("arp"):
                if step % 2 == 0: note(tt, GCHORD, chord[(step // 2) % 3] + 12, int(66 + 14 * energy), st * 1.8)
            elif not GEN.get("oompah"):
                if step in (0, 8) and energy > .3: [note(tt, GCHORD, n, int(60 + 16 * energy), B * (3.8 if GEN["chord"] in (48, 88, 89, 98) else 1.2)) for n in chord]
                elif step in (4, 12, 14) and GEN["chord"] in (7, 24, 25, 27, 0): [note(tt, GCHORD, n, 66, st * 1.4) for n in chord]
            # lead motif on 8th notes; quieter under heavy speech sections handled by ducking
            if step % 2 == 0 and energy > .45:
                m = MOT[bar % 2][step // 2]
                if m is not None:
                    n = sdeg(d0 + m, 1) + GEN["oct"] - (12 if bar % 4 == 3 and step > 8 else 0)
                    note(tt, GLEAD, n, int(84 + 16 * energy) if step % 4 == 0 else int(72 + 10 * energy), st * 1.7)
        if bar % 4 == 3: drum(t + 15 * st, 38, 90, .08); drum(t + 14 * st, 38, 70, .08)
        t += 16 * st; bar += 1

# merge consecutive sections with same mood
blocks = []
for s in plan["sections"]:
    if blocks and blocks[-1]["mood"] == s["mood"] and s["mood"] not in ("sad",): blocks[-1]["end"] = s["end"]
    else: blocks.append(dict(s))

def hero(a, b):
    for k in range(14): note(a + k * .045, TIMP, 43, 40 + k * 5, .1)
    t = a + .65; note(t, HIT, 60, 115, .6); drum(t, 49, 110, 1.5); drum(t, 36, 120)
    chords = [[48, 55, 60, 64], [50, 55, 59, 62], [52, 55, 60, 64], [53, 57, 60, 65], [55, 59, 62, 67]]
    steps = [0, .6, .9, 1.5, 1.8]; k = 0
    while t + steps[k % 5] < b - .3 and k < 10:
        tt = t + steps[k % 5] + (k // 5) * 2.2
        if tt >= b - .3: break
        for n in chords[k % 5]: note(tt, BRASS, n, 100, .5)
        note(tt, TIMP, 36 if k % 2 == 0 else 43, 100, .3); k += 1
def sad(a, b):
    for k, (n, d) in enumerate([(55, .32), (54, .32), (53, .32), (52, 1.0)]): note(a + .05 + k * .3, TROMB, n, 115, d - .02)
    for k in range(30): ev.append((a + .95 + k * .03, 4, TROMB, int(8192 + 600 * np.sin(k * 1.3)), 0))
    ev.append((a + 2.0, 4, TROMB, 8192, 0))
GROOVES = [
    dict(bpm=118, prog=[(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [53, 57, 60]), (43, [55, 59, 62])],
         mel=[[72, 0, 76, 79, 76, 0, 72, 74], [76, 0, 72, 69, 72, 0, 76, 0], [77, 0, 72, 69, 72, 74, 76, 0], [79, 0, 74, 71, 74, 0, 79, 77],
              [72, 76, 79, 84, 79, 0, 76, 0], [69, 72, 76, 0, 81, 79, 76, 0], [77, 0, 81, 79, 77, 76, 74, 0], [71, 74, 79, 0, 83, 0, 79, 0]]),
    dict(bpm=124, prog=[(45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62]), (48, [55, 60, 64])],
         mel=[[69, 72, 0, 76, 74, 72, 0, 69], [72, 0, 77, 0, 76, 74, 72, 0], [71, 74, 79, 0, 77, 76, 74, 0], [72, 76, 0, 79, 0, 76, 72, 0]]),
    dict(bpm=112, prog=[(48, [60, 64, 67]), (53, [60, 65, 69]), (55, [59, 62, 67]), (48, [60, 64, 67])],
         mel=[[84, 0, 79, 0, 76, 79, 84, 0], [81, 0, 77, 0, 72, 77, 81, 0], [83, 0, 79, 74, 79, 0, 83, 86], [84, 79, 76, 72, 0, 0, 72, 0]])]
def groove(a, b):
    g = rnd.choice(GROOVES); B = 60 / g["bpm"]; lead = rnd.choice([MAR, MAR, XYL, BASSOON])
    for k in range(4): drum(a - B + k * B / 4, 38, 70 + k * 12, .1)
    drum(a, 49, 100, 1.5); t = a; bar = 0
    while t < b - .05:
        root, ch = g["prog"][bar % len(g["prog"])]
        for beat in range(4):
            bt = t + beat * B
            if bt >= b: break
            if beat in (0, 2): drum(bt, 36, 112); note(bt, TUBA, root - 12 + (7 if beat == 2 else 0), 105, B * .7)
            else:
                drum(bt, 39, 95); drum(bt, 38, 60)
                for n in ch: note(bt, PIZZ, n - 12, 85, B * .4)
            drum(bt, 42, 70, .05); drum(bt + B / 2, 42, 50, .05)
            m = g["mel"][bar % len(g["mel"])]
            for e in range(2):
                n = m[beat * 2 + e]
                if n and bt + e * B / 2 < b: note(bt + e * B / 2, lead, n - (12 if lead == BASSOON else 0), 96 if e == 0 else 80, B * .45)
        if bar % 4 == 3: drum(t, 49, 70, 1.0)
        t += 4 * B; bar += 1
def mystery(a, b):
    drum(a, 49, 60, 2.0); B = 60 / 90; t = a; bar = 0
    pc = [(45, [57, 60, 64, 69]), (41, [53, 57, 60, 65]), (48, [55, 60, 64, 67]), (40, [52, 56, 59, 64])]
    while t < b - .05:
        root, ch = pc[bar % 4]
        for n in ch: note(t, STR, n - 12, 70, 4 * B - .05)
        note(t, TUBA, root - 12, 60, 4 * B * .9)
        for k in range(8):
            tt = t + k * B / 2
            if tt >= b: break
            note(tt, VIB, ch[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 12, 75 if k % 2 == 0 else 60, B * .8)
        for o in (0, 2 * B): drum(t + o, 36, 70); drum(t + o + B * .35, 36, 50)
        t += 4 * B; bar += 1
def tense(a, b):
    B = 60 / 132; t = a
    while t < b - .05:
        for k in range(8):
            tt = t + k * B / 2
            if tt >= b: break
            note(tt, PIZZ, 45 if k % 2 == 0 else 46, 90, B * .3)
        drum(t, 36, 90); drum(t + 2 * B, 36, 90); note(t, STR, 57, 70, 4 * B); note(t, STR, 63, 60, 4 * B); t += 4 * B
def warm(a, b):
    B = 60 / 100; t = a; bar = 0; drum(a, 49, 70, 1.5)
    fc = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [60, 64, 69, 72]), (41, [60, 65, 69, 72])]
    while t < b - .05:
        root, ch = fc[bar % 4]; note(t, PIANO, root - 12, 85, 4 * B); note(t, PIANO, root, 70, 4 * B)
        for n in ch: note(t, STR, n - 12, 60, 4 * B - .05)
        for k in range(8):
            tt = t + k * B / 2
            if tt >= b: break
            note(tt, PIANO, ch[[0, 1, 2, 3, 2, 1, 2, 1][k]], 78 if k % 2 == 0 else 62, B * .9)
        for beat in range(4):
            bt = t + beat * B
            if bt < b:
                if beat in (0, 2): drum(bt, 36, 75)
                drum(bt + B / 2, 70, 55, .05)
        t += 4 * B; bar += 1
def finale(a, b, hit):
    hit = hit if hit and a < hit < b else max(a + 1.5, b - 3.0)
    B = 60 / 96; t = a; bar = 0
    ec = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]
    while t < hit - .05:
        root, ch = ec[bar % 4]; note(t, PIANO, root - 12, 90, 4 * B); note(t, PIANO, root, 80, 4 * B)
        for n in ch: note(t, STR, n, min(120, 80 + bar * 8), 4 * B - .05)
        for k in range(8):
            tt = t + k * B / 2
            if tt >= hit - .05: break
            note(tt, PIANO, ch[[0, 1, 2, 1][k % 4]] + 12, 75, B * .8)
        t += 4 * B; bar += 1
    for k in range(16): note(hit - .8 + k * .05, TIMP, 36, 50 + k * 4, .08)
    note(hit, HIT, 60, 127, 1.0); drum(hit, 49, 127, 3.0); drum(hit, 57, 120, 3.0); drum(hit, 36, 127)
    for n in [36, 48, 55, 60, 64, 67, 72]: note(hit, BRASS, n, 115, 2.5)
    for n in [48, 55, 60, 64, 67]: note(hit, STR, n, 110, max(.5, TOTAL - hit))
    note(hit, TIMP, 36, 127, 1.5)

final_hit = plan.get("final_hit")
for blk in blocks:
    a, b, m = blk["start"], blk["end"], blk["mood"]
    if GEN and m in ("hero", "groove", "warm", "mystery"): genre_section(a, b, {"hero": 1.0, "groove": .9, "warm": .6, "mystery": .4}[m])
    elif GEN and m == "finale":
        hit = final_hit if final_hit and a < final_hit < b else max(a + 1.5, b - 3.0); genre_section(a, hit, 1.0); note(hit, HIT, 60, 127, 1.0); drum(hit, 49, 127, 3.0); drum(hit, 36, 127)
        for n in [sdeg(DEG[0] + k) for k in (0, 2, 4, 7)]: note(hit, GCHORD, n, 110, max(.5, TOTAL - hit)); note(hit, BRASS, n, 105, 2.0)
    else: {"hero": hero, "sad": sad, "groove": groove, "mystery": mystery, "warm": warm, "tense": tense}.get(m, groove)(a, b) if m != "finale" else finale(a, b, final_hit)
for h in plan["hits"]:
    if final_hit and abs(h - final_hit) < .05: continue
    note(h, HIT, 60, 125, .7); drum(h, 49, 120, 1.8); drum(h, 36, 127); note(h, TIMP, 36, 120, .8)
    for n in [48, 55, 60, 64]: note(h, BRASS, n, 115, .7)
for bl in plan["blips"]: note(bl - .03, XYL, rnd.choice([84, 88, 91, 96]), 105, .2)

fs = fluidsynth.Synth(samplerate=float(SR), gain=0.5); sfid = fs.sfload(SF)
for c, p in PROG.items(): fs.program_select(c, sfid, 0, p); fs.cc(c, 7, VOL[c])
fs.program_select(9, sfid, 128, 0)
ev.sort(key=lambda e: (e[0], 0 if e[1] in (0, 4) else 1))
n_total = int((TOTAL + 1.0) * SR); buf = []; cur = 0
for (tt, kind, ch, a_, b_) in ev:
    s = int(max(0, tt) * SR)
    if s > cur and cur < n_total: buf.append(fs.get_samples(min(s, n_total) - cur)); cur = min(s, n_total)
    if kind == 1: fs.noteon(ch, max(0, min(127, a_)), int(min(127, b_)))
    elif kind == 0: fs.noteoff(ch, max(0, min(127, a_)))
    elif kind == 4: fs.pitch_bend(ch, a_ - 8192)
if n_total > cur: buf.append(fs.get_samples(n_total - cur))
x = np.concatenate(buf).astype(np.float32).reshape(-1, 2) / 32768.0
# level each section
g = np.ones(len(x), np.float32)
TGT = {"hero": -20, "sad": -24, "groove": -22, "mystery": -23, "warm": -22, "finale": -21, "tense": -22}
for s in plan["sections"]:
    i0, i1 = int(s["start"] * SR), min(len(x), int(s["end"] * SR)); seg = x[i0:i1]
    if len(seg) == 0: continue
    r = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9); g[i0:i1] = 10 ** ((TGT.get(s["mood"], -22) - r) / 20)
k = int(.12 * SR); g = np.convolve(g, np.ones(k) / k, mode="same"); x *= g[:, None]
pk = np.abs(x).max()
if pk > .95: x *= .95 / pk
np.save(out, x); print("music ok", x.shape, len(ev), "transpose", TR)
