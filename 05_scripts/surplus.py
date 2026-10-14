import csv,re,sys,unicodedata
sys.path.insert(0,sys.argv[1])
SP=sys.argv[1]
def norm(s):
    s=s.replace('**More**','')
    s=re.sub(r'\(\([^)]*\)\)',' ',s)
    s=unicodedata.normalize('NFD',s); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=re.sub(r'<([a-z]+)=([a-z]*)>',r'\1',s,flags=re.I); s=re.sub(r'\{[^}]*\}','',s); s=re.sub(r'\([^)]*\)','',s)
    s=re.sub(r'[〈〉⌜⌝`´\[\]/;|!?.,:·\-–—=<>\\+%0-9]',' ',s)
    return s.lower().replace('j','i').replace('u','v').split()
C=list(csv.DictReader(open(SP+'/collation_edcs_edb.csv')))
res=[]
for r in C:
    if not r['edb_text']: continue
    E=norm(r['edb_text']); D=set(norm(r['edcs_text']))
    extra=[w for w in E if len(w)>=4 and w not in D]
    if len(extra)>=2: res.append((int(r['n']),' '.join(extra)))
w=csv.writer(open(SP+'/surplus_edb.csv','w',newline='')); w.writerow(['n','mots EDB absents du texte EDCS (normalisés, ≥4 lettres)']); w.writerows(res)
print(len(res))
for x in res: print(x[0],'|',x[1][:150])
