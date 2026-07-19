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
| [Architecture LSG](architecture/LSG_Architecture_v3.2.md) | v3.2 | Proposition courante, à valider conjointement | Informatif jusqu’à validation | Architecture globale de génération, exécution et arbitrage. Les documents amont LSGA v2 et `rig-e2e.md` restent hébergés dans le dépôt `tactical_scenario_maker` et sont référencés par des liens externes. |
| [DEM-1 — Semantic Design Rules](dem/DEM-1_Semantic_Design_Rules_v0.6.md) | v0.6 | Brouillon courant | Normatif pour la méthode | Règles de conception sémantique, références d’état stables et tuples canoniques. |
| [DEM-2 — Task Catalog Specification](dem/DEM-2_Task_Catalog_Specification_v0.6.md) | v0.6 | Brouillon courant | Normatif pour la méthode | Métamodèle des signatures aligné sur le State Model normatif. |
| [DEM-3 — Method Catalog Specification](dem/DEM-3_Method_Catalog_Specification_v0.2.md) | v0.2 | Pilote courant | Normatif pour la méthode | Métamodèle des méthodes HTN, distinction entre maturité métier et aptitude à la projection, synchronisations et projection HDDL. |
| [Naval Maritime Ontology](../references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl) | 2.0.0-draft | Brouillon courant | Normatif pour les concepts, types, capacités, équipements et relations structurelles | La version interne et le nom de fichier sont cohérents. |
| [Mission Catalog](../references/mission-catalog/LOTUSim_Mission_Catalog_v1.0.4.md) | v1.0.4 | Courant, brouillon de travail | Normatif pour les missions et objectifs | Les 66 missions disposent d’une spécification active conforme au métamodèle canonique. |
| [Task Catalog](../references/task-catalog/LOTUSim_Task_Catalog_v0.12.0.md) | v0.12.0 | Courant, brouillon de travail | Normatif pour les tâches et leurs sémantiques | Les 32 signatures enrichies couvrent le noyau ISR, deux lots d’extension ISR et les familles Movement et Protection. |
| [Method Catalog](../references/method-catalog/LOTUSim_Method_Catalog_v0.2.0.md) | v0.2.0 | Pilote courant | Normatif pour les décompositions documentées | Deux méthodes Escort : garde rapprochée techniquement `ready`, escorte avec écran `partial` uniquement faute de fermeture primitive de Screen. Les deux restent au statut métier `pilot`. |
| [State Model — source normative](../references/state-model/LOTUSim_State_Model_v0.6.yaml) | v0.6.0 | Courant, brouillon de travail | Normatif pour les états dynamiques | 105 états, 23 types propres, producteurs, consommateurs, contraintes et traçabilité. |
| [State Model — spécification](state-model/LOTUSim_State_Model_Specification_v0.6.md) | v0.6 | Courant, brouillon de travail | Normatif pour le métamodèle | Catégories, politique d’identifiants, normalisations, cycle de vie et règles de validation. |
| [Profil HDDL LOTUSim](hddl/LOTUSim_HDDL_Profile_v0.1.md) | v0.1 | Pilote expérimental | Normatif pour la projection pilote uniquement | Sous-ensemble HDDL classique et compilation `start/stop` de `spans` ; le maintien continu reste à l’exécution. |

## Archives des catalogues

| Document | Version | Statut | Autorité | Motif d’archivage |
|---|---:|---|---|---|
| [Method Catalog — pilote initial](../references/method-catalog/archive/LOTUSim_Method_Catalog_v0.1.0.md) | v0.1.0 | Archivé | Non normatif | Remplacé par v0.2.0 après validation de la compilation `start/stop` et suppression des blockers de projection devenus obsolètes. |
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
| [DEM-3 — Method Catalog Specification](archive/dem/DEM-3_Method_Catalog_Specification_v0.1.md) | v0.1 | Archivé | Non normatif | Remplacé par DEM-3 v0.2 après validation du profil `start/stop` et distinction entre maturité métier et aptitude technique à la projection. |
| [DEM Part 1 — Task Semantics & State Model](archive/dem/DEM_Part1_Task_Semantics_State_Model_v0.1.md) | v0.1 | Archivé | Non normatif | Ancien document composite. Ses décisions utiles sont réparties entre DEM-1 et DEM-2 ; aucun Task Semantics Catalog séparé ne doit être recréé. |

## Documents de gouvernance et de support

