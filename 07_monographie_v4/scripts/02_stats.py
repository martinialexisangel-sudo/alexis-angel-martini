#!/usr/bin/env python3
"""PRISME v4.0 — calcul de toutes les mesures citées dans le volume.

Entrée : data/corpus_v4.json (01_build_data.py).
Sorties : data/stats.json (valeurs et listes) ; tex/generated/stats.tex (macros \\st{clé}).
Toute valeur chiffrée du texte courant provient de ce script.
"""
import json, os, re, sys, math, collections, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leiden as L

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
R = json.load(open(os.path.join(ROOT, 'data', 'corpus_v4.json'), encoding='utf-8'))
BYN = {r['n']: r for r in R}
S = collections.OrderedDict()      # valeurs scalaires (macros)
LST = collections.OrderedDict()    # listes et tableaux


def put(k, v):
    S[k] = v


def pct(a, b, d=1):
    return ('%.*f' % (d, 100.0 * a / b)).replace('.', ',') if b else '0'


def nlist(xs):
    return ', '.join(str(x) for x in sorted(xs))


A = R
B = [r for r in R if r['inB']]
C = [r for r in R if r['inC']]
C0 = [r for r in R if r['inC0_v35']]
put('nA', len(A)); put('nB', len(B)); put('nC', len(C)); put('nCzero', len(C0))
put('nD', len({tuple(sorted([r['n']] + r['joint'])) for r in B}) - 1)  # 313/314 = une unité
G = collections.Counter(r['genre'] for r in B)
put('nEpit', G['épitaphe']); put('nMixte', G['mixte (épitaphe et acte d’achat)'])
put('nActe', G['acte d’achat ou de réservation']); put('nNonfun', G['non funéraire (inscription architecturale)'])
LST['actes'] = [r['n'] for r in B if r['genre'].startswith('acte')]
LST['mixtes'] = [r['n'] for r in B if r['genre'].startswith('mixte')]
LST['grecs_C'] = [r['n'] for r in C if r['grec']]
put('acteslist', nlist(LST['actes'])); put('mixteslist', nlist(LST['mixtes']))
put('nGrecA', sum(r['grec'] for r in A)); put('nGrecC', len(LST['grecs_C']))

# ------------------------------------------------------------------ datation
D = collections.Counter(r['datation'] for r in C)
LST['datation_C'] = {k: sorted(r['n'] for r in C if r['datation'] == k) for k in D}
lvl = lambda k: sum(v for kk, v in D.items() if kk.startswith(k))
put('datLu', D['directe : nom consulaire lu']); put('datPartiel', D['directe : lecture partielle d’un nom consulaire'])
put('datInit', D['directe : initiales consulaires']); put('datRest', D['directe : consulat restitué'])
put('datEDB', lvl('formule transmise par l’EDB')); put('datConj', D['conjecturale']); put('datIndir', D['indirecte'])
put('datDirect', lvl('directe'))
DA = collections.Counter(r['datation'] for r in A)
put('datLuA', DA['directe : nom consulaire lu']); put('datPartielA', DA['directe : lecture partielle d’un nom consulaire'])
put('datInitA', DA['directe : initiales consulaires']); put('datRestA', DA['directe : consulat restitué'])
put('datDirectA', sum(v for k, v in DA.items() if k.startswith('directe')))
LST['contestees'] = sorted(r['n'] for r in A if r['contestee'])
LST['alertes'] = sorted(r['n'] for r in A if r['alerte'])
LST['edb_fautive'] = sorted(r['n'] for r in A if r['edb_fautive'])
put('nContest', len(LST['contestees'])); put('nAlertes', len(LST['alertes']))
LST['faux_consuls'] = sorted(r['n'] for r in A if r['faux_consuls'])
put('nFauxConsulsNotices', len(LST['faux_consuls'])); put('nFauxConsuls', sum(len(r['faux_consuls']) for r in A))

# années et périodes
PER = [(340, 359), (360, 374), (375, 389), (390, 403)]
PERL = ['340–359', '360–374', '375–389', '390–403']


def per(y):
    for i, (a, b) in enumerate(PER):
        if a <= y <= b:
            return i
    return None


perN = collections.Counter(per(r['annee']) for r in C)
for i in range(4):
    put('perC%d' % i, perN[i])
