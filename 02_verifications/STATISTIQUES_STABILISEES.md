# Statistiques recalculées sur les lectures stabilisées (lot 4)

Script : `05_scripts/stats_stabilisees.py` ; données : `collation_edcs_edb.csv` et base v2.0.

**Définition.** Une lecture est dite *stabilisée* quand le texte EDCS de la v2.0 et le texte de l'EDB concordent, aux conventions de notation près (statut « concordant »). Elle n'est pas pour autant **validée** : les deux bases dépendent de l'ICVR, et aucune n'a été contrôlée ici sur l'édition imprimée ni sur la pierre.

| Mesure | Valeur | Dénominateur |
|---|---|---|
| Notices | 478 | — |
| Textes distincts après fusion des doublons 106→120, 282→288, 329→336 et des fragments 393+394 | **474** (473 après exclusion du n° 98, daté de 461/482) | 478 |
| Lectures stabilisées | **279** | 474 |
| Répartition par décennie (393/394 comptés une fois) | 340s : 16 ; 350s : 10 ; 360s : 46 ; 370s : 49 ; 380s : 72 ; 390s : 64 ; 400–403 : 22 | 279 |
| *in pace* présent dans le texte EDB, hors cas où le mot est entièrement entre crochets (mesure approximative) | 94 | 279 |
| Chrisme ou croix selon l'EDB | 27 | 279 |

## Limites

- Les 195 autres textes ne sont pas « faux ». Ils présentent un écart à examiner, n'ont pas encore été appariés, ou ne portent pas de numéro ICUR. Les en exclure introduit un **biais de sélection** : les textes longs et fragmentaires divergent plus souvent. Ces chiffres servent de **contrôle de robustesse**, non de résultats définitifs.
- Les statistiques de la v2.0 sur l'ensemble du corpus restent les seules exhaustives. Elles doivent être republiées accompagnées de ce contrôle, et recalculées après arbitrage des écarts.
