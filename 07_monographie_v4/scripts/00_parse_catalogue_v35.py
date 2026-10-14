import re, json, sys
W='/tmp/claude-0/-home-claude/d911377c-55ff-5098-8431-9cdd9150e21e/scratchpad/w/'
raw=open(W+'cat_raw.txt',encoding='utf-8').read()
lines=raw.split('\n')
clean=[]
for l in lines:
    s=l.strip()
    if s.startswith('Alexis Angel Martini · Version 3.5'): continue
    if s.startswith('PRISME · Épitaphes chrétiennes'): continue
    if re.fullmatch(r'\d{1,3}',s) and False: pass
    clean.append(l.rstrip())
# remove form feeds / page numbers: lines that are only digits and preceded by footer removal -> detect pattern '\x0c'
txt='\n'.join(clean).replace('\x0c','\n')
FIELDS=['NUMÉRO ET IDENTIFIANT','DATATION ET CERTITUDE','IDENTIFICATION',"RÉFÉRENCES D’ÉDITION",'PROVENANCE','DESCRIPTION MATÉRIELLE','TEXTE TRANSMIS','VARIANTES ET RESTITUTIONS','APPARAT','TRADUCTION DE TRAVAIL','COMMENTAIRE LINGUISTIQUE','COMMENTAIRE CHRONOLOGIQUE','COMMENTAIRE HISTORIQUE ET THÉOLOGIQUE','CONCORDANCES','PHOTOGRAPHIES ET DROITS','BIBLIOGRAPHIE PROPRE','NOTE DE CONTRÔLE']
# split into notices at "1. NUMÉRO ET IDENTIFIANT"
parts=re.split(r'\n1\. NUMÉRO ET IDENTIFIANT\n',txt)
pre=parts[0]
notices=[]
for i,p in enumerate(parts[1:]):
    d={}
    # field boundaries
    pat=r'\n(\d{1,2})\. ('+'|'.join(re.escape(f) for f in FIELDS[1:])+r')[^\n]*\n'
    segs=re.split(pat,'\n'+p)
    d['f1']=segs[0]
    k=1
    while k<len(segs):
        num=int(segs[k]); body=segs[k+2]; d['f%d'%num]=body; k+=3
    notices.append(d)
def strip_tail(s):
    # remove trailing running header of next notice e.g. "\n\n2\nANNÉE RETENUE 340\n\nEDCS-... · ICUR..."
    s=re.sub(r'\n\s*\d{1,3}\s*\n\s*ANNÉE RETENUE[^\n]*\n.*$','',s,flags=re.S)
    s=re.sub(r'\n\s*\d{1,3}\s*ANNÉE RETENUE[^\n]*\n.*$','',s,flags=re.S)
    return s
def clean_prose(s):
    s=strip_tail(s)
    ls=[x.strip() for x in s.split('\n')]
    ls=[x for x in ls if x and not re.fullmatch(r'\d{1,3}',x)]
    out=''
    for x in ls:
        if out.endswith('-') and x and (x[0].islower()):
            out=out[:-1]+x
        else:
            out=(out+' '+x) if out else x
    return out.strip()
res=[]
for d in notices:
    r={}
    m=re.search(r'N° (\d+)',d['f1']); r['n']=int(m.group(1))
    for k in range(1,18):
        v=d.get('f%d'%k,'')
        if k==7:
            v=strip_tail(v)
            ls=[x.rstrip() for x in v.split('\n') if x.strip() and not re.fullmatch(r'\s*\d{1,3}\s*',x)]
            # join wrapped text lines (lines not starting with a line number)
            tl=[]
            for x in ls:
                mm=re.match(r'^\s*(\d{1,2}) (.*)$',x)
                if mm and (not tl or int(mm.group(1))==len(tl)+1):
                    tl.append(mm.group(2))
                elif tl:
                    tl[-1]=(tl[-1][:-1]+x.strip()) if tl[-1].endswith('-') else tl[-1]+' '+x.strip()
                else:
                    tl.append(x.strip())
            r['f7']=tl
        else:
            r['f%d'%k]=clean_prose(v)
    res.append(r)
# header line before each notice: "EDCS-xxx · ICUR..." captured at end of previous; fine
print(len(res), [r['n'] for r in res][:5], sorted(set(range(1,479))-set(r['n'] for r in res)))
json.dump(res,open(W+'notices_v35.json','w'),ensure_ascii=False,indent=1)
