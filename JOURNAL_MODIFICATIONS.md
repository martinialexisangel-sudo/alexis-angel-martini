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
