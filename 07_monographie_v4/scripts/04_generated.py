#!/usr/bin/env python3
"""PRISME v4.0 — tableaux, répertoires, concordances et index générés depuis les données.

Sorties dans tex/generated/ : un fichier .tex par élément, inclus par les chapitres.
"""
import json, os, re, sys, csv, collections, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leiden as L
from texutil import esc, md, join_fr

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..'))
G = os.path.join(ROOT, 'tex', 'generated')
R = json.load(open(os.path.join(ROOT, 'data', 'corpus_v4.json'), encoding='utf-8'))
ST = json.load(open(os.path.join(ROOT, 'data', 'stats.json'), encoding='utf-8'))
S, LS = ST['S'], ST['L']
FAST = json.load(open(os.path.join(ROOT, 'data', 'fastes.json'), encoding='utf-8'))
BYN = {r['n']: r for r in R}
C = [r for r in R if r['inC']]
SEQ = {r['n']: L.letters(r['texte_leiden']) for r in R}
PERL = ['340–359', '360–374', '375–389', '390–403']


def w(name, txt):
    open(os.path.join(G, name), 'w', encoding='utf-8').write('% généré par scripts/04_generated.py\n' + txt + '\n')


def nl(ns):
    return ', '.join(str(n) for n in sorted(ns))


def per(y):
    for i, (a, b) in enumerate([(340, 359), (360, 374), (375, 389), (390, 403)]):
        if a <= y <= b:
            return i


# ------------------------------------------------------------------ table des fastes (chap. 7)
rows = []
for y in range(340, 404):
    ns = [r for r in R if r['annee'] == y and not r['hors_periode'] and r['inB']]
    rows.append('%d & %s & %d \\\\' % (y, esc(FAST[str(y)]), len(ns)))
w('tab_fastes.tex', '\\begin{longtable}{@{}r p{0.70\\linewidth} r@{}}\n'
  '\\caption{Collèges consulaires 340–403 selon la tradition des fastes et nombre de textes distincts (ensemble B) classés sous chaque année. Table non collationnée sur la CLRE.}\\label{tab:fastes}\\\\\n'
  '\\toprule Année & Collège consulaire & Textes\\\\\\midrule\\endfirsthead\n\\toprule Année & Collège consulaire & Textes\\\\\\midrule\\endhead\n\\bottomrule\\endfoot\n'
  + '\n'.join(rows) + '\n\\end{longtable}')

# ------------------------------------------------------------------ chronique consulaire (chap. 11)
out = []
for y in range(340, 404):
    ns = [r for r in R if r['annee'] == y and r['inB']]
    if not ns:
        out.append('\\chronan{%d}{%s}{Aucun texte du corpus.}' % (y, esc(FAST[str(y)])))
        continue
    groups = collections.OrderedDict()
    for r in ns:
        groups.setdefault(r['datation'], []).append(r['n'])
    desc = '; '.join('%s : %s' % (k, nl(v)) for k, v in groups.items())
    items = []
    for r in ns:
        bits = []
        lt = r['consuls_lecture']
        if lt and not r['datation'].startswith('formule') and r['datation'] not in ('conjecturale',):
            parts = []
            for p in lt.split(';'):
                m = re.match(r'\s*([^:]+):(\w+)', p)
                if m:
                    parts.append('%s (%s)' % (m.group(1).strip(), {'lu': 'lu', 'partiel': 'partiel', 'restitué': 'restitué'}.get(m.group(2), m.group(2))))
            bits.append(', '.join(parts))
        if r['datation'].startswith('formule'):
            bits.append('formule transmise par l’EDB')
        if r['datation'] == 'conjecturale':
            bits.append('restitution conjecturale')
        if r['datation'] == 'indirecte':
            bits.append('aucun élément consulaire')
        if r['post_consulatum']:
            bits.append('post-consulat')
        if r['contestee']:
            bits.append('\\textit{contestée}')
        if r['alerte']:
            bits.append('\\textit{réserve}')
        if r['grec']:
            bits.append('grec')
        if r['absorbe'] or r['joint']:
            bits.append('absorbe %s' % nl(r['absorbe'] + r['joint']))
        items.append('\\no{%d} %s' % (r['n'], esc('; '.join(b for b in bits if not b.startswith('\\'))) + ('; ' + '; '.join(b for b in bits if b.startswith('\\')) if any(b.startswith('\\') for b in bits) else '')))
    out.append('\\chronan{%d}{%s}{%s}' % (y, esc(FAST[str(y)]), ' \\textbullet{} '.join(items)))
w('chronique.tex', '\n'.join(out).replace('\\no{', '\\nnum{'))

# ------------------------------------------------------------------ in pace : listes
ip = LS['inpace']
lab = {'ecrit': 'en toutes lettres, sans correction', 'abrege': 'abrégée, sans restitution ni correction',
       'corrige': 'avec correction éditoriale, sans restitution', 'restitue': 'seulement avec restitution'}
t = []
for k in ('ecrit', 'abrege', 'corrige', 'restitue'):
    t.append('\\item[%s] (%d textes) %s.' % (esc(lab[k]).capitalize(), len(ip.get(k, [])), nl(ip.get(k, []))))
w('liste_inpace.tex', '\\begin{description}[style=nextline,leftmargin=1.5em,font=\\normalfont\\scshape]\n' + '\n'.join(t) + '\n\\end{description}')

# ------------------------------------------------------------------ formulaire : tableau et répertoire
rows = []
for f in LS['formulaire']:
    rows.append('\\lat{%s} & %d & %s & %d & %s \\\\' % (esc(f['element']), f['avec'], esc(('%.1f' % (100 * f['avec'] / len(C))).replace('.', ',')),
                                                     f['sans'], esc(('%.1f' % (100 * f['sans'] / len(C))).replace('.', ','))))
