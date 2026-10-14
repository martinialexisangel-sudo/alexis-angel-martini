# PRISME — *Épitaphes chrétiennes datées de Rome (340–403)*

Dossier de consolidation scientifique du manuscrit d'Alexis Angel Martini.
Lot de travail du 14 octobre 2026.

## 1. Point de départ réel (à lire d'abord)

La mission visait « PRISME v3.1, 696 pages, 478 notices ». **Cette version n'a été trouvée ni dans ce dépôt (vide à l'ouverture), ni dans le Google Drive de l'auteur.** Les seuls fichiers PRISME accessibles sont les suivants :

| Fichier (Drive) | Contenu | Empreinte SHA-256 (copie dans `00_originaux/`) |
|---|---|---|
| `PRISME_MONOGRAPHIE_REVISEE.pdf` | « Version 2.0 révisée », 13 oct. 2026, **726 pages**, 478 notices | `9d1f9513…8ace7` |
| `PRISME_BASE_SCIENTIFIQUE_V2` (tableur) | base v2.0 : 14 feuilles, registre de 62 anomalies (A001–A062) | `3914ed18…9775` (export .xlsx) |
| « État critique de la recherche… » (Google Doc) | essai de 7 sections | non copié (voir `03_dossiers_anomalies/AUDIT_ETAT_CRITIQUE.md`) |

Les anomalies citées dans la mission (106/120, 282/288, 329/336, 313/314, 393/394, 439, 38, 474) sont exactement celles du registre de la v2.0 (A006–A010, A014, A039…). Le travail a donc porté sur la **v2.0**, et les corrections sont formulées pour être reportées dans la v3.1 si celle-ci en dérive. **Pour l'appliquer à la v3.1, déposez-la (PDF et, si possible, sources LaTeX) dans ce dépôt ou dans le Drive.**

## 2. Ce qui a été fait réellement dans ce lot

1. **Conservation des originaux.** Les fichiers sont copiés dans `00_originaux/` avec leurs empreintes (`SHA256SUMS`). Aucun original n'a été modifié.
2. **Extraction de la base v2.0** en CSV (`01_donnees/base_v2_csv/`) et du texte du PDF (`01_donnees/monographie_v2.0_texte_extrait.txt`).
3. **Collation base contre base : EDCS (texte de la v2.0) / EDB (Epigraphic Database Bari).** C'est la première confrontation systématique du corpus à une seconde base savante, indépendante de l'EDCS. L'EDB est rédigée à Bari à partir des ICVR et révisée par ses épigraphistes.
   - Méthode : lecture des listes de résultats de l'EDB triées par numéro ICVR (20 fiches par page), puis appariement par numéro ICUR et par similarité de texte. Les scripts sont dans `05_scripts/`.
   - État : voir `02_verifications/ETAT_COLLATION.md`. La collation est **partielle** ; le détail est donné ci-dessous.
4. **Dossiers d'anomalies** argumentés, avec preuves et degré de certitude : `03_dossiers_anomalies/DOSSIERS_ANOMALIES.md`.
5. **Registre des consultations** (URL, date, outil, résultat, échecs compris) : `02_verifications/REGISTRE_CONSULTATIONS.csv`.
6. **Journal des modifications** : `JOURNAL_MODIFICATIONS.md`.
7. **Contrôle « consul lu / consul restitué »** (lot 5) : fondement de l'année de chaque notice à datation directe, et relevé des faux consuls de la v2.0 (`02_verifications/consuls_lus_restitues.csv`, dossiers § G).
8. **Dossier de soumission** (grille d'évaluation sur 20, état des consignes d'éditeurs, projet de proposition) : `04_soumission/`.

## 3. Ce qui n'a PAS été fait (et pourquoi)

- **Aucune collation sur les ICVR imprimées, sur les photographies ou sur les pierres.** Les volumes ICUR n.s. ne sont pas en accès libre. Depuis ce conteneur, les sites EDCS, EDR, Internet Archive, Gallica, Persée, HathiTrust, JSTOR, Zenon, Crossref, WorldCat et KVK étaient **inaccessibles** (refus du proxy réseau ; voir le registre). Seule l'EDB a pu être lue, par un relais de lecture externe à débit limité.
- **Les fiches EDB détaillées** (dimensions, support, photographies, bibliographie complète) n'ont été ouvertes que pour quelques notices de test. Les listes ne donnent que : ID, n° ICVR, bibliographie complémentaire, cimetière, lieu de conservation, date, texte (parfois tronqué, mention « More »).
- **Le jeu de données EDB complet** (EpiDoc, CC BY 4.0, DOI 10.5281/zenodo.3575485, 73,8 Mo) a été identifié mais n'a pas pu être téléchargé : Zenodo est bloqué. Le télécharger hors de cet environnement permettrait de terminer la collation en une seule passe.
- **La réécriture intégrale des chapitres et la régénération du PDF de 726 pages** supposent les sources LaTeX et les scripts de la v2.0 (« déposés avec le manuscrit » selon la page de titre), qui ne sont pas dans le Drive.

## 4. Licences

Les extraits de l'EDB (`02_verifications/edb/`) sont publiés par l'EDB sous licence **CC BY-SA 4.0** (« The data related to the epigraphs are released under the CC-by-SA 4.0 license », pied de page de chaque fiche). Leur réutilisation exige l'attribution à l'Epigraphic Database Bari (Università di Bari) et le partage dans les mêmes conditions.
