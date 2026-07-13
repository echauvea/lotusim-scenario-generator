# Index documentaire LSG

Cet index est la source unique d’inventaire documentaire du dépôt **LSG — LOTUSim Scenario Generator**.

## Statuts employés

- **Courant** : version à utiliser dans le dépôt à ce jour.
- **Brouillon** : document en cours de validation ou de stabilisation.
- **Expérimental** : essai non normatif qui ne remplace pas le référentiel courant.
- **Archivé** : version conservée pour traçabilité, à ne pas utiliser comme référence courante.
- **Normatif** : source de vérité dans son périmètre, sous réserve du statut de validation indiqué.
- **Informatif** : documentation, contexte, historique ou instruction sans autorité métier propre.

## Documents courants et référentiels

| Document | Version déclarée | Statut | Autorité | Rôle et observations |
|---|---:|---|---|---|
| [Architecture LSG](architecture/LSG_Architecture_v3.2.md) | v3.2 | Proposition courante, à valider conjointement | Informatif jusqu’à validation | Architecture globale de génération, exécution et arbitrage. Les documents amont `lsga-architecture-v2.md` et `rig-e2e.md` cités par la source ne sont pas présents dans ce dépôt. |
| [DEM-1 — Semantic Design Rules](dem/DEM-1_Semantic_Design_Rules_v0.2.md) | v0.2 | Brouillon courant | Normatif pour la méthode | Consolidation complète de v0.1 et de SDR-11 ; fixe les règles de conception sémantique. |
| [DEM-2 — Task Catalog Specification](dem/DEM-2_Task_Catalog_Specification_v0.2.md) | v0.2 | Brouillon courant | Normatif pour la méthode | Métamodèle du Task Catalog, rendu cohérent avec DEM-1 au strict nécessaire. |
| [Naval Maritime Ontology](../references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl) | 2.0.0-draft | Brouillon courant | Normatif pour les concepts, types, capacités, équipements et relations structurelles | La version interne et le nom de fichier sont cohérents. |
| [Mission Catalog](../references/mission-catalog/LOTUSim_Mission_Catalog_v1.0.3.md) | 0.7.0 dans le document / v1.0.3 dans le nom | Courant, version à confirmer | Normatif pour les missions et objectifs | Incohérence de version non corrigée afin de ne pas modifier silencieusement le référentiel métier. |
| [Task Catalog](../references/task-catalog/LOTUSim_Task_Catalog_v0.5.3.md) | 0.3.4 dans le document / v0.5.3 dans le nom | Baseline synchronisée courante, version à confirmer | Normatif pour les tâches avant enrichissement sémantique | Incohérence de version non corrigée afin de ne pas modifier silencieusement le référentiel métier. |

## Travaux en cours

| Document | Version déclarée | Statut | Autorité | Rôle et observations |
|---|---:|---|---|---|
| [Task Catalog — semantics pilot](../work-in-progress/task-semantics/LOTUSim_Task_Catalog_v0.6.0-semantics-pilot.md) | v0.6.0 | Expérimental | Non normatif | Pilote sémantique limité, notamment sur Navigate, Follow et Escort. Ne remplace pas la baseline courante. Son métamodèle doit être réaligné avec DEM-1/DEM-2 avant promotion. |

## Archives DEM

| Document | Version | Statut | Autorité | Motif d’archivage |
|---|---:|---|---|---|
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par DEM-1 v0.2. |
| [Mise à jour SDR-11](archive/dem/DEM-1_SDR11_update_merged_into_v0.2.md) | sans version autonome | Archivé, fusionné | Non normatif | Contenu intégré dans DEM-1 v0.2. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par DEM-2 v0.2. |
| [DEM-2 v0.2 avant revue de cohérence](archive/dem/DEM-2_Task_Catalog_Specification_v0.2-pre-consolidation.md) | v0.2 | Archivé, état antérieur | Non normatif | Instantané conservé pour rendre relisible le diff des compléments apportés à la version courante. |
| [DEM Part 1 — Task Semantics & State Model](archive/dem/DEM_Part1_Task_Semantics_State_Model_v0.1.md) | v0.1 | Archivé | Non normatif | Ancien document composite. Ses décisions utiles sont réparties entre DEM-1 et DEM-2 ; aucun Task Semantics Catalog séparé ne doit être recréé. |