w('tab_formulaire.tex', '\\begin{table}[tbp]\\centering\\small\n\\caption{Éléments du formulaire dans l’ensemble C (n = %d) : textes où l’élément est attesté, restitutions comprises, et textes où il l’est au moins une fois sans restitution (abréviations et corrections admises).}\\label{tab:formulaire}\n'
  '\\begin{tabular}{@{}l r r r r@{}}\\toprule Élément & Avec rest. & \\%% & Sans rest. & \\%% \\\\\\midrule\n' % len(C) + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\\end{table}')
rep = []
for i, f in enumerate(LS['formulaire']):
    perc = []
    dens = [S['perC%d' % k] for k in range(4)]
    for k in range(4):
        perc.append('%s : %d/%d (%s~\\%%)' % (PERL[k], f['par_periode'][k], dens[k], ('%.1f' % (100 * f['par_periode'][k] / dens[k])).replace('.', ',')))
    forms = ', '.join('%s (%d)' % (esc(a), b) for a, b in f['formes'])
    rep.append('\\subsection*{%s}\n\\addcontentsline{toc}{subsection}{%s}\n\\noindent Règle (texte normalisé, \\textit{u/v} et \\textit{i/j} unifiés) : \\texttt{\\small %s}. Ensemble C : %d textes avec restitutions, %d sans restitution ; écart dû aux restitutions : %d.\\par\n'
               '\\noindent Par période (attestations sans restitution / textes de la période) : %s.\\par\n\\noindent Formes relevées (occurrences) : %s.\\par\n\\noindent{\\small Notices (élément attesté sans restitution) : %s.}\\par\\medskip'
               % (esc(f['element']), esc(f['element']), esc(f['regle']).replace('|', '|\\allowbreak{}').replace('(', '(\\allowbreak{}'), f['avec'], f['sans'], f['avec'] - f['sans'], ' ; '.join(perc), forms, nl(f['notices'])))
w('repertoire_formulaire.tex', '\n'.join(rep))

# ------------------------------------------------------------------ graphies
rows = []
for g in LS['graphies']:
    if g['occ'] < 2:
        continue
    rows.append('\\lat{%s} & %s & %d & %s & {\\footnotesize %s} \\\\' % (esc(g['attendu']), esc(g['grave']), g['occ'], esc(g['phen']), nl(g['notices'])))
rest = [g for g in LS['graphies'] if g['occ'] < 2]
w('tab_graphies.tex', '\\begin{longtable}{@{}l l r l p{0.45\\linewidth}@{}}\n\\caption{Corrections éditoriales signalées par l’EDCS (état 2022, ensemble A) : lettre attendue, lettre déclarée gravée, occurrences, phénomène, notices. Correspondances attestées au moins deux fois.}\\label{tab:graphies}\\\\\n'
  '\\toprule Attendu & Gravé & Occ. & Phénomène & Notices\\\\\\midrule\\endfirsthead\\toprule Attendu & Gravé & Occ. & Phénomène & Notices\\\\\\midrule\\endhead\\bottomrule\\endfoot\n' + '\n'.join(rows) +
  '\n\\end{longtable}\n\\noindent{\\small Correspondances attestées une seule fois (%d) : %s.}' % (len(rest), '; '.join('%s/%s (%s)' % (esc(g['attendu']), esc(g['grave']), nl(g['notices'])) for g in rest)))

rows = ['%s & \\lat{%s} & %d \\\\' % (esc(a['abrege']), esc(a['exemple']), a['occ']) for a in LS['abreviations']]
half = (len(rows) + 1) // 2
w('tab_abreviations.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Les abréviations les plus fréquentes de l’ensemble A : forme abrégée (lettres gravées), exemple de développement éditorial, occurrences.}\\label{tab:abrev}\n'
  '\\begin{tabular}{@{}l l r@{}}\\toprule Abrégé & Exemple & Occ.\\\\\\midrule ' + '\n'.join(rows[:half]) + '\\bottomrule\\end{tabular}\\hspace{1.5em}'
  '\\begin{tabular}{@{}l l r@{}}\\toprule Abrégé & Exemple & Occ.\\\\\\midrule ' + '\n'.join(rows[half:]) + '\\bottomrule\\end{tabular}\\end{table}')

# ------------------------------------------------------------------ textes grecs
rows = []
for r in R:
    if r['grec']:
        rows.append('%d & %s & {\\small %s} \\\\' % (r['n'], r['annee'] if not r['hors_periode'] else '—', esc(' / '.join(r['v35']['f7']))))
w('tab_grecs.tex', '\\begin{longtable}{@{}r r p{0.78\\linewidth}@{}}\\caption{Textes grecs et bilingues (texte EDCS, état 2022).}\\label{tab:grecs}\\\\\\toprule N° & Année & Texte\\\\\\midrule\\endfirsthead\\bottomrule\\endfoot\n' + '\n'.join(rows) + '\n\\end{longtable}')

# ------------------------------------------------------------------ jours de la semaine (recalcul julien)
DOW = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
PLAN = {'Solis': 0, 'Lunae': 1, 'Martis': 2, 'Mercurii': 3, 'Iovis': 4, 'Veneris': 5, 'Saturni': 6, 'Saturnis': 6}


def jdn(Y, M, D):
    a = (14 - M) // 12; y = Y + 4800 - a; m = M + 12 * a - 3
    return D + (153 * m + 2) // 5 + 365 * y + y // 4 - 32083


EVENT_YEAR = {(55, 'XI Kalendas Iulias'): 340, (126, 'III Idus Augustas'): 350}
rows = []
with open(os.path.join(REPO, '01_donnees', 'base_v2_csv', 'Jours_semaine.csv'), encoding='utf-8') as f:
    for d in csv.DictReader(f):
        n = int(float(d['n'])); ment = d['mention']; q = (d['quantième rattaché'] or '').strip()
        planet = [v for k, v in PLAN.items() if k in ment]
        if not q or not d['date (a/m/j)']:
            rows.append((n, int(float(d['année'])), ment, '—', '—', '—', 'quantième lacunaire'))
            continue
        Y, M, D = [int(x) for x in d['date (a/m/j)'].split('/')]
        Y = EVENT_YEAR.get((n, q), Y)
        dw = (jdn(Y, M, D) + 1) % 7
        res = 'concordant' if planet and planet[0] == dw else ('écart d’un jour' if planet and (abs(planet[0] - dw) in (1, 6)) else 'discordant')
        rows.append((n, Y, ment, esc(q), '%d/%d/%d' % (D, M, Y), DOW[dw], res))
        if n == 428:
            dw2 = (jdn(399, M, D) + 1) % 7
            rows.append((n, 399, ment, esc(q), '%d/%d/399' % (D, M), DOW[dw2], 'concordant' if planet[0] == dw2 else 'écart d’un jour'))
nconc = sum(1 for r in rows if r[6] == 'concordant'); necart = sum(1 for r in rows if r[6].startswith('écart'))
S['jsConc'] = nconc; S['jsEcart'] = necart; S['jsTot'] = len(rows)
w('tab_jours.tex', '\\begin{table}[tbp]\\centering\\footnotesize\\setlength{\\tabcolsep}{3.5pt}\\caption{Contrôle des jours de la semaine (calendrier julien, recalcul ; l’année est celle de l’événement daté : naissance pour les \\nnums{55} et 126 première mention).}\\label{tab:jours}\n'
  '\\begin{tabular}{@{}r r l l l l l@{}}\\toprule N° & Année & Mention & Quantième & Date & Calcul & Résultat\\\\\\midrule\n'
  + '\n'.join('%d & %d & \\lat{%s} & \\lat{%s} & %s & %s & %s \\\\' % r for r in rows) + '\n\\bottomrule\\end{tabular}\\end{table}')

# ------------------------------------------------------------------ vie conjugale, fonctions
rows = []
for n in LS['vie_conjugale']:
    ex = L.extract(SEQ[n], r'(fecit|uixit|fecerunt)\s+(cum\s+\w+(\s+\w+)?|mecum)[^/]{0,40}|in\s+coniugio[^/]{0,30}')
    rows.append('%d & %d & \\lat{%s} \\\\' % (n, BYN[n]['annee'], esc(ex)))
w('tab_conjugale.tex', '\\begin{longtable}{@{}r r p{0.75\\linewidth}@{}}\\caption{Durées de vie commune déclarées (ensemble C ; extrait du texte transmis).}\\label{tab:conjugale}\\\\\\toprule N° & Année & Passage\\\\\\midrule\\endfirsthead\\bottomrule\\endfoot\n' + '\n'.join(rows) + '\n\\end{longtable}')

FUNC = collections.OrderedDict([('lector', r'\blector\w*'), ('presbyter', r'\b(presb\w*|prb)\b'), ('diaconus', r'\bdiac\w*'),
                                ('episcopus', r'\bep(is)?c\w*|\bepiscop\w*'), ('fossor', r'\bfossor\w*'), ('medicus', r'\bmedic(us|i|o|um)\b'),
                                ('pictor', r'\bpictor\b'), ('numerarius', r'\bnumerari\w*'), ('scholasticus', r'\bscholastic\w*'),
                                ('quadratarius', r'\bquadratari\w*'), ('armararius', r'\barmarari\w*'), ('praefectus', r'\bpraefect\w*'),
                                ('praeses (ex praesidibus)', r'\bpraesid\w*'), ('tribunus', r'\btrib\w*\s+praetor\w*'), ('sacerdos', r'\bsacerdo\w*'),
                                ('matrona (diaconi, presbyteri)', r'\bmatrona\b')])
rows = []
for lab_, pat in FUNC.items():
    hits = []
    for r in R:
        if not r['inB'] and not r['n'] == 321:
            continue
        occ = L.find(SEQ[r['n']], pat)
        if occ:
            st_ = 'lu' if any('R' not in o['statuts'] for o in occ) else 'restitué'
            hits.append('%d%s' % (r['n'], '' if st_ == 'lu' else '*'))
    if hits:
        rows.append('\\lat{%s} & %d & %s \\\\' % (esc(lab_), len(hits), ', '.join(hits)))
w('tab_fonctions.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Fonctions, rangs et métiers mentionnés (ensemble B et \\nnum{321} ; l’astérisque signale une attestation seulement restituée). Le rang n’est pas toujours celui du défunt.}\\label{tab:fonctions}\n\\begin{tabular}{@{}l r p{0.5\\linewidth}@{}}\\toprule Terme & Textes & Notices\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\\end{table}')

# ------------------------------------------------------------------ relations familiales
REL = collections.OrderedDict([('coniux, compar', r'\b(coniu[gnx]\w*|compar(i|e|em)?)\b'), ('maritus', r'\bmarit\w*'), ('uxor', r'\buxor\w*'),
                               ('filius, filia', r'\bfili(us|a|o|ae|i|is|um|am|e)\b'), ('pater', r'\b(pater|patri|patre|patris|patrem)\b'),
                               ('mater', r'\b(mater|matri|matre|matris|matrem)\b'), ('parentes', r'\bparent\w*'), ('frater', r'\bfrat(er|ri|re|ris|res|rem|ribus)\b'),
                               ('soror', r'\bsoror\w*'), ('nepos, neptis', r'\bnep(os|ot\w*|tis)\b'), ('amicus, amica', r'\bamic(us|a|o|ae|i|um|orum|is)\b'),
                               ('socrus, gener, nurus', r'\b(socr\w*|gener\b|genero|nurus)'), ('virginius, virginia', r'\b[bu]irgini(us|a|o|um|ae)\b')])
rows = []; notes = []
for lab_, pat in REL.items():
    tot, cons, byp, ns = 0, 0, collections.Counter(), []
    for r in C:
        occ = L.find(SEQ[r['n']], pat)
        if occ:
            tot += 1; ns.append(r['n'])
            if any('R' not in o['statuts'] for o in occ):
                cons += 1; byp[per(r['annee'])] += 1
    rows.append('\\lat{%s} & %d & %d & %s \\\\' % (esc(lab_), tot, cons, ' & '.join(str(byp[k]) for k in range(4))))
    notes.append('\\lat{%s} : %s.' % (esc(lab_), nl(ns)))
w('tab_relations.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Termes de parenté et de relation dans l’ensemble C (textes, non occurrences) : attestations restitutions comprises, attestations lues, et répartition des attestations lues par période.}\\label{tab:relations}\n'
  '\\begin{tabular}{@{}l r r r r r r@{}}\\toprule Terme & Total & Lu & 340–359 & 360–374 & 375–389 & 390–403\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\\end{table}')
w('liste_relations.tex', '\\begin{small}\\noindent ' + '\\par\\noindent '.join(notes) + '\\end{small}')

# ------------------------------------------------------------------ vocabulaire religieux (répertoire)
EMPLOI_ORDER = ['désignation de Dieu', 'désignation du Christ', 'Esprit saint', 'mention de la Trinité', 'initiation et foi',
                'vocabulaire ecclésial', 'Église (épithète)', 'saints (communion des saints)', 'intercession', 'résurrection',
                'repos et sommeil de la mort', 'allusion interprétative (niveau 5)', 'identité chrétienne (christianus)',
                'âme humaine (non doctrinal)', 'épithète du défunt (non doctrinal)', 'anthroponyme (niveau 6)', 'Dominus (référent indéterminé)']
OVR = {(38, 'christi'): ('signe (S)', 'monogramme décrit par l’EDB et par l’estampage ILCV 3252A ; non compté comme mot'),
       (140, 'christi'): (None, 'chrisme décrit par l’EDB : monogramme probable'),
       (151, 'christi'): (None, 'chrisme décrit par l’EDB : monogramme probable'),
       (311, 'christo'): (None, 'chrisme décrit par l’EDB : monogramme probable'),
       (447, 'ἀναστάσεως'): (None, 'restitution contestée : l’EDB restitue κρίσεως'),
       (152, 'redemptus'): (None, 'lecture contestée par l’EDB : [cor]p⟨o⟩re demptus'),
       (152, 'redemptum'): (None, 'lecture contestée par l’EDB'),
       (73, 'deum'): (None, 'restitution de l’EDCS ; l’EDB imprime [quaeque de]metuisti'),
       (73, 'caelo'): (None, 'restitution de l’EDCS ; l’EDB restitue [corpore namque tu]us'),
       (73, 'sanctis'): (None, 'verbe restitué différemment : [vivit cum] (EDCS), [est sociatu]s (EDB)'),
       (85, 'domino'): (None, 'lettres soulignées par l’EDB : lues par des éditeurs antérieurs, non visibles aujourd’hui'),
       (232, 'in domino'): (None, 'développement assorti d’un point d’interrogation par l’éditeur'),
       (330, 'sanctis'): (None, 'sigle p. t. c. s. : développement éditorial de quatre initiales'),
       (249, 'sanctum'): (None, 'l’identification de l’Esprit saint dépend de cette restitution')}
import unicodedata
OVR = {(k[0], unicodedata.normalize('NFC', k[1])): v for k, v in OVR.items()}
by = collections.defaultdict(list)
for r in R:
    for t in r['termes']:
        by[t['emploi']].append((r, t))
out = []
for e in EMPLOI_ORDER + [k for k in by if k not in EMPLOI_ORDER]:
    if e not in by:
        continue
    items = by[e]
    out.append('\\subsection*{%s (%d occurrence%s)}\\addcontentsline{toc}{subsection}{%s}' % (esc(e[0].upper() + e[1:]), len(items), 's' if len(items) > 1 else '', esc(e)))
    out.append('\\begin{itemize}[leftmargin=1.2em,itemsep=0pt]')
    for r, t in sorted(items, key=lambda x: (x[1]['forme'].lower(), x[0]['n'])):
        frm = t['forme']; key = (r['n'], unicodedata.normalize('NFC', frm.lower()))
        lvl = t['niveau (libellé)']
        note = ''
        if key in OVR:
            if OVR[key][0]:
                lvl = OVR[key][0]
            note = ' — \\textit{%s}' % esc(OVR[key][1])
        flags = []
        if not r['inC']:
            flags.append('hors C')
        out.append('\\item \\no{%d} (%s) \\lat{%s}, %s%s%s' % (r['n'], r['annee'], esc(frm), esc(lvl), (' [%s]' % ', '.join(flags)) if flags else '', note))
    out.append('\\end{itemize}')
w('repertoire_religieux.tex', '\n'.join(out).replace('\\no{', '\\nnum{'))

# ------------------------------------------------------------------ actes d'achat et textes mixtes
rows = []
for r in R:
    if r['inB'] and (r['genre'].startswith('acte') or r['genre'].startswith('mixte')):
        rows.append('%d & %d & %s & {\\small\\lat{%s}} \\\\' % (r['n'], r['annee'], 'mixte' if r['genre'].startswith('mixte') else 'acte',
                                                               esc(' / '.join(r['v35']['f7'])[:190].strip()) + ('…' if len(' / '.join(r['v35']['f7'])) > 190 else '')))
w('tab_achats.tex', '\\begin{longtable}{@{}r r l p{0.68\\linewidth}@{}}\\caption{Actes d’achat ou de réservation d’emplacement et textes mixtes (ensemble B ; début du texte transmis).}\\label{tab:achats}\\\\\\toprule N° & Année & Genre & Texte (début)\\\\\\midrule\\endfirsthead\\toprule N° & Année & Genre & Texte (début)\\\\\\midrule\\endhead\\bottomrule\\endfoot\n' + '\n'.join(rows) + '\n\\end{longtable}')

# ------------------------------------------------------------------ provenance, conservation, supports, signes
def tab_counts(name, caption, label, items, head):
    rows = '\n'.join('%s & %d \\\\' % (esc(k), v) for k, v in items)
    w(name, '\\begin{table}[tbp]\\centering\\small\\caption{%s}\\label{%s}\n\\begin{tabular}{@{}l r@{}}\\toprule %s & Textes\\\\\\midrule\n%s\n\\bottomrule\\end{tabular}\\end{table}' % (caption, label, head, rows))


cem = [(k, v) for k, v in LS['cimetieres_C'] if v >= 3] + [('autres rattachements (moins de trois textes chacun)', sum(v for k, v in LS['cimetieres_C'] if v < 3))]
tab_counts('tab_cimetieres.tex', 'Rattachement topographique des textes de l’ensemble C selon l’EDB (%d textes appariés). Les rattachements de moins de trois textes sont regroupés.' % S['edbAppC'], 'tab:cimetieres', cem, 'Cimetière ou secteur')
cons = [(k, v) for k, v in LS['conservation_C'] if v >= 4] + [('autres lieux', sum(v for k, v in LS['conservation_C'] if v < 4))]
tab_counts('tab_conservation.tex', 'Lieu de conservation actuel indiqué par l’EDB (ensemble C ; %d textes). Indication de la base, non contrôlée.' % S['nConsConnue'], 'tab:conservation', cons, 'Lieu de conservation')
rows = []
for (k1, v1), (k2, v2) in zip(LS['supports'] + [('', 0)] * 6, LS['materiaux'] + [('', 0)] * 6):
    pass
w('tab_supports.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Support, matériau et technique d’exécution selon les fiches EpiDoc de l’EDB (ensemble C ; %d fiches).}\\label{tab:supports}\n' % S['edbXmlC'] +
  '\\begin{tabular}[t]{@{}l r@{}}\\toprule Support & N\\\\\\midrule ' + ' '.join('%s & %d\\\\' % (esc(k), v) for k, v in LS['supports']) + '\\bottomrule\\end{tabular}\\hspace{1.2em}'
  '\\begin{tabular}[t]{@{}l r@{}}\\toprule Matériau & N\\\\\\midrule ' + ' '.join('%s & %d\\\\' % (esc(k), v) for k, v in LS['materiaux']) + '\\bottomrule\\end{tabular}\\hspace{1.2em}'
  '\\begin{tabular}[t]{@{}l r@{}}\\toprule Exécution & N\\\\\\midrule ' + ' '.join('%s & %d\\\\' % (esc(k), v) for k, v in LS['execution']) + '\\bottomrule\\end{tabular}\\end{table}')
sig = LS['signes']
rows = []
for n in sorted(int(k) for k in sig):
    r = BYN[n]
    rows.append('%d & %s & %s \\\\' % (n, r['annee'] if not r['hors_periode'] else '—', esc(join_fr(sig[str(n)]))))
w('tab_signes.tex', '\\begin{longtable}{@{}r r p{0.7\\linewidth}@{}}\\caption{Signes chrétiens décrits par l’EDB (fiches EpiDoc de 2019 et texte des listes de résultats de 2026), ensemble A.}\\label{tab:signes}\\\\\\toprule N° & Année & Signes\\\\\\midrule\\endfirsthead\\toprule N° & Année & Signes\\\\\\midrule\\endhead\\bottomrule\\endfoot\n' + '\n'.join(rows) + '\n\\end{longtable}')
w('tab_signes_periode.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Textes de l’ensemble C portant un chrisme ou une croix selon l’EDB, par période, rapportés aux textes appariés à une fiche EDB.}\\label{tab:signesper}\n\\begin{tabular}{@{}l r r r@{}}\\toprule Période & Signes & Textes appariés & \\%\\\\\\midrule\n' +
  '\n'.join('%s & %d & %d & %s \\\\' % (p, a, b, ('%.1f' % (100 * a / b)).replace('.', ',')) for p, a, b in LS['signes_periode']) + '\n\\bottomrule\\end{tabular}\\end{table}')

# ------------------------------------------------------------------ mesures et sensibilité
rows = '\n'.join('%s & %s & %d & %d & %s & %s \\\\' % (esc(a), esc(b), c, d, e, f) for a, b, c, d, e, f in LS['mesures'])
w('tab_mesures.tex', '\\begin{longtable}{@{}p{0.27\\linewidth} p{0.27\\linewidth} r r r l@{}}\\caption{Principales mesures selon trois dénominateurs. Les intervalles de Wilson (95~\\%) sont des résumés binomiaux conditionnels, non des marges d’erreur sur la population antique.}\\label{tab:mesures}\\\\\n'
  '\\toprule Mesure & Ensemble & n & k & \\% & IC 95 \\%\\\\\\midrule\\endfirsthead\\toprule Mesure & Ensemble & n & k & \\% & IC 95 \\%\\\\\\midrule\\endhead\\bottomrule\\endfoot\n' + rows + '\n\\end{longtable}')

# ------------------------------------------------------------------ datation : listes
dl = LS['datation_C']
order = ['directe : nom consulaire lu', 'directe : lecture partielle d’un nom consulaire', 'directe : initiales consulaires', 'directe : consulat restitué',
         'formule transmise par l’EDB (lue)', 'formule transmise par l’EDB (lue, itération restituée)', 'formule transmise par l’EDB (partiellement restituée)', 'conjecturale', 'indirecte']
rows = []
for k in order:
    if k in dl:
        lst = dl[k]
        rows.append('%s & %d & {\\footnotesize %s} \\\\' % (esc(k[0].upper() + k[1:]), len(lst), nl(lst) if len(lst) < 40 else '—'))
w('tab_datation.tex', '\\begin{table}[tbp]\\centering\\small\\caption{Fondement de l’année dans l’ensemble C (n = %d). Les listes de plus de quarante notices sont données dans la chronique (chapitre~\\ref{ch:chronique}).}\\label{tab:datation}\n' % len(C) +
  '\\begin{tabular}{@{}p{0.36\\linewidth} r p{0.5\\linewidth}@{}}\\toprule Fondement & Textes & Notices\\\\\\midrule\n' + '\n'.join(rows) + '\n\\bottomrule\\end{tabular}\\end{table}')
rows = []
for n in sorted(set(LS['contestees']) | set(LS['alertes']) | set(LS['edb_fautive'])):
    r = BYN[n]
    txt = r['contestee'] or r['alerte'] or r['edb_fautive']
    kind = 'contestée' if r['contestee'] else ('réserve' if r['alerte'] else 'EDB fautive')
    rows.append('%d & %d & %s & {\\footnotesize %s} \\\\' % (n, r['annee'], kind, esc(txt)))
w('tab_contestees.tex', '\\begin{longtable}{@{}r r l p{0.6\\linewidth}@{}}\\caption{Datations contestées, réserves et divergences attribuées à l’EDB. L’année de classement est conservée dans tous les cas.}\\label{tab:contestees}\\\\\\toprule N° & Année & Statut & Motif\\\\\\midrule\\endfirsthead\\toprule N° & Année & Statut & Motif\\\\\\midrule\\endhead\\bottomrule\\endfoot\n' + '\n'.join(rows) + '\n\\end{longtable}')

# ------------------------------------------------------------------ concordances
def icur_keys(r):
    ks = []
    for m in re.finditer(r'ICUR-(\d\d), 0*(\d+[a-z]?)', r['refs'] or ''):
        ks.append((int(m.group(1)), m.group(2)))
    return sorted(set(ks), key=lambda x: (x[0], int(re.match(r'\d+', x[1]).group(0)), x[1]))


ROM = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
items = []
for r in R:
    for v, num in icur_keys(r):
        items.append((v, int(re.match(r'\d+', num).group(0)), num, r['n']))
items.sort()
w('conc_icur.tex', '\\begin{multicols}{4}\\footnotesize\\noindent ' + '\\\\\n'.join('ICUR %s %s → %d' % (ROM[v], num, n) for v, _, num, n in items) + '\\end{multicols}')
items = sorted((r['edcs_id'], r['n']) for r in R)
w('conc_edcs.tex', '\\begin{multicols}{4}\\footnotesize\\noindent ' + '\\\\\n'.join('%s → %d' % x for x in items) + '\\end{multicols}')
items = sorted(((int(e[3:]), e, r['n']) for r in R for e in r['edb_ids']))
w('conc_edb.tex', '\\begin{multicols}{4}\\footnotesize\\noindent ' + '\\\\\n'.join('%s → %d' % (e, n) for _, e, n in items) + '\\end{multicols}')
oth = []
for r in R:
    for x in (r['v35']['f16'] or '').split(';'):
        x = x.strip().rstrip('.')
        if x and not x.startswith('ICUR'):
            x = re.sub(r'^AE (\d{4}), \+?0*(\d+)', r'AE \1, \2', x)
            x = re.sub(r'^(ILCV|CLE) \+?0*(\d+)', r'\1 \2', x)
            x = re.sub(r'^CIL 0?(\d+), \*?0*(\d+)', lambda m_: 'CIL %s %s' % ({'06': 'VI', '6': 'VI', '14': 'XIV'}.get(m_.group(1), m_.group(1)), m_.group(2)), x)
            x = re.sub(r', 0+(\d)', r', \1', x)
            oth.append((x, r['n']))
oth.sort(key=lambda t: (re.sub(r'\d+', lambda m: m.group(0).zfill(6), t[0]), t[1]))
w('conc_autres.tex', '\\begin{multicols}{3}\\footnotesize\\noindent ' + '\\\\\n'.join('%s → %d' % (esc(a), b) for a, b in oth) + '\\end{multicols}')
lines = []
for r in R:
    first = re.search(r'ICUR-(\d\d), 0*(\d+[a-z]?)', r['refs'] or '')
    ic = ('ICUR %s %s' % (ROM[int(first.group(1))], first.group(2))) if first else '—'
    lines.append('%d & %s & %s & %s & %s \\\\' % (r['n'], r['annee'] if not r['hors_periode'] else '—', ic, r['edcs_id'], ', '.join(r['edb_ids']) or '—'))
w('conc_generale.tex', '\\begin{longtable}{@{}r r l l l@{}}\\caption{Concordance générale : notice, année de classement, première référence ICUR, EDCS, EDB.}\\label{tab:concgen}\\\\\\toprule N° & Année & ICUR & EDCS & EDB\\\\\\midrule\\endfirsthead\\toprule N° & Année & ICUR & EDCS & EDB\\\\\\midrule\\endhead\\bottomrule\\endfoot\n\\footnotesize ' + '\n'.join(lines) + '\n\\end{longtable}')

# ------------------------------------------------------------------ index
words = collections.defaultdict(set)
for r in R:
    s, pos = L.plain(SEQ[r['n']], keep=('L', 'A', 'C', 'R'))
    for m in re.finditer(r'[a-zà-ÿ]{2,}', s):
        words[m.group(0)].add(r['n'])
lat = sorted(words.items())
w('index_latin.tex', '\\begin{multicols}{3}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em \\lat{%s} %s\\par' % (esc(k), nl(v)) for k, v in lat) + '\\end{multicols}')
gwords = collections.defaultdict(set)
for r in R:
    s, _ = L.plain(SEQ[r['n']])
    for m in re.finditer(r'[\u0370-\u03ff\u1f00-\u1fff]{3,}', s):
        gwords[m.group(0)].add(r['n'])
