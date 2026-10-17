import json,sys
# python3 voj.py job1 job2 -> writes ../tmp/vo_1018.json with those jobs from vo2_all.txt
d={}
for l in open('vo2_all.txt'):
    p=l.split()
    if len(p)==3 and p[0] in sys.argv[1:]: d.setdefault(p[0],{})[p[1]]=p[2]
json.dump(d,open('../tmp/vo_1018.json','w')); print({k:len(v) for k,v in d.items()})