years = collections.Counter(r['annee'] for r in C)
LST['annees_C'] = {y: years.get(y, 0) for y in range(340, 404)}
put('partApres380', pct(sum(v for y, v in years.items() if y >= 380), len(C)))

# ------------------------------------------------------------------ formulaire
SEQ = {r['n']: L.letters(r['texte_leiden']) for r in R}
FORM = collections.OrderedDict([
    ('in pace', r'\bin\s+pace\b'),
    ('depositio / depositus', r'\bdepo?s+\w*'),
    ('vixit (et variantes)', r'\b(uix\w*|bix\w*|uiuit|uibit)\b'),
    ('bene merenti', r'\bbene\s*mere\w*'),
    ('fecit / fecerunt', r'\bfec(it|erunt|i)\b'),
    ('hic (iacet, positus, requiescit…)', r'\bhic\b'),
    ('requiescit / quiescit', r'\b(re)?quie(sc|u)\w*'),
    ('decessit / recessit / defunctus', r'\b(de|re)cess\w*|\bdefunct\w*'),
    ('dormitio / dormit', r'\bdorm\w*'),
    ('locus', r'\bloc(us|um|o|i)\b'),
    ('bisomus / trisomus / quadrisomus', r'\b(bi|tri|quadri)som\w*'),
    ('achat (emere, comparare)', r'\b(emit|emerunt|empt\w*|comparau\w*|comparat\w*|comparass\w*)\b'),
    ('fossor', r'\bfossor\w*'),
    ('coniux / compar / maritus / uxor', r'\b(coniu[gnx]\w*|compar(i|e|em)?|marit\w*|uxor\w*)\b'),
    ('virginius / virginia', r'\b[bu]irgini(us|a|o|um|ae)\b'),
    ('filius / filia', r'\bfili(us|a|o|ae|i|is|um|am|e)\b'),
    ('parentes / pater / mater', r'\b(parent\w*|pater|patri|patre|patris|patrem|mater|matri|matre|matris|matrem)\b'),
    ('dulcissimus / carissimus', r'\b(dulciss\w*|cariss\w*|kariss\w*)'),
    ('plus minus', r'\bplus\s+minus\b'),
    ('se vivo / se viva', r'\bse\s+[ub]i[ub]\w*'),
    ('post consulatum', r'\bpost\s+con\w*'),
])
form_rows = []
for lab, pat in FORM.items():
    tot, cons, byp, byp_c, ns_c, forms = 0, 0, collections.Counter(), collections.Counter(), [], collections.Counter()
    for r in C:
        occ = L.find(SEQ[r['n']], pat)
        if not occ:
            continue
        tot += 1; byp[per(r['annee'])] += 1
        for o in occ:
            forms[o['match']] += 1
        if any('R' not in o['statuts'] for o in occ):
            cons += 1; byp_c[per(r['annee'])] += 1; ns_c.append(r['n'])
    form_rows.append({'element': lab, 'regle': pat, 'avec': tot, 'sans': cons,
                      'par_periode': [byp_c[i] for i in range(4)], 'par_periode_avec': [byp[i] for i in range(4)],
                      'notices': ns_c, 'formes': forms.most_common(12)})
LST['formulaire'] = form_rows

# in pace : quatre catégories exclusives
def inpace(rows):
    cats = collections.defaultdict(list)
    for r in rows:
        occ = L.find(SEQ[r['n']], r'\bin\s+pace\b')
        if occ:
            cats[L.best(occ)].append(r['n'])
    return cats


IP = inpace(C); IP0 = inpace(C0)
for k in ('ecrit', 'abrege', 'corrige', 'restitue'):
    put('ip_' + k, len(IP[k])); put('ipz_' + k, len(IP0[k]))
put('ip_tot', sum(len(v) for v in IP.values())); put('ipz_tot', sum(len(v) for v in IP0.values()))
put('ip_sansrest', len(IP['ecrit']) + len(IP['abrege']) + len(IP['corrige']))
put('ip_pct', pct(S['ip_tot'], len(C))); put('ip_ecrit_pct', pct(len(IP['ecrit']), len(C)))
LST['inpace'] = {k: sorted(v) for k, v in IP.items()}
LST['inpace_C0'] = {k: sorted(v) for k, v in IP0.items()}

