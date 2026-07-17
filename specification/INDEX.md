# Index documentaire LSG

Cet index est la source unique d’inventaire documentaire du dépôt **LSG — LOTUSim Scenario Generator**.

## Statuts employés

- **Courant** : version à utiliser dans le dépôt à ce jour.
- **Brouillon** : document en cours de validation ou de stabilisation.
- **Archivé** : version conservée pour traçabilité, à ne pas utiliser comme référence courante.
- **Normatif** : source de vérité dans son périmètre, sous réserve du statut de validation indiqué.
- **Informatif** : documentation, contexte, historique ou instruction sans autorité métier propre.

## Documents courants et référentiels

| Document | Version déclarée | Statut | Autorité | Rôle et observations |
|---|---:|---|---|---|
| [Architecture LSG](architecture/LSG_Architecture_v3.2.md) | v3.2 | Proposition courante, à valider conjointement | Informatif jusqu’à validation | Architecture globale de génération, exécution et arbitrage. Les documents amont `lsga-architecture-v2.md` et `rig-e2e.md` cités par la source ne sont pas présents dans ce dépôt. |
| [DEM-1 — Semantic Design Rules](dem/DEM-1_Semantic_Design_Rules_v0.6.md) | v0.6 | Brouillon courant | Normatif pour la méthode | Règles de conception sémantique, références d’état stables et tuples canoniques. |
| [DEM-2 — Task Catalog Specification](dem/DEM-2_Task_Catalog_Specification_v0.6.md) | v0.6 | Brouillon courant | Normatif pour la méthode | Métamodèle des signatures aligné sur le State Model normatif. |
| [DEM-3 — Method Catalog Specification](dem/DEM-3_Method_Catalog_Specification_v0.1.md) | v0.1 | Pilote courant | Normatif pour la méthode | Métamodèle des méthodes HTN, réseaux de sous-tâches, synchronisations et projection HDDL. |
| [Naval Maritime Ontology](../references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl) | 2.0.0-draft | Brouillon courant | Normatif pour les concepts, types, capacités, équipements et relations structurelles | La version interne et le nom de fichier sont cohérents. |
| [Mission Catalog](../references/mission-catalog/LOTUSim_Mission_Catalog_v1.0.4.md) | v1.0.4 | Courant, brouillon de travail | Normatif pour les missions et objectifs | Les 66 missions disposent d’une spécification active conforme au métamodèle canonique. |
| [Task Catalog](../references/task-catalog/LOTUSim_Task_Catalog_v0.12.0.md) | v0.12.0 | Courant, brouillon de travail | Normatif pour les tâches et leurs sémantiques | Les 32 signatures enrichies couvrent le noyau ISR, deux lots d’extension ISR et les familles Movement et Protection. |
| [Method Catalog](../references/method-catalog/LOTUSim_Method_Catalog_v0.1.0.md) | v0.1.0 | Pilote courant | Normatif pour les décompositions documentées | Deux méthodes Escort : garde rapprochée et escorte avec écran ; projection HDDL partielle. |
| [State Model — source normative](../references/state-model/LOTUSim_State_Model_v0.6.yaml) | v0.6.0 | Courant, brouillon de travail | Normatif pour les états dynamiques | 105 états, 23 types propres, producteurs, consommateurs, contraintes et traçabilité. |
| [State Model — spécification](state-model/LOTUSim_State_Model_Specification_v0.6.md) | v0.6 | Courant, brouillon de travail | Normatif pour le métamodèle | Catégories, politique d’identifiants, normalisations, cycle de vie et règles de validation. |

## Archives des catalogues

| Document | Version | Statut | Autorité | Motif d’archivage |
|---|---:|---|---|---|
| [Mission Catalog — avant consolidation](../references/mission-catalog/archive/LOTUSim_Mission_Catalog_v1.0.3.md) | v1.0.3 | Archivé | Non normatif | Version antérieure conservant les deux séries de missions incompatibles avant confirmation de l’inventaire canonique. |
| [Task Catalog baseline](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.5.3.md) | v0.5.3 dans le nom / 0.3.4 dans l’en-tête historique | Archivé | Non normatif | Baseline antérieure au pilote sémantique, remplacée successivement par v0.6.0 puis v0.6.1. |
| [Task Catalog — pilote initial](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.6.0.md) | v0.6.0 | Archivé | Non normatif | Remplacé par v0.6.1 après correction des anomalies révélées par le pilote sémantique. |
| [Task Catalog — pilote corrigé](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.6.1.md) | v0.6.1 | Archivé | Non normatif | Remplacé par v0.7.0 après stabilisation et affectation des Semantic Families au niveau signature. |
| [Task Catalog — Semantic Families](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.7.0.md) | v0.7.0 | Archivé | Non normatif | Remplacé par v0.8.0 après enrichissement du noyau ISR. |
| [Task Catalog — noyau ISR](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.8.0.md) | v0.8.0 | Archivé | Non normatif | Remplacé par v0.8.1 après alignement sur les identifiants du State Model v0.1. |
| [Task Catalog — noyau ISR aligné](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.8.1.md) | v0.8.1 | Archivé | Non normatif | Remplacé par v0.9.0 après enrichissement complet de la famille Movement. |
| [Task Catalog — famille Movement](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.9.0.md) | v0.9.0 | Archivé | Non normatif | Remplacé par v0.10.0 après enrichissement complet de la famille Protection. |
| [Task Catalog — famille Protection](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.10.0.md) | v0.10.0 | Archivé | Non normatif | Remplacé par v0.11.0 après le premier lot d’extension ISR consacré à la couverture et aux produits. |
| [Task Catalog — couverture et produits ISR](../references/task-catalog/archive/LOTUSim_Task_Catalog_v0.11.0.md) | v0.11.0 | Archivé | Non normatif | Remplacé par v0.12.0 après enrichissement de la caractérisation et de l’inspection. |

