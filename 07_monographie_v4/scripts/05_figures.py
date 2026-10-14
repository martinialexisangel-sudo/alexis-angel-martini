#!/usr/bin/env python3
"""PRISME v4.0 — figures (PDF vectoriels) calculées depuis data/stats.json et data/corpus_v4.json."""
import json, os, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIG = os.path.join(ROOT, 'tex', 'figures')
os.makedirs(FIG, exist_ok=True)
for f in os.listdir(os.path.join(ROOT, 'fonts')):
    if f.endswith('.otf'):
        font_manager.fontManager.addfont(os.path.join(ROOT, 'fonts', f))
plt.rcParams.update({'font.family': 'Libertinus Serif', 'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#555555', 'axes.linewidth': 0.6, 'xtick.color': '#333333', 'ytick.color': '#333333',
                     'axes.titlesize': 9.5, 'figure.dpi': 150, 'pdf.fonttype': 42})
RED, DARK, MID, LIGHT, PALE = '#7a1e1e', '#3d3d3d', '#8c8c8c', '#c4bfb7', '#e6e1d8'
ST = json.load(open(os.path.join(ROOT, 'data', 'stats.json'), encoding='utf-8'))
S, LS = ST['S'], ST['L']
R = json.load(open(os.path.join(ROOT, 'data', 'corpus_v4.json'), encoding='utf-8'))
C = [r for r in R if r['inC']]


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.pdf'), bbox_inches='tight')
    plt.close(fig)


# 1. années de classement par fondement de la datation
cats = [('directe : nom consulaire lu', 'nom consulaire lu', DARK),
        ('directe : lecture partielle d’un nom consulaire', 'lecture partielle', MID),
        ('directe : consulat restitué|directe : initiales consulaires', 'restitué ou initiales', LIGHT),
        ('formule transmise par l’EDB', 'formule transmise par l’EDB', RED),
        ('conjecturale|indirecte', 'conjecturale ou indirecte', PALE)]
years = list(range(340, 404))
fig, ax = plt.subplots(figsize=(6.3, 2.6))
bottom = [0] * len(years)
for keys, lab, col in cats:
    ks = keys.split('|')
    vals = [sum(1 for r in C if r['annee'] == y and any(r['datation'].startswith(k) for k in ks)) for y in years]
    ax.bar(years, vals, bottom=bottom, color=col, width=0.8, label=lab, edgecolor='white', linewidth=0.2)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_xlim(338.5, 404.5); ax.set_ylabel('Textes'); ax.set_ylim(0, max(bottom) * 1.45)
ax.legend(frameon=False, fontsize=7.5, ncol=3, loc='upper left')
save(fig, 'fig_annees')

# 2. in pace : catégories
ip = LS['inpace']
lab = ['en toutes lettres', 'abrégée', 'avec correction', 'restituée']
vals = [len(ip.get(k, [])) for k in ('ecrit', 'abrege', 'corrige', 'restitue')]
fig, ax = plt.subplots(figsize=(4.8, 1.7))
ax.barh(lab[::-1], vals[::-1], color=[PALE, LIGHT, MID, DARK], height=0.6)
for i, v in enumerate(vals[::-1]):
    ax.text(v + 1.5, i, str(v), va='center', fontsize=8.5)
ax.set_xlabel('Textes de l’ensemble C'); ax.set_xlim(0, max(vals) * 1.15)
save(fig, 'fig_inpace')

# 3. formulaire par période (attestations sans restitution)
sel = ['in pace', 'depositio / depositus', 'vixit (et variantes)', 'bene merenti', 'locus', 'coniux / compar / maritus / uxor', 'filius / filia', 'plus minus']
dens = [S['perC%d' % k] for k in range(4)]
fig, axes = plt.subplots(2, 4, figsize=(6.4, 3.2), sharey=True)
for ax, name in zip(axes.flat, sel):
    f = [x for x in LS['formulaire'] if x['element'] == name][0]
    pc = [100 * f['par_periode'][k] / dens[k] for k in range(4)]
    ax.plot(range(4), pc, color=RED, marker='o', markersize=3, linewidth=1)
    ax.set_title(name.split(' (')[0], fontsize=8, style='italic')
    ax.set_xticks(range(4)); ax.set_xticklabels(['340', '360', '375', '390'], fontsize=7)
    ax.set_ylim(0, 60)
axes[0][0].set_ylabel('% des textes'); axes[1][0].set_ylabel('% des textes')
fig.tight_layout()
save(fig, 'fig_formulaire')

# 4. âges
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.2))
a1.bar(range(9), LS['ages_classes'], color=DARK, width=0.75)
a1.set_xticks(range(9)); a1.set_xticklabels(['0–9', '10', '20', '30', '40', '50', '60', '70', '80+'], fontsize=7.5)
a1.set_title('Âges exprimés en années, par décennie'); a1.set_ylabel('Personnes')
a2.bar(range(10), LS['ages_terminaux'], color=[RED if i in (0, 5) else MID for i in range(10)], width=0.75)
a2.set_xticks(range(10)); a2.set_title('Chiffre terminal des âges de 20 ans et plus')
fig.tight_layout(); save(fig, 'fig_ages')

# 5. mois
M = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
tot = sum(LS['mois']); L_ = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
fig, ax = plt.subplots(figsize=(6.0, 2.1))
ax.bar(range(12), LS['mois'], color=[RED if i in (6, 7, 8) else MID for i in range(12)], width=0.75, label='observé')
ax.plot(range(12), [tot * l / 365.25 for l in L_], color=DARK, linewidth=0.8, linestyle='--', label='répartition proportionnelle')
ax.set_xticks(range(12)); ax.set_xticklabels(M, fontsize=7.5); ax.set_ylabel('Textes')
ax.legend(frameon=False, fontsize=7.5)
save(fig, 'fig_mois')

# 6. cimetières (EDB)
cem = [(k, v) for k, v in LS['cimetieres_C'] if v >= 4]
fig, ax = plt.subplots(figsize=(5.8, 3.0))
ks = [k for k, v in cem][::-1]; vs = [v for k, v in cem][::-1]
ax.barh(ks, vs, color=[LIGHT if k == 'origine incertaine' else DARK for k in ks], height=0.65)
for i, v in enumerate(vs):
    ax.text(v + 1, i, str(v), va='center', fontsize=7.5)
ax.tick_params(axis='y', labelsize=7.5); ax.set_xlabel('Textes de l’ensemble C')
save(fig, 'fig_cimetieres')

# 7. signes par période
sp = LS['signes_periode']
fig, ax = plt.subplots(figsize=(4.4, 1.9))
ax.bar(range(4), [100 * a / b for _, a, b in sp], color=RED, width=0.6)
for i, (_, a, b) in enumerate(sp):
    ax.text(i, 100 * a / b + 0.6, '%d/%d' % (a, b), ha='center', fontsize=7.5)
ax.set_xticks(range(4)); ax.set_xticklabels([p for p, _, _ in sp]); ax.set_ylabel('% des textes appariés')
save(fig, 'fig_signes')

# 8. parts restituées
fig, ax = plt.subplots(figsize=(4.6, 1.9))
lab = ['0 %', '1–24 %', '25–49 %', '50–74 %', '75–100 %']
ax.bar(lab, LS['classes_restit'], color=DARK, width=0.6)
for i, v in enumerate(LS['classes_restit']):
    ax.text(i, v + 2, str(v), ha='center', fontsize=7.5)
ax.set_ylabel('Textes')
save(fig, 'fig_restitution')
print('figures ok')
