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
