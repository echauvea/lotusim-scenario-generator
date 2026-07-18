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
- Les contrôles locaux et la CI vérifient les identifiants, références, familles, types, états, bindings et méthodes.

## 2. Pilote Escort

Deux alternatives sont documentées :

1. garde rapprochée : `Follow` + `Guard` pendant `Navigate Route` ;
2. escorte avec écran : `Follow` + `Screen` pendant `Navigate Route`.

La route commandée est représentée explicitement par `SM-ST-105 escort_route_assigned`. Les événements récupérables entraînent une décision de reprise ; ils ne sont pas assimilés automatiquement à un échec de la tâche Escort.

Les deux méthodes restent `partial` pour la projection HDDL : la relation `spans` impose que les tâches continues restent actives pendant le transit, et `Screen` demeure abstraite.

## 3. Prochain incrément recommandé

Produire un premier fragment HDDL expérimental pour la méthode de garde rapprochée `TM-023-S01-M01`, testé sur `MC-026 Escort High-Value Unit`.

Ordre de travail :

1. définir le sous-ensemble initial du profil HDDL LOTUSim ;
2. choisir la compilation des tâches continues et de `spans` : temporelle, cycle `start/maintain/stop`, ou transit segmenté ;
3. construire un cas MC-026 minimal avec objets, état initial et réseau de tâches ;
4. dériver le fragment HDDL sans ajouter de sémantique absente des référentiels ;
5. vérifier la sélection de méthode, le plan produit et les décisions de reprise ;
6. consigner les limites du profil avant toute généralisation.

## 4. Travaux suivants

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
- stratégie HDDL pour le temps continu et les synchronisations.

## 6. Règle de continuité

Ontology, Mission Catalog et Task Catalog portent la sémantique métier. Le State Model normalise le vocabulaire dynamique. Le Method Catalog porte les décompositions HTN. Le Domain HDDL et les Problem HDDL sont des projections exécutables et ne deviennent pas des sources métier indépendantes.
