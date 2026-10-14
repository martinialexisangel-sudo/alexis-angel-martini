# Scripts de collation EDCS/EDB

- `edb_parse.py DIR OUT.csv` : extrait les lignes des pages de résultats EDB archivées (JSON du relais de lecture) ; fusionne `manual_rows.csv`.
- `edb_plan.py DIR` : estime les pages EDB à lire pour les numéros ICUR non encore appariés (interpolation sur les bornes lues ; `anchors_extra.csv`).
- `compare.py DIR OUT.csv` : apparie notices v2.0 et fiches EDB, calcule un score de similarité et un statut de tri.
- `surplus.py DIR` : relève les mots présents dans le texte EDB et absents du texte EDCS (à revoir manuellement).
- `registre.py DIR OUT.csv` : produit le registre des consultations.
- `ingest.sh` : enchaîne ces étapes dans l'environnement de travail (chemins propres à la session ; à adapter).

Les chemins absolus de l'environnement de travail sont codés en dur ; remplacer par les chemins locaux avant réemploi.
