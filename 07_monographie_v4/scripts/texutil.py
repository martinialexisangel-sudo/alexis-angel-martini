"""Utilitaires de composition LaTeX."""
import re

_SPECIAL = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '#': r'\#', '%': r'\%', '&': r'\&',
            '_': r'\_', '$': r'\$', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}


def esc(s):
    if s is None:
        return ''
    s = str(s)
    return ''.join(_SPECIAL.get(c, c) for c in s)


def md(s):
    """Échappe puis convertit *italique* en \\emph{}."""
    s = esc(s)
    s = re.sub(r'\*([^*]+)\*', r'\\emph{\1}', s)
    return s


def edb_clean(s):
    """Texte de l'EDB : signes de balisage interne omis, chevrons normalisés."""
    if not s:
        return s
    s = s.replace('〈', '⟨').replace('〉', '⟩').replace('%', '').replace('£', '')
    s = re.sub(r'\s*;\s*;\s*\*\*More\*\*', ' [texte tronqué dans la liste de résultats]', s)
    s = re.sub(r'\s*;\s*;\s*\[tronqué : More\]', ' [texte tronqué dans la liste de résultats]', s)
    s = s.replace('\\-', '-').replace('\\------', '------')
    return s.strip()


def fr_num(x):
    return str(x).replace('.', ',')


def join_fr(items, last=' et '):
    items = [i for i in items if i]
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + last + items[-1]
