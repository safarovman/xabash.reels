"""Reel engine: builds a 1080x1920 motion-design reel from a job folder.

Job folder layout:
  scenes.json      scene + element description (see SCHEMA.md)
  img/NN.jpg       one 9:16 illustration per scene
  aud/vo_NN.mp3    one voice-over clip per scene
Usage:
  python3 reel/engine.py JOB_DIR [--preview] [--frames=1.0,5.2]
Outputs (in JOB_DIR/out): video_master.mp4, video.mp4 (<28 MB), cover.jpg, timing.json
"""
import os, sys, math, random, subprocess, json, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = os.path.abspath(sys.argv[1])
CFG = json.load(open(f"{JOB}/scenes.json", encoding="utf-8"))
OUT = f"{JOB}/out"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
ONLY = None
for a_ in sys.argv:
    if a_.startswith("--frames="): ONLY = [float(x) for x in a_.split("=")[1].split(",")]

def find_font(names):
    for n in names:
        for d in ["/usr/share/fonts/opentype/inter", "/usr/share/fonts/truetype/inter", f"{HERE}/fonts"]:
            p = f"{d}/{n}"
            if os.path.exists(p): return p
    raise FileNotFoundError(names)
INTER_BLACK = find_font(["Inter-Black.otf", "Inter-Black.ttf"])
INTER_XB = find_font(["Inter-ExtraBold.otf", "Inter-ExtraBold.ttf", "Inter-Black.otf"])
CAVEAT = f"{HERE}/fonts/Caveat-Bold.ttf"; MARKER = f"{HERE}/fonts/Marker.ttf"
def F(p, s): return ImageFont.truetype(p, s)

YEL = (255, 210, 63); RED = (214, 40, 57); INK = (28, 26, 30); PAPER = (246, 240, 226)
COLORS = {"white": (255, 255, 255), "yellow": YEL, "red": RED, "pink": (255, 150, 180), "blue": (130, 200, 255),
          "sticky_yellow": (255, 214, 92), "green": (140, 220, 140), "navy": (40, 46, 70), "orange": (230, 150, 20),
          "royal": (40, 110, 200), "crimson": (214, 40, 57), "purple": (150, 90, 210)}
def col(c, default=(255, 255, 255)):
    if isinstance(c, list): return tuple(c)
    if c == "yellow" and False: return YEL
    return COLORS.get(c, default)

# ---------------- timing ----------------
LEAD, TAIL = 0.15, 0.30
scenes = CFG["scenes"]; N = len(scenes)
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
def pauses(p):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", o)]
    starts_ = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", o)]
    return starts_, ends
vod, vop = [], []
for i, sc in enumerate(scenes):
    p = f"{JOB}/aud/{sc.get('vo', f'vo_{i + 1:02d}.mp3')}"
    vod.append(dur(p)); vop.append(pauses(p))
scene_len = [LEAD + d + TAIL + scenes[i].get("extra", 0) for i, d in enumerate(vod)]
scene_len[-1] += CFG.get("end_hold", 1.4)
starts = np.cumsum([0] + scene_len[:-1]).tolist()
TOTAL = sum(scene_len)

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("‘", "'").replace("’", "'").replace("ʻ", "'").replace("'", ""))
def anchor(i, at):
    """at: number (s after VO start), 'start' (scene start), 'end', or phrase in the VO text."""
    if at is None or at == "start": return 0.1
    if at == "end": return scene_len[i] - 0.6
    if isinstance(at, (int, float)): return LEAD + float(at)
    txt = norm(scenes[i].get("text", "")); ph = norm(at)
    k = txt.find(ph)
    if k < 0: print(f"WARN scene {i + 1}: phrase '{at}' not in text", file=sys.stderr); return LEAD
    est = vod[i] * (k / max(1, len(txt)))
    # snap to a pause end if near (speech resumes there)
    ends = [0.0] + vop[i][1]
    best = min(ends, key=lambda e: abs(e - est))
    if abs(best - est) < 0.45: est = best
    return LEAD + est