## Archives du State Model

| Document | Version | Statut | Autorité | Motif d’archivage |
|---|---:|---|---|---|
| [State Model — source normative initiale](../references/state-model/archive/LOTUSim_State_Model_v0.1.yaml) | v0.1.0 | Archivé | Non normatif | Remplacé par v0.2.0 après ajout des états et types nécessaires à la famille Movement. |
| [State Model — spécification initiale](state-model/archive/LOTUSim_State_Model_Specification_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par v0.2 après formalisation des règles Movement et des états géométriques dérivés. |
| [State Model — source Movement](../references/state-model/archive/LOTUSim_State_Model_v0.2.yaml) | v0.2.0 | Archivé | Non normatif | Remplacé par v0.3.0 après ajout des états, types et transitions nécessaires à la famille Protection. |
| [State Model — spécification Movement](state-model/archive/LOTUSim_State_Model_Specification_v0.2.md) | v0.2 | Archivé | Non normatif | Remplacé par v0.3 après formalisation des résultats de protection dérivés et du premier état de ressource. |
| [State Model — source Protection](../references/state-model/archive/LOTUSim_State_Model_v0.3.yaml) | v0.3.0 | Archivé | Non normatif | Remplacé par v0.4.0 après ajout des exigences de recherche/couverture et des produits ISR typés. |
| [State Model — spécification Protection](state-model/archive/LOTUSim_State_Model_Specification_v0.3.md) | v0.3 | Archivé | Non normatif | Remplacé par v0.4 après promotion de la couverture de zone et formalisation des relevés, cartes et mesures. |
| [State Model — source couverture et produits ISR](../references/state-model/archive/LOTUSim_State_Model_v0.4.yaml) | v0.4.0 | Archivé | Non normatif | Remplacé par v0.5.0 après ajout des états et types de caractérisation et d’inspection. |
| [State Model — spécification couverture et produits ISR](state-model/archive/LOTUSim_State_Model_Specification_v0.4.md) | v0.4 | Archivé | Non normatif | Remplacé par v0.5 après formalisation des produits de caractérisation et des constats d’inspection. |
| [State Model — source caractérisation et inspection](../references/state-model/archive/LOTUSim_State_Model_v0.5.yaml) | v0.5.0 | Archivé | Non normatif | Remplacé par v0.6.0 après ajout de l’affectation de route nécessaire aux méthodes Escort. |
| [State Model — spécification caractérisation et inspection](state-model/archive/LOTUSim_State_Model_Specification_v0.5.md) | v0.5 | Archivé | Non normatif | Remplacé par v0.6 après formalisation du premier besoin d’état issu du Method Catalog. |

## Archives DEM

| Document | Version | Statut | Autorité | Motif d’archivage |
|---|---:|---|---|---|
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par DEM-1 v0.2. |
| [Mise à jour SDR-11](archive/dem/DEM-1_SDR11_update_merged_into_v0.2.md) | sans version autonome | Archivé, fusionné | Non normatif | Contenu intégré dans DEM-1 v0.2. |
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.2.md) | v0.2 | Archivé | Non normatif | Remplacé par DEM-1 v0.3 après clôture du pilote sémantique. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par DEM-2 v0.2. |
| [DEM-2 v0.2 avant revue de cohérence](archive/dem/DEM-2_Task_Catalog_Specification_v0.2-pre-consolidation.md) | v0.2 | Archivé, état antérieur | Non normatif | Instantané conservé pour rendre relisible le diff des compléments apportés à la version courante. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.2.md) | v0.2 | Archivé | Non normatif | Version consolidée remplacée par DEM-2 v0.3 après stabilisation du métamodèle canonique. |
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.3.md) | v0.3 | Archivé | Non normatif | Remplacé par DEM-1 v0.4 après adoption de l’affectation familiale au niveau signature. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.3.md) | v0.3 | Archivé | Non normatif | Remplacé par DEM-2 v0.4 après ajout du métamodèle des familles et du schéma explicatif. |
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.4.md) | v0.4 | Archivé | Non normatif | Remplacé par DEM-1 v0.5 après introduction des sorties d’exécution et des règles de connaissance ISR. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.4.md) | v0.4 | Archivé | Non normatif | Remplacé par DEM-2 v0.5 après formalisation de la progression ISR. |
| [DEM-1 — Semantic Design Rules](archive/dem/DEM-1_Semantic_Design_Rules_v0.5.md) | v0.5 | Archivé | Non normatif | Remplacé par DEM-1 v0.6 après introduction des références d’état stables. |
| [DEM-2 — Task Catalog Specification](archive/dem/DEM-2_Task_Catalog_Specification_v0.5.md) | v0.5 | Archivé | Non normatif | Remplacé par DEM-2 v0.6 après alignement sur le State Model normatif. |
| [DEM Part 1 — Task Semantics & State Model](archive/dem/DEM_Part1_Task_Semantics_State_Model_v0.1.md) | v0.1 | Archivé | Non normatif | Ancien document composite. Ses décisions utiles sont réparties entre DEM-1 et DEM-2 ; aucun Task Semantics Catalog séparé ne doit être recréé. |

