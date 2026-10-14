import csv,re,difflib,sys,collections,unicodedata
SP=sys.argv[1]; OUT=sys.argv[2]
B='/home/user/alexis-angel-martini/01_donnees/base_v2_csv/'
N={int(float(r['n'])):r for r in csv.DictReader(open(B+'Notices.csv'))}
T={int(float(r['n'])):r for r in csv.DictReader(open(B+'Textes.csv'))}
E=collections.defaultdict(list)
for r in csv.DictReader(open(SP+'/edb_rows.csv')):
    m=re.match(r'(\d+)(.*)',r['icvr'])
    if m: E[int(m.group(1))].append(r)
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
NUMRE=re.compile(r'\b[IVXL]{1,7}\b')
EXTRA={r['n']:r for r in csv.DictReader(open(SP+'/mapping_extra.csv'))}
BYID={r['edb']:r for r in csv.DictReader(open(SP+'/edb_rows.csv'))}
out=[]
for n,r in sorted(N.items()):
    refs=r['ICUR / refs catalogue']+' '+r['publications EDCS']
    icur=sorted(set((int(v),int(k),s) for v,k,s in re.findall(r'ICUR-(\d\d), (\d+)([a-z]?)',refs)))
    t=T[n]['texte (Leyde, EDCS état source)']
    rec=dict(n=n,icur='; '.join(f'ICUR {v}, {k}{s}' for v,k,s in icur),edcs=r['EDCS-ID'],annee=r['annee_retenue'],edb_id='',edb_icvr='',edb_pert='',edb_cons='',edb_date='',edb_bib='',edb_text='',edcs_text=t,ratio='',statut='')
    if str(n) in EXTRA:
        cands=[BYID[EXTRA[str(n)]['edb']]]
    elif not icur: rec['statut']='sans numéro ICUR (non trouvé dans l\'EDB)'; out.append(rec); continue
    else: cands=[e for v,k,s in icur for e in E.get(k,[])]
    if not cands:
        rec['statut']='page EDB non encore consultée'; out.append(rec); continue
    best=max(cands,key=lambda e: difflib.SequenceMatcher(None,norm(t),norm(e['text'])).ratio())
    ratio=difflib.SequenceMatcher(None,norm(t),norm(best['text'])).ratio()
    rec.update(edb_id='EDB'+best['edb'],edb_icvr=best['icvr'],edb_pert=best['pert'],edb_cons=best['cons'],edb_date=best['date'],edb_bib=best['bib'],edb_text=best['text'],ratio=f'{ratio:.3f}')
    if not best['text'].strip(): rec['statut']='fiche EDB sans texte dans la liste (fiche détaillée à ouvrir)'
    elif ratio>=0.92: rec['statut']='concordant (écarts mineurs de notation)'
    elif ratio>=0.75: rec['statut']='écarts à examiner'
    else: rec['statut']='divergence forte ou appariement douteux'
    out.append(rec)
w=csv.DictWriter(open(OUT,'w',newline=''),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
c=collections.Counter(o['statut'] for o in out)
for k,v in c.most_common(): print(v,k)
