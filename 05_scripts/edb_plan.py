import csv,re,sys,collections
SP=sys.argv[1]
def num(s):
    m=re.match(r'(\d+)',s); return int(m.group(1)) if m else None
rows=list(csv.DictReader(open(SP+'/edb_rows.csv')))
have=set(num(r['icvr']) for r in rows if num(r['icvr']))
anch=collections.defaultdict(list)
for r in rows:
    n=num(r['icvr'])
    if n: anch[int(r['page'])].append(n)
import os
for r in csv.DictReader(open(SP+'/anchors_extra.csv')):
    anch[int(r['page'])]+= [int(r['first']),int(r['last'])]
A=sorted((p,min(v),max(v)) for p,v in anch.items())
N=list(csv.DictReader(open('/home/user/alexis-angel-martini/01_donnees/base_v2_csv/Notices.csv')))
targets=set()
for r in N:
    for v,n,s in re.findall(r'ICUR-(\d\d), (\d+)([a-z]?)',r['ICUR / refs catalogue']+' '+r['publications EDCS']): targets.add(int(n))
inside=lambda t: any(a[1]<=t<=a[2] for a in A)
absent=sorted(t for t in targets if t not in have and inside(t))
open(SP+'/absent.txt','w').write('\n'.join(map(str,absent)))
missing=sorted(t for t in targets if t not in have and not inside(t))
print('absents de la liste EDB (dans une plage déjà lue):',len(absent),absent)
def est(t):
    lo=[a for a in A if a[2]<t]; hi=[a for a in A if a[1]>t]
    if lo and hi:
        a=lo[-1]; b=hi[0]
        if b[0]-a[0]<=1: return a[0]+1
        rate=(b[1]-a[2])/max(1,(b[0]-a[0]-1))
        return a[0]+1+int((t-a[2])/max(rate,1)) if rate>0 else a[0]+1
    if lo: a=lo[-1]; return a[0]+max(1,int((t-a[2])/19))+0
    b=hi[0]; return max(1,b[0]-max(1,int((b[1]-t)/19)))
plan=collections.Counter(est(t) for t in missing)
print('targets',len(targets),'have',len(targets&have),'missing',len(missing))
pp=sorted(plan); print('pages to fetch',len(pp)); print(pp)