# ---------------- easing ----------------
def clamp(x, lo=0, hi=1): return max(lo, min(hi, x))
def ease_out_back(x, s=1.9): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x): x = clamp(x); return 3 * x * x - 2 * x * x * x

# ---------------- sprites ----------------
def text_size(font, txt): b = font.getbbox(txt); return b[2] - b[0], b[3] - b[1], b
def caption_word(txt, color, size=96, stroke=11):
    f = F(INTER_BLACK, size); w, h, b = text_size(f, txt); pad = stroke + 24
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2 + 10), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((pad - b[0] + 5, pad - b[1] + 9), txt, font=f, fill=(0, 0, 0, 170), stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text((pad - b[0], pad - b[1]), txt, font=f, fill=color, stroke_width=stroke, stroke_fill=(15, 12, 10))
    return im
def torn_paper(w, h, color=PAPER, seed=0, jag=7):
    rnd = random.Random(seed); m = 14; pts = []
    for x in range(0, w + 1, 9): pts.append((m + x, m + rnd.uniform(0, jag)))
    for y in range(0, h + 1, 9): pts.append((m + w - rnd.uniform(0, jag * .5), m + y))
    for x in range(w, -1, -9): pts.append((m + x, m + h - rnd.uniform(0, jag)))
    for y in range(h, -1, -9): pts.append((m + rnd.uniform(0, jag * .5), m + y))
    im = Image.new("RGBA", (w + 2 * m + 16, h + 2 * m + 22), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 6, y + 12) for x, y in pts], fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(im).polygon(pts, fill=tuple(color) + (255,))
    arr = np.array(im).astype(np.int16); noise = np.random.RandomState(seed).randint(-7, 7, arr.shape[:2]); mask = arr[..., 3] > 250
    for c in range(3): arr[..., c][mask] = np.clip(arr[..., c][mask] + noise[mask], 0, 255)
    return Image.fromarray(arr.astype(np.uint8)), m
def note_strip(txt, size=78, seed=1, color=PAPER, ink=INK, font=CAVEAT, maxw=960):
    f = F(font, size); w, h, b = text_size(f, txt)
    while w + 70 > maxw: size -= 4; f = F(font, size); w, h, b = text_size(f, txt)
    im, m = torn_paper(w + 70, h + 50, color, seed)
    ImageDraw.Draw(im).text((m + 35 - b[0], m + 22 - b[1]), txt, font=f, fill=ink); return im