w('index_grec.tex', '\\begin{multicols}{3}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %s %s\\par' % (esc(k), nl(v)) for k, v in sorted(gwords.items())) + '\\end{multicols}')
cons = collections.defaultdict(set)
for r in R:
    faux = {f['nom'] for f in (r['faux_consuls'] or [])}
    for p in (r['consuls_lecture'] or '').split(';'):
        m = re.match(r'\s*([^:]+):\s*(\w+)', p)
        if m and m.group(1).strip() not in faux:
            mark = {'lu': '', 'partiel': '°'}.get(m.group(2), '*')
            cons[m.group(1).strip()].add('%d%s' % (r['n'], mark))
def _ck(x):
    return int(re.sub(r'\D', '', x))
w('index_consuls.tex', '\\begin{multicols}{2}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %s : %s\\par' % (esc(k), ', '.join(sorted(v, key=_ck))) for k, v in sorted(cons.items())) + '\\end{multicols}')
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
cal = collections.defaultdict(list)
for r in R:
    for d in r['dates']:
        if d['date julienne']:
            parts = d['date julienne'].split()
            if len(parts) == 2 and parts[1] in MOIS:
                cal[(MOIS.index(parts[1]), int(parts[0].replace('er', '')))].append('%d (%s)' % (r['n'], {'dépo': 'dépo.', 'décè': 'déc.', 'nais': 'nais.', 'acha': 'ach.', 'indé': 'indét.'}.get(d['événement (indice contextuel)'][:4], d['événement (indice contextuel)'][:4] + '.')))
