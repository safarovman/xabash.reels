import json, struct, sys, os
src, dst = sys.argv[1], sys.argv[2]
b = open(src, "rb").read(); n = struct.unpack(">I", b[:4])[0]; idx = json.loads(b[4:4 + n]); p = 4 + n
os.makedirs(dst, exist_ok=True)
for name, size, *_ in idx:
    open(os.path.join(dst, name), "wb").write(b[p:p + size]); p += size
print(len(idx), "fayl ->", dst)
