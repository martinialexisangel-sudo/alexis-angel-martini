#!/usr/bin/env python3
"""PRISME v4.0 — consolidation des données.

Réunit, notice par notice :
  * le catalogue v3.5 (17 champs, extrait du PDF : data/notices_v35.json) ;
  * la base scientifique v2.0 (01_donnees/base_v2_csv) ;
  * la collation EDCS/EDB, lots 1-5 (06_livrables/PRISME_collation_EDCS_EDB.xlsx) ;
  * les fiches EpiDoc de l'Epigraphic Database Bari, état Zenodo 2019
    (DOI 10.5281/zenodo.3575485 ; data/edb_xml).

Produit data/corpus_v4.json : une entrée par notice (1-478), avec les décisions
éditoriales de la version 4.0 et leur justification.
"""
import csv, json, re, os, sys, collections
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..'))
DATA = os.path.join(ROOT, 'data')


def num(x):
    try:
        return int(float(x))
    except Exception:
        return None


def read_csv(name):
    with open(os.path.join(REPO, '01_donnees', 'base_v2_csv', name + '.csv'), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def by_n(rows, key='n'):
    d = collections.defaultdict(list)
    for r in rows:
        n = num(r[key])
        if n:
            d[n].append(r)
    return d


# ---------------------------------------------------------------- sources
v35 = {r['n']: r for r in json.load(open(os.path.join(DATA, 'notices_v35.json'), encoding='utf-8'))}
NOT = {num(r['n']): r for r in read_csv('Notices')}
TXT = {num(r['n']): r for r in read_csv('Textes')}
AGES = by_n(read_csv('Personnes_ages'))
DATES = by_n(read_csv('Dates'))
TERMS = by_n(read_csv('Termes_religieux'))
CONS = by_n(read_csv('Consuls'))
REFS = by_n(read_csv('References_editions'))

wb = openpyxl.load_workbook(os.path.join(REPO, '06_livrables', 'PRISME_collation_EDCS_EDB.xlsx'), read_only=True)


def sheet(name):
    rows = list(wb[name].iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:] if any(c is not None for c in r)]


COLL = {num(r['N°']): r for r in sheet('Collation')}
CHRI = {num(r['N°']): r for r in sheet('Chrismes_croix')}
DIVD = {num(r['N°']): r for r in sheet('Divergences_dates')}
DIVF = {num(r['n']): r for r in sheet('Divergences_fortes')}
LVL = {num(r['N°']): r for r in sheet('Consuls_lus_restitues')}
FAUX = collections.defaultdict(list)
for r in sheet('Faux_consuls_v2'):
    FAUX[num(r['n'])].append(r)

# ---------------------------------------------------------------- EDB EpiDoc
OBJ = {'Tafel': 'plaque', 'Sarkophag': 'sarcophage', 'arenatum': 'enduit de mortier', 'Mur': 'paroi',
       'Ziegel': 'brique', 'ignoratur': None}
MAT = {'Marmor': 'marbre', 'arenatum': 'mortier', 'tectorium': 'enduit', 'opus latericium': 'maçonnerie de briques',
       'ignoratur': None}
EXE = {'Insculptus': 'gravée', 'Exaratus': 'tracée dans le mortier frais', 'Pictus': 'peinte',
       'Scariphatus': 'graffitée', 'ignoratur': None}
DEC = {'chi-rho': 'chrisme', 'Monogr. Christi cum Alpha et Omega': 'chrisme avec alpha et oméga',
       'Monogr. Christi in crucem translatum': 'croix monogrammatique',
       'Monogr. Christi in crucem transl. cum Alpha et Omega': 'croix monogrammatique avec alpha et oméga',
       'cross': 'croix', 'Crux Gammata': 'croix gammée', 'Alpha et Omega': 'alpha et oméga',
       'Monogr. Christi radiatum': 'chrisme radié'}