w('index_calendrier.tex', '\\begin{multicols}{3}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %d %s : %s\\par' % (d, MOIS[m], ', '.join(v)) for (m, d), v in sorted(cal.items())) + '\\end{multicols}')
ages = collections.defaultdict(list)
for r in C:
    for p in r['ages']:
        if p['années']:
            a = int(float(p['années']))
            if (r['n'], a) == (411, 20):
                a = 22
            ages[a].append('%d%s' % (r['n'], '' if p['certitude'] == 'lu' else '*'))
w('index_ages.tex', '\\begin{multicols}{3}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %d ans : %s\\par' % (a, ', '.join(v)) for a, v in sorted(ages.items())) + '\\end{multicols}')
# noms de personnes : mots à initiale majuscule hors formule consulaire (relevé automatique)
GREEK = re.compile(r'[Ͱ-Ͽἀ-῿]')
MONTHS = re.compile(r'^(ianuar|febr|februar|mart|april|apr|mai|iun|iul|august|aug|septemb|septimb|sept|octob|oct|novemb|nouemb|nov|decemb|dec)(i|ias|iis|ies|es|is|ibus|as|a|ae|e|ium|res|ribus|ris|re)?$', re.I)
STOPW = {'kalendas', 'kalendis', 'kalndas', 'kal', 'idus', 'idibus', 'nonas', 'nonis', 'dis', 'manibus', 'hic', 'huic', 'hoc', 'depositus', 'deposita', 'depositio',
         'locus', 'bene', 'quae', 'qui', 'dep', 'in', 'et', 'saturni', 'saturnis', 'solis', 'lunae', 'martis', 'mercurii', 'iouis', 'ueneris', 'luna',
         'augusto', 'augusti', 'augustis', 'auggustis', 'aauuggustis', 'auggustorum', 'augg', 'aug', 'augusta', 'dormitio', 'mirae', 'mire', 'carissimo',
         'carissimae', 'sanctae', 'columna', 'depossio', 'uiuit', 'innocens', 'innox', 'dulcis', 'dulcissimae', 'dulcissimo', 'uix', 'domino', 'domini',
         'dominis', 'ddominis', 'dei', 'deo', 'deus', 'christi', 'christo', 'christus', 'christum', 'urbi', 'urbis', 'romae', 'roma', 'quiesces', 'quod',
         'haec', 'conss', 'cons', 'consulatu', 'decessit', 'comparauerunt', 'maerentes', 'laborum', 'matri', 'infanti', 'episcopus', 'civem', 'ciuem',
         'capricornus', 'octrobres', 'septembrium', 'pridie', 'post', 'pace', 'quid', 'quo', 'puer', 'uixit', 'sepulcrum', 'praestantissimo', 'uenerabili', 'reuerendo', 'presbyteri', 'aniciis', 'caesare', 'recemede', 'romodoro', 'totius', 'flauiis', 'fflauiis', 'ffllauiis', 'ffllauis', 'ffllauuis', 'christianae'}
