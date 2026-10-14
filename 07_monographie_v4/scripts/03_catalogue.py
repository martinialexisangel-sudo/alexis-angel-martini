#!/usr/bin/env python3
"""PRISME v4.0 — génération du catalogue raisonné (tex/generated/catalogue.tex)."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texutil import esc, md, edb_clean, join_fr
from notes_v4 import NOTES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
R = json.load(open(os.path.join(ROOT, 'data', 'corpus_v4.json'), encoding='utf-8'))
ST = json.load(open(os.path.join(ROOT, 'data', 'stats.json'), encoding='utf-8'))
SIGNS = {int(k): v for k, v in ST['L']['signes'].items()}
BYN = {r['n']: r for r in R}
DOSSIERS = [4, 15, 22, 26, 36, 38, 43, 70, 72, 73, 110, 118, 126, 133, 134, 140, 151, 183, 202, 209, 214, 231, 232, 244, 249,
            268, 275, 287, 306, 311, 321, 324, 352, 378, 382, 387, 388, 393, 400, 405, 411, 433, 447, 458, 470, 474, 475]
EDH = {106: 'HD030246', 120: 'HD030246', 282: 'HD021839', 288: 'HD021839', 329: 'HD009698', 336: 'HD009698', 98: 'HD028015'}
PROFIL_LARGE = set(ST['L']['profil_large']); STRICT = set(ST['L']['profil_strict'])
RESTRICTIF = set(ST['L']['profil_restrictif'])

DROP = re.compile(r'v1\.0|v2\.0|\bv2\b|v3\.|version|3\.5|3\.1|anomalie|Anomalies du registre|\bA0\d\d\b|\bN00\d|codage historique|'
                  r'Contrôle v|catalogue de travail|relevé ne signale pas|Cette absence de codage|Commentaire développé|'
                  r'apparat dérivé|Statut du contrôle|^Base :|\bC1\b|\bC0\b|export de 2020 supprime|lettres sont restituées|'
                  r'lettres du texte transmis|Profil religieux du catalogue|cette révision|du manuscrit|dossier 35|chapitre \d|'
                  r'annexe|registre|hérité|historique|en attente|Lecture secondaire non collationnée|'
                  r'non collationné\)|Doublon probable|Rapprochement avec|regroupement|Unité documentaire partagée|'
                  r'Titulature v\(iri\) c\(larissimi\) des consuls|Genre :|Année non contrôlable|Texte majoritairement', re.I)


def sentences(s):
    s = (s or '').strip()
    if not s:
        return []
    parts = re.split(r'(?<=[.;])\s+(?=[A-ZÀ-ÖØ-Þ«(])', s)
    return [p.strip() for p in parts if p.strip()]


def keep(s):
    out = [x for x in sentences(s) if not DROP.search(x)]
    return ' '.join(out)


CEM_FR = None


def lvl_txt(s):
    if not s:
        return ''
    out = []
    for part in s.split(';'):
        part = part.strip()
        m = re.match(r'([^:]+):(\w+)', part)
        if not m:
            continue
        nm, stt = m.group(1).strip(), m.group(2)
        stt = {'lu': 'lu', 'partiel': 'lu en partie', 'restitué': 'restitué', 'initiale': 'initiale'}.get(stt, stt)
        out.append('%s (%s)' % (nm, stt))
    return join_fr(out)


def ensemble(r):
    if r['hors_periode']:
        return 'notice hors période : exclue des ensembles B et C'
    if r['fusionnee_dans']:
        return 'doublon fusionné dans le n° %d : exclue des ensembles B et C' % r['fusionnee_dans']
    if r['jointe_a']:
        return 'fragment joint au n° %d : exclu des ensembles B et C' % r['jointe_a']
    e = ['A', 'B'] + (['C'] if r['inC'] else [])
    return 'ensembles ' + ', '.join(e)


def fmt_dates(r):
    out = []
    for d in r['dates']:
        ev = d['événement (indice contextuel)']
        jul = d['date julienne']
        s = '%s : %s%s (%s)' % (ev if ev != 'indéterminé' else 'événement indéterminé',
                                esc(re.sub(r'\s+', ' ', d['expression'].replace('|', ' '))), (' = %s %s' % (jul, r['annee'])) if jul else '', d['certitude'])
        out.append(s)
    return out


def fmt_ages(r):
    fix = {}  # corrections appliquées dans 01_build_data.py
    out = []
    for p in r['ages']:
        p = dict(p); p.update(fix.get((r['n'], int(float(p['rang dans le texte']))), {}))
        bits = []
        for k, u in (('années', 'a.'), ('mois', 'm.'), ('jours', 'j.'), ('heures', 'h')):
            if p[k]:
                bits.append('%s %s' % (str(p[k]).replace('.0', ''), u))
        if bits:
            out.append(('env. ' if p['plus minus'] == 'True' else '') + ' '.join(bits) + ' (%s)' % p['certitude'])
    return out


def support(r):
    if not r['edb_xml']:
        return 'Non documenté dans les sources consultées.' if not r['edb_ids'] else 'La fiche EDB ne figure pas dans l’état 2019 des données EpiDoc ; support non documenté.'
    e = r['edb_xml'][0]
    bits = []
    obj = e['object']; mat = e['material']
    if obj or mat:
        bits.append(' de '.join(x for x in [obj.capitalize() if obj else 'Support', mat] if x))
    d = e['dims']
    if d.get('height') and d.get('width'):
        dd = ' × '.join(d[k] for k in ('height', 'width', 'depth') if d.get(k))
        bits.append('%s cm (h. × l.%s)' % (dd, ' × ép.' if d.get('depth') else ''))
    if e['execution']:
        bits.append('inscription %s' % e['execution'])
    if e['metrical']:
        bits.append('texte métrique')
    s = '. '.join(b[0].upper() + b[1:] for b in bits) + '.' if bits else 'Support non précisé par l’EDB.'
    if r['n'] in SIGNS:
        s += ' Signes décrits par l’EDB : %s.' % join_fr(SIGNS[r['n']])
    fac = collections.Counter(e['facsimile'])
    if fac:
        s += ' Reproductions signalées par l’EDB : %s (droits réservés ; non reproduites).' % join_fr(
            ['%s%s' % (k, (' ×%d' % v) if v > 1 else '') for k, v in fac.items()])
    if e['editors']:
        s += ' Fiche EDB : %s%s.' % (join_fr(e['editors']), (', première version %s' % e['first_version'][:4]) if e['first_version'] else '')
    return s


def provenance(r):
    out = []
    if r['provenance_douteuse']:
        out.append(r['provenance_douteuse'][0].upper() + r['provenance_douteuse'][1:] + '.')
    if r['edb_pertinence']:
        p = r['edb_pertinence'].strip()
        out.append('Rattachement selon l’EDB : \\emph{%s}%s.' % (esc(p), ' (le volume I des ICVR réunit les inscriptions dont la provenance est perdue)' if p.startswith('Incertae') else ''))
    else:
        out.append('Rome (indication de l’EDCS) ; aucun rattachement cimétérial transmis.')
    if r['edb_conservation']:
        out.append('Conservation selon l’EDB : \\emph{%s}.' % esc(r['edb_conservation']))
    return ' '.join(out)


def temoins(r, v):
    out = []
    t20 = v['f8']
    m = re.search(r'Export 2020 : (.*)$', t20)
    if m and 'Pas de divergence' not in t20:
        out.append('Export EDCS de 2020 : \\emph{%s}.' % esc(m.group(1).rstrip('.')))
    if r['edb_texte'] and not r['fusionnee_dans'] and not r['jointe_a']:
        stt = r['edb_statut_v4'] or ''
        if stt.startswith('concordant après'):
            out.append('EDB (%s) : même texte ; les écarts relevés dans la liste de résultats tiennent à la notation (relecture de la fiche détaillée).' % ', '.join(r['edb_ids']))
        elif stt.startswith('concordant'):
            out.append('EDB (%s) : texte concordant aux conventions de notation près (indice de similarité %s).' % (', '.join(r['edb_ids']), str(r['edb_similarite'])[:5].replace('.', ',')))
        else:
            lab = 'écarts à examiner' if stt.startswith('écarts') else 'divergence forte'
            out.append('EDB (%s ; %s) : \\emph{%s}.' % (', '.join(r['edb_ids']), lab, esc(edb_clean(r['edb_texte']))))
    elif not r['edb_ids']:
        out.append('Aucune fiche EDB appariée (%s).' % ('numéro ICUR absent de la liste publique de l’EDB' if (r['edb_statut'] or '').startswith('absent') else 'pas de numéro ICUR ; recherche par le texte infructueuse' if r['edb_statut'] else 'pas d’appariement'))
    n = NOTES.get(r['n'], {})
    if r['div_forte'] and not (n.get('temoins') or n.get('chrono') or n.get('fusion') or n.get('relig')):
        c = r['div_forte'].get('constat (fiche EDB détaillée, lue le 14/10/2026)') or ''
        if c and not c.startswith('Déjà'):
            out.append('Relecture de la fiche détaillée de l’EDB : ' + esc(c.rstrip('.')) + '.')
    if n.get('temoins'):
        out.append(md(n['temoins']))
    if n.get('fusion'):
        out.append(md(n['fusion']))
    for a in r['absorbe'] + r['joint']:
        out.append('Absorbe la notice %d (voir cette notice).' % a)
    return ' '.join(out)


def religion(r, v):
    out = []
    n = NOTES.get(r['n'], {})
    k = keep(v['f13'])
    if n.get('skip13'):
        k = ''
    if r['n'] in (38,):
        k = ''
    if r['n'] in (152,):
        k = 'Le catalogue antérieur relevait une allusion à la rédemption (*redemptum*, *redemptus*) ; la lecture *redemptus* est contestée par l’EDB (voir les témoins).'
        k = md(k)
    else:
        k = esc(k)
    if k:
        out.append(k)
    if n.get('relig'):
        out.append(md(n['relig']))
    if r['n'] in SIGNS and r['n'] not in (38, 140, 151, 311, 400, 73) and r['edb_xml']:
        pass  # signes déjà décrits au champ Support
    elif r['n'] in SIGNS and not r['edb_xml']:
        out.append('L’EDB transcrit les signes suivants : %s.' % join_fr(SIGNS[r['n']]))
    if r['n'] in PROFIL_LARGE:
        prof = 'profil strict' if r['n'] in STRICT else ('profil restrictif' if r['n'] in RESTRICTIF else 'profil large seulement')
        out.append('Désignation divine : retenue dans le %s.' % prof)
    if r['n'] in DOSSIERS:
        out.append('Commentaire développé : dossier p.~\\pageref{dos:%d}.' % r['n'])
    return ' '.join(out)


def chrono(r, v):
    out = []
    lt = lvl_txt(r['consuls_lecture'])
    if lt and not r['datation'].startswith('formule') and r['datation'] not in ('conjecturale', 'hors période'):
        out.append('Noms consulaires : %s.' % lt)
    if r['faux_consuls']:
        out.append('Ne sont pas des consuls : %s.' % '; '.join('%s (%s)' % (esc(f['forme']), esc(f['role'])) for f in r['faux_consuls']))
    if r['post_consulatum']:
        out.append('Datation par post-consulat.')
    n = NOTES.get(r['n'], {})
    if n.get('chrono'):
        out.append(md(n['chrono']))
    else:
        if r['contestee']:
            out.append(esc(r['contestee']))
        if r['edb_fautive']:
            out.append(esc(r['edb_fautive']))
        if r['datation'] == 'conjecturale' and r['datation_note']:
            out.append(esc(r['datation_note']))
    if r['alerte']:
        out.append('Réserve : ' + esc(r['alerte']))
    ds = fmt_dates(r)
    if ds:
        out.append('Dates du jour : ' + ' ; '.join(ds) + '.')
    ag = fmt_ages(r)
    if ag:
        out.append(('Âge déclaré : ' if len(ag) == 1 else 'Âges déclarés : ') + ' ; '.join(ag) + '.')
    return ' '.join(out)


def langue(v):
    s = keep(v['f11'])
    s = re.sub(r'\s*\(\s*\)', '', s)
    return esc(s)


ROM = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV'}


def normref(x):
    x = x.strip()
    x = re.sub(r'^ICUR-(\d\d), 0*(\d+)', lambda m: 'ICUR %s %s' % (ROM[int(m.group(1))], m.group(2)), x)
    x = re.sub(r'^CIL (\d\d), 0*(\d+)', lambda m: 'CIL %s %s' % (ROM[int(m.group(1))], m.group(2)), x)
    x = re.sub(r'^CIL (\d\d), \*0*(\d+)', lambda m: 'CIL %s *%s' % (ROM[int(m.group(1))], m.group(2)), x)
    x = re.sub(r'^ILCV 0*(\d+)', r'ILCV \1', x)
    x = re.sub(r'^ILCV \+0*(\d+)', r'ILCV +\1', x)
    x = re.sub(r'^AE (\d{4}), \+?0*(\d+)', r'AE \1, \2', x)
    x = re.sub(r'^SEG-(\d+), 0*(\d+)', r'SEG \1, \2', x)
    x = re.sub(r'^(\w+) 0+(\d)', r'\1 \2', x)
    return x


def refs_list(v):
    return [normref(x.strip().rstrip('.')) for x in v['f16'].split(';') if x.strip()]


def refs(v):
    return esc(' = '.join(refs_list(v)))


def biblio(r, v):
    s = esc(' ; '.join(refs_list(v)))
    if r['edb_bibl']:
        eb = [x.strip() for x in str(r['edb_bibl']).split(';') if x.strip()]
        s += ('. ' if s else '') + 'Bibliographie complémentaire selon l’EDB : ' + esc(' ; '.join(eb))
    return s.rstrip('.') + '.'


def statut(r):
    st = r['edb_statut_v4'] or ''
    if r['fusionnee_dans'] or r['jointe_a']:
        base = 'Témoin conservé pour la stabilité de la numérotation.'
    elif st.startswith('concordant'):
        base = 'Lecture secondaire (EDCS) concordante avec l’EDB : lecture stabilisée entre deux bases, non collationnée sur l’ICVR ni sur le monument.'
    elif st.startswith('écarts'):
        base = 'Lecture secondaire (EDCS) ; écarts avec l’EDB à arbitrer sur l’ICVR.'
    elif 'divergence' in st:
        base = 'Lecture secondaire (EDCS) ; divergence forte avec l’EDB : le texte ne doit pas être exploité sans contrôle de l’édition imprimée.'
    else:
        base = 'Lecture secondaire (EDCS) sans second témoin numérique.'
    if (r['ratio_restitue'] or 0) > .5:
        base += ' Plus de la moitié des lettres sont restituées.'
    if r['photo_edcs']:
        base += ' L’EDCS signale une photographie (non consultée).'
    return base


def notice(r):
    v = r['v35']; n = r['n']
    head_refs = re.sub(r'^EDCS-\d+ · ', '', '')
    first_icur = re.search(r'ICUR n\.s\. [IVX]+, \d+[a-z]?', v['f4'])
    hdr = []
    if first_icur:
        hdr.append(re.sub(r', 0+', ', ', first_icur.group(0)))
    hdr.append(r['edcs_id'])
    if r['edb_ids']:
        hdr.append(', '.join(r['edb_ids']))
    if n in EDH:
        hdr.append('EDH ' + EDH[n])
    year = str(r['annee']) if not r['hors_periode'] else '461/482'
    status_tag = r['datation']
    if r['contestee']:
        status_tag += ' ; datation contestée'
    L = []
    L.append('\\begin{notice}{%d}{%s}{%s}' % (n, year, esc(' · '.join(hdr))))
    L.append('\\label{not:%d}' % n)
    if r['fusionnee_dans'] or r['jointe_a']:
        tgt = r['fusionnee_dans'] or r['jointe_a']
        L.append('\\nf{Statut}{%s}' % md(NOTES.get(n, {}).get('fusion', 'Fusionnée dans le n° %d.' % tgt)))
        L.append('\\nf{Références}{%s}' % refs(v))
        L.append('\\ntext{%s}' % '\\\\\n'.join('\\lnum{%d}%s' % (i + 1, esc(t)) for i, t in enumerate(v['f7'])))
        L.append('\\nf{Traduction}{%s}' % esc(v['f10']))
        L.append('\\nf{Voir}{la notice %d (p.~\\pageref{not:%d}).}' % (tgt, tgt))
        L.append('\\end{notice}')
        return '\n'.join(L)
    L.append('\\nf{Datation}{%s — %s%s}' % (year, esc(status_tag), ('. ' + md(r['datation_note'])) if r['datation'].startswith('formule') and r['datation_note'] and not NOTES.get(n, {}).get('chrono') else ''))
    L.append('\\nf{Genre}{%s ; %s ; %s lettres transmises%s.}' % (esc(r['genre'][0].upper() + r['genre'][1:]), ensemble(r), r['nb_lettres'],
                                                                  (' ; %d \\%% restituées' % round(100 * r['ratio_restitue'])) if r['ratio_restitue'] else ''))
    L.append('\\nf{Références}{%s.}' % refs(v))
    L.append('\\nf{Provenance}{%s}' % provenance(r))
    L.append('\\nf{Support}{%s}' % esc(support(r)) if True else '')
    L.append('\\ntext{%s}' % '\\\\\n'.join('\\lnum{%d}%s' % (i + 1, esc(t)) for i, t in enumerate(v['f7'])))
    tm = temoins(r, v)
    if tm:
        L.append('\\nf{Témoins}{%s}' % tm)
    ap = re.sub(r'\s*\(apparat dérivé de la notation EDCS ; non collationné\)', '', v['f9']).strip()
    if ap and not ap.startswith('Aucune correction'):
        L.append('\\nf{Apparat}{%s}' % esc(ap))
    tr = NOTES.get(n, {}).get('trad') or v['f10']
    L.append('\\nf{Traduction}{%s}' % (md(tr) if NOTES.get(n, {}).get('trad') else esc(tr)))
    lg = langue(v)
    if lg:
        L.append('\\nf{Langue}{%s}' % lg)
    ch = chrono(r, v)
    if ch:
        L.append('\\nf{Chronologie}{%s}' % ch)
    rl = religion(r, v)
    if rl:
        L.append('\\nf{Commentaire}{%s}' % rl)
    L.append('\\nf{Bibliographie}{%s}' % biblio(r, v))
    L.append('\\nf{Statut}{%s}' % esc(statut(r)))
    L.append('\\end{notice}')
    return '\n'.join(L)


def main():
    out = ['% généré par scripts/03_catalogue.py — ne pas modifier']
    cur = None
    for r in R:
        y = r['annee']
        if y != cur and not r['hors_periode']:
            out.append('\\annee{%d}' % y); cur = y
        out.append(notice(r))
    os.makedirs(os.path.join(ROOT, 'tex', 'generated'), exist_ok=True)
    open(os.path.join(ROOT, 'tex', 'generated', 'catalogue.tex'), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print('notices', len(R))


if __name__ == '__main__':
    main()