# ------------------------------------------------------------------ graphies et abréviations
corr = collections.Counter(); corr_n = collections.defaultdict(set); corr_per = collections.defaultdict(collections.Counter)
for r in A:
    for a, b in re.findall(r'<([^=>]*)=([^>]*)>', r['texte_leiden'] or ''):
        corr[(a, b)] += 1; corr_n[(a, b)].add(r['n']); corr_per[(a, b)][per(r['annee']) if r['annee'] else None] += 1
put('nCorrOcc', sum(corr.values())); put('nCorrNotices', len({n for s in corr_n.values() for n in s}))
PHEN = {('v', 'B'): 'bêtacisme', ('b', 'V'): 'bêtacisme', ('o', 'V'): 'confusion o/u', ('u', 'O'): 'confusion o/u',
        ('e', 'I'): 'confusion e/i', ('i', 'E'): 'confusion e/i', ('y', 'I'): 'graphie de y', ('y', 'V'): 'graphie de y',
        ('g', 'C'): 'c pour g', ('m', 'N'): 'n pour m', ('x', 'S'): 's pour x', ('a', 'E'): 'e pour a', ('c', 'Q'): 'q pour c',
        ('c', 'K'): 'k pour c', ('t', 'I'): 'i pour t (lecture)', ('ae', 'E'): 'monophtongaison'}
LST['graphies'] = [{'attendu': a, 'grave': b, 'occ': n, 'notices': sorted(corr_n[(a, b)]), 'phen': PHEN.get((a, b), ''),
                    'per': [corr_per[(a, b)][i] for i in range(4)]} for (a, b), n in corr.most_common()]

abbr = collections.Counter(); abbr_ex = collections.defaultdict(collections.Counter)
for r in A:
    for tok in re.split(r'[\s/]+', r['texte_leiden'] or ''):
        if '(' not in tok or '[' in tok or ']' in tok or re.search(r'\((!|\?)\)', tok):
            continue
        t = re.sub(r'<([^=>]*)=[^>]*>', r'\1', tok)
        t = re.sub(r'[{}]', '', t)
        ab = re.sub(r'\([^)]*\)', '', t).lower().strip('.,;:')
        ex = t.replace('(', '').replace(')', '').strip('.,;:')
        if ab and len(ab) <= 8 and ab != ex.lower():
            abbr[ab] += 1; abbr_ex[ab][t] += 1
LST['abreviations'] = [{'abrege': a, 'occ': n, 'exemple': abbr_ex[a].most_common(1)[0][0]} for a, n in abbr.most_common(45)]

# ------------------------------------------------------------------ âges (table des personnes, corrigée)
# Corrections de la table des personnes après contrôle sur le texte (v4) :
#  411 : viginti duo ; 400 : les 17 jours sont une date ; 133 (1) et 19 (2) ne sont pas des âges
#  (durée de mariage ; durée du séjour à Rome) ; 364 : seules les unités (et quinque) sont lues,
#  le 5 de la table est la durée du mariage restituée ; mois et jours de 53, 83, 184, 324, 365
#  appartiennent à la durée du mariage ou à la date.
AGE_FIX = {}  # corrections appliquées dans 01_build_data.py
persons = []
for r in C:
    for p in r['ages']:
        p = dict(p); key = (r['n'], int(float(p['rang dans le texte'])))
        if key in AGE_FIX and AGE_FIX[key] is None:
            continue
        p.update(AGE_FIX.get(key) or {})
        p['n'] = r['n']; persons.append(p)
