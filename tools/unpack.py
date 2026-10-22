"""Brauzerdan yuklangan paketni ochadi: python3 tools/unpack.py <fayl.tmp>
Kalitlar "job/fayl" ko'rinishida; .jpg lar ffmpeg bilan qayta saqlanadi, .mp3 to'g'ridan-to'g'ri aud/ ga."""
import json, struct, sys, subprocess, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jobs')
b = open(sys.argv[1], 'rb').read(); n = struct.unpack('>I', b[:4])[0]; idx = json.loads(b[4:4 + n]); o = 4 + n
for name, l in idx:
    job, f = name.split('/'); raw = b[o:o + l]; o += l
    if f.endswith('.mp3'):
        os.makedirs(f'{R}/{job}/aud', exist_ok=True); open(f'{R}/{job}/aud/{f}', 'wb').write(raw)
    else:
        os.makedirs(f'{R}/{job}/img', exist_ok=True); p = f'{R}/{job}/img/{f}'; open(p + '.src', 'wb').write(raw)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', p + '.src', '-q:v', '2', p], check=True); os.remove(p + '.src')
print(len(idx), 'fayl', 'OK' if o == len(b) else 'XATO')
