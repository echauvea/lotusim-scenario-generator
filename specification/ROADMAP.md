# Feuille de route LSG

> **Statut :** note de pilotage courante, informative
> **Date de référence :** 2026-07-18
> **Baseline métier :** intégration du pilote Escort par la [PR #11](https://github.com/echauvea/lotusim-scenario-generator/pull/11), commit de fusion `cd529c1`

## 1. Baseline disponible

- Naval Maritime Ontology v2.0-draft : 263 classes déclarées, dont 46 classes de capacité.
- Mission Catalog v1.0.4 : 66 missions actives ; MC-034 à MC-066 restent candidates en attente de revue métier.
- Task Catalog v0.12.0 : 64 tâches, 79 signatures typées et 7 Semantic Families.
- 32 signatures possèdent une sémantique complète ; 47 restent à enrichir.
- State Model v0.6 : 105 états normatifs, 23 types propres et 4 candidats différés.
- Method Catalog v0.1.0 : deux méthodes pilotes décomposent `TC-023-S01 Escort Unit`.
- Profil HDDL LOTUSim v0.1 : compilation expérimentale `start/stop` des tâches continues, sans boucle de maintien au niveau 1.
- Fragment HDDL MC-026 : premier Domain / Problem dérivé pour `TM-023-S01-M01` avec traçabilité explicite.
- Les contrôles locaux et la CI vérifient les identifiants, références, familles, types, états, bindings et méthodes.

## 2. Pilote Escort

Deux alternatives sont documentées :

1. garde rapprochée : `Follow` + `Guard` pendant `Navigate Route` ;
2. escorte avec écran : `Follow` + `Screen` pendant `Navigate Route`.

La route commandée est représentée explicitement par `SM-ST-105 escort_route_assigned`. Les événements récupérables entraînent une décision de reprise ; ils ne sont pas assimilés automatiquement à un échec de la tâche Escort.

La stratégie pilote de projection de `spans` est désormais `start/stop` : Follow et Guard sont démarrées avant Navigate Route et arrêtées après le transit. Leur maintien et leurs invariants restent supervisés à l’exécution. La seconde méthode reste en plus non primitivement close car `Screen` demeure abstraite.

## 3. Incrément HDDL expérimental

Le premier fragment HDDL expérimental pour la méthode de garde rapprochée `TM-023-S01-M01`, appliqué à `MC-026 Escort High-Value Unit`, est disponible sous `references/hddl/experimental/mc-026-close-guard/`.

Décisions et résultats :

1. sous-ensemble HDDL classique typé, hiérarchique et totalement ordonné pour le pilote ;
2. compilation de `spans` par cycles `start/stop`, sans discrétisation temporelle ;
3. réutilisation exclusive des prédicats du State Model ;
4. préservation de `protected_unit_preserved` comme résultat d’évaluation externe, jamais comme effet de Guard ;
5. décisions de reprise conservées comme contrats d’exécution et de replanification ;
6. limites et rejets de projection consignés avant généralisation.

## 4. Travaux suivants

- Parser le fragment avec la chaîne HDDL retenue et vérifier le plan primitif attendu.
- Définir l’interprétation des commandes `start/stop` dans l’Execution Adaptation Layer, puis tester les arrêts normaux et les incidents injectés.
- Décomposer `TC-024-S01 Screen` afin de fermer primitivement la seconde méthode Escort.
- Modéliser l’escorte de convoi ou de groupe séparément de l’escorte d’une plateforme unique.
- Enrichir les 47 signatures restantes en priorité lorsqu’elles sont requises par une méthode ou une mission pilote.
- Promouvoir les quatre candidats différés du State Model seulement lorsqu’un producteur ou une règle d’agrégation existe.
- Étendre progressivement le Method Catalog aux autres tâches abstraites.
- Relier ultérieurement les référentiels LSG au vocabulaire exécutable de `tactical_scenario_maker`.

## 5. Décisions humaines différées

- validation métier des missions MC-034 à MC-066 ;
- statut normatif final de l’architecture v3.2 et choix de son dépôt canonique avec l’équipe `tactical_scenario_maker` ;
- maintien ou suppression de la couche éditoriale Capability Types `CT-01` à `CT-11` ;
- éventuel ajout ontologique de `TargetLocalizationCapability` ;
- promotion éventuelle du profil HDDL v0.1 après validation planificateur et exécution.

## 6. Règle de continuité

Ontology, Mission Catalog et Task Catalog portent la sémantique métier. Le State Model normalise le vocabulaire dynamique. Le Method Catalog porte les décompositions HTN. Le Domain HDDL et les Problem HDDL sont des projections exécutables et ne deviennent pas des sources métier indépendantes.
