# LSG — LOTUSim Scenario Generator

Ce dépôt est le référentiel officiel de spécification et de méthode d’ingénierie de domaine de **LSG — LOTUSim Scenario Generator**. Il rassemble l’architecture, les référentiels métier, l’ontologie navale maritime et les règles permettant de dériver des modèles de planification traçables.

La documentation publiée de la Naval Maritime Ontology est accessible sur [GitHub Pages](https://echauvea.github.io/lotusim-scenario-generator/).

## Référentiels et responsabilités

- La **Naval Maritime Ontology** est la source normative des concepts, types, capacités, équipements et relations structurelles.
- Le **Mission Catalog** est la source normative des missions et de leurs objectifs.
- Le **Task Catalog** est la source normative des tâches. Les sémantiques sont portées par chaque signature typée ; les sémantiques communes sont centralisées dans les Semantic Families.
- Le **Method Catalog** décrit les méthodes HTN qui décomposent les tâches abstraites en réseaux de sous-tâches typées.
- La **LSG Domain Engineering Method (DEM)** fixe les règles de conception et les métamodèles du Task Catalog et du Method Catalog.
- Le **State Model v0.6** est le vocabulaire dynamique dérivé des référentiels métier. Sa source YAML est normative pour les états des signatures et méthodes enrichies.
- Le **profil HDDL LOTUSim v0.1** définit la première projection expérimentale `start/stop` des tâches continues ; il n’ajoute aucune sémantique métier.
- Un premier **fragment Domain / Problem HDDL** dérivé est disponible pour `TM-023-S01-M01` et `MC-026`. Il reste expérimental et ne constitue pas encore le Naval Domain complet.

## Chaîne de dérivation

```text
Ontology + Mission Catalog + Task Catalog ─> State Model
Task Catalog + State Model + mission evidence ─> Method Catalog
State Model + Method Catalog ─> HDDL Domain / Problems
```

L’ontologie fournit les concepts et relations structurelles, le Mission Catalog les préconditions et objectifs, et le Task Catalog les lectures, effets et conditions des tâches. Le Method Catalog ajoute les alternatives de décomposition, l’ordonnancement, la synchronisation et la propagation des échecs.

## Arborescence

```text
.
├── .github/workflows/           Génération et publication automatiques
├── README.md
├── references/
│   ├── ontology/                Source TTL normative
│   ├── mission-catalog/         Mission Catalog
│   ├── task-catalog/            Task Catalog courant synchronisé
│   ├── method-catalog/          Méthodes de décomposition HTN
│   ├── hddl/                    Fragments HDDL dérivés expérimentaux
│   └── state-model/             State Model YAML normatif
├── site/                         Fichiers maintenus du site publié
├── specification/
│   ├── INDEX.md                 Index documentaire officiel
│   ├── ROADMAP.md               État courant et ordre de reprise
│   ├── architecture/            Architecture de référence de LSG
│   ├── dem/                     Versions courantes de la méthode DEM
│   ├── hddl/                    Profil de projection HDDL
│   ├── notes/                   Notes de coordination datées, non normatives
│   ├── state-model/             Spécification du State Model
│   └── archive/dem/             Versions DEM obsolètes ou fusionnées
```

Les sources documentaires maintenues manuellement se trouvent dans `references/`, `specification/` et `site/`. Les fichiers produits par WIDOCO ne sont pas suivis par Git. Les contrôles transversaux se trouvent dans `tools/validation/`.

## Documentation de l’ontologie avec WIDOCO

La documentation est générée avec WIDOCO 1.4.25 à partir de :

```text
references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl
```

Le workflow [`.github/workflows/ontology-pages.yml`](.github/workflows/ontology-pages.yml) constitue la chaîne officielle :

- chaque pull request qui touche l’ontologie, le site ou le workflow génère et valide la documentation ;
- chaque changement correspondant fusionné dans `main` génère puis publie automatiquement le site sur GitHub Pages ;
- les sorties HTML, RDF, JSON-LD et WebVOWL sont vérifiées avant publication.

La génération locale reste facultative. Commande de référence :

```powershell
java -jar <chemin-vers-widoco.jar> `
  -ontFile references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl `
  -outFolder build/widoco `
  -rewriteAll -webVowl -lang en-fr
```

Les scripts personnels `generer_doc.bat` et `ouvrir_doc.bat` restent volontairement ignorés par Git. Ils utilisent la source TTL ci-dessus et écrivent dans `build/widoco/`, également ignoré. Le dossier publié par GitHub Pages est produit à la volée par la CI et n’est jamais modifié manuellement.

## Contrôle d’intégrité des référentiels

Le workflow [`.github/workflows/referential-integrity.yml`](.github/workflows/referential-integrity.yml) exécute automatiquement le validateur à chaque pull request concernée et après fusion dans `main`. Il contrôle notamment les identifiants, la traçabilité missions–tâches, l’affectation des Semantic Families, les références ontologiques, ainsi que les états, types et bindings des signatures et méthodes enrichies.

Exécution locale :

```powershell
python -m pip install -r tools/validation/requirements.txt
python -m unittest discover -s tools/validation/tests -v
python tools/validation/validate_referentials.py
```

Une validation réussie affiche les effectifs contrôlés. En cas d’erreur, le code du contrôle, le document concerné et l’incohérence sont indiqués ; dans GitHub, ces erreurs apparaissent aussi comme annotations de la pull request.

## Statut

Les référentiels sont encore à des niveaux de maturité différents : l’architecture est une proposition à valider, l’ontologie, les catalogues et le State Model v0.6 sont des brouillons de travail, et les spécifications DEM sont en brouillon. Le Task Catalog v0.12.0 est la version courante : ses 32 signatures enrichies utilisent les identifiants stables du State Model selon DEM-1/DEM-2 v0.6. Le Method Catalog v0.1.0 contient le pilote Escort. Le profil HDDL v0.1 et son fragment MC-026 compilent expérimentalement `spans` en cycles `start/stop`, avec maintien continu délégué à l’exécution. Les 47 autres signatures restent à traiter progressivement.

La liste exhaustive, les versions, le statut et le caractère normatif ou informatif de chaque document figurent dans [specification/INDEX.md](specification/INDEX.md).

Pour reprendre les travaux sans reconstruire le contexte, consulter la [feuille de route courante](specification/ROADMAP.md). Elle récapitule le dernier incrément validé, les limites du pilote Escort et l’ordre recommandé des prochaines étapes.
