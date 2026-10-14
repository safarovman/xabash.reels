"""Cut the main subject out of an illustration and build a clean background plate.
Writes NN_fg.png (RGBA subject) and NN_bg.jpg (inpainted background) next to the image.
usage: python3 reel/cutout.py JOB_DIR   (processes img/NN.jpg that have no _fg.png yet)
"""
import sys, os, glob
import numpy as np, cv2
from PIL import Image

MODEL = os.environ.get("CUTOUT_MODEL", "isnet-general-use")

def process(path, session):
    from rembg import remove
    base = path[:-4]
    if os.path.exists(base + "_fg.png"): return "cached"
    im = Image.open(path).convert("RGB")
    mask = remove(im, session=session, only_mask=True, post_process_mask=True)
    m = np.asarray(mask).astype(np.float32) / 255.0
    cov = (m > 0.5).mean()
    if cov < 0.04 or cov > 0.80:
        open(base + "_nocut", "w").write(f"{cov:.3f}")
        return f"skip coverage {cov:.2f}"
    # keep only the biggest blobs (drop specks)
    bm = (m > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(bm, 8)
    keep = np.zeros_like(bm)
    if n > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]; big = areas.max()
        for k, a in enumerate(areas, 1):
            if a > big * 0.08: keep[lab == k] = 1
    m = m * cv2.dilate(keep, np.ones((9, 9), np.uint8)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    a = np.asarray(im)
    fg = np.dstack([a, (np.clip(m, 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(fg, "RGBA").save(base + "_fg.png")
    # background plate: inpaint the subject area (on a smaller image for speed, then upscale)
    hole = cv2.dilate((m > 0.15).astype(np.uint8) * 255, np.ones((25, 25), np.uint8))
    s = 0.5
    small = cv2.resize(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    hs = cv2.resize(hole, (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST)
    fill = cv2.inpaint(small, hs, 9, cv2.INPAINT_TELEA)
    fill = cv2.GaussianBlur(fill, (0, 0), 3)
    fill = cv2.resize(fill, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_CUBIC)
    hf = (cv2.GaussianBlur(hole, (0, 0), 6) / 255.0)[..., None]
    bg = cv2.cvtColor(a, cv2.COLOR_RGB2BGR) * (1 - hf) + fill * hf
    cv2.imwrite(base + "_bg.jpg", bg.astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return f"ok coverage {cov:.2f}"

if __name__ == "__main__":
    from rembg import new_session
    sess = new_session(MODEL)
    job = sys.argv[1]
    for p in sorted(glob.glob(f"{job}/img/[0-9][0-9].jpg")):
        print(os.path.basename(p), process(p, sess), flush=True)
