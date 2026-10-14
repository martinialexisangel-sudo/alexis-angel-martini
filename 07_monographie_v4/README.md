# PRISME v4.0 — Épitaphes chrétiennes datées de Rome (340–403)

Monographie entièrement reconstruite à partir des données (refonte de la v3.5).
Les corrections y sont intégrées directement aux chapitres et aux notices.

## Construction

    ./build.sh        # données → statistiques → catalogue → tableaux → figures → PDF

Prérequis : Python 3 (matplotlib, PyEphem), XeLaTeX (TeX Live, polyglossia, fontspec),
polices Libertinus (fournies dans `fonts/`, OFL).

## Organisation

- `data/` : catalogue v3.5 extrait (`notices_v35.json`), fiches EpiDoc EDB (`edb_xml/`),
  fastes (`fastes.json`), données consolidées (`corpus_v4.json`), mesures (`stats.json`).
- `scripts/` : chaîne de production (00 à 06), analyse Leyde (`leiden.py`),
  commentaires de notices (`notes_v4.py`).
- `tex/` : `main.tex`, `prisme.sty`, chapitres, fichiers générés (`generated/`), figures.

Aucun chiffre n'est saisi à la main : le texte appelle `\st{clé}`, valeurs de `stats.json`.

## Format

17 × 24 cm, XeLaTeX, Libertinus ; environ 750 pages
(analyse ~190 p., dossiers commentés 47 textes, catalogue raisonné 478 notices, instruments).

## Limites déclarées

Lectures non collationnées sur les ICVR ni sur les monuments ; fastes non collationnés sur la CLRE ;
études citées vérifiées comme notices, non lues (statuts dans la bibliographie).