def parse_edb(eid):
    p = os.path.join(DATA, 'edb_xml', eid + '.xml')
    if not os.path.exists(p):
        return None
    s = open(p, encoding='utf-8').read()
    g = lambda pat: (re.search(pat, s, re.S).group(1).strip() if re.search(pat, s, re.S) else None)
    d = {'id': eid}
    d['title'] = g(r'<title>(.*?)</title>')
    d['object'] = OBJ.get(g(r'<objectType[^>]*>([^<]*)<'), g(r'<objectType[^>]*>([^<]*)<'))
    d['material'] = MAT.get(g(r'<material[^>]*>([^<]*)<'), g(r'<material[^>]*>([^<]*)<'))
    dims = {}
    for k in ('height', 'width', 'depth'):
        v = g(r'<%s>([^<]+)</%s>' % (k, k))
        if v:
            dims[k] = v.replace('.', ',')
    d['dims'] = dims
    d['decoration'] = [DEC.get(v, v) for v in re.findall(r'<rs [^>]*type="decoration"[^>]*>([^<]*)<', s)]
    d['execution'] = EXE.get(g(r'<rs [^>]*type="execution"[^>]*>([^<]*)<'), None)
    d['metrical'] = g(r'<rs type="metre">([^<]*)<') == 'Metrical'
    d['date'] = g(r'<origDate[^>]*>([^<]*)<')
    d['editors'] = sorted(set(w for _, w in re.findall(r'<change when="([^"]*)" who="([^"]*)"', s)))
    d['first_version'] = g(r'<change when="([^"]*)"')
    d['bibl'] = re.findall(r'<bibl>([^<]*)</bibl>', s)
    d['facsimile'] = []
    for n, url in re.findall(r'<graphic n="([^"]*)" url="([^"]*)"', s):
        if 'PCAS' in url:
            src = 'photographie PCAS'
        elif '/IC I/' in url:
            src = 'dessin, ICVR I (de Rossi)'
        else:
            m = re.search(r'/images/[^/]+/images/[^/]+/([^/]+)/', url)
            src = ('reproduction, ' + m.group(1)) if m else 'reproduction'
        d['facsimile'].append(src)
    d['text'] = g(r'<!--(.*?)-->')
    d['notes'] = re.findall(r'<note[^>]*>(.*?)</note>', s, re.S)
    return d


# ---------------------------------------------------------------- décisions v4
# Corrections de la table des personnes (v4), contrôlées sur le texte transmis :
#  411 : viginti duo ; 400 : les 17 jours sont une date ; 133 (1) et 19 (2) ne sont pas des âges
#  (durée du mariage ; durée du séjour à Rome) ; 364 : seules les unités (et quinque) sont lues,
#  le 5 de la table est la durée restituée du mariage ; les mois et jours de 53, 83, 184, 324, 365
#  appartiennent à la durée du mariage ou à la date.
AGE_FIX = {(411, 1): {'années': '22.0'}, (400, 1): {'jours': ''}, (133, 1): None, (19, 2): None,
           (364, 1): {'années': ''}, (53, 1): {'mois': ''}, (83, 1): {'mois': '', 'jours': ''},
           (184, 1): {'mois': '', 'jours': ''}, (324, 1): {'mois': '', 'jours': ''}, (365, 1): {'mois': ''}}
FUSION = {106: 120, 282: 288, 329: 336}          # notice absorbée -> notice de référence
JOINT = {394: 393}                               # second fragment d'un même texte
HORS_PERIODE = {98}                              # Severinus lu : 461 ou 482
UNITE_DEUX_TEXTES = {(313, 314)}
GENRE_V4 = {406: 'mixte (épitaphe et acte d’achat)'}   # quievit : décès explicitement mentionné
PROV_DOUTEUSE = {439: 'provenance non établie ; Tibur probable d’après CIL XIV 3896 = InscrIt IV 1, 543 ; '
                      'exclue des analyses topographiques propres à Rome'}

