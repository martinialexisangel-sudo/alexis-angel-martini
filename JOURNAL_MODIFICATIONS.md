# Journal des modifications

Les originaux ne sont jamais modifiés (`00_originaux/`, empreintes dans `SHA256SUMS`). Toute correction est proposée dans un fichier dérivé et justifiée dans `03_dossiers_anomalies/`.

## 2026-10-14 — lot 1

| # | Objet | Action | Fichier | Preuve |
|---|---|---|---|---|
| 1 | Originaux v2.0 | copie et empreintes SHA-256 | `00_originaux/` | — |
| 2 | Base v2.0 | export de 14 feuilles en CSV (lignes vides retirées) | `01_donnees/base_v2_csv/` | fichier xlsx original |
| 3 | Monographie v2.0 | extraction du texte (`pdftotext -layout`) | `01_donnees/monographie_v2.0_texte_extrait.txt` | PDF original |
| 4 | Collation EDCS/EDB | 295/478 notices appariées ; statuts par notice | `02_verifications/collation_edcs_edb.csv` | `02_verifications/edb/brut/*.json` |
| 5 | A006 (329/336) | doublon **certain**, établi par la bibliographie EDB10126 ; conservation à Ostie ; âge `L[X]V` partiellement restitué | dossiers § A | EDB10126 |
| 6 | A007 (106/120) | doublon **très probable** ; fusion proposée dans le n° 120 ; variante *c(iu)esq(it)*/*recessit* en apparat | dossiers § A | EDB13167 |
| 7 | A008 (282/288) | doublon **très probable** ; fusion proposée dans le n° 288 | dossiers § A | EDB11278 |
| 8 | A014 (439) | provenance **non établie** ; exclusion des analyses topographiques romaines ; variantes de lecture relevées | dossiers § B | EDB33162 |
| 9 | n° 38 | *Chr(isti)* (EDCS) = **chrisme** (EDB) ; traduction et codage religieux à corriger | dossiers § C | EDB17657 |
| 10 | n° 474 | lecture identique dans les deux bases ; séparation lecture / portée dogmatique / date | dossiers § C | EDB35329 |
| 11 | A016 | 8 notices sur 16 reçoivent de l'EDB une formule consulaire absente du texte EDCS ; 2 restent conjecturales | dossiers § D | fiches EDB citées |
| 12 | Dates | 4 divergences de date EDB/v2.0 signalées, non résolues | dossiers § D | fiches EDB citées |
| 13 | Signes chrétiens | 34 chrismes ou croix sur 295 notices collationnées, invisibles dans l'EDCS ; nouvelle catégorie de codage proposée | dossiers § E | `collation_edcs_edb.csv` |
| 14 | Document « État critique » (Drive) | audité : chiffres et citations incompatibles avec la base ; **à ne pas utiliser** | `03_dossiers_anomalies/AUDIT_ETAT_CRITIQUE.md` | base v2.0 |

**Corrections non appliquées au manuscrit lui-même.** Les sources LaTeX de la v2.0 ou de la v3.1 sont absentes : le PDF n'a pas été régénéré. Les corrections sont formulées pour être reportées.

## 2026-10-14 — lot 2 (reprise automatique, 04:04 UTC)

| # | Objet | Action | Fichier | Preuve |
|---|---|---|---|---|
| 15 | Collation EDCS/EDB | 435/478 notices appariées (265 concordantes, 133 à examiner, 37 divergentes) ; 21 restent à chercher, 22 sans n° ICUR | `02_verifications/collation_edcs_edb.csv` | `edb/brut/*.json` |
| 16 | A009 (313/314) | une fiche EDB (EDB39579), deux dépositions successives ; année de (b) = consulat **restitué** | dossiers § A | EDB39579 |
| 17 | A010 (393/394) | une fiche EDB (EDB39590) ; l'EDCS restitue davantage que l'EDB ; ne compter qu'une occurrence datée | dossiers § A | EDB39590 |
| 18 | Dates | 3 divergences supplémentaires (n° 40, 206, 328) ; n° 328 : 381 ou 390 selon la restitution | dossiers § D | fiches EDB citées |
| 19 | A016 | n° 123 et 326 : restitutions consulaires conjecturales de l'EDB ; n° 123 : lecture EDCS *obiit* contre EDB *[Lupicin]o et Iovi[no]* | dossiers § D | EDB24921, EDB24920 |
| 20 | Signes chrétiens | 45 chrismes ou croix sur 435 notices (10,3 %) | dossiers § E | `collation_edcs_edb.csv` |

## 2026-10-14 — lot 3 (reprise automatique, 05:16 UTC)

| # | Objet | Action | Fichier | Preuve |
|---|---|---|---|---|
| 21 | Collation EDCS/EDB | parcours des listes EDB terminé pour les 462 n° ICUR du corpus : 440 notices appariées (269 concordantes, 134 à examiner, 37 divergentes) | `02_verifications/collation_edcs_edb.csv` | `edb/brut/*.json` ; `edb/manual_rows.csv` |
| 22 | 16 n° ICUR II (4798–4836, 4948, 5711–5712) | absents de la liste publique EDB ; recherche par texte infructueuse ; cause non établie | `ETAT_COLLATION.md` | registre |
| 23 | Signes chrétiens | 46 chrismes ou croix sur 440 notices (10,5 %) | dossiers § E | `collation_edcs_edb.csv` |
| 24 | Statistiques stabilisées | recalcul : 269 lectures stabilisées | `STATISTIQUES_STABILISEES.md` | script |

## 2026-10-14 — lot 4

| # | Objet | Action | Fichier | Preuve |
|---|---|---|---|---|
| 25 | Fiches EDB détaillées | 15 fiches ouvertes (dimensions, support, notes d'éditeur, photos signalées) | `02_verifications/edb/fiches/` | fiches EDB |
| 26 | A007, A008 | doublons 106/120 et 282/288 **certains** (EDH HD030246, HD021839) | dossiers § A | dump EDH |
| 27 | A010 (393/394) | deux fragments d'une même plaque (lecture de Ferrua citée par l'EDB) → fusion | dossiers § A | EDB39590 |
| 28 | A009 (313/314) | note EDB : le frère est mort **avant** → restitution 390 contradictoire ; datation de (b) incertaine | dossiers § A | EDB39579 |
| 29 | n° 98 | **hors corpus** : consul lu Severinus (461/482) ; *Dagalaiphi* restitué | dossiers § F | EDB20076, EDH HD028015 |
| 30 | Notices sans ICUR | 13 retrouvées (EDB/EDH), 6 non trouvées ; n° 369 conservé à Valencia : provenance non établie | dossiers § F | `mapping_extra.csv` |
| 31 | Collation | 456/478 notices appariées (281 concordantes, 137 à examiner, 38 divergentes) | `collation_edcs_edb.csv` | — |
| 32 | Corpus | 473 textes distincts datés de 340–403 | dossiers § F | — |

## 2026-10-14 — lot 5

| # | Objet | Action | Fichier | Preuve |
|---|---|---|---|---|
| 33 | Consuls lus / restitués | classement de 462 notices à datation directe selon l'état des lettres (gravé, restitué, développé) ; 38 cas relus à la main | `02_verifications/consuls_lus_restitues.csv`, `consuls_revue_manuelle.csv` | `05_scripts/consuls_lus_restitues.py` |
| 34 | Faux consuls de la v2.0 | 30 noms de personnes (défunts, dédicants, apôtre Paul…) comptés comme consuls dans 29 notices ; l'année n'est pas affectée | `02_verifications/consuls_faux_positifs_v2.csv` | forme citée du texte EDCS |
| 35 | Datations par restitution | sur 457 textes à datation directe : A 338, B 97, C 2, R 20 ; liste des 20 textes datés par restitution | dossiers § G | idem |
| 36 | Consuls lus omis par la v2.0 | n° 53, 155, 309, 423, 450, 456, 476 | dossiers § G | texte EDCS |
| 37 | Script du cahier | `05_scripts/build_cahier.sh` versé au dépôt (pandoc + Chromium) | — | — |
| 38 | Divergences fortes | 33 fiches EDB détaillées ouvertes (36 fiches pour 38 notices) ; analyse notice par notice | `02_verifications/edb/divergences_fortes_fiches.csv` | `edb/fiches/fiches_lot5_*.json` |
| 39 | Datations | n° 52 : 333/358 (CLRE p. 631, Dalmatius) ; n° 431 : 398 (CLRE p. 661) contre 399 ; n° 165 : 372 conjectural (Ferrua) ; n° 220 : 381 incertain | dossiers § D et § H | EDB17462, EDB27849, EDB40555, EDB30687 |
| 40 | Textes à vérifier sur l'ICVR | n° 306 (ligne *virgo ancilla dei* absente de l'EDB), n° 378 (formule consulaire absente des 3 fragments EDB) | dossiers § H | EDB27045 ; EDB25348, 25442, 42793 |
| 41 | 6 notices introuvables | page EDB 2069 lue (sans résultat) ; EDCS (nouvelle adresse) lue : aucune équivalence ICUR ; EDH : aucune correspondance | dossiers § F | `02_verifications/edcs/*.json` |
