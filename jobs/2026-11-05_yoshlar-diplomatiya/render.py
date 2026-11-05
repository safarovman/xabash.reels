#!/usr/bin/env python3
"""Yoshlar Diplomatiya Markazi: diplomatiyada ayollar. 44 s, 1080x1920, karaoke subtitr.
Ishlatish: render.py frames | render.py full"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); W, H, FPS = 1080, 1920, 30
AT = "/mnt/user-data/attachments/19573d39-f4c6-5545-9cc0-9a0cbe7860f3"
AUDIO = f"{AT}/8943a229-______008.mp3"; LOGO = f"{AT}/688875b0-image.jpg"
CREAM = (246, 236, 214); CORAL = (247, 92, 88); NAVY = (9, 22, 58)
F = lambda n, s: ImageFont.truetype(f"{D}/font/{n}.ttf", s)
PX = ("cute 3D clay render, soft plasticine claymation miniature, isometric diorama on a rounded dark navy platform, "
      "plain deep navy blue background with a faint dot grid, soft studio lighting, cream, navy and coral red palette, "
      "vertical 9:16, the diorama sits in the lower 60 percent of the frame, the upper 40 percent is completely empty background, "
      "no text, no letters, no numbers, no logos, no real flags. ")
# (boshlanish, sarlavha [1-2 qator], yorliq, prompt)
SC = [
 (0.00, ["DIPLOMATIYA"], None, "two clay diplomats shaking hands in front of a big clay globe, a white dove above them"),
 (2.40, ["TINCHLIK", "VA DO'STLIK"], None, "a cheerful clay woman and man holding a big olive branch together on a small green hill with a white dove"),
 (4.35, ["HAMKORLIK"], None, "two small clay houses of different styles joined by a little bridge, tiny people meeting in the middle"),
 (6.90, ["AYOLLAR"], "DIPLOMATIYADA", "a confident young clay woman diplomat in a navy suit and cream blouse speaking at a small podium with a microphone"),
 (10.75, ["ELCHI"], None, "an elegant clay woman ambassador in a navy suit holding a folder, standing beside a small embassy building with columns"),
 (11.55, ["DIPLOMAT"], None, "a clay woman diplomat at a desk signing a document with a fountain pen, a globe on the desk"),
 (12.50, ["XALQARO", "TASHKILOT"], None, "a clay woman sitting at a small round conference table with tiny blank name plates and microphones, other delegates around"),
 (16.25, ["MUNOSABATLAR"], "RIVOJLANTIRISH", "two clay women diplomats shaking hands and smiling across a small table with documents"),
 (19.70, ["TINCHLIK"], "SAQLASH", "a clay woman in a navy suit releasing a white dove from her hands, gentle and happy"),
 (21.05, ["INSON", "HUQUQLARI"], None, "a clay woman holding a big cream shield with a heart shape, protecting a small group of clay people"),
 (24.75, ["BILIM"], None, "a clay girl student sitting on a tall stack of books reading happily, a desk lamp beside her"),
 (26.55, ["XORIJIY", "TILLAR"], None, "a clay young woman with headphones at a laptop surrounded by empty colorful speech bubbles without any writing"),
 (27.90, ["KENG", "DUNYOQARASH"], None, "a clay young woman looking through a telescope from a small hill at a miniature globe with clouds"),
 (29.10, ["MAS'ULIYAT"], None, "a serious clay woman holding a briefcase and a folder, checking her watch beside a small flagless pole"),
 (32.70, ["AYOLLAR", "ISHTIROKI"], None, "a group of three diverse clay women diplomats walking together with folders, confident and smiling"),
 (35.50, ["TENGLIK"], None, "a balanced golden scale with a clay woman on one plate and a clay man on the other, perfectly level"),
 (36.40, ["JAMIYAT", "TARAQQIYOTI"], None, "a miniature clay city growing upward with little cranes, trees and rising arrows of buildings, tiny people cheering"),
 (39.10, ["MAQSADLI", "AYOLLAR"], None, "a clay young woman climbing cream steps made of books toward a glowing golden star"),
 (41.30, ["KELAJAK", "DIPLOMATIYASI"], None, "a proud clay young woman diplomat standing on top of a big clay globe holding a folder, sunrise glow behind her"),
]
WORDS = json.load(open(f"{D}/words.json"))
# subtitr bo'laklari: gap chegarasi yoki 4 so'z
CH, cur = [], []
for w in WORDS:
    cur.append(w)
    if len(cur) == 4 or w["t"][-1] in ".,":
        CH.append(cur); cur = []
if cur: CH.append(cur)
TOTAL = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUDIO])) + 0.2

def bg(i):
    p = f"{D}/img/{i:02d}.jpg"
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        r = max(W * 1.1 / im.width, H * 1.1 / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        x, y = (im.width - round(W * 1.1)) // 2, (im.height - round(H * 1.1)) // 2
        return np.array(im.crop((x, y, x + round(W * 1.1), y + round(H * 1.1))))
    a = np.zeros((round(H * 1.1), round(W * 1.1), 3), np.uint8); a[:] = NAVY
    for yy in range(0, a.shape[0], 34):
        a[yy:yy + 2, ::34] = (30, 48, 96)
    cv2.circle(a, (a.shape[1] // 2, 1450), 400, (34, 52, 104), -1)
    return a
BG = {}
def getbg(i):
    if i not in BG:
        if len(BG) > 3: BG.pop(next(iter(BG)))
        BG[i] = bg(i)
    return BG[i]

def logo_layer():
    l = Image.open(LOGO).convert("RGB"); s = 196
    l = l.crop((40, 40, l.width - 40, l.height - 40)).resize((s, s), Image.LANCZOS)
    mask = Image.new("L", (s, s), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), 34, fill=255)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L.paste(l, (40, 70), mask); return L
LOGOL = logo_layer()

def title_img(lines):
    sz = 250 if max(map(len, lines)) <= 8 else 190 if max(map(len, lines)) <= 11 else 150
    if len(lines) > 1: sz = min(sz, 170)
    f = F("anton", sz); hs = [f.getbbox(t) for t in lines]
    tw = max(b[2] for b in hs); lh = int(sz * 1.2); im = Image.new("RGBA", (W, lh * len(lines) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, t in enumerate(lines):
        w = f.getlength(t); d.text(((W - w) / 2 + 4, i * lh + 5), t, font=f, fill=(0, 0, 0, 120)); d.text(((W - w) / 2, i * lh), t, font=f, fill=CREAM)
    return im

def fit(tokens, f, maxw):
    return sum(f.getlength(t) for t in tokens) + 26 * (len(tokens) - 1) <= maxw

def subtitle(d, t):
    c = next((c for c in CH if c[0]["s"] - .12 <= t <= c[-1]["e"] + .28), None)
    if not c: return
    f = F("mont800", 58); ws = [w["t"] for w in c]; rows = [ws]
    if not fit(ws, f, 960):
        m = len(ws) // 2; rows = [ws[:m], ws[m:]]
    y = 700 if len(rows) == 1 else 660; k = 0
    for r in rows:
        tw = sum(f.getlength(w) for w in r) + 26 * (len(r) - 1); x = (W - tw) / 2
        for w in r:
            on = c[k]["s"] <= t < c[k]["e"] + .05; k += 1; wl = f.getlength(w)
            if on:
                d.rounded_rectangle((x - 12, y - 4, x + wl + 12, y + 74), 14, fill=CORAL + (255,))
            else:
                d.text((x + 2, y + 3), w, font=f, fill=(0, 0, 0, 150))
            d.text((x, y), w, font=f, fill=(255, 255, 255, 255) if on else CREAM + (255,)); x += wl + 26
        y += 84

TI = [title_img(s[1]) for s in SC]
def chip(text):
    f = F("anton", 62); w = int(f.getlength(text)); im = Image.new("RGBA", (w + 60, 104), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w + 59, 103), 20, fill=CORAL); d.text((30, 6), text, font=f, fill=(255, 255, 255)); return im
CHIP = {i: chip(s[2]) for i, s in enumerate(SC) if s[2]}
def ease(x): x = min(1, max(0, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def frame(t):
    i = max(k for k, s in enumerate(SC) if s[0] <= t)
    st = SC[i][0]; en = SC[i + 1][0] if i + 1 < len(SC) else TOTAL
    def layer(k, tt, dur):
        a = getbg(k); z = 1 / 1.1 * (1.0 + .06 * min(1, tt / max(dur, 1)))
        h, w = a.shape[:2]; cw, ch = W / (z * 1.1) * 1.0, H / (z * 1.1)
        M = np.float32([[W / (w * 0.909 / (1 + .06 * min(1, tt / max(dur, 1)))), 0, 0], [0, W / (w * 0.909 / (1 + .06 * min(1, tt / max(dur, 1)))), 0]])
        s = M[0, 0]; M[0, 2] = W / 2 - s * w / 2; M[1, 2] = H / 2 - s * h / 2
        return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR)
    fr = layer(i, t - st, en - st)
    p = (t - st) / .28
    if i and p < 1:
        fr = cv2.addWeighted(layer(i - 1, t - SC[i - 1][0], st - SC[i - 1][0]), 1 - p, fr, p, 0)
    im = Image.fromarray(fr).convert("RGBA")
    sc = .72 + .28 * ease((t - st) / .32); T = TI[i]
    if sc < 1:
        T2 = T.resize((round(T.width * sc), round(T.height * sc)), Image.BILINEAR)
    else: T2 = T
    y = 300 - (len(SC[i][1]) - 1) * 40
    if i in CHIP: y = 235
    im.alpha_composite(T2, ((W - T2.width) // 2, y + (T.height - T2.height) // 2))
    if i in CHIP and t - st > .18:
        C = CHIP[i]; s2 = ease((t - st - .18) / .25); C2 = C.resize((max(1, round(C.width * s2)), max(1, round(C.height * s2))))
        im.alpha_composite(C2, ((W - C2.width) // 2 + 170, 585 + (C.height - C2.height) // 2))
    d = ImageDraw.Draw(im, "RGBA"); subtitle(d, t); im.alpha_composite(LOGOL)
    return np.array(im.convert("RGB"))

if __name__ == "__main__":
    if sys.argv[1] == "prompts":
        json.dump([[f"{i:02d}.jpg", PX + s[3]] for i, s in enumerate(SC)], open(f"{D}/prompts.json", "w"), ensure_ascii=False); print(len(SC))
    elif sys.argv[1] == "frames":
        ts = [float(x) for x in sys.argv[2:]] or [1, 8.2, 12, 28, 42]
        S = Image.new("RGB", (len(ts) * 360, 640))
        for k, t in enumerate(ts): S.paste(Image.fromarray(frame(t)).resize((360, 640)), (k * 360, 0))
        S.save(f"{D}/sheet.jpg", quality=85)
    else:
        n = int(TOTAL * FPS); o = f"{D}/video.mp4"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", AUDIO,
                              "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5", "-shortest", "-movflags", "+faststart", o], stdin=subprocess.PIPE)
        for k in range(n):
            p.stdin.write(frame(k / FPS).tobytes())
            if k % 150 == 0: print(k, n, flush=True)
        p.stdin.close(); p.wait(); print("done", o)