## Documents de gouvernance et de support

| Document | Version | Statut | Autorité | Rôle |
|---|---:|---|---|---|
| [README racine](../README.md) | non versionné | Courant | Informatif | Présentation du dépôt, responsabilités, chaîne de dérivation, arborescence et statuts. |
| [Documentation WIDOCO](../docs/index.html) | 2.0.0-draft | Générée | Informatif | Représentation HTML, WebVOWL et sérialisations RDF de la Naval Maritime Ontology, publiée par GitHub Pages. |

## Artefacts prévus mais absents

| Artefact | Statut attendu | Dépendances |
|---|---|---|
| State Model | À dériver, non créé | Relations pertinentes de l’ontologie, préconditions/objectifs des missions, lectures/effets des tâches. |
| HDDL Domain / Problems | À dériver, non créés | State Model stabilisé et règles de projection. |
| Schémas, validateurs et benchmarks | À planifier | Métamodèles et référentiels stabilisés. |

## Résultats de l’audit de consolidation

- Les 66 identifiants de mission `MC-001` à `MC-066` sont présents et les 64 identifiants de tâche `TC-001` à `TC-064` sont présents, sans doublon d’en-tête détecté.
- Le Mission Catalog porte les traces d’une mise à jour partielle : les spécifications `MC-034` à `MC-066` apparaissent après les sections de changements et de points ouverts, et la numérotation des sections de changements n’est pas monotone.
- Le Task Catalog courant conserve un historique de versions non monotone (`0.2.0`, `0.3.0`, `0.3.1`, `0.3.2`, `0.3.3`, `0.3.4`) et une version de schéma d’exemple `0.3.0`; cela ne constitue pas en soi une nouvelle version courante.
- Le pilote v0.6.0 reprend les 64 tâches de la baseline et ajoute principalement le métamodèle sémantique ainsi que quatre blocs de sémantique de signature pour Navigate (deux signatures), Follow et Escort. Il s’agit donc d’un enrichissement partiel, pas d’un catalogue entièrement sémantisé.
- L’architecture v3.2 cite encore Mission Catalog v0.3.1 et Task Catalog v0.3, antérieurs aux versions visibles dans les référentiels présents. Ces références n’ont pas été actualisées tant que les versions faisant autorité ne sont pas confirmées.
- La version d’architecture fournie comme source courante contient deux liens vers LSGA v2 et un lien vers `rig-e2e.md`, alors que ces fichiers sont absents du dépôt. Ils sont conservés tels quels dans le document source et restent donc à résoudre.

## Décisions humaines encore requises

1. Déterminer la version faisant autorité pour le Mission Catalog : `v1.0.3` (nom de fichier) ou `0.7.0` (en-tête).
2. Déterminer la version faisant autorité pour le Task Catalog courant : `v0.5.3` (nom de fichier) ou `0.3.4` (en-tête).
3. Valider le statut normatif futur de l’architecture v3.2, actuellement présentée comme proposition à valider conjointement.
4. Décider si les documents amont absents (`lsga-architecture-v2.md` et `rig-e2e.md`) doivent être intégrés au dépôt ou rester des références externes.
5. Arbitrer l’écart architectural entre LSGA v3.2, qui présente encore le Domain HDDL comme source de vérité de la doctrine, et DEM-1/DEM-2, qui imposent Ontology + Mission Catalog + Task Catalog comme sources métier normatives et HDDL comme artefact dérivé. Cette divergence n’a pas été corrigée silencieusement dans l’architecture.
6. Confirmer le traitement du pilote v0.6.0, dont certains candidats d’état et certaines formulations du métamodèle précèdent la stabilisation de DEM-1/DEM-2.
7. Après résolution des versions faisant autorité, remettre en ordre la structure et l’historique du Mission Catalog puis actualiser les versions citées par l’architecture, sans changer les identifiants `MC-*` ou `TC-*`.