## Documents de gouvernance et de support

| Document | Version | Statut | Autorité | Rôle |
|---|---:|---|---|---|
| [README racine](../README.md) | non versionné | Courant | Informatif | Présentation du dépôt, responsabilités, chaîne de dérivation, arborescence et statuts. |
| [Validateur des référentiels](../tools/validation/validate_referentials.py) | non versionné | Courant | Contrôle automatisé | Vérifie les identifiants, références croisées, familles, types, états, bindings, méthodes HTN et principales règles DEM ; exécuté par la CI. |
| [Documentation WIDOCO](https://echauvea.github.io/lotusim-scenario-generator/) | 2.0.0-draft | Générée par CI | Informatif | Représentation HTML, WebVOWL et sérialisations RDF de la Naval Maritime Ontology, publiée par GitHub Pages sans fichiers générés suivis dans Git. |
| [État des lieux — Interfaçage LSG ↔ tsm](notes/2026-07-14-etat-des-lieux-interface-tsm.md) | 2026-07-14 | Note de coordination | Informatif | Constats sur la divergence du document d'architecture entre les deux dépôts et sur l'écart de vocabulaire entre `knowledge_base.json` (tsm) et le Task Catalog. Questions ouvertes à trancher avec Cyril Moron, non résolues dans ce document. |

## Artefacts prévus mais absents

| Artefact | Statut attendu | Dépendances |
|---|---|---|
| HDDL Domain / Problems | À dériver, non créés | State Model, Method Catalog et règles de projection stabilisés. |
| Schémas formels et benchmarks | À planifier | Métamodèles et référentiels stabilisés. Le premier validateur transversal est maintenant disponible. |

## Résultats de l’audit de consolidation

- Les 66 identifiants de mission `MC-001` à `MC-066` sont présents dans l’inventaire canonique et les 64 identifiants de tâche `TC-001` à `TC-064` sont présents, sans doublon d’en-tête détecté.
- Le Mission Catalog v1.0.4 contient 66 spécifications actives conformes au métamodèle. Les anciennes propositions incompatibles autrefois numérotées MC-039 à MC-066 sont conservées dans une annexe explicitement non normative.
- Le Task Catalog v0.12.0 reprend les 64 tâches et 79 signatures. Trente-deux signatures possèdent une sémantique complète ; les 47 autres restent à enrichir progressivement.
- Le State Model v0.6 contient 105 états normatifs, 23 types propres et 4 candidats de mission différés faute de producteurs sémantisés.
- Le Method Catalog v0.1.0 introduit deux méthodes pilotes pour Escort. Elles explicitent les sous-tâches concurrentes, leurs conditions et les décisions de reprise ; leur projection HDDL reste partielle.
- Le validateur transversal et sa CI contrôlent automatiquement les inventaires, la traçabilité, les Semantic Families et la cohérence entre sémantiques de tâche, méthodes HTN, State Model et ontologie.
- Les références de versions de l’architecture v3.2 ont été actualisées vers Mission Catalog v1.0.4, Task Catalog v0.12.0, Method Catalog v0.1.0 et State Model v0.6.
- La version d’architecture fournie comme source courante contient deux liens vers LSGA v2 et un lien vers `rig-e2e.md`, alors que ces fichiers sont absents du dépôt. Ils sont conservés tels quels dans le document source et restent donc à résoudre.

## Décisions humaines encore requises

1. Valider le statut normatif futur de l’architecture v3.2, actuellement présentée comme proposition à valider conjointement.
2. Décider si les documents amont absents (`lsga-architecture-v2.md` et `rig-e2e.md`) doivent être intégrés au dépôt ou rester des références externes.
3. Arbitrer l’écart architectural entre LSGA v3.2, qui présente encore le Domain HDDL comme source de vérité de la doctrine, et DEM-1/DEM-2, qui imposent Ontology + Mission Catalog + Task Catalog comme sources métier normatives et HDDL comme artefact dérivé. Cette divergence n’a pas été corrigée silencieusement dans l’architecture.
4. Faire relire et valider par les experts métier les 33 spécifications nouvellement consolidées MC-034 à MC-066 avant de promouvoir leur statut de `candidate` à `draft`.