| Document | Version | Statut | Autorité | Rôle |
|---|---:|---|---|---|
| [README racine](../README.md) | non versionné | Courant | Informatif | Présentation du dépôt, responsabilités, chaîne de dérivation, arborescence et statuts. |
| [Feuille de route](ROADMAP.md) | 2026-07-18 | Courant | Informatif | Baseline vérifiée, limites du pilote Escort, ordre de reprise et décisions différées. |
| [Validateur des référentiels](../tools/validation/validate_referentials.py) | non versionné | Courant | Contrôle automatisé | Vérifie les identifiants, références croisées, familles, types, états, bindings, méthodes HTN et principales règles DEM ; exécuté par la CI. |
| [Documentation WIDOCO](https://echauvea.github.io/lotusim-scenario-generator/) | 2.0.0-draft | Générée par CI | Informatif | Représentation HTML, WebVOWL et sérialisations RDF de la Naval Maritime Ontology, publiée par GitHub Pages sans fichiers générés suivis dans Git. |
| [État des lieux — Interfaçage LSG ↔ tsm](notes/2026-07-14-etat-des-lieux-interface-tsm.md) | 2026-07-14, mise à jour 2026-07-18 | Note de coordination | Informatif | Constats sur la divergence entre les dépôts et sur l'écart avec `knowledge_base.json` ; addenda couvrant les liens corrigés, le pilote Method Catalog et le déplacement du chemin critique vers l’EAL/tsm. |
| [Fragment HDDL MC-026](../references/hddl/experimental/mc-026-close-guard/README.md) | profil v0.1 | Dérivé, expérimental, validé par Aries 0.5.0 | Non normatif | Premier Domain / Problem minimal pour `TM-023-S01-M01`, avec table de traçabilité explicite, plan primitif vérifié et résultat JSON publié par la CI. |
| [Dispositif de revue experte](../validation/expert-review/README.md) | campagne escort-v0.1 | Courant, prototype | Contrôle métier outillé | Validation opérationnelle du Method Catalog : items dérivés structurellement (couverture garantie), questionnaire HTML autonome hors-ligne, matrice de statuts et rapport d'adjudication. Campagne pilote Escort prête : 35 items, 23 questions. |
| [Tableau de bord des référentiels](https://echauvea.github.io/lotusim-scenario-generator/dashboard/) | non versionné | Généré par CI | Informatif | Chaîne de dérivation, versions, taux de remplissage et avancement des revues expertes ; métriques issues des parseurs du validateur, régénéré à chaque fusion (`tools/reporting/generate_dashboard.py`). |

## Artefacts prévus mais absents

| Artefact | Statut attendu | Dépendances |
|---|---|---|
| Naval Domain / Problems complets | Premier fragment MC-026 validé avec Aries ; généralisation à produire | Validation de l’adaptation d’exécution, puis extension progressive du Method Catalog. |
| Schémas formels et benchmarks | À planifier | Métamodèles et référentiels stabilisés. Le premier validateur transversal est maintenant disponible. |

## Résultats de l’audit de consolidation

- Les 66 identifiants de mission `MC-001` à `MC-066` sont présents dans l’inventaire canonique et les 64 identifiants de tâche `TC-001` à `TC-064` sont présents, sans doublon d’en-tête détecté.
- Le Mission Catalog v1.0.4 contient 66 spécifications actives conformes au métamodèle. Les anciennes propositions incompatibles autrefois numérotées MC-039 à MC-066 sont conservées dans une annexe explicitement non normative.
- Le Task Catalog v0.12.0 reprend les 64 tâches et 79 signatures. Trente-deux signatures possèdent une sémantique complète ; les 47 autres restent à enrichir progressivement.
- Le State Model v0.6 contient 105 états normatifs, 23 types propres et 4 candidats de mission différés faute de producteurs sémantisés.
- Le Method Catalog v0.2.0 contient deux méthodes pilotes pour Escort. La garde rapprochée est techniquement `ready` après validation par Aries ; l’escorte avec écran reste `partial` faute de décomposition complète de Screen. Leur statut métier reste `pilot` dans l’attente de la revue experte et de la validation d’exécution.
- Le profil HDDL v0.1 choisit la compilation `start/stop` pour les tâches continues et projette les deux relations `spans` de `TM-023-S01-M01` dans un fragment expérimental MC-026 sans nouveau prédicat métier. Unified Planning 1.3.0 et Aries 0.5.0 produisent exactement le plan primitif attendu.
- Le validateur transversal et sa CI contrôlent automatiquement les inventaires, la traçabilité, les Semantic Families et la cohérence entre sémantiques de tâche, méthodes HTN, State Model et ontologie.
- Les références de versions de l’architecture v3.2 ont été actualisées vers Mission Catalog v1.0.4, Task Catalog v0.12.0, Method Catalog v0.2.0 et State Model v0.6.
- L’architecture référence LSGA v2 et `rig-e2e.md` par des liens externes vers `tactical_scenario_maker` ; aucun lien local cassé ne subsiste dans la documentation Markdown.
- L’architecture présente désormais Ontology, Mission Catalog, Task Catalog, State Model et Method Catalog comme sources normatives de la projection HDDL, conformément à DEM-1/DEM-3.

## Décisions humaines encore requises

1. Valider le statut normatif futur de l’architecture v3.2, actuellement présentée comme proposition à valider conjointement.
2. Confirmer avec l’équipe `tactical_scenario_maker` quel dépôt porte la copie canonique de l’architecture ; les documents amont restent pour l’instant des références externes.
3. Faire relire et valider par les experts métier les 33 spécifications nouvellement consolidées MC-034 à MC-066 avant de promouvoir leur statut de `candidate` à `draft` ; le dispositif de revue experte (`validation/expert-review/`) est prévu pour outiller cette campagne après son pilote sur les méthodes Escort.
4. Valider le profil HDDL `start/stop` avec l’adaptation d’exécution avant de promouvoir les méthodes Escort ; la validation avec le planificateur Aries est acquise pour le pilote MC-026.
5. Identifier les experts métier mobilisables (nombre et profils) pour lancer la campagne de revue experte `escort-v0.1`, prête à distribuer.
