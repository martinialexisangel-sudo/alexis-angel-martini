import csv,re,sys,difflib
import unicodedata
def norm(s):
    s=unicodedata.normalize('NFD',s)
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=re.sub(r'<([a-z]+)=([a-z]*)>',r'\1',s,flags=re.I)   # EDCS <corr=stone>: keep corrected
    s=re.sub(r'\{[^}]*\}','',s)                           # superfluous
    s=re.sub(r'\([^)]*\)','',s)                           # expansions
    s=re.sub(r'\(\(.*?\)\)','',s)
    s=s.replace('〈','').replace('〉','').replace('⌜','').replace('⌝','')
    s=re.sub(r'---|\[3\]|\[\d\]|\+',' ',s)
    s=re.sub(r'[\[\]/;|!?.,:·\-–—=<>\\]',' ',s)
    s=s.lower().replace('j','i').replace('u','v')
    return ' '.join(s.split())
SP='/tmp/claude-0/-home-user-alexis-angel-martini/fdf41730-a49c-58dc-81a0-9336a7868929/scratchpad'
T={r['n'].split('.')[0]:r['texte (Leyde, EDCS état source)'] for r in csv.DictReader(open('/home/user/alexis-angel-martini/01_donnees/base_v2_csv/Textes.csv'))}
targets=[l.split('\t') for l in open(SP+'/edh/noicur.tsv').read().strip().split('\n')]
rows=[r for r in csv.DictReader(open(SP+'/edb_rows.csv')) if not re.match(r'\d',r['icvr'])]
print('fiches EDB sans ICVR lues:',len(rows))
for n,aes,refs in targets:
    best=None
    for r in rows:
        bib=r['bib'].replace(',','').replace(' ','')
        hit=any(a and a.replace(',','').replace(' ','').replace('AE','AE').replace(', 0',',') in bib for a in [])
        aehit=False
        for a in aes.split('|'):
            m=re.match(r'AE (\d{4}), 0*(\d+)',a)
            if m and re.search(r'AE,?\s*%s,?\s*0*%s\b'%(m.group(1),m.group(2)),r['bib']): aehit=True
        s=difflib.SequenceMatcher(None,norm(T[n]),norm(r['text'])).ratio()
        sc=s+(1 if aehit else 0)
        if not best or sc>best[0]: best=(sc,aehit,s,r)
    if best and (best[1] or best[2]>0.7):
        r=best[3]; print(n,'| AE' if best[1] else '| txt',round(best[2],2),'EDB'+r['edb'],r['bib'][:60],'|',r['pert'][:35],'|',r['date'])