def stamp(txt, size=104, color=RED, maxw=880):
    f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    while w + 70 > maxw: size -= 4; f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    pw, ph = w + 70, h + 56
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), 12, fill=(250, 244, 236, 235), outline=color + (255,), width=10)
    d.rounded_rectangle((34, 34, 6 + pw, 6 + ph), 6, outline=color + (255,), width=3)
    d.text((20 + 35 - b[0], 20 + 28 - b[1]), txt, font=f, fill=color + (255,))
    arr = np.array(im); rs = np.random.RandomState(7); spk = (rs.rand(*arr.shape[:2]) < 0.035) & (arr[..., 3] > 0)
    arr[..., 3][spk] = (arr[..., 3][spk] * 0.35).astype(np.uint8); im = Image.fromarray(arr)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), mask=im.split()[3])
    out = Image.new("RGBA", (im.width + 20, im.height + 20), (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (10, 14)); out.alpha_composite(im, (4, 2)); return out
def sticky(lines, color, size=60, w=330):
    h = w; im = Image.new("RGBA", (w + 50, h + 60), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((22, 30, 22 + w, 30 + h), fill=(0, 0, 0, 130)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(im); d.rectangle((14, 14, 14 + w, 14 + h), fill=color + (255,))
    d.rectangle((14, 14, 14 + w, 54), fill=tuple(int(c * .9) for c in color) + (255,))
    d.rectangle((14 + w // 2 - 60, 2, 14 + w // 2 + 60, 34), fill=(255, 255, 255, 140))
    fonts = [F(MARKER, size)] + [F(CAVEAT, int(size * .85))] * (len(lines) - 1)
    total = sum(text_size(f, l)[1] + 22 for f, l in zip(fonts, lines)); y = 14 + (h - total) // 2 + 10
    for f, l in zip(fonts, lines):
        tw, th, b = text_size(f, l)
        while tw > w - 40: f = F(f.path, int(f.size * .9)); tw, th, b = text_size(f, l)
        d.text((14 + (w - tw) // 2 - b[0], y - b[1]), l, font=f, fill=INK); y += th + 22
    return im
def clock(day, tm):
    f1 = F(INTER_XB, 40); f2 = F(INTER_BLACK, 120); w1, h1, b1 = text_size(f1, day); w2, h2, b2 = text_size(f2, tm)
    w = max(w1, w2) + 110; h = h1 + h2 + 90; im = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((40, 40, 40 + w, 40 + h), 30, fill=(60, 200, 255, 120))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22))); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, 40 + w, 40 + h), 30, fill=(14, 22, 44, 240), outline=(90, 210, 255, 255), width=4)
    d.text((40 + (w - w1) // 2 - b1[0], 40 + 26 - b1[1]), day, font=f1, fill=(150, 220, 255))
    t = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(t).text((40 + (w - w2) // 2 - b2[0], 40 + 40 + h1 - b2[1]), tm, font=f2, fill=(110, 230, 255))
    im.alpha_composite(t.filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(t); return im
def pill(txt, bg, fg=(255, 255, 255), size=58):
    f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    while w + 80 > 980: size -= 4; f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    pw, ph = w + 80, h + 50; im = Image.new("RGBA", (pw + 40, ph + 46), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((24, 30, 24 + pw, 30 + ph), ph // 2, fill=(0, 0, 0, 140)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((18, 18, 18 + pw, 18 + ph), ph // 2, fill=bg + (255,)); d.text((18 + 40 - b[0], 18 + 25 - b[1]), txt, font=f, fill=fg); return im
def info_card(kicker, title_lines, sub):
    w = 900; f0 = F(INTER_XB, 34); f1 = F(INTER_BLACK, 84); f2 = F(CAVEAT, 52)
    while max(text_size(f1, l)[0] for l in title_lines) > w - 60: f1 = F(INTER_BLACK, f1.size - 4)
    lh = text_size(f1, "HQ")[1] + 22; h = 120 + lh * len(title_lines) + (110 if sub else 30)
    im, m = torn_paper(w, h, PAPER, 11, jag=9); d = ImageDraw.Draw(im)
    def ct(y, txt, f, c):
        tw, th, b = text_size(f, txt); d.text((m + (w - tw) // 2 - b[0], y - b[1]), txt, font=f, fill=c)
    ct(m + 40, " ".join(kicker.upper()), f0, (110, 100, 90)); y = m + 105
    for l in title_lines: ct(y, l, f1, RED); y += lh
    if sub:
        d.line((m + 200, y + 10, m + w - 200, y + 10), fill=(170, 160, 150), width=3); ct(y + 35, sub, f2, (70, 64, 60))
    return im
def big_paper(txt, size=150, color=RED):
    f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    while w + 90 > 980: size -= 6; f = F(INTER_BLACK, size); w, h, b = text_size(f, txt)
    im, m = torn_paper(w + 90, h + 70, (255, 248, 230), 23); ImageDraw.Draw(im).text((m + 45 - b[0], m + 32 - b[1]), txt, font=f, fill=color); return im
def to_np(im): return np.array(im.convert("RGBA")).astype(np.float32)

# ---------------- compositing ----------------
def paste(frame, spr, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.003 or scale <= 0.01: return
    h, w = spr.shape[:2]; M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
    tc = M @ np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]]).T
    x0, y0 = tc[0].min(), tc[1].min(); ow, oh = int(math.ceil(tc[0].max() - x0)) + 2, int(math.ceil(tc[1].max() - y0)) + 2
    M[0, 2] -= x0; M[1, 2] -= y0
    t = cv2.warpAffine(spr, M, (ow, oh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    X = int(round(cx - ow / 2)); Y = int(round(cy - oh / 2))
    fx0, fy0 = max(0, X), max(0, Y); fx1, fy1 = min(W, X + ow), min(H, Y + oh)
    if fx1 <= fx0 or fy1 <= fy0: return
    sub = t[fy0 - Y:fy1 - Y, fx0 - X:fx1 - X]; al = sub[..., 3:4] / 255.0 * alpha
    roi = frame[fy0:fy1, fx0:fx1]; roi[:] = roi * (1 - al) + sub[..., :3] * al

# ---------------- backgrounds ----------------
KB_DEF = [(1.00, 1.12, 0.0, -0.4), (1.02, 1.14, 0.2, 0.2), (1.00, 1.10, -0.3, 0.0), (1.10, 1.00, 0.3, 0.1), (1.00, 1.11, 0.0, 0.2),
          (1.02, 1.10, -0.2, -0.2), (1.00, 1.08, 0.0, 0.0), (1.10, 1.01, -0.2, 0.0), (1.00, 1.13, 0.0, -0.3)]
bases = []
for i, sc in enumerate(scenes):
    im = cv2.cvtColor(cv2.imread(f"{JOB}/img/{sc.get('img', f'{i + 1:02d}.jpg')}"), cv2.COLOR_BGR2RGB)
    s = max(W / im.shape[1], H / im.shape[0]) * 1.16
    bases.append(cv2.resize(im, (int(im.shape[1] * s), int(im.shape[0] * s)), interpolation=cv2.INTER_LANCZOS4).astype(np.float32))
yy, xx = np.mgrid[0:H, 0:W]
vign = np.clip(1 - 0.38 * (((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .72)) ** 2), 0.55, 1)[..., None].astype(np.float32)
grain_bank = [np.random.RandomState(k).normal(0, 4, (H // 2, W // 2)).astype(np.float32) for k in range(6)]
def bg(i, t):
    base = bases[i]; bh, bw = base.shape[:2]
    z0, z1, px, py = scenes[i].get("kb", KB_DEF[i % len(KB_DEF)])
    p = ease_in_out(t / scene_len[i]); z = z0 + (z1 - z0) * p
    cw = (bw / 1.16) / z; ch = cw * H / W
    cx = bw / 2 + px * (bw - cw) / 2 * (p - .5) * 2; cy = bh / 2 + py * (bh - ch) / 2 * (p - .5) * 2
    x0, y0 = cx - cw / 2, cy - ch / 2
    M = np.array([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]], np.float32)
    return cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

# ---------------- build elements ----------------
SFX = []; HITS = []; BLIPS = []
E = {i: [] for i in range(N)}; DARK = {i: [] for i in range(N)}; SHAKE = {i: [] for i in range(N)}
def sfx(i, t, k): SFX.append((starts[i] + t, k))
def caption_line(i, words, color, y, t0, gap=0.16, size=96):
    sprs = [to_np(caption_word(wd, color, size)) for wd in words]; space = 26
    widths = [s.shape[1] - 2 * 35 for s in sprs]; total = sum(widths) + space * (len(words) - 1); k = min(1.0, 980 / total)
    x = W / 2 - total * k / 2; out = []
    for j, (s, wd) in enumerate(zip(sprs, widths)):
        out.append(dict(kind="pop", spr=s, x=x + wd * k / 2, y=y, t0=t0 + j * gap, scale=k, dur=0.22, cap=True)); x += (wd + space) * k
        sfx(i, t0 + j * gap, "pop")
    return out
seed = 100
for i, sc in enumerate(scenes):
    for el in sc.get("elements", []):
        seed += 1; ty = el["type"]; t0 = anchor(i, el.get("at"))
        x = el.get("x", W / 2); y = el.get("y", 1400); rot = el.get("rot", 0)
        if ty == "caption":
            E[i] += caption_line(i, el["words"], col(el.get("color", "white")), y, t0, el.get("gap", 0.16), el.get("size", 96))
        elif ty == "stamp":
            E[i].append(dict(kind="slam", spr=to_np(stamp(el["text"], el.get("size", 104))), x=x, y=y, t0=t0, rot=rot)); SHAKE[i].append(t0); sfx(i, t0, "thud"); HITS.append(starts[i] + t0)
        elif ty == "big":
            E[i].append(dict(kind="slam", spr=to_np(big_paper(el["text"], el.get("size", 150), col(el.get("color", "red")))), x=x, y=y, t0=t0, rot=rot)); SHAKE[i].append(t0); sfx(i, t0, "thud"); HITS.append(starts[i] + t0)
        elif ty == "note":
            E[i].append(dict(kind="slideup", spr=to_np(note_strip(el["text"], el.get("size", 78), seed, col(el.get("paper"), PAPER) if el.get("paper") else PAPER)), x=x, y=y, t0=t0, rot=rot or random.Random(seed).uniform(-3, 3))); sfx(i, t0, "paper")
        elif ty == "sticker":
            cmap = {"yellow": (255, 214, 92), "pink": (255, 150, 180), "blue": (130, 200, 255), "green": (150, 225, 150)}
            E[i].append(dict(kind="pop", spr=to_np(sticky(el["lines"], cmap.get(el.get("color", "yellow"), (255, 214, 92)), el.get("size", 58), el.get("w", 300))), x=x, y=y, t0=t0, rot=rot, dur=.28)); sfx(i, t0, "pop"); BLIPS.append(starts[i] + t0)
        elif ty == "pill":
            E[i].append(dict(kind="pop", spr=to_np(pill(el["text"], col(el.get("bg", "navy")), col(el.get("fg", "white")), el.get("size", 58))), x=x, y=y, t0=t0, rot=rot, dur=.25)); sfx(i, t0, "pop"); BLIPS.append(starts[i] + t0)
        elif ty == "clock":
            E[i].append(dict(kind="drop", spr=to_np(clock(el["day"], el["time"])), x=x, y=el.get("y", 290), t0=t0, rot=0)); sfx(i, t0, "tick")
        elif ty == "card":
            E[i].append(dict(kind="slideup", spr=to_np(info_card(el.get("kicker", ""), el["title"], el.get("sub", ""))), x=x, y=y, t0=t0, rot=rot or -1.5)); sfx(i, t0, "whoosh")
        elif ty == "xmark":
            E[i].append(dict(kind="xmark", x=x, y=y, t0=t0, size=el.get("size", 300))); sfx(i, t0, "marker")
        elif ty == "ring":
            E[i].append(dict(kind="ring", x=int(x), y=int(y), t0=t0, t1=t0 + el.get("dur", 1.6))); sfx(i, t0, "alarm")
        elif ty == "dark":
            DARK[i].append((t0, t0 + el.get("fade", 0.5), el.get("amount", 0.45)))
        elif ty == "hide_captions":
            for e in E[i]:
                if e.get("cap") or e["kind"] in ("slam", "slideup", "pop"): e.setdefault("t_out", t0)
        elif ty == "final":   # big end question, e.g. SIZNIKI QACHON?
            lines = el["lines"]; y0 = el.get("y", 900)
            for k, ln in enumerate(lines):
                E[i] += caption_line(i, ln.split(), YEL if k % 2 else (255, 255, 255), y0 + k * 180, t0 + k * 0.32, size=el.get("size", 150))
            SHAKE[i].append(t0); HITS.append(starts[i] + t0); CFG.setdefault("_final_hit", starts[i] + t0)
for i in range(1, N): sfx(i, 0.0, "whoosh")

def draw_el(frame, e, t):
    if t < e["t0"]: return
    al_out = 1 - clamp((t - e["t_out"]) / 0.25) if "t_out" in e else 1.0
    if al_out <= 0: return
    dt = t - e["t0"]; k = e["kind"]; rot = e.get("rot", 0); sc = e.get("scale", 1.0); wob = 0.6 * math.sin(t * 2.1 + e["x"] * .01)
    if k == "pop":
        p = ease_out_back(dt / e.get("dur", .22), 2.4); paste(frame, e["spr"], e["x"], e["y"], sc * (0.2 + 0.8 * p), rot * p + wob * .5, clamp(dt / .08) * al_out)
    elif k == "slam":
        p = clamp(dt / .16); s = 2.3 - 1.3 * ease_out(p)
        if p >= 1: s = 1.0 + 0.04 * math.exp(-dt * 10) * math.sin(dt * 40)
        paste(frame, e["spr"], e["x"], e["y"], s * sc, rot, clamp(dt / .06) * al_out)
    elif k == "slideup":
        p = ease_out(dt / .4); paste(frame, e["spr"], e["x"], e["y"] + 160 * (1 - p), sc, rot + (1 - p) * 6 + wob * .4, clamp(dt / .15) * al_out)
    elif k == "drop":
        p = ease_out_back(dt / .45, 1.6); paste(frame, e["spr"], e["x"], e["y"] - 260 * (1 - p), sc, rot, clamp(dt / .1) * al_out)
    elif k == "xmark":
        s = e["size"]; x, y = e["x"], e["y"]
        for (ax, ay), (bx, by), p in [((x - s / 2, y - s / 2), (x + s / 2, y + s / 2), clamp(dt / .12)), ((x + s / 2, y - s / 2), (x - s / 2, y + s / 2), clamp((dt - .12) / .12))]:
            if p <= 0: continue
            ov = frame.copy(); cv2.line(ov, (int(ax), int(ay)), (int(ax + (bx - ax) * p), int(ay + (by - ay) * p)), (200, 25, 40), 26, cv2.LINE_AA)
            frame[:] = frame * 0.12 + ov * 0.88
    elif k == "ring":
        if t > e["t1"]: return
        for j in range(3):
            ph = ((dt * 2.2) + j / 3) % 1; al = (1 - ph) * 0.8
            ov = frame.copy(); cv2.circle(ov, (e["x"], e["y"]), int(60 + 140 * ph), (255, 240, 170), 8, cv2.LINE_AA); frame[:] = frame * (1 - al) + ov * al

def render_scene(i, t):
    fr = bg(i, t)
    for (t0, t1, amt) in DARK[i]:
        if t >= t0: fr *= (1 - amt * ease_out((t - t0) / max(.01, t1 - t0)))
    for e in E[i]: draw_el(fr, e, t)
    return fr
def torn_edge(seed_, x_edge):
    rnd = np.random.RandomState(seed_); ys = np.arange(H)
    n = np.cumsum(rnd.normal(0, 3.2, H)); n -= np.linspace(n[0], n[-1], H)
    return x_edge + n + 10 * np.sin(ys / 37.0 + seed_) + rnd.normal(0, 2.5, H)
def frame_at(T):
    i = max(j for j in range(N) if starts[j] <= T + 1e-9); t = T - starts[i]; fr = render_scene(i, t); TR = 0.42
    if i > 0 and t < TR:
        prev = render_scene(i - 1, scene_len[i - 1] + t); p = ease_in_out(t / TR)
        edge = torn_edge(i * 13, W + 80 - (W + 200) * p)[:, None]; X = np.arange(W)[None, :]
        newm = X >= edge; fiber = (X >= edge - 16) & (X < edge)
        out = prev.copy(); sh = np.clip(1 - (edge - X) / 70.0, 0, 1) * (X < edge); out *= (1 - 0.45 * sh[..., None])
        out[newm] = fr[newm]; out[fiber] = out[fiber] * 0.15 + np.array([245, 240, 228], np.float32) * 0.85; fr = out
    for ts in SHAKE[i]:
        d = t - ts
        if 0 <= d < 0.3:
            amp = 16 * (1 - d / 0.3); fr = cv2.warpAffine(fr, np.float32([[1, 0, amp * math.sin(d * 90)], [0, 1, amp * math.cos(d * 73)]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    fr = fr * vign + cv2.resize(grain_bank[int(T * FPS) % 6], (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
    if T < 0.25: fr *= T / 0.25
    if T > TOTAL - 0.5: fr *= max(0, (TOTAL - T) / 0.5)
    return np.clip(fr, 0, 255).astype(np.uint8)

# ---------------- audio ----------------
SR = 48000
def load_mp3(p): return np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]), np.float32).copy()
def env(n, a_, d_): t = np.arange(n) / SR; return np.minimum(1, t / max(a_, 1e-4)) * np.exp(-t / d_)
def mk_sfx(kind, rs):
    if kind == "pop":
        n = int(.12 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 18) + 380; return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .035)
    if kind == "thud":
        n = int(.35 * SR); t = np.arange(n) / SR; return 0.5 * np.sin(2 * np.pi * (55 + 90 * np.exp(-t * 30)) * t) * env(n, .001, .1)
    if kind == "whoosh":
        n = int(.45 * SR); noise = rs.normal(0, 1, n); k = 1 + (np.sin(np.linspace(0, np.pi, n)) * 40).astype(int)
        cs = np.cumsum(np.concatenate([[0], noise])); idx = np.arange(n); lo = np.clip(idx - k, 0, n)
        return 1.5 * (cs[idx + 1] - cs[lo]) / (idx + 1 - lo) * np.sin(np.linspace(0, np.pi, n)) ** 2
    if kind == "paper":
        n = int(.3 * SR); noise = rs.normal(0, 1, n); return 0.12 * (np.diff(np.concatenate([[0], noise])) + (rs.rand(n) < 0.02) * rs.normal(0, 3, n)) * np.sin(np.linspace(0, np.pi, n)) ** 1.5
    if kind == "marker":
        n = int(.26 * SR); hp = np.diff(np.concatenate([[0], rs.normal(0, 1, n)])); return 0.13 * hp * (0.6 + 0.4 * np.sin(np.arange(n) / SR * 2 * np.pi * 28)) * np.sin(np.linspace(0, np.pi, n))
    if kind == "tick":
        out = np.zeros(int(.5 * SR))
        for j in range(2): n = int(.02 * SR); s0 = int(j * .22 * SR); out[s0:s0 + n] += 0.4 * rs.normal(0, 1, n) * env(n, .0005, .004)
        return out
    if kind == "alarm":
        n = int(1.5 * SR); t = np.arange(n) / SR
        return 0.13 * (np.sin(2 * np.pi * 2200 * t) + .5 * np.sin(2 * np.pi * 3300 * t)) * (np.sin(2 * np.pi * 14 * t) > 0) * np.minimum(1, (1.5 - t) / .3)
    return np.zeros(10)
def build_audio(path):
    n = int((TOTAL + 0.5) * SR); vo = np.zeros(n, np.float32)
    for i, sc in enumerate(scenes):
        c = load_mp3(f"{JOB}/aud/{sc.get('vo', f'vo_{i + 1:02d}.mp3')}"); s0 = int((starts[i] + LEAD) * SR); vo[s0:s0 + len(c)] += c[:max(0, n - s0)]
    plan = dict(total=TOTAL, sections=[dict(start=starts[i], end=starts[i] + scene_len[i], mood=sc.get("mood", "groove")) for i, sc in enumerate(scenes)],
                hits=sorted(HITS), blips=sorted(BLIPS), final_hit=CFG.get("_final_hit"), seed=CFG.get("music_seed", 1))
    json.dump(plan, open(f"{OUT}/music_plan.json", "w"))
    subprocess.run([sys.executable, f"{HERE}/music.py", f"{OUT}/music_plan.json", f"{OUT}/music.npy"], check=True)
    m = np.load(f"{OUT}/music.npy")[:n]
    if len(m) < n: m = np.vstack([m, np.zeros((n - len(m), 2), np.float32)])
    e = np.abs(vo); k = int(.12 * SR); e = np.convolve(e, np.ones(k) / k, mode="same")
    duck = np.convolve(1 - 0.5 * np.clip(e / 0.03, 0, 1), np.ones(k) / k, mode="same"); m = m * duck[:, None]
    fx = np.zeros(n, np.float32); rs = np.random.RandomState(3)
    for (T, kind) in SFX:
        s = mk_sfx(kind, rs).astype(np.float32); s0 = int(T * SR)
        if s0 < n: fx[s0:s0 + len(s)] += s[:n - s0]
    mix = m * CFG.get("music_gain", 0.8) + (vo + fx * 0.45)[:, None]
    fade = np.ones(n); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl); mix *= fade[:, None]
    pk = np.abs(mix).max(); mix = mix / pk * 0.92 if pk > 0.92 else mix
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=mix.astype(np.float32).tobytes(), check=True)

timing = dict(starts=starts, scene_len=scene_len, total=TOTAL, hits=sorted(HITS))
json.dump(timing, open(f"{OUT}/timing.json", "w"), indent=1)
if ONLY:
    os.makedirs(f"{OUT}/preview", exist_ok=True)
    ims = []
    for T in ONLY:
        f = frame_at(T); ims.append(Image.fromarray(f).resize((324, 576)))
    cols = min(5, len(ims)); rows = math.ceil(len(ims) / cols); sheet = Image.new("RGB", (324 * cols, 576 * rows))
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(f"{OUT}/preview/sheet.jpg", quality=85); print("preview", f"{OUT}/preview/sheet.jpg", "starts", [round(s, 2) for s in starts]); sys.exit()
if "--auto-preview" in sys.argv:
    pts = [starts[i] + scene_len[i] * 0.85 for i in range(N)]
    os.makedirs(f"{OUT}/preview", exist_ok=True); ims = [Image.fromarray(frame_at(T)).resize((324, 576)) for T in pts]
    cols = 5; rows = math.ceil(len(ims) / cols); sheet = Image.new("RGB", (324 * cols, 576 * rows))
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(f"{OUT}/preview/sheet.jpg", quality=85); print("preview", f"{OUT}/preview/sheet.jpg"); sys.exit()

build_audio(f"{OUT}/audio.wav")
cover_t = (HITS[0] + 0.5) if HITS else min(3.0, TOTAL / 2)
Image.fromarray(frame_at(cover_t)).save(f"{OUT}/cover.jpg", quality=92)
timing["cover_ms"] = int(cover_t * 1000); json.dump(timing, open(f"{OUT}/timing.json", "w"), indent=1)
nf = int(TOTAL * FPS)
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{OUT}/audio.wav",
                         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{OUT}/video_master.mp4"], stdin=subprocess.PIPE)
for f in range(nf):
    proc.stdin.write(frame_at(f / FPS).tobytes())
    if f % 300 == 0: print(f, "/", nf, flush=True)
proc.stdin.close(); proc.wait()
br = int(min(4.0, 26 * 8 / TOTAL * 0.92) * 1000)  # keep final under ~26 MB
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video_master.mp4", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{br - 200}k", "-maxrate", f"{br}k", "-bufsize", f"{br * 2}k",
                "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", f"{OUT}/video.mp4"], check=True)
print("done", round(TOTAL, 2), "s ->", f"{OUT}/video.mp4", os.path.getsize(f"{OUT}/video.mp4") // 1024, "KB")
