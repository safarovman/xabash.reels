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

ev = []
def note(t, ch, n, v, d): ev.append((t, 1, ch, n + (TR if ch not in (9, 1, 2) else 0), v)); ev.append((t + d, 0, ch, n + (TR if ch not in (9, 1, 2) else 0), 0))
def drum(t, n, v, d=0.2): ev.append((t, 1, 9, n, v)); ev.append((t + d, 0, 9, n, 0))
BRASS, TIMP, HIT, TROMB, MAR, PIZZ, TUBA, VIB, STR, PIANO, CEL, XYL, BASSOON = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13
PROG = {BRASS: 61, TIMP: 47, HIT: 55, TROMB: 57, MAR: 12, PIZZ: 45, TUBA: 58, VIB: 11, STR: 48, PIANO: 0, CEL: 8, XYL: 13, BASSOON: 70}
VOL = {BRASS: 100, TIMP: 110, HIT: 105, TROMB: 110, MAR: 105, PIZZ: 100, TUBA: 90, VIB: 95, STR: 80, PIANO: 100, CEL: 80, XYL: 85, BASSOON: 90}

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
    {"hero": hero, "sad": sad, "groove": groove, "mystery": mystery, "warm": warm, "tense": tense}.get(m, groove)(a, b) if m != "finale" else finale(a, b, final_hit)
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
