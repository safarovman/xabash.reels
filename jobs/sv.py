import sys,json,glob
# sv.py job NN url [new tts]
job,n,url=sys.argv[1],int(sys.argv[2]),sys.argv[3]
open('vo2_all.txt','a').write(f"{job} vo_{n:02d}.mp3 {url}\n")
if len(sys.argv)>4:
    M={'pult':'0800_pult','bepul':'1230_bepul-sinov','muz':'1600_ai-muzlatkich','non':'1830_non-odobi','yuz':'2100_yuzga-qol','gitler':'1030_gitler-moskva','anqara':'1430_anqara'}
    p=f'2026-10-18_{M[job]}/script.json';d=json.load(open(p))
    import re
    for s in d['scenes']:
        if s['n']==n: s['tts']=sys.argv[4]; s['text']=re.sub(r'\[[^\]]*\]\s*','',sys.argv[4]).strip()
    json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
print('ok')
