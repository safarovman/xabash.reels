import json, struct, sys, os
M = {"pult": "2026-10-18_0800_pult", "bepul": "2026-10-18_1230_bepul-sinov", "muz": "2026-10-18_1600_ai-muzlatkich", "non": "2026-10-18_1830_non-odobi", "yuz": "2026-10-18_2100_yuzga-qol"}
b = open(sys.argv[1], "rb").read(); n = struct.unpack(">I", b[:4])[0]; idx = json.loads(b[4:4 + n]); p = 4 + n
for name, size, *_ in idx:
    job, f = name.split("__"); d = os.path.join(os.path.dirname(os.path.abspath(__file__)), M[job], "aud"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f), "wb").write(b[p:p + size]); p += size
print(len(idx), "fayl")
