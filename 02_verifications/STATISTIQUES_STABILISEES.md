# Statistiques recalculées sur les lectures stabilisées (lot 3)

Script : `05_scripts/stats_stabilisees.py` ; données : `collation_edcs_edb.csv` et base v2.0.

**Définition.** Une lecture est dite *stabilisée* quand le texte EDCS de la v2.0 et le texte de l'EDB concordent, aux conventions de notation près (statut « concordant »). Elle n'est pas pour autant **validée** : les deux bases dépendent de l'ICVR, et aucune n'a été contrôlée ici sur l'édition imprimée ni sur la pierre.

| Mesure | Valeur | Dénominateur |
|---|---|---|
| Notices | 478 | — |
| Textes distincts après fusion des doublons 106→120, 282→288, 329→336 | **475** | 478 |
| Lectures stabilisées | **269** | 475 |
| Répartition par décennie (393/394 comptés une fois) | 340s : 16 ; 350s : 10 ; 360s : 46 ; 370s : 48 ; 380s : 68 ; 390s : 59 ; 400–403 : 22 | 269 |
| *in pace* présent dans le texte EDB, hors cas où le mot est entièrement entre crochets (mesure approximative) | 88 | 269 |
| Chrisme ou croix selon l'EDB | 26 | 269 |

## Limites

- Les 206 autres textes ne sont pas « faux ». Ils présentent un écart à examiner, n'ont pas encore été appariés, ou ne portent pas de numéro ICUR. Les en exclure introduit un **biais de sélection** : les textes longs et fragmentaires divergent plus souvent. Ces chiffres servent de **contrôle de robustesse**, non de résultats définitifs.
- Les statistiques de la v2.0 sur l'ensemble du corpus restent les seules exhaustives. Elles doivent être republiées accompagnées de ce contrôle, et recalculées après arbitrage des écarts.