# notices dont la formule consulaire, absente du texte EDCS, est transmise par l'EDB
EDB_FORMULE = {
    84: ('lue', '[di]v̲o Ioviano et Fl(avio) Barronian`o c(on)s(ule)´'),
    214: ('lue', 'dd(ominis) nn(ostris) Gratiano V et Teodosio aaugg(ustis)'),
    268: ('lue', 'VII k(alendas) iul(ias) Ricomere et Clearcho cons(ulibu)s'),
    388: ('lue', 'dd(ominis) n̅n(ostris) / Arcadio Au̅g(usto) quater et Hono/rio Au̅g(usto) ter consulibus'),
    51: ('partiellement restituée', '[--- Datiano et C]aereale [consulibus? ---]'),
    180: ('partiellement restituée', 'post c[onsulatum ---] / [--- et] Fl(avii) Aequ[itii ---]'),
    447: ('partiellement restituée', '[ὑπατίᾳ Βινκεντί]ου καὶ Φραβίτου'),
    445: ('lue, itération restituée', 'cons(ulatu) Stellici v(iri) c(larissimi) [iterum? ---]'),
}
EDB_CONJECTURE = {
    123: 'EDB : [--- Lupicin?]o et 〈I〉ovi[no cons(ulibus?)] ; EDCS : [---]o et o⸢b⸣i[it ---] (obiit). Lectures incompatibles ; seule l’ICVR peut trancher.',
    326: 'EDB : [Valentiniano Aug(usto) IIII et N]eute[rio cons(ulibus)] sur la seule séquence …eute… lue.',
    435: 'EDB : [--- Mallio Theodo]ro v(iro) c(larissimo) c[onsule ---] ; seul …ro v. c. est lu.',
    457: 'EDB : [--- Vincent]io et Ep̣[atio consulibus? ---] ; restitution douteuse (EDB : « 359 ; 401 »).',
}
# divergences de date documentées (l'année de classement est maintenue ; statut « contestée »)
CONTESTEE = {
    40: 'Magnence III et Décence II (353) selon la lecture retenue ; l’EDB, citant CLRE p. 636, date de 352 en supposant une erreur du lapicide.',
    52: 'Da[tiano] (358) selon Silvagni ; la CLRE (p. 631, citée par l’EDB) rappelle que Dalmatius, consul en 333, commence aussi par DA. Si 333, la notice sort du corpus.',
    141: 'Valentinien III : Valentinien Ier (370) ou Valentinien II (387) ; la CLRE (p. 644, citée par l’EDB) note « Year doubtful: 387 possible ».',
    165: 'L’année 372 repose sur la seule séquence « dest », interprétée par Ferrua comme [Mo]dest[o] ; l’EDB date « 300-399 ».',
    220: 'Seul …erio est lu ; l’EDB signale d’autres restitutions possibles (Val]erio, Gal]erio, Neot]erio, Ast]erio) : 381 ou 390.',
    328: 'Seul …terio est lu : Eucherio (381) ou Neoterio (390).',
    431: 'La CLRE (p. 661, citée par l’EDB) attribue le texte à 398 ; 399 suppose un post restitué que l’EDB juge trop long.',
    311: 'Maximo cons(ule) : consulat de Magnus Maximus (388) ; l’EDB date de 389 et signale une transcription différente de l’ICVR.',
    434: 'Post-consulat d’Arcadius IV : 397 ; l’EDB date de 399.',
    314: 'Second texte du monument ICUR IV 11117 : seul d(omino) n(ostro) V[…] est lu ; 390 est une restitution partagée par l’EDCS et l’EDB, que la note de l’EDB juge contradictoire avec l’ordre des décès.',
}
EDB_FAUTIVE = {
    206: 'L’EDB date de 377 ; la formule Valentiniano III et Valente Augg. ne convient qu’à 370 : erreur probable de saisie de l’EDB.',
    278: 'L’EDB date de 385 ; Merobaude II et Saturnino = 383, et la fiche voisine EDB8750 (même consulat) est datée de 383 : incohérence interne probable de l’EDB.',
}
ALERTES_V35 = {
    395: 'Itération d’Honorius (IIII transmis) à confronter au collège de 396 (Arcadius IV et Honorius III).',
    411: 'Collège Caesarius et Maximus ; les fastes donnent pour 397 Caesarius et Atticus.',
    428: 'Post-consulat d’Honorius IV et Eutychianus (399 ?) ou consulat (398) ; le jour de la semaine (samedi) convient au 18 décembre 398.',
    444: 'Itération [iter(um)] de Stilichon restituée ; compatibilité avec 400 à contrôler.',
    466: 'Paire Arcadius–Théodose à contrôler sur les fastes de 402.',
}