GENT_CONS = ('flaui', 'fl', 'ffl', 'anici', 'claudi', 'cl', 'aureli', 'aur', 'noni', 'malli', 'magn', 'ma')


def _norm(t):
    t = t.lower().replace('ph', 'f').replace('th', 't').replace('ch', 'c').replace('y', 'i').replace('v', 'u').replace('ae', 'e').replace('k', 'c')
    t = t.replace('u', 'o').replace('b', 'o')
    return re.sub(r'(.)\1', r'\1', t)


def _stem(name):
    n = _norm(name)
    if n.endswith('ns'):
        return n[:-1]
    for e in ('ius', 'us', 'is', 'es', 'a'):
        if n.endswith(_norm(e)) and len(n) - len(e) >= 4:
            return n[:-len(e)]
    return n


names = collections.defaultdict(set)
for r in R:
    seq = L.letters(r['texte_leiden'] or '')
    words, cur = [], []
    for c, st in seq:
        if st in (' ', '/'):
            if cur:
                words.append(cur); cur = []
            continue
        if st in ('/w', 'S'):
            continue
        cur.append((c, st))
    if cur:
        words.append(cur)
    keep = {_stem(f['nom']) for f in (r['faux_consuls'] or [])}
    cn = set()
    for c in (r['consuls_table'] or []):
        cn.add(re.sub(r'\s*\d+$', '', c['consul identifié (itération)']))
    for y in (r['annee'], r['annee'] - 1):
        for t in re.findall(r'[A-Z][a-z]+', FAST.get(str(y), '')):
            if t not in ('Aug', 'Caes', 'Occident', 'II', 'III', 'IV'):
                cn.add(t)
    stems = {_stem(x) for x in cn} - keep
    toks = [(''.join(c for c, _ in wd), any(st == 'R' for _, st in wd)) for wd in words]
    skip = set()
    for k, (t, _) in enumerate(toks):
        nt = _norm(t)
        if t[:1].isupper() and any(difflib.SequenceMatcher(None, nt[:len(sm)], sm).ratio() >= 0.75 for sm in stems if len(sm) >= 4):
            skip.add(k)
            for b in (1, 2):
                if k - b >= 0 and _norm(toks[k - b][0]).startswith(tuple(_norm(g) for g in GENT_CONS)):
                    skip.add(k - b)
    for k, (t, part) in enumerate(toks):
        if k in skip or len(t) < 3 or not t.isalpha() or GREEK.search(t):
            continue
        if not (t[0].isupper() and t[1:].islower()):
            continue   # sigles, chiffres romains, fragments en capitales
        if _norm(t) in {_norm(x) for x in STOPW} or MONTHS.match(t):
            continue
        names[t].add('%d%s' % (r['n'], '*' if part else ''))
