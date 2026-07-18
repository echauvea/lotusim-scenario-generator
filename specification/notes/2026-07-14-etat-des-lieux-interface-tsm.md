# État des lieux — Interfaçage LSG ↔ tactical_scenario_maker (tsm)

**Date** : 2026-07-14
**Objet** : point de synchronisation entre le dépôt LSG (référentiels, méthode, architecture) et le dépôt tsm (exécution, planification HTN, rig LOTUSim), avant d'aller plus loin sur l'un ou l'autre.
**Repos concernés** :
- `echauvea/lotusim-scenario-generator` (LSG — Estelle)
- `cmoron-lab/tactical_scenario_maker` (tsm — Cyril)

Ce document ne tranche rien : il liste des constats factuels et les questions qui en découlent, à décider ensemble.

---

## 1. Constat — le document d'architecture diverge déjà entre les deux dépôts

`LSGA v3.2` (LSG, daté 13/07) se présente comme l'unification de LSGA v2 et des travaux tsm. Le dépôt tsm ne contient que **`lsga-architecture-v3.md`, daté 12/07** — une itération en retard.

- D'après le changelog de la v3.2, le delta v3.1 → v3.2 est "sans changement de fond" (traduction FR d'une section, mention d'un validateur CI, mise à jour de statuts de versions des référentiels). Pas critique en soi.
- Mais le changelog **ne documente pas** la transition v3 → v3.1 : trou dans l'historique, indépendamment de la synchro entre dépôts.
- La v3.2 contenait alors des liens relatifs vers `lsga-architecture-v2.md` et `rig-e2e.md` comme s'ils étaient dans le même dépôt — ces fichiers n'existent que dans tsm. Les liens étaient donc cassés depuis le dépôt LSG isolé.

**Conséquence** : il n'y a aujourd'hui aucune source unique de vérité pour ce document. Deux copies, dans deux dépôts, sans mécanisme de synchronisation.

---

## 2. Constat — le vocabulaire des tâches ne se rejoint pas encore

`doctrine/knowledge_base.json` (tsm) encode la doctrine HTN réellement exécutée. Extrait de vocabulaire :

- **Tasks / leaf tasks** : `surveiller_zone`, `escorter_convoi`, `suivre_agent`, `reconnaissance`, `naviguer_vers_base`, `maintenir_contact`, `poursuivre`… — français, snake_case, verbes libres.
- **Primitive actions** : `aller_a` / `goto`, `follow_target`, `attack_target` — mixte, s'anglicise sur les primitives les plus récentes.

Le **Task Catalog** (LSG) utilise des verbes canoniques anglais typés (`Navigate`, `Follow`, `Escort`, `Detect`…), identifiants `TC-NNN`, signatures typées référençant les classes de capacité de l'ontologie.

