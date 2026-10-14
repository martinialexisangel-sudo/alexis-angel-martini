# État de la collation EDCS / EDB (au 14 octobre 2026, lots 4-5)

## Méthode

1. **Source B, EDB.** Les listes publiques de l'EDB (`https://www.edb.uniba.it/search/quick/do?page=N`), triées par numéro ICVR, comptent 42 333 fiches sur 2 117 pages de 20 fiches. Chaque ligne donne l'ID EDB, le numéro ICVR, la bibliographie complémentaire, le rattachement topographique (*Pertinence*), le lieu de conservation, la date retenue par l'EDB et le texte. Le texte est parfois tronqué ; une mention « **More** » le signale.
2. **Accès.** Le conteneur de travail n'atteignait pas l'EDB directement. Les pages ont été lues par un relais de lecture web (Parallel Search, `web_fetch`) dont la réponse brute est archivée dans `edb/brut/*.json`. Le relais indique pour certaines pages une « date de publication » : c'est une estimation du relais, non une date de l'EDB.
3. **Appariement.** Les numéros ICUR de chaque notice viennent de la base v2.0 (champs « ICUR / refs catalogue » et « publications EDCS »). Quand plusieurs fiches EDB partagent un même numéro (sous-numéros a, b…), on retient la plus proche du texte EDCS. Le score est un `SequenceMatcher` calculé sur les textes normalisés : sigles et développements retirés, u/v et i/j unifiés.
4. **Classement automatique.**
   - *concordant* : score ≥ 0,92, écarts de notation seulement.
   - *écarts à examiner* : 0,75 ≤ score < 0,92.
   - *divergence forte ou appariement douteux* : score < 0,75. C'est souvent l'effet d'une troncature, d'un côté ou de l'autre.
   - Ces seuils servent au **tri**. Ils ne valent pas jugement philologique : chaque cas « à examiner » ou « divergence » doit être relu.

## Résultats chiffrés (478 notices)

| statut | notices |
|---|---|
| concordant (écarts mineurs de notation) | 281 |
| écarts à examiner | 137 |
| divergence forte ou appariement douteux | 38 |
| **appariées à une fiche EDB** | **456** |
| numéro ICUR absent de la liste publique EDB (voir ci-dessous) | 16 |
| sans numéro ICUR, non trouvée (EDB ni EDH) | 6 |

16 numéros ICUR se trouvent dans des plages déjà parcourues sans y figurer sous ce numéro : 4798, 4799, 4800, 4802, 4804, 4805, 4807, 4808, 4815, 4829, 4830, 4832, 4836, 4948, 5711 et 5712. La liste EDB saute par exemple de 4781 à 4900. Une recherche par texte (n° 202, *Cinnamius Opas lector tituli Fasciolae*) n'a rien donné. L'EDB indique dans son bandeau que certaines fiches ne sont pas publiques (« only selected records are publicly available online on the Vatican Museums website »). Il est possible que ces numéros, attribués à la basilique Saint-Paul dans la v2.0, en fassent partie : c'est une **hypothèse non vérifiée**. Les notices concernées sont les n° 12, 13, 25, 26, 45, 65, 116, 117, 149, 161, 202, 212, 374, 406, 407 et 452.

## Apports de l'EDB aux notices appariées

- **Rattachement topographique** (absent de 478/478 notices v2.0, anomalie A052). Exemples : *Coem. Commodillae* (41), *Basilica ss. Nerei et Achillei in coem. Domitillae* (27), *Coem. Domitillae* (15), *Coem. Pontiani* (8), basilique Saint-Pierre et aire *sub divo* (8)… ; *Incertae originis* : 159.
- **Lieu de conservation**, pour une partie des fiches : Musei Vaticani, Lapidario Cristiano (41) et Galleria Lapidaria (25) ; « Basilica ss. Nerei et Achillei in coem. Domitillae » (24) ; Musei Capitolini (10) ; « Museo Archeologico Nazionale » (10 ; libellé EDB reproduit tel quel) ; Collegio Teutonico (6) ; Ostia Antica, Lapidario (n° 336)…
- **Signes figurés** (chrisme, croix, oiseaux, palmes…), absents de l'EDCS (voir les dossiers, § E).
- **Lignes et parties absentes du texte EDCS de la v2.0**, dont des formules consulaires (dossiers, § D).
- **Restitutions différentes** de celles de l'EDCS. Exemple : le n° 73, *carmen* d'Eleuteria (363), où l'EDB restitue `[corpore namque tu]us spiritus … [est sociatu]s sanctis` là où l'EDCS donne `[at tuus in caelo] spiritus … [vivit cum] sanctis`. Ces deux restitutions sont **conjecturales** et produisent des lectures eschatologiques différentes : aucune ne doit être traduite comme acquise.

## Pour terminer la collation

- **Voie la plus sûre.** Télécharger hors de cet environnement le dépôt EpiDoc complet de l'EDB (Zenodo, DOI 10.5281/zenodo.3575485, CC BY 4.0, 73,8 Mo), puis apparier les 478 notices en local avec les scripts de `05_scripts/`, adaptés à l'EpiDoc.
- **Sinon.** Les listes ont été entièrement parcourues pour les numéros ICUR du corpus. Lot 5 : les fiches détaillées des 38 divergences fortes ont été ouvertes (dossiers, § H ; `edb/divergences_fortes_fiches.csv`). Restent à ouvrir les fiches des 137 notices « à examiner » dont le texte de liste est tronqué (« More »).
- **Dans tous les cas.** Les écarts substantiels doivent être tranchés sur l'**ICVR imprimée** (photographies et commentaires) : c'est la seule édition critique de référence pour ces textes.