# ---------------------------------------------------------------- consolidation
out = []
for n in range(1, 479):
    N, T, V = NOT[n], TXT[n], v35[n]
    c = COLL.get(n) or {}
    edb_ids = [x.strip() for x in str(c.get('EDB') or '').replace(';', ',').split(',') if x.strip()]
    edb = [e for e in (parse_edb(i) for i in edb_ids) if e]
    r = {'n': n}
    r['edcs_id'] = N['EDCS-ID']
    r['jn'] = N['id EDCS (J/N)']
    r['refs'] = N['ICUR / refs catalogue']
    r['pub_edcs'] = N['publications EDCS']
    r['genre'] = GENRE_V4.get(n, N['genre'])
    r['genre_v35'] = N['genre']
    r['annee'] = num(N['annee_retenue']) or num(N['annee_catalogue'])
    r['annee_edcs'] = N['annee_edcs']
    r['datation_mode_v2'] = N['datation_mode']
    r['statut_consulaire_v2'] = N['statut_consulaire']
    r['consuls_v2'] = N['consuls_identifies']
    r['post_consulatum'] = N['post_consulatum'] == 'True'
    r['grec'] = N['grec'] == 'True'
    r['ratio_restitue'] = float(N['ratio_restitue'].replace(',', '.')) if N['ratio_restitue'] else None
    r['nb_lettres'] = num(N['nb_lettres'])
    r['photo_edcs'] = N['photo_signalee_EDCS'] == 'True'
    r['rang_senatorial'] = N['rang_senatorial_defunt'] == 'True'
    r['texte_leiden'] = T['texte (Leyde, EDCS état source)']
    r['etat_source'] = T['état source']
    r['texte_2020'] = T['texte EDCS 2020']
    r['texte_dev'] = T['texte développé (normalisé)']
    r['v35'] = V
    # EDB
    r['edb_ids'] = edb_ids
    r['edb_statut'] = c.get('Statut')
    r['edb_similarite'] = c.get('Similarité')
    r['edb_hors_icur'] = c.get('Appariement hors ICUR')
    r['edb_pertinence'] = (c.get('Provenance (EDB)') or '').strip() or None
    cons = (c.get('Conservation (EDB)') or '').strip()
    cons = re.sub(r'^Roma\s*;\s*', '', cons).strip(' ;')
    r['edb_conservation'] = None if cons in ('', '-', '\\-') else cons
    r['edb_date'] = c.get('Date (EDB)')
    r['edb_bibl'] = c.get('Bibliographie EDB')
    r['edb_texte'] = c.get('Texte EDB')
    r['edb_xml'] = edb
    r['edb_signes'] = (CHRI.get(n) or {}).get("Signes décrits par l'EDB")
    r['div_forte'] = DIVF.get(n)
    # relecture des fiches EDB détaillées (lot 5) : les écarts « de notation » ne sont pas des divergences de texte
    r['edb_statut_v4'] = r['edb_statut']
    if r['div_forte'] and str(r['div_forte'].get('cause', '')).startswith('notation'):
        r['edb_statut_v4'] = 'concordant après relecture de la fiche détaillée'
    lv = LVL.get(n)
    r['niveau_consulaire'] = (lv or {}).get('Niveau final')
    r['consuls_lecture'] = (lv or {}).get('Noms consulaires et état (auto)')
    r['faux_consuls'] = [{'nom': f['nom_liste_v2'], 'forme': f['forme_dans_le_texte'], 'role': f['role']} for f in FAUX.get(n, [])]
    r['ages'] = []
    for p_ in AGES.get(n, []):
        key_ = (n, int(float(p_['rang dans le texte'])))
        if key_ in AGE_FIX and AGE_FIX[key_] is None:
            continue
        p_ = dict(p_); p_.update(AGE_FIX.get(key_) or {})
        if key_ in AGE_FIX:
            p_['correction_v4'] = True
        r['ages'].append(p_)
    r['dates'] = DATES.get(n, [])
    r['termes'] = TERMS.get(n, [])
    r['consuls_table'] = CONS.get(n, [])
    r['references'] = REFS.get(n, [])

    # ensembles v4
    r['fusionnee_dans'] = FUSION.get(n)
    r['absorbe'] = [k for k, v in FUSION.items() if v == n]
    r['jointe_a'] = JOINT.get(n)
    r['joint'] = [k for k, v in JOINT.items() if v == n]
    r['hors_periode'] = n in HORS_PERIODE
    r['inB'] = not (r['fusionnee_dans'] or r['jointe_a'] or r['hors_periode'])
    r['funeraire'] = r['genre'].startswith('épitaphe') or r['genre'].startswith('mixte')
    r['inC'] = r['inB'] and r['funeraire']
    r['inC0_v35'] = N['corpus_C'] == 'True'
    r['provenance_douteuse'] = PROV_DOUTEUSE.get(n)

    # datation v4
    if n in HORS_PERIODE:
        st = ('hors période', 'Severinus lu ; [Dagalaiphi] restitué. La CLRE (p. 680, citée par l’EDB) et l’EDH placent le texte en 461 ou 482.')
    elif n in EDB_FORMULE:
        st = ('formule transmise par l’EDB (%s)' % EDB_FORMULE[n][0], EDB_FORMULE[n][1])
    elif n in EDB_CONJECTURE:
        st = ('conjecturale', EDB_CONJECTURE[n])
    elif N['datation_mode'].startswith('indirecte'):
        st = ('indirecte', 'Aucun élément consulaire lisible dans le texte EDCS ni dans la fiche EDB ; année de la base.')
    else:
        lvl = (r['niveau_consulaire'] or '')[:1]
        st = ({'A': ('directe : nom consulaire lu', None), 'B': ('directe : lecture partielle d’un nom consulaire', None),
               'C': ('directe : initiales consulaires', None), 'R': ('directe : consulat restitué', None)}
              .get(lvl, ('directe', None)))
    r['datation'] = st[0]
    r['datation_note'] = st[1]
    r['contestee'] = CONTESTEE.get(n)
    r['edb_fautive'] = EDB_FAUTIVE.get(n)
    r['alerte'] = ALERTES_V35.get(n)
    out.append(r)

json.dump(out, open(os.path.join(DATA, 'corpus_v4.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- bilan
B = [r for r in out if r['inB']]
C = [r for r in out if r['inC']]
print('A', len(out), 'B', len(B), 'C', len(C), 'C0 v3.5', sum(r['inC0_v35'] for r in out))
print('datation', collections.Counter(r['datation'] for r in C))
print('EDB appariées', sum(1 for r in out if r['edb_ids']), 'fiches XML', sum(1 for r in out if r['edb_xml']))
print('signes', sum(1 for r in out if r['edb_signes']))
print('dims', sum(1 for r in out if r['edb_xml'] and r['edb_xml'][0]['dims']))
