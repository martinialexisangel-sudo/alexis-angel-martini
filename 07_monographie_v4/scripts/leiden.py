"""Analyse des textes en notation EDCS (Leyde) : statut de chaque lettre.

Statuts : L lue ; A développement d'abréviation (entre parenthèses) ;
R restituée (entre crochets) ; C corrigée par l'éditeur (<a=B> : a attendu, B gravé) ;
S superflue (entre accolades, gravée mais écartée par l'éditeur).
Les séparateurs sont rendus par ' ' (espace) et '/' (changement de ligne).
"""
import re

GREEK = re.compile(r'[Ͱ-Ͽἀ-῿]')


def letters(text):
    """Renvoie une liste de (caractère, statut)."""
    out = []
    t = text or ''
    # un crochet fermant sans ouvrant initial : ce qui précède est restitué
    first_open = t.find('[')
    first_close = t.find(']')
    in_br = first_close != -1 and (first_open == -1 or first_close < first_open)
    in_par = False
    in_curly = False
    i = 0
    while i < len(t):
        ch = t[i]
        if ch == '<':
            m = re.match(r'<([^=>]*)=([^>]*)>', t[i:])
            if m:
                for c in m.group(1):
                    out.append((c, 'R' if in_br else 'C'))
                i += m.end()
                continue
        if ch == '[':
            in_br = True; i += 1; continue
        if ch == ']':
            in_br = False; i += 1; continue
        if ch == '(':
            m = re.match(r'\((!|\?)\)', t[i:])
            if m:
                i += m.end(); continue
            in_par = True; i += 1; continue
        if ch == ')':
            in_par = False; i += 1; continue
        if ch == '{':
            in_curly = True; i += 1; continue
        if ch == '}':
            in_curly = False; i += 1; continue
        if ch.isdigit() and in_br:
            i += 1; continue
        if ch == '/':
            prev = t[i-1] if i > 0 else ' '
            nxt = t[i+1] if i + 1 < len(t) else ' '
            internal = not prev.isspace() and not nxt.isspace() and nxt != '/' and prev != '/'
            out.append(('/', '/w' if internal else '/')); i += 1; continue
        if ch.isspace():
            out.append((' ', ' ')); i += 1; continue
        if ch.isalpha():
            if in_curly:
                st = 'S'
            elif in_br:
                st = 'R'
            elif in_par:
                st = 'A'
            else:
                st = 'L'
            out.append((ch, st))
        i += 1
    return out


def plain(seq, keep=('L', 'A', 'R', 'C')):
    """Chaîne normalisée (minuscules, u/v et i/j unifiés) avec positions."""
    s, pos = [], []
    for k, (c, st) in enumerate(seq):
        if st == '/w':
            continue
        if st in ('/', ' '):
            s.append(' '); pos.append(k)
        elif st in keep:
            c = c.lower().replace('v', 'u').replace('j', 'i')
            s.append(c); pos.append(k)
    return ''.join(s), pos


def find(seq, pattern):
    """Occurrences d'un motif (sur texte normalisé) ; renvoie, pour chacune, les statuts des lettres."""
    s, pos = plain(seq)
    res = []
    for m in re.finditer(pattern, s):
        sts = [seq[pos[j]][1] for j in range(m.start(), m.end()) if seq[pos[j]][1] not in (' ', '/')]
        k0, k1 = pos[m.start()], pos[m.end() - 1]
        multiline = any(seq[k][1] in ('/', '/w') for k in range(k0, k1 + 1))
        res.append({'match': m.group(0), 'statuts': sts, 'multiligne': multiline})
    return res


def classify(occ):
    """Classe une occurrence : 'ecrit', 'abrege', 'corrige', 'restitue'."""
    sts = set(occ['statuts'])
    if 'R' in sts:
        return 'restitue'
    if 'C' in sts:
        return 'corrige'
    if 'A' in sts:
        return 'abrege'
    return 'ecrit'


def best(occs):
    """Meilleur statut d'un texte (ordre : écrit > abrégé > corrigé > restitué)."""
    order = ['ecrit', 'abrege', 'corrige', 'restitue']
    cl = [classify(o) for o in occs]
    for o in order:
        if o in cl:
            return o
    return None


def ratio_restitue(seq):
    n = [st for c, st in seq if st in ('L', 'A', 'R', 'C')]
    return (sum(1 for x in n if x == 'R') / len(n)) if n else 0.0


def render(seq, i0=0, i1=None):
    """Reconstitue une notation lisible d'un segment : [restitué], (développé), ⸢corrigé⸣, {superflu}."""
    if i1 is None:
        i1 = len(seq)
    marks = {'R': ('[', ']'), 'A': ('(', ')'), 'C': ('⸢', '⸣'), 'S': ('{', '}')}
    out, cur = '', None
    for c, st in seq[i0:i1]:
        if st in (' ', '/', '/w'):
            out += ' ' if st == ' ' else (' /' if st == '/' else '/')
            continue
        k = st if st in marks else None
        if k != cur:
            if cur:
                core = out.rstrip(' /')
                out = core + marks[cur][1] + out[len(core):]
            if k:
                out += marks[k][0]
            cur = k
        out += c
    if cur:
        core = out.rstrip(' /')
        out = core + marks[cur][1] + out[len(core):]
    return re.sub(r'\s+', ' ', out).strip()


def extract(seq, pattern, after=0):
    """Premier passage correspondant au motif (texte normalisé), rendu en notation lisible."""
    s, pos = plain(seq)
    m = re.search(pattern, s)
    if not m:
        return ''
    k0 = pos[m.start()]
    k1 = pos[min(len(pos) - 1, m.end() - 1 + after)] + 1
    return render(seq, k0, k1)