put('nPersAge', len(persons))
yrs = [p for p in persons if p['années']]
put('nAgeAns', len(yrs)); put('nAgeMoisJours', len(persons) - len(yrs))
vals = [float(p['années']) for p in yrs]
lu = [float(p['années']) for p in yrs if p['certitude'] == 'lu']
put('nAgeAnsLu', len(lu))
put('ageMed', ('%.0f' % statistics.median(vals)))
put('ageMoy', ('%.1f' % statistics.mean(vals)).replace('.', ','))
put('ageMedLu', ('%.0f' % statistics.median(lu))); put('ageMoyLu', ('%.1f' % statistics.mean(lu)).replace('.', ','))
cls = collections.Counter(min(int(v // 10), 8) for v in vals)
LST['ages_classes'] = [cls[i] for i in range(9)]
def whipple(v):
    w = [x for x in v if 23 <= x <= 62]
    return (100.0 * sum(1 for x in w if x % 5 == 0) / (len(w) / 5.0), len(w)) if w else (0, 0)
wi, wn = whipple(vals); wl, wln = whipple(lu)
put('whipple', '%.0f' % wi); put('whippleN', wn); put('whippleLu', '%.0f' % wl); put('whippleLuN', wln)
term = collections.Counter(int(v) % 10 for v in vals if v >= 20)
LST['ages_terminaux'] = [term[i] for i in range(10)]; put('nAges20', sum(term.values()))
put('nPlusMinus', sum(1 for p in persons if p['plus minus'] == 'True'))
LST['multi_ages'] = sorted({p['n'] for p in persons if int(float(p['rang dans le texte'])) > 1})
put('multiageslist', nlist(LST['multi_ages']))

# vie conjugale
conj = []
for r in C:
    m = re.search(r'\b(fecit|uixit|fecerunt)\s+(cum\s+(marito|coniuge|uirginia|uirginio|compare|uxore|maritum)|mecum)\b|\bin\s+coniugio\b',
                  L.plain(SEQ[r['n']])[0])
    if m:
        conj.append(r['n'])
LST['vie_conjugale'] = conj; put('nVieConj', len(conj))

# ------------------------------------------------------------------ dates du jour
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
ev = collections.Counter(); first = {}
for r in C:
    for d in r['dates']:
        ev[d['événement (indice contextuel)']] += 1
        if d['date julienne'] and r['n'] not in first:
            first[r['n']] = d
put('nDatesConv', sum(1 for r in C for d in r['dates'] if d['date julienne']))
put('nTextesDate', len(first))
for k, v in ev.items():
    put('ev_' + {'déposition': 'depo', 'décès': 'deces', 'naissance': 'naiss', 'achat': 'achat', 'indéterminé': 'indet'}.get(k, 'x'), v)
mon = collections.Counter()
mon_lu = collections.Counter()
for n, d in first.items():
    m = d['date julienne'].split()
    mm = [x for x in m if x in MOIS]
    if mm:
        mon[MOIS.index(mm[0])] += 1
        if d['certitude'] == 'lu':
            mon_lu[MOIS.index(mm[0])] += 1
LST['mois'] = [mon[i] for i in range(12)]
tot = sum(mon.values()); L_ = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
exp = [tot * l / 365.25 for l in L_]
chi2 = sum((mon[i] - exp[i]) ** 2 / exp[i] for i in range(12))
put('chi2', ('%.2f' % chi2).replace('.', ',')); put('nMoisTot', tot)
# p-valeur (11 ddl) par la fonction gamma incomplète
def chi2_sf(x, k):
    a, xx = k / 2.0, x / 2.0
    # série pour la fonction gamma incomplète inférieure régularisée
    s, term, n = 0.0, 1.0 / a, 0
    while abs(term) > 1e-14 and n < 1000:
        s += term; n += 1; term *= xx / (a + n)
    P = s * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
    return 1 - P
put('chi2p', ('%.3f' % chi2_sf(chi2, 11)).replace('.', ','))
put('ete', pct(mon[6] + mon[7] + mon[8], tot))

# ------------------------------------------------------------------ EDB : collation, provenance, supports, signes
st = collections.Counter((r['edb_statut'] or 'non apparié') for r in A)
LST['edb_statut'] = st.most_common()
put('edbApp', sum(1 for r in A if r['edb_ids'])); put('edbXml', sum(1 for r in A if r['edb_xml']))
put('edbConc', sum(v for k, v in st.items() if k.startswith('concordant')))
put('edbExam', sum(v for k, v in st.items() if k.startswith('écarts')))
put('edbDiv', sum(v for k, v in st.items() if 'divergence' in k))
put('edbDoub', st.get('doublon (fusionné)', 0)); put('edbAbsent', st.get('absent de la liste publique EDB', 0))
put('edbSansIcur', sum(v for k, v in st.items() if k.startswith('sans numéro')))
put('edbConcRel', sum(1 for r in A if (r['edb_statut_v4'] or '').startswith('concordant après')))
put('edbConcTotC', sum(1 for r in C if (r['edb_statut_v4'] or '').startswith('concordant')))
matchedC = [r for r in C if r['edb_ids']]
put('edbAppC', len(matchedC))
put('edbXmlC', sum(1 for r in C if r['edb_xml']))


def cemetery(p):
    if not p:
        return None
    p = p.strip()
    rules = [('Incertae originis', 'origine incertaine'), ('Commodillae', 'Commodilla (via Ostiensis)'),
             ('Domitillae', 'Domitilla (via Ardeatina)'), ('Callist', 'Calliste (via Appia)'),
             ('Pontiani', 'Pontien (via Portuensis)'), ('S.Petri', 'Saint-Pierre (Vatican)'), ('S. Petri', 'Saint-Pierre (Vatican)'),
             ('Cyriacae', 'Cyriaque (via Tiburtina)'), ('Octavillae', 'Octavilla / Saint-Pancrace (via Aurelia)'),
             ('anonymum ad viam Appiam', 'cimetière anonyme de la via Appia'), ('anonymum ad viam Ardeatinam', 'cimetière anonyme de la via Ardeatina'),
             ('Catacumbas', 'Saint-Sébastien, ad Catacumbas (via Appia)'), ('Lucinae', 'aire de Lucine (via Appia)'),
             ('Pamphili', 'Pamphile (via Salaria vetus)'), ('paulianum', 'Saint-Paul (via Ostiensis)'), ('Pauli', 'Saint-Paul (via Ostiensis)'),
             ('Ostiensis', 'Saint-Paul (via Ostiensis)'),
             ('Cornelii', 'crypte de Corneille (Calliste)'), ('inter vias Appiam', 'entre via Appia et via Ardeatina'),
             ('Inter vias Appiam', 'entre via Appia et via Ardeatina')]
    for k, v in rules:
        if k in p:
            return v
    return 'autres cimetières (' + p + ')'


cem = collections.Counter(cemetery(r['edb_pertinence']) for r in C if r['edb_pertinence'])
LST['cimetieres_C'] = cem.most_common()
put('nOrigInc', cem.get('origine incertaine', 0)); put('nProvConnue', sum(v for k, v in cem.items() if k != 'origine incertaine'))
cons = collections.Counter()
for r in C:
    c = r['edb_conservation']
    if not c:
        continue
    if 'Vaticani' in c:
        k = 'Musées du Vatican'
    elif 'Capitolini' in c:
        k = 'Musées du Capitole'
    elif 'Nazionale' in c or 'Diocleziano' in c:
        k = 'Museo Nazionale Romano'
    elif 'Nerei' in c:
        k = 'basilique des Saints-Nérée-et-Achillée (Domitilla)'
    elif 'Callisti' in c:
        k = 'catacombe de Calliste'
    elif 'Commodillae' in c:
        k = 'catacombe de Commodilla'
    elif 'Teutonico' in c:
        k = 'Collegio Teutonico'
    elif 'Ostia' in c:
        k = 'Ostie, lapidaire'
    else:
        k = 'autres lieux (' + c + ')'
    cons[k] += 1
LST['conservation_C'] = cons.most_common(); put('nConsConnue', sum(cons.values()))

sup = collections.Counter(); mat = collections.Counter(); exe = collections.Counter(); dims = []; metr = []
fac = collections.Counter(); facn = 0
for r in C:
    if not r['edb_xml']:
        continue
    e = r['edb_xml'][0]
    sup[e['object'] or 'non précisé'] += 1; mat[e['material'] or 'non précisé'] += 1; exe[e['execution'] or 'non précisé'] += 1
    if e['dims'].get('height') and e['dims'].get('width'):
        dims.append(r['n'])
    if e['metrical']:
        metr.append(r['n'])
    if e['facsimile']:
        facn += 1
        for f in set(e['facsimile']):
            fac[f.split(',')[0]] += 1
LST['supports'] = sup.most_common(); LST['materiaux'] = mat.most_common(); LST['execution'] = exe.most_common()
put('nDims', len(dims)); put('nMetricalEDB', len(metr)); LST['metriques_edb'] = metr
put('nFacsim', facn); LST['facsimiles'] = fac.most_common()

# signes chrétiens (description EDB : champ décor des fiches EpiDoc ∪ mention dans le texte des listes)
signs = {}
for r in A:
    s = set()
    for e in r['edb_xml']:
        s.update(e['decoration'])
    if r['edb_signes']:
        for x in re.split(r'\s*;\s*', r['edb_signes']):
            x = x.strip()
            if not x:
                continue
            if 'monogramma Christi' in x and 'crucem' in x:
                s.add('croix monogrammatique')
            elif 'monogramma Christi' in x:
                s.add('chrisme')
            elif 'crux' in x or 'cross' in x:
                s.add('croix')
            elif 'Alpha' in x or 'alpha' in x:
                s.add('alpha et oméga')
    if s:
        signs[r['n']] = sorted(s)
LST['signes'] = signs
signC = [n for n in signs if BYN[n]['inC']]
put('nSignesA', len(signs)); put('nSignesC', len(signC)); put('pSignesC', pct(len(signC), S['edbAppC']))
sp = collections.Counter(per(BYN[n]['annee']) for n in signC)
spd = collections.Counter(per(r['annee']) for r in matchedC)
LST['signes_periode'] = [(PERL[i], sp[i], spd[i]) for i in range(4)]
typ = collections.Counter()
for n in signC:
    for t in signs[n]:
        typ[t] += 1
LST['signes_types'] = typ.most_common()

# dimensions des plaques ; signes et in pace
HH, WW = [], []
for r in C:
    if r['edb_xml'] and r['edb_xml'][0]['object'] == 'plaque':
        d = r['edb_xml'][0]['dims']
        if d.get('height') and d.get('width'):
            HH.append(float(d['height'].replace(',', '.'))); WW.append(float(d['width'].replace(',', '.')))
put('nPlaquesMes', len(HH)); put('medH', ('%g' % statistics.median(HH)).replace('.', ',')); put('medW', ('%g' % statistics.median(WW)).replace('.', ','))
put('maxW', ('%g' % max(WW)).replace('.', ',')); put('minW', ('%g' % min(WW)).replace('.', ','))
LST['sarcophages'] = sorted(r['n'] for r in C if r['edb_xml'] and r['edb_xml'][0]['object'] == 'sarcophage')
LST['mortier'] = sorted(r['n'] for r in C if r['edb_xml'] and r['edb_xml'][0]['execution'] == 'tracée dans le mortier frais')
LST['peintes'] = sorted(r['n'] for r in C if r['edb_xml'] and r['edb_xml'][0]['execution'] == 'peinte')
put('sarcolist', nlist(LST['sarcophages'])); put('mortierlist', nlist(LST['mortier'])); put('peinteslist', nlist(LST['peintes']))
put('nSarco', len(LST['sarcophages'])); put('nMortier', len(LST['mortier']))
ipS = sum(1 for r in matchedC if r['n'] in signs and L.find(SEQ[r['n']], r'\bin\s+pace\b'))
ipN = sum(1 for r in matchedC if r['n'] not in signs and L.find(SEQ[r['n']], r'\bin\s+pace\b'))
nS = sum(1 for r in matchedC if r['n'] in signs); nN = len(matchedC) - nS
put('ipSigne', '%d/%d (%s %%)' % (ipS, nS, pct(ipS, nS))); put('ipSansSigne', '%d/%d (%s %%)' % (ipN, nN, pct(ipN, nN)))
put('metrlist', nlist(LST['metriques_edb']))

# ------------------------------------------------------------------ vocabulaire religieux (scénarios v4)
PROFIL_LARGE = [73, 85, 140, 151, 214, 232, 249, 306, 311, 400, 458, 474, 475]
RESTRICTIF = [x for x in PROFIL_LARGE if x not in (232, 249)]
MONOGR = [x for x in (140, 151, 311) if x in signs]
STRICT = [x for x in RESTRICTIF if x not in MONOGR]
RESTITUES = [43, 104, 352, 382, 447]
LST['profil_large'] = PROFIL_LARGE; LST['profil_restrictif'] = RESTRICTIF; LST['profil_strict'] = STRICT
LST['monogrammes_lexicaux'] = MONOGR; LST['profil_restitues'] = RESTITUES
put('nProfilLarge', len(PROFIL_LARGE)); put('nProfilRestr', len(RESTRICTIF)); put('nProfilStrict', len(STRICT))
put('nProfilAvecRest', len(PROFIL_LARGE) + len(RESTITUES))
put('pProfilLarge', pct(len(PROFIL_LARGE), len(C))); put('pProfilRestr', pct(len(RESTRICTIF), len(C))); put('pProfilStrict', pct(len(STRICT), len(C)))
for n in PROFIL_LARGE + RESTITUES:
    assert BYN[n]['inC'], n
tr = collections.Counter(); trn = collections.defaultdict(set)
for r in C:
    for t in r['termes']:
        tr[t['emploi']] += 1; trn[t['emploi']].add(r['n'])
LST['termes_emploi'] = [(k, v, len(trn[k])) for k, v in tr.most_common()]

# ------------------------------------------------------------------ restitution
rr = [(r['ratio_restitue'] or 0.0) for r in C]   # part déclarée par la base v2.0
put('nPlusMoitie', sum(1 for x in rr if x > 0.5)); put('nZeroRest', sum(1 for x in rr if x == 0))
LST['classes_restit'] = [sum(1 for x in rr if x == 0), sum(1 for x in rr if 0 < x < .25), sum(1 for x in rr if .25 <= x < .5),
                         sum(1 for x in rr if .5 <= x < .75), sum(1 for x in rr if x >= .75)]

# ------------------------------------------------------------------ ICUR (premier volume cité)
def icur_vol(r):
    m = re.search(r'ICUR n\.s\. ([IVX]+)', r['refs'] or '')
    return m.group(1) if m else 'sans ICUR'
iv = collections.Counter(icur_vol(r) for r in C)
LST['icur_vol_C'] = iv.most_common()
put('nVolI', iv.get('I', 0))

# ------------------------------------------------------------------ sensibilité in pace
def frac(rows):
    k = sum(1 for r in rows if L.find(SEQ[r['n']], r'\bin\s+pace\b'))
    return k, len(rows)
k1, n1 = frac(C); C_no406 = [r for r in C if r['n'] != 406]; k2, n2 = frac(C_no406)
put('sens406', '%d/%d (%s %%)' % (k2, n2, pct(k2, n2)))
put('sensC', '%d/%d (%s %%)' % (k1, n1, pct(k1, n1)))
Cdirect = [r for r in C if r['datation'].startswith('directe') or r['datation'].startswith('formule')]
k3, n3 = frac(Cdirect); put('sensDirect', '%d/%d (%s %%)' % (k3, n3, pct(k3, n3))); put('nCdirect', n3)
Cstab = [r for r in C if (r['edb_statut_v4'] or '').startswith('concordant')]
k4, n4 = frac(Cstab); put('sensStab', '%d/%d (%s %%)' % (k4, n4, pct(k4, n4))); put('nCstab', n4)


def wilson(k, n, z=1.96):
    if not n:
        return (0, 0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d * 100, (c + h) / d * 100)


meas = []
def addm(lab, test):
    for nm, rows in (('C', C), ('C, datation directe ou transmise', Cdirect), ('C, lecture concordante EDCS/EDB', Cstab)):
        k = sum(1 for r in rows if test(r)); n = len(rows); lo, hi = wilson(k, n)
        meas.append((lab, nm, n, k, pct(k, n), ('%.1f–%.1f' % (lo, hi)).replace('.', ',')))
addm('in pace (attestée)', lambda r: bool(L.find(SEQ[r['n']], r'\bin\s+pace\b')))
addm('in pace (en toutes lettres)', lambda r: r['n'] in IP['ecrit'])
addm('Profil religieux large (niv. 1–2)', lambda r: r['n'] in PROFIL_LARGE)
addm('Profil religieux strict', lambda r: r['n'] in STRICT)
addm('Chrisme ou croix (EDB)', lambda r: r['n'] in signs)
addm('Texte grec ou bilingue', lambda r: r['grec'])
addm('Âge indiqué', lambda r: bool(r['ages']))
addm('Plus de la moitié des lettres restituées', lambda r: (r['ratio_restitue'] or 0) > .5)
LST['mesures'] = meas

# ------------------------------------------------------------------ sorties
json.dump({'S': S, 'L': LST}, open(os.path.join(ROOT, 'data', 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
os.makedirs(os.path.join(ROOT, 'tex', 'generated'), exist_ok=True)
with open(os.path.join(ROOT, 'tex', 'generated', 'stats.tex'), 'w', encoding='utf-8') as f:
    f.write('%% généré par scripts/02_stats.py — ne pas modifier\n')
    for k, v in S.items():
        f.write('\\expandafter\\def\\csname st@%s\\endcsname{%s}\n' % (k, str(v).replace('%', '\\%')))
for k, v in S.items():
    print(k, '=', v)
