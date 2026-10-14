"""Pour chaque notice datée « directe », détermine si les noms consulaires identifiés
sont lus (hors crochets) ou restitués (entre crochets) dans le texte EDCS (Leyde)."""
import csv,re,sys,unicodedata
B=sys.argv[1]; OUT=sys.argv[2]
T={r['n'].split('.')[0]:r['texte (Leyde, EDCS état source)'] for r in csv.DictReader(open(B+'/Textes.csv'))}
N={r['n'].split('.')[0]:r for r in csv.DictReader(open(B+'/Notices.csv'))}
# radicaux distinctifs (latin ; grec translittéré pour quelques cas)
ST={'Acindynus':['cind','kind'],'Proculus':['procul'],'Dagalaifus':['dagal'],'Gratianus':['gratian'],'Valentinianus':['valentin','balentin'],'Valens':['valent','balent'],'Theodosius':['theodos','teodos','θεοδοσ'],'Arcadius':['arcad','arkad'],'Honorius':['honor','onori'],'Stilicho':['stilic','stelic','stilich','istilic'],'Timasius':['timas'],'Promotus':['promot'],'Tatianus':['tatian'],'Symmachus':['symma','summa','simma'],'Merobaudes':['meroba','moerop','meropa'],'Saturninus':['saturnin'],'Eucherius':['eucher','euceri','euter'],'Syagrius':['syagri','suagri','siagri','sygari'],'Richomeres':['ricome','recem','richome'],'Clearchus':['clearc','clearch','clarc'],'Lupicinus':['lupicin','λουππικ'],'Iovinus':['iovin','iobin','ἰοβιν'],'Decentius':['decent'],'Paulus':['paul'],'Constantius':['constant','constat'],'Constans':['constan'],'Iulianus':['iulian'],'Sallustius':['sallust'],'Eusebius':['euseb','εὐσεβ'],'Hypatius':['ypat','hypat'],'Rufinus':['rufin','ῥουφιν'],'Probinus':['probin'],'Olybrius':['olybr','olibr','lybr'],'Caesarius':['caesar','cesar'],'Atticus':['attic','atic'],'Eutropius':['eutrop'],'Neoterius':['neoter','neuter'],'Rumoridus':['rumor','rimor','romodor'],'Vincentius':['vincent'],'Fravitta':['fravit','fraudit'],'Mamertinus':['mamert','mamer'],'Nevitta':['nevit','nebit','nevet'],'Arinthaeus':['arinth'],'Modestus':['modest'],'Ausonius':['auson'],'Olybrius ':['olybr'],'Equitius':['equit'],'Bauto':['baut','baud'],'Euodius':['euod','evod'],'Cynegius':['cyneg','cineg'],'Philippus':['philip','filip'],'Salia':['salia','sallia'],'Limenius':['limen'],'Catullinus':['catul'],'Amantius':['amant'],'Albinus':['albin'],'Placidus':['placid'],'Romulus':['romul','ῥωμουλ'],'Datianus':['datian'],'Cerealis':['cereal','ceriale','caereal'],'Gallus':['gall'],'Antonius':['anton'],'Eutychianus':['eutych','eutic','euthyc','eutyc'],'Magnentius':['magnent','mvannent'],'Marcellinus':['marcellin'],'Volusianus':['volusian'],'Lollianus':['lollian'],'Arbitio':['arbit','arb'],'Taurus':['taur'],'Florentius':['florent'],'Severinus':['severin'],'Maximus':['maxim'],'Aequitius':['aequit'],'Probus':['prob'],'Eugenius':['eugen','εὐγεν'],'Iovianus':['iovian','iobian','ἰοβιαν'],'Varronianus':['varron','barron','οὐαρρων'],'Arintheus':['arinth','arint'],'Theodorus':['theodor','teodor','θεοδωρ'],'Magnus Maximus':['maxim'],'Leontius':['leont','λεοντ'],'Nicomachus Flavianus':['flavian','nicomach'],'Victor':['victor','bictor','βικτωρ'],'Nigrinianus':['nigrin'],'Sergius':['sergi'],'Abundantius':['abundant'],'Anicii':['anic','olybr','probin']}
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); return ''.join(c for c in s if unicodedata.category(c)!='Mn')
def state_chars(t):
    """liste (char, état) : 0 = lu sur la pierre, 1 = restitué [ ], 2 = développement d'abréviation ( ).
    Un ']' initial sans '[' préalable met le début du texte en état restitué."""
    first_open=t.find('['); first_close=t.find(']')
    rest = first_close!=-1 and (first_open==-1 or first_close<first_open)
    par=0; out=[]
    for ch in t:
        if ch=='[': rest=True; continue
        if ch==']': rest=False; continue
        if ch=='(': par+=1; continue
        if ch==')': par=max(0,par-1); continue
        out.append((ch,1 if rest else (2 if par else 0)))
    return out
