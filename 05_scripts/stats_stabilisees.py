"""Statistiques recalculées sur les seules lectures stabilisées (lot 2)."""
import csv,collections,re,sys
B=sys.argv[1]; C=sys.argv[2]
N={int(float(r['n'])):r for r in csv.DictReader(open(B+'/Notices.csv'))}
COL={int(r['n']):r for r in csv.DictReader(open(C))}
doublons={106:120,282:288,329:336,394:393}          # fusion proposée (dossiers § A)
unite_unique=[(393,394)]                     # un seul monument, une seule occurrence datée
textes=[n for n in N if n not in doublons]
print('notices',len(N),'| textes distincts après fusion des doublons',len(textes))
stab=[n for n in textes if COL[n]['statut'].startswith('concordant')]
print('lectures stabilisées (EDCS = EDB aux conventions près)',len(stab))
annees=collections.Counter()
for n in stab:
    if n==394: continue
    a=int(float(N[n]['annee_retenue'])); annees[(a//10)*10]+=1
print('répartition par décennie (lectures stabilisées, 393/394 comptés une fois) :',dict(sorted(annees.items())))
ip=sum(1 for n in stab if re.search(r'\bin pace',COL[n]['edb_text'],re.I) and '[in pace' not in COL[n]['edb_text'])
print('in pace lu dans le texte EDB (lectures stabilisées) :',ip,'/',len(stab))
chr_=sum(1 for n in stab if re.search(r'\(\((monogramma Christi|crux)',COL[n]['edb_text']))
print('chrisme ou croix (EDB, lectures stabilisées) :',chr_,'/',len(stab))