def _nk(x):
    return (int(x.rstrip('*')), x)
w('index_noms.tex', '\\begin{multicols}{3}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %s %s\\par' % (esc(k), ', '.join(sorted(v, key=_nk))) for k, v in sorted(names.items())) + '\\end{multicols}')
gr = collections.defaultdict(set)
for g in LS['graphies']:
    gr['%s pour %s' % (g['grave'], g['attendu'])] |= set(g['notices'])
w('index_graphies.tex', '\\begin{multicols}{2}\\footnotesize\\setlength{\\parindent}{0pt}\\raggedright\n' + '\n'.join('\\hangindent=1em %s gravé : %s\\par' % (esc(k), nl(v)) for k, v in sorted(gr.items())) + '\\end{multicols}')


# ------------------------------------------------------------------ répertoire des graphies
def corr_word(word):
    """Forme développée d'un mot portant des corrections <a=B> : lettres attendues entre ⸢ ⸣."""
    word = re.sub(r'<([^=<>]*)=([^<>]*)>', lambda m: '⸢%s⸣' % m.group(1), word)
    word = re.sub(r'[\[\]{}()/]|\(\?\)', '', word)
    return word
rep = []
for g in LS['graphies']:
    if g['occ'] < 2:
        continue
    pat = re.compile(r'[^\s/]*<%s=%s>[^\s/]*' % (re.escape(g['attendu']), re.escape(g['grave'])))
    ex = []
    for n in g['notices']:
        m = pat.search(BYN[n]['texte_leiden'])
        if m:
            ex.append('\\lat{%s} (%d)' % (esc(corr_word(m.group(0))), n))
        if len(ex) >= 12:
            break
    ph = (' (%s)' % g['phen']) if g['phen'] else ''
    rep.append('\\subsection*{%s gravé pour \\textit{%s}%s}\n\\noindent Occurrences : %d dans %d notices ; par période (ensemble A, année de classement) : %s.\\par\n'
               '\\noindent Exemples (forme développée, lettre attendue entre demi-crochets) : %s.\\par\n\\noindent{\\small Notices : %s.}\\par\\medskip'
               % (esc(g['grave']), esc(g['attendu']), esc(ph), g['occ'], len(g['notices']),
                  ' ; '.join('%s : %d' % (PERL[k], g['per'][k]) for k in range(4)), ' ; '.join(ex), nl(g['notices'])))
w('repertoire_graphies.tex', '\n'.join(rep))

# ------------------------------------------------------------------ statistiques complémentaires
open(os.path.join(G, 'stats_extra.tex'), 'w', encoding='utf-8').write(''.join(
    '\\expandafter\\def\\csname st@%s\\endcsname{%s}\n' % (k, v) for k, v in S.items() if k.startswith('js')))
print('ok', len(lat), 'formes latines', len(names), 'noms')
