# Feuille de route LSG

> **Statut :** note de pilotage courante, informative
> **Date de référence :** 2026-07-18
> **Baseline métier :** fragment HDDL MC-026 validé par Aries ([PR #14](https://github.com/echauvea/lotusim-scenario-generator/pull/14)) et dispositif de revue experte ([PR #15](https://github.com/echauvea/lotusim-scenario-generator/pull/15)), commit de fusion `df4d647`

## 1. Baseline disponible

- Naval Maritime Ontology v2.0-draft : 263 classes déclarées, dont 46 classes de capacité.
- Mission Catalog v1.0.4 : 66 missions actives ; MC-034 à MC-066 restent candidates en attente de revue métier.
- Task Catalog v0.12.0 : 64 tâches, 79 signatures typées et 7 Semantic Families.
- 32 signatures possèdent une sémantique complète ; 47 restent à enrichir.
- State Model v0.6 : 105 états normatifs, 23 types propres et 4 candidats différés.
- Method Catalog v0.1.0 : deux méthodes pilotes décomposent `TC-023-S01 Escort Unit`.
- Profil HDDL LOTUSim v0.1 : compilation expérimentale `start/stop` des tâches continues, sans boucle de maintien au niveau 1.
- Fragment HDDL MC-026 : premier Domain / Problem dérivé pour `TM-023-S01-M01` avec traçabilité explicite.
- Chaîne planificateur pilote : Unified Planning 1.3.0 et Aries 0.5.0 parsèment le fragment et produisent exactement le plan primitif attendu.
- Dispositif de revue experte du Method Catalog (`validation/expert-review/`) : items dérivés structurellement du catalogue, questionnaire hors-ligne et agrégateur de statuts ; campagne pilote `escort-v0.1` prête à distribuer (35 items, 23 questions, ~20 minutes par expert).
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
7. validation reproductible par Aries du cycle complet `start Follow / start Guard / Navigate / evaluate / stop Guard / stop Follow`.

## 4. Travaux suivants

- Lancer la campagne de revue experte `escort-v0.1` dès que les experts sont identifiés ; adjuger les items contestés puis reporter les corrections dans le Method Catalog.
- Définir l’interprétation des commandes `start/stop` dans l’Execution Adaptation Layer, puis tester les arrêts normaux et les incidents injectés.
- Décomposer `TC-024-S01 Screen` afin de fermer primitivement la seconde méthode Escort.
- Modéliser l’escorte de convoi ou de groupe séparément de l’escorte d’une plateforme unique.
- Enrichir les 47 signatures restantes en priorité lorsqu’elles sont requises par une méthode ou une mission pilote.
- Promouvoir les quatre candidats différés du State Model seulement lorsqu’un producteur ou une règle d’agrégation existe.
- Étendre progressivement le Method Catalog aux autres tâches abstraites.
- Relier ultérieurement les référentiels LSG au vocabulaire exécutable de `tactical_scenario_maker`.

## 5. Décisions humaines différées

- validation métier des missions MC-034 à MC-066 (le dispositif de revue experte sera réutilisé après son pilote Escort) ;
- identification des experts métier mobilisables pour la campagne `escort-v0.1` ;
- statut normatif final de l’architecture v3.2 et choix de son dépôt canonique avec l’équipe `tactical_scenario_maker` ;
- maintien ou suppression de la couche éditoriale Capability Types `CT-01` à `CT-11` ;
- éventuel ajout ontologique de `TargetLocalizationCapability` ;
- promotion éventuelle du profil HDDL v0.1 après validation planificateur et exécution.

## 6. Pistes exploratoires

Pistes identifiées lors de la passe documentaire du 2026-07-18, non planifiées, à instruire opportunément :

1. **Vérificateur de plan `spans`.** La compilation `start/stop` garantit la continuité des tâches spannantes par persistance d’état, sans protection contre l’entrelacement d’autres méthodes dans un problème plus riche que MC-026. Un contrôle post-planification (vérifier sur le plan produit qu’aucune action n’invalide `following` ou `guarding` entre leurs `start` et `stop`) fermerait cette limite à peu de frais et pourrait rejoindre la CI planificateur.
2. **Actualisation du Method Catalog v0.2.** Les fiches Escort déclarent encore le blocker « HDDL profile must define… », satisfait depuis le profil v0.1. Le prochain incrément du catalogue devrait réviser les blockers et conditionner la promotion `pilot → draft` à deux preuves désormais outillées : le passage planificateur (acquis) et la campagne de revue experte (prête).
3. **Métrique de couverture doctrinale.** Le validateur connaît missions, méthodes et readiness : il pourrait publier un indicateur de pilotage — part des missions actives disposant d’au moins une méthode primitivement close et validée par les experts — pour objectiver la progression vers le Naval Domain complet.
4. **Pont de vocabulaire LSG ↔ tsm.** L’écart entre `knowledge_base.json` (tâches en français, non typées) et le Task Catalog (signatures anglaises typées) reste le principal risque d’intégration. Une table de correspondance générée et validée par le validateur transversal transformerait ce risque en artefact contrôlé, sans attendre la décision sur le dépôt canonique de l’architecture.
5. **Industrialisation des campagnes de revue.** Si le pilote Escort confirme le rendement du dispositif (temps par expert, taux de « Ça dépend »), générer les campagnes suivantes par lot — missions MC-034 à MC-066 par famille sémantique, puis chaque nouvelle méthode HTN — ferait de la validation métier un flux continu plutôt qu’un événement.

## 7. Règle de continuité

Ontology, Mission Catalog et Task Catalog portent la sémantique métier. Le State Model normalise le vocabulaire dynamique. Le Method Catalog porte les décompositions HTN. Le Domain HDDL et les Problem HDDL sont des projections exécutables et ne deviennent pas des sources métier indépendantes.