- **Point positif** : au niveau `primitive_actions`, `follow_target` / `goto` / `attack_target` correspondent exactement aux familles d'action typée déjà formalisées dans l'architecture v3.2 (§6.4) : `navigation.follow_target`, `navigation.goto`, `engage.attack_target`. C'est le point de jonction déjà pensé conceptuellement (chaîne verbe → capacité → `nmo:manifestKey` → implémentation).
- **Écart** : tout ce qui est au-dessus (tasks/leaf_tasks — l'essentiel de la doctrine encodée par tsm) n'a aucune correspondance avec le Task Catalog ou le Mission Catalog. `knowledge_base.json` a été écrit indépendamment des référentiels sémantiques.
- Ce n'est pas une découverte surprise : le §10.1 de l'architecture v3.2 le documente déjà explicitement — *« Domain HDDL : Implémenté en code — delta n°1 : traduction HDDL (dépend du profil) »*.

---

## 3. Constat — la chaîne d'exécution technique est aujourd'hui indépendante des référentiels sémantiques

`docs/rig-e2e.md` (tsm) est un runbook opérationnel (Docker Compose, ROS 2 Jazzy, Gazebo, scénario `escorte_ormuz`, profil `kinematic-ormuz`). Il ne mentionne à aucun moment l'ontologie, le Mission Catalog ou le Task Catalog. La chaîne d'exécution tourne aujourd'hui sur `knowledge_base.json` seul, sans lien technique avec les référentiels LSG.

---

## 4. Ce qui va déjà dans le bon sens

- La démarche de convergence a eu lieu conceptuellement : la v3.2 absorbe explicitement les décisions D1–D8 du POC tsm (agent = plateforme + autonomie, manifestes de capacités, cycle de vie des objectifs, multi-fidélité...).
- L'alignement au niveau primitive (`follow_target`, `goto`, `attack_target`) montre que la direction prise par tsm et celle formalisée dans l'architecture ne sont pas en contradiction — juste pas encore reliées mécaniquement.
- Les deux écarts principaux (doc et vocabulaire) sont déjà nommés dans les documents existants (LSG `INDEX.md` décision n°2 ; architecture v3.2 §10.1 et §11.3 point 3) — ce n'est pas un problème caché, juste pas encore traité.

---

## 5. Questions à trancher ensemble

1. **Où vit la version canonique de l'architecture ?** Un des deux dépôts fait foi et l'autre pointe dessus (lequel ?), ou un dépôt dédié séparé des deux ?
2. **Documente-t-on rétroactivement le delta v3 → v3.1** manquant dans le changelog, pour que l'historique soit complet ?
3. **Priorise-t-on le mapping `knowledge_base.json` → Task Catalog** sur le sous-ensemble déjà pilote côté sémantique (Navigate, Follow, Escort — les 4 signatures du pilote DEM) avant de l'étendre au reste de la doctrine ?
4. **`rig-e2e.md` doit-il évoluer** pour référencer les profils d'exécution et manifestes de capacités définis dans l'architecture (§4.2, §4.4), ou reste-t-il volontairement un runbook bas niveau indépendant ?
5. **Répartition des dépôts** : LSG reste spécification pure, tsm reste code d'exécution — séparation confirmée par les deux, ou faut-il envisager un rapprochement structurel (pas via un fork/PR massif, mais une vraie discussion de design si le besoin se confirme) ?

---

## 6. Proposition

Un point court (30 min) centré sur les questions 1 et 3 en priorité : elles conditionnent la suite (où corriger les liens cassés, et sur quel périmètre lancer le premier mapping vocabulaire ↔ doctrine).

---

## 7. Mise à jour au 2026-07-18

- Les liens LSGA v2 et `rig-e2e.md` de l’architecture LSG pointent désormais explicitement vers le dépôt GitHub `tactical_scenario_maker` ; le défaut de lien local est résolu.
- Le choix du dépôt canonique de l’architecture reste à confirmer avec l’équipe tsm.
- Le premier mapping doctrinal est désormais représenté côté LSG par le Method Catalog v0.1.0 : deux méthodes pilotes décomposent Escort, sans encore remplacer ni modifier `knowledge_base.json` dans tsm.
- La priorité technique suivante est le profil de projection HDDL et son expérimentation sur MC-026, avant un raccordement mécanique au runtime tsm.

---

## 8. Mise à jour après validation HDDL/Aries

- Le profil HDDL v0.1 a retenu la compilation `start/stop` et le fragment MC-026
  a été résolu par Aries 0.5.0 ; le choix du profil n’est plus une question ouverte
  pour le pilote de garde rapprochée.
- Le Method Catalog v0.2.0 distingue désormais la projection techniquement
  `ready` de `TM-023-S01-M01` de son statut métier encore `pilot`.
- La priorité technique se déplace vers le raccordement EAL/tsm : interprétation
  des commandes `start/stop`, surveillance des invariants, arrêts sur incident et
  replanification.
- Le mapping entre `knowledge_base.json` et les signatures typées LSG reste un
  chantier distinct et toujours ouvert.