def clean(t):
    t=re.sub(r'<([^=<>]*)=([^<>]*)>',r'\1',t)      # <corr=stone> -> corr
    t=re.sub(r'\{[^}]*\}','',t)
    t=re.sub(r'(?<=\S)/(?=\S)','',t)              # coupure de mot en fin de ligne (« cu/m ») : supprimée
    return t
import os
OVR={}
ovp=os.path.join(os.path.dirname(OUT),'consuls_revue_manuelle.csv')
if os.path.exists(ovp):
    OVR={r['n']:r for r in csv.DictReader(open(ovp))}
NIV={'A':'A. au moins un nom consulaire lu','B':'B. lecture partielle (≥ 3 lettres gravées d\'un nom)','C':'C. noms abrégés (initiales ou sigles gravés)','R':'R. noms restitués (≤ 2 lettres gravées par nom)','D':'D. indéterminé'}
def word_read(txt,flags,a,b):
    while a>0 and txt[a-1].isalpha(): a-=1
    while b<len(txt) and txt[b].isalpha(): b+=1
    return sum(1 for i in range(a,b) if txt[i].isalpha() and flags[i]==0)
# noms de la liste v2.0 qui ne sont pas des consuls (défunts, dédicants…) : relevé manuel, exclus du calcul
FP=set()
fpp=os.path.join(os.path.dirname(OUT),'consuls_faux_positifs_v2.csv')
if os.path.exists(fpp):
    FP={(r['n'],r['nom_liste_v2']) for r in csv.DictReader(open(fpp))}
rows=[]
for k,r in N.items():
    if not r['datation_mode'].startswith('directe'): continue
    names=[re.sub(r'\s*\(.*|\s+\d+$','',x).strip() for x in r['consuls_identifies'].split(';') if x.strip()]
    names=[x for x in names if (k,x) not in FP]
    if not names: continue
    sc=state_chars(clean(T.get(k,'')))
    txt=''.join((norm(c)[:1] or ' ') for c,_ in sc); flags=[f for _,f in sc]
    res=[]
    for nm in names:
        stems=ST.get(nm)
        if not stems: res.append((nm,'?',0)); continue
        best=None
        for st in stems:
            st=norm(st)
            for m in re.finditer(re.escape(st),txt):
                w=word_read(txt,flags,m.start(),m.end())
                full=all(f!=1 for f in flags[m.start():m.end()]) and w>=3   # aucune lettre restituée, ≥ 3 lettres gravées
                key=(0 if full else 1,-w)
                if best is None or key<best[0]: best=(key,'lu' if full else ('partiel' if w>=3 else 'restitué'),w)
        if best is None: res.append((nm,'absent/abrégé',0))
        else: res.append((nm,best[1],best[2]))
    # noms consulaires du lexique lus en entier mais absents de la liste v2.0 (ex. n° 53) — à contrôler à la main
    for nm2,stems in (ST.items() if not any(c=='lu' for _,c,_ in res) else []):
        nm2=nm2.strip()
        if nm2 in names or any(x[0]==nm2 for x in res) or (k,nm2) in FP: continue
        for st in stems:
            st=norm(st)
            if len(st)<5: continue
            if any(all(f==0 for f in flags[m.start():m.end()]) for m in re.finditer(re.escape(st),txt)):
                res.append((nm2,'lu (hors liste v2.0, à contrôler)',0)); break
    cl=[c for _,c,_ in res]
    if any(c.startswith('lu') for c in cl): auto='A'
    elif 'partiel' in cl: auto='B'
    elif cl and all(c=='restitué' for c in cl): auto='R'
    else: auto='D'
    o=OVR.get(k)
    fin=o['niveau_revu'] if o else auto
    rows.append(dict(n=int(k),annee=r['annee_retenue'],
        consuls='; '.join(f'{a}:{b}'+(f' [{w} l. lues]' if b in('partiel','restitué') else '') for a,b,w in res),
        niveau_auto=NIV[auto],niveau_final=NIV[fin],revu_main='oui' if o else 'non',
        justification=o['justification'] if o else '',mode_v2=r['datation_mode'],texte=T.get(k,'')))
rows.sort(key=lambda x:x['n'])
w=csv.DictWriter(open(OUT,'w',newline=''),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
print('auto ',sorted(collections.Counter(r['niveau_auto'][0] for r in rows).items()))
print('revus',sum(r['revu_main']=='oui' for r in rows))
print('final',sorted(collections.Counter(r['niveau_final'][0] for r in rows).items()))
for r in rows:
    if (r['niveau_auto'][0] not in 'AB' or 'hors liste' in r['consuls']) and r['revu_main']=='non':
        print('A REVOIR',r['n'],r['annee'],r['niveau_auto'][:2],'|',r['consuls'],'|',r['texte'][-140:])
