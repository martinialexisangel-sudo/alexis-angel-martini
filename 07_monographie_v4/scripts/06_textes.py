"""Blocs de texte des dossiers commentés : texte transmis (EDCS, état 2022) et texte de l'EDB, ligne à ligne."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from texutil import esc, edb_clean
import importlib.util
_spec = importlib.util.spec_from_file_location('cat', os.path.join(os.path.dirname(__file__), '03_catalogue.py'))
CAT = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(CAT)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'tex', 'generated', 'txt')
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(ROOT, 'data', 'corpus_v4.json'), encoding='utf-8'))
BYN = {r['n']: r for r in R}
DOSSIERS = CAT.DOSSIERS


def lines_block(lines):
    return '\\par\n'.join('\\lnum{%d}%s' % (i + 1, esc(t.strip())) for i, t in enumerate(lines) if t.strip())


for n in DOSSIERS:
    r = BYN[n]
    parts = ['% généré par scripts/06_textes.py']
    v = r['v35']
    meta = 'Année de classement : %s (%s%s). Références : %s. %s Support : %s Notice du catalogue p.~\\pageref{not:%d}.' % (
        r['annee'], esc(r['datation']), ' ; datation contestée' if r['contestee'] else '', CAT.refs(v), CAT.provenance(r), esc(CAT.support(r)), n)
    parts.append('\\dosmeta{%s}' % meta)
    parts.append('\\txtbloc{Texte transmis (EDCS, état 2022)}{%s}' % lines_block(r['v35']['f7']))
    for x in (r['edb_xml'] or []):
        t = edb_clean(x['text'] or '')
        ls = re.split(r'\s+/\s*|\s*//\s*|\s*\|\|\s*', t)
        parts.append('\\txtbloc{Texte de l’EDB (%s)}{%s}' % (esc(x['id']), lines_block(ls)))
    if not r['edb_xml'] and r['edb_texte']:
        t = edb_clean(r['edb_texte'])
        ls = re.split(r'\s+/\s*', t)
        parts.append('\\txtbloc{Texte de l’EDB (liste de résultats)}{%s}' % lines_block(ls))
    open(os.path.join(OUT, '%d.tex' % n), 'w', encoding='utf-8').write('\n'.join(parts) + '\n')
print('textes', len(DOSSIERS))
