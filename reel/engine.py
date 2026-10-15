"""Reel engine: builds a 1080x1920 motion-design reel from a job folder.

Job folder layout:
  scenes.json      scene + element description (see SCHEMA.md)
  img/NN.jpg       one 9:16 illustration per scene
  aud/vo_NN.mp3    one voice-over clip per scene
Usage:
  python3 reel/engine.py JOB_DIR [--preview] [--frames=1.0,5.2]
Outputs (in JOB_DIR/out): video_master.mp4, video.mp4 (max quality, <95 MB), cover.jpg, timing.json
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
SCENES_END = sum(scene_len)
COVER_LEN = 1.8 if CFG.get("cover_title") else 0.0
TOTAL = SCENES_END + COVER_LEN

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

# ---------------- PNG stickers (characters / props) + speech bubbles ----------------
def load_rgba(name):
    """img/<name>: PNG with alpha used as-is; JPG/PNG without alpha -> background removed with rembg (cached as _cut.png)."""
    p = f"{JOB}/img/{name}"
    im = Image.open(p)
    if im.mode == "RGBA" and np.asarray(im)[..., 3].min() < 250: return im
    cache = p.rsplit(".", 1)[0] + "_cut.png"
    if os.path.exists(cache): return Image.open(cache).convert("RGBA")
    from rembg import remove, new_session
    global _RB
    try: _RB
    except NameError: _RB = new_session("isnet-general-use")
    out = remove(im.convert("RGB"), session=_RB, post_process_mask=True); out.save(cache); return out
def sticker_img(name, height=900, outline=14, flip=False):
    im = load_rgba(name); bb = im.getbbox(); im = im.crop(bb)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    s = height / im.height; im = im.resize((max(1, int(im.width * s)), int(height)), Image.LANCZOS)
    pad = outline + 30; a = np.zeros((im.height + 2 * pad, im.width + 2 * pad), np.uint8); a[pad:pad + im.height, pad:pad + im.width] = np.asarray(im)[..., 3]
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * outline + 1, 2 * outline + 1))
    ring = cv2.GaussianBlur(cv2.dilate((a > 110).astype(np.uint8) * 255, k), (0, 0), 1.2)
    canvas = Image.new("RGBA", (a.shape[1] + 20, a.shape[0] + 28), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), (8, 18), Image.fromarray(ring)); canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    wl = Image.new("RGBA", (a.shape[1], a.shape[0]), (255, 255, 255, 0)); wl.putalpha(Image.fromarray(ring)); canvas.alpha_composite(wl, (0, 0))
    canvas.alpha_composite(im, (pad, pad)); return canvas
def label_tag(txt, bg=(46, 160, 100), fg=(255, 255, 255), size=40):
    f = F(INTER_BLACK, size); w, h, b = text_size(f, txt); im = Image.new("RGBA", (w + 44, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w + 43, h + 29), 8, fill=bg + (255,)); d.text((22 - b[0], 15 - b[1]), txt, font=f, fill=fg); return im
def wrap_words(f, words, maxw):
    lines, cur = [], []
    for wd in words:
        if cur and text_size(f, " ".join(cur + [wd]))[0] > maxw: lines.append(cur); cur = [wd]
        else: cur.append(wd)
    if cur: lines.append(cur)
    return lines
def bubble_layout(text, speaker, w=860, size=66, tail="down", tail_x=0.5, tag_color=(60, 70, 90)):
    f = F(INTER_BLACK, size); words = text.upper().split()
    lines = wrap_words(f, words, w - 90)
    while len(lines) > 4 and size > 40: size -= 4; f = F(INTER_BLACK, size); lines = wrap_words(f, words, w - 90)
    lh = int(size * 1.18); bh = lh * len(lines) + 70; im_w, im_h = w + 40, bh + 110
    pos = []; y = 60 + 35
    for ln in lines:
        lw = text_size(f, " ".join(ln))[0]; x = 20 + (w - lw) / 2
        for wd in ln:
            pos.append((wd, x, y)); x += text_size(f, wd + " ")[0]
        y += lh
    return dict(f=f, pos=pos, w=w, bh=bh, im_w=im_w, im_h=im_h, tail=tail, tail_x=tail_x, speaker=speaker.upper() if speaker else "", tag_color=tag_color)
def bubble_frame(L, n_lit, hl):
    im = Image.new("RGBA", (L["im_w"], L["im_h"]), (0, 0, 0, 0)); sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); top = 50
    ImageDraw.Draw(sh).rounded_rectangle((26, top + 12, 26 + L["w"], top + 12 + L["bh"]), 30, fill=(0, 0, 0, 120)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((20, top, 20 + L["w"], top + L["bh"]), 30, fill=(255, 255, 255, 255), outline=(30, 30, 36, 255), width=4)
    tx = 20 + L["w"] * L["tail_x"]
    if L["tail"] == "down": d.polygon([(tx - 34, top + L["bh"] - 3), (tx + 34, top + L["bh"] - 3), (tx + 6, top + L["bh"] + 52)], fill=(255, 255, 255, 255), outline=(30, 30, 36, 255))
    elif L["tail"] == "up": d.polygon([(tx - 34, top + 3), (tx + 34, top + 3), (tx + 6, top - 46)], fill=(255, 255, 255, 255), outline=(30, 30, 36, 255))
    if L["speaker"]:
        tf = F(INTER_BLACK, 30); tw, th, b = text_size(tf, L["speaker"]); d.rounded_rectangle((44, top - 22, 44 + tw + 30, top + th + 4), 6, fill=L["tag_color"] + (255,)); d.text((59 - b[0], top - 13 - b[1]), L["speaker"], font=tf, fill=(255, 255, 255))
    for k, (wd, x, y) in enumerate(L["pos"]):
        key = re.sub(r"[^\w']", "", wd.lower())
        c = (190, 190, 196) if k >= n_lit else (hl.get(key) or (28, 26, 30))
        d.text((x, y + top - 60), wd, font=L["f"], fill=c)
        if k < n_lit and hl.get(key): ww = text_size(L["f"], wd)[0]; d.line((x, y + top - 60 + L["f"].size * 1.05, x + ww, y + top - 60 + L["f"].size * 1.05), fill=hl[key], width=5)
    return im

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
bases = []; FG = {}; BGC = {}; BASE2 = {}; SW = {}
ANIM = CFG.get("anim", "static")   # "cutout" is disabled by default (owner: keep pictures whole)
for i, sc in enumerate(scenes):
    ip = f"{JOB}/img/{sc.get('img', f'{i + 1:02d}.jpg')}"
    im = cv2.cvtColor(cv2.imread(ip), cv2.COLOR_BGR2RGB)
    s = max(W / im.shape[1], H / im.shape[0]) * 1.16
    sz = (int(im.shape[1] * s), int(im.shape[0] * s))
    bases.append(cv2.resize(im, sz, interpolation=cv2.INTER_LANCZOS4).astype(np.float32))
    stem = ip[:-4]
    # 2-frame animation: NN_b.jpg = same picture with a small change (hand moved, eyes, etc.)
    ip2 = f"{JOB}/img/{sc['img2']}" if sc.get("img2") else stem + "_b.jpg"
    if os.path.exists(ip2) and not sc.get("no_img2"):
        im2 = cv2.cvtColor(cv2.imread(ip2), cv2.COLOR_BGR2RGB)
        BASE2[i] = cv2.resize(im2, sz, interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        if sc.get("img2_at") is not None: SW[i] = anchor(i, sc["img2_at"])
    if sc.get("anim", ANIM) == "cutout" and os.path.exists(stem + "_fg.png") and os.path.exists(stem + "_bg.jpg"):
        fgi = np.asarray(Image.open(stem + "_fg.png").convert("RGBA"))
        FG[i] = cv2.resize(fgi, sz, interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        BGC[i] = cv2.resize(cv2.cvtColor(cv2.imread(stem + "_bg.jpg"), cv2.COLOR_BGR2RGB), sz, interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        ys, xs = np.where(FG[i][..., 3] > 128)
        FG[i] = (FG[i], float(xs.mean()), float(ys.max()), float(ys.min()))
yy, xx = np.mgrid[0:H, 0:W]
vign = np.clip(1 - 0.38 * (((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .72)) ** 2), 0.55, 1)[..., None].astype(np.float32)
VIGN_SOFT = None
grain_bank = [np.random.RandomState(k).normal(0, 2.5, (H // 2, W // 2)).astype(np.float32) for k in range(6)]
VIGN_SOFT = (1 - (1 - vign) * 0.35).astype(np.float32)
BUMPS = {}
def bump(i, t):
    """camera punch-in on hits: quick zoom kick that decays"""
    z = 0.0
    for tb in BUMPS.get(i, []):
        d = t - tb
        if 0 <= d < 0.6: z += 0.045 * math.exp(-d * 7) * (1 if d > 0.03 else d / 0.03)
    return z
def bg(i, t):
    base = bases[i]; bh, bw = base.shape[:2]
    z0, z1, px, py = scenes[i].get("kb", KB_DEF[i % len(KB_DEF)])
    p = ease_in_out(t / scene_len[i])
    cut = i in FG
    zb = z0 + (z1 - z0) * p * (0.55 if cut else 1.0)   # background moves slower (parallax)
    zb += bump(i, t)
    def view(z):
        cw = (bw / 1.16) / z; ch = cw * H / W
        cx = bw / 2 + px * (bw - cw) / 2 * (p - .5) * 2; cy = bh / 2 + py * (bh - ch) / 2 * (p - .5) * 2
        x0, y0 = cx - cw / 2, cy - ch / 2
        return np.array([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]], np.float32)
    M = view(zb)
    if not cut:
        fr = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if i in BASE2:
            sw = SW.get(i, scene_len[i] * 0.5); a = clamp((t - sw) / 0.12)
            if a > 0:
                f2 = cv2.warpAffine(BASE2[i], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                fr = f2 if a >= 1 else fr * (1 - a) + f2 * a
        return fr
    fr = cv2.warpAffine(BGC[i], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    fg, fx, fyb, fyt = FG[i]
    zf = z0 + (z1 - z0) * p * 1.35 + bump(i, t) * 1.3   # subject moves more -> depth
    Mf = view(zf)
    # character life: breathing (scale about feet), sway, bob, entrance pop
    seed = (i * 7.31) % 6.28
    br = 1 + 0.014 * math.sin(2 * math.pi * t / 1.7 + seed)
    rot = 0.9 * math.sin(2 * math.pi * t / 2.9 + seed)
    bob = 7 * math.sin(2 * math.pi * t / 1.25 + seed)
    ent = ease_out_back(clamp(t / 0.45), 1.6)
    br *= 0.94 + 0.06 * ent; bob += (1 - ent) * 60
    R = cv2.getRotationMatrix2D((fx, fyb), rot, br); R[1, 2] += bob
    A = np.vstack([Mf, [0, 0, 1]]) @ np.vstack([R, [0, 0, 1]])
    lay = cv2.warpAffine(fg, A[:2].astype(np.float32), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    al = lay[..., 3:4] / 255.0
    # soft contact shadow
    sh = cv2.GaussianBlur(al, (0, 0), 14)
    if sh.ndim == 2: sh = sh[..., None]
    sh = np.roll(sh, (14, 10), (0, 1))
    fr = fr * (1 - 0.35 * sh)
    return fr * (1 - al) + lay[..., :3] * al

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
        elif ty in ("char", "prop"):
            spr = to_np(sticker_img(el["img"], el.get("h", 900 if ty == "char" else 420), el.get("outline", 14 if ty == "char" else 10), el.get("flip", False)))
            side = el.get("from", "bottom" if ty == "char" else "pop")
            talk = []
            for tr in el.get("talk", []):
                if tr == "vo": talk.append((LEAD, LEAD + vod[i]))
                else: talk.append((anchor(i, tr[0]), anchor(i, tr[1])))
            E[i].append(dict(kind="char", spr=spr, x=x, y=y, t0=t0, rot=rot, side=side, talk=talk, seed=seed % 7, label=to_np(label_tag(el["label"], col(el.get("label_bg", "green"), (46, 160, 100)))) if el.get("label") else None))
            if el.get("out") is not None: E[i][-1]["t_out"] = anchor(i, el["out"])
            sfx(i, t0, "whoosh" if side in ("left", "right", "bottom") else "pop")
        elif ty == "bubble":
            txt = el.get("text") or sc.get("text", ""); L = bubble_layout(txt, el.get("speaker", sc.get("speaker_name", "")), el.get("w", 860), el.get("size", 62), el.get("tail", "down"), el.get("tail_x", 0.5), col(el.get("tag", "navy"), (60, 70, 90)))
            hl = {re.sub(r"[^\w']", "", k.lower()): col(v, RED) for k, v in el.get("hl", {}).items()}
            t1 = anchor(i, el["until"]) if el.get("until") else LEAD + vod[i]
            nW = len(L["pos"]); lens = np.cumsum([len(w_) + 1 for w_, _, _ in L["pos"]]); lens = lens / lens[-1]
            frames = [to_np(bubble_frame(L, k, hl)) for k in range(nW + 1)]
            E[i].append(dict(kind="bubble", frames=frames, cum=lens, t1=t1, x=x, y=y, t0=t0, rot=rot)); sfx(i, t0, "pop")
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
for i in range(N):
    BUMPS[i] = sorted(set([round(ts, 3) for ts in SHAKE[i]] + [round(e["t0"], 3) for e in E[i] if e.get("cap") and e is E[i][0]]))

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
    elif k == "char":
        side = e["side"]; sd = e["seed"]
        p = ease_out_back(dt / .5, 1.5)
        ox = oy = 0
        if side == "left": ox = -(W * 0.7) * (1 - p)
        elif side == "right": ox = (W * 0.7) * (1 - p)
        elif side == "bottom": oy = 900 * (1 - p)
        scl = sc * (0.3 + 0.7 * ease_out_back(dt / .3, 2.2)) if side == "pop" else sc
        bob = 8 * math.sin(t * 2.3 + sd); rr = rot + 1.2 * math.sin(t * 1.7 + sd)
        talking = any(a <= t <= b for a, b in e["talk"])
        if talking: scl *= 1 + 0.022 * abs(math.sin(t * 13)); rr += 1.5 * math.sin(t * 9)
        if "t_out" in e and t > e["t_out"]:
            q = clamp((t - e["t_out"]) / .35); ox += (-1 if side == "left" else 1) * W * 0.8 * q * q; al_out = 1.0
        paste(frame, e["spr"], e["x"] + ox, e["y"] + oy + bob, scl, rr, clamp(dt / .1) * al_out)
        if e.get("label") is not None and dt > .3:
            paste(frame, e["label"], e["x"] + ox + e["spr"].shape[1] * 0.18, e["y"] + oy + bob + e["spr"].shape[0] * 0.36, ease_out_back((dt - .3) / .25, 2), -4, 1.0)
    elif k == "bubble":
        prog = clamp((t - e["t0"]) / max(.3, e["t1"] - e["t0"])); n_lit = int(np.searchsorted(e["cum"], prog + 1e-6, side="right")); n_lit = min(n_lit, len(e["frames"]) - 1)
        p = ease_out_back(dt / .25, 2.0); paste(frame, e["frames"][n_lit], e["x"], e["y"], sc * (0.4 + 0.6 * p), rot, clamp(dt / .08) * al_out)
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
LOGO = None
_lp = CFG.get("logo") or (f"{HERE}/../brand/logo_99foiz.png" if os.path.exists(f"{HERE}/../brand/logo_99foiz.png") else None)
if _lp and CFG.get("logo", True) is not False:
    _li = Image.open(_lp).convert("RGBA")
    LOGO = to_np(_li.resize((150, 150), Image.LANCZOS)); LOGO_BIG = to_np(_li.resize((300, 300), Image.LANCZOS))
COVER = None
if COVER_LEN:
    ci = CFG.get("cover_scene", 0)
    cb = bases[ci]; bh, bw = cb.shape[:2]; cw = bw / 1.16; ch = cw * H / W
    crop = cb[int((bh - ch) / 2):int((bh - ch) / 2 + ch), int((bw - cw) / 2):int((bw - cw) / 2 + cw)]
    COVER = cv2.resize(crop, (W, H)).astype(np.float32)
    COVER = cv2.GaussianBlur(COVER, (0, 0), 6) * 0.55 + COVER * 0.0
    COVER = COVER * 0.72
    yy2 = np.linspace(0, 1, H)[:, None, None]; COVER = COVER * (1 - 0.35 * np.abs(yy2 - 0.5) * 2)
    cov_lines = CFG["cover_title"]
    COVER_SPR = []
    for k, ln in enumerate(cov_lines):
        words = ln.split(); color = (255, 255, 255) if k % 2 == 0 else YEL
        sprs = [to_np(caption_word(wd, color, 150, 14)) for wd in words]
        widths = [sp.shape[1] - 2 * 38 for sp in sprs]; total = sum(widths) + 30 * (len(words) - 1); kf = min(1.0, 990 / total)
        x = W / 2 - total * kf / 2
        for sp, wd in zip(sprs, widths): COVER_SPR.append((sp, x + wd * kf / 2, 0, kf, k)); x += (wd + 30) * kf
    n_lines = len(cov_lines); y0 = 960 - (n_lines - 1) * 95 + 60
    COVER_SPR = [(sp, x, y0 + k * 190, kf, k) for (sp, x, _, kf, k) in COVER_SPR]
    COVER_SUB = to_np(note_strip(CFG["cover_sub"], 64, 77)) if CFG.get("cover_sub") else None

def render_cover(t):
    fr = COVER.copy()
    z = 1.0 + 0.03 * t / max(COVER_LEN, .1)
    if LOGO is not None: paste(fr, LOGO_BIG, W / 2, 560 - (y0_shift if False else 0), ease_out_back(t / .35, 1.8), 0, clamp(t / .15))
    for j, (sp, x, y, kf, k) in enumerate(COVER_SPR):
        tt = t - 0.08 - k * 0.12
        if tt > 0: paste(fr, sp, x, y, kf * (0.3 + 0.7 * ease_out_back(tt / .25, 2.2)), 0, clamp(tt / .08))
    if COVER_SUB is not None and t > .4: paste(fr, COVER_SUB, W / 2, 1400, 1.0, -2, clamp((t - .4) / .2))
    return fr

def frame_at(T):
    if T >= SCENES_END and COVER is not None:
        t = T - SCENES_END; fr = render_cover(t)
        if t < 0.25:  # quick flash transition
            fr = fr * (0.4 + 0.6 * t / 0.25) + 255 * (1 - t / 0.25) * 0.25
        fr = fr * vign
        if T > TOTAL - 0.3: fr *= max(0, (TOTAL - T) / 0.3)
        return np.clip(fr, 0, 255).astype(np.uint8)
    return frame_scene(T)

def frame_scene(T):
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
    fr = fr * (VIGN_SOFT if CFG.get("bright", True) else vign) + cv2.resize(grain_bank[int(T * FPS) % 6], (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
    if LOGO is not None: paste(fr, LOGO, W - 105, H - 115, 1.0, 0, 0.95)
    if T < 0.25: fr *= T / 0.25
    if COVER is None and T > TOTAL - 0.5: fr *= max(0, (TOTAL - T) / 0.5)
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
    pts = [starts[i] + scene_len[i] * 0.85 for i in range(N)] + ([SCENES_END + 1.0] if COVER is not None else [])
    os.makedirs(f"{OUT}/preview", exist_ok=True); ims = [Image.fromarray(frame_at(T)).resize((324, 576)) for T in pts]
    cols = 5; rows = math.ceil(len(ims) / cols); sheet = Image.new("RGB", (324 * cols, 576 * rows))
    for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 324, (k // cols) * 576))
    sheet.save(f"{OUT}/preview/sheet.jpg", quality=85); print("preview", f"{OUT}/preview/sheet.jpg"); sys.exit()

build_audio(f"{OUT}/audio.wav")
cover_t = (SCENES_END + 1.0) if COVER is not None else ((HITS[0] + 0.5) if HITS else min(3.0, TOTAL / 2))
Image.fromarray(frame_at(cover_t)).save(f"{OUT}/cover.jpg", quality=92)
timing["cover_ms"] = int(cover_t * 1000); json.dump(timing, open(f"{OUT}/timing.json", "w"), indent=1)
nf = int(TOTAL * FPS)
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{OUT}/audio.wav",
                         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{OUT}/video_master.mp4"], stdin=subprocess.PIPE)
for f in range(nf):
    proc.stdin.write(frame_at(f / FPS).tobytes())
    if f % 300 == 0: print(f, "/", nf, flush=True)
proc.stdin.close(); proc.wait()
# Final upload file: as high quality as possible but < 95 MB (GitHub hard limit is 100 MB per file).
MAX_MB = float(CFG.get("max_mb", 95))
br = int(min(16000, MAX_MB * 8 * 1024 / TOTAL * 0.93 - 192))  # kbit/s for video
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video_master.mp4", "-c:v", "libx264", "-preset", "slow", "-tune", "film",
                "-b:v", f"{br}k", "-maxrate", f"{int(br * 1.25)}k", "-bufsize", f"{br * 2}k", "-profile:v", "high", "-level", "4.2",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", f"{OUT}/video.mp4"], check=True)
if os.path.getsize(f"{OUT}/video.mp4") > 99 * 1024 * 1024:
    raise SystemExit("video.mp4 > 99 MB, lower max_mb in scenes.json")
print("done", round(TOTAL, 2), "s ->", f"{OUT}/video.mp4", os.path.getsize(f"{OUT}/video.mp4") // 1024, "KB")
