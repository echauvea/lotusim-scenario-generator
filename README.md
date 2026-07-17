# LSG — LOTUSim Scenario Generator

Ce dépôt est le référentiel officiel de spécification et de méthode d’ingénierie de domaine de **LSG — LOTUSim Scenario Generator**. Il rassemble l’architecture, les référentiels métier, l’ontologie navale maritime et les règles permettant de dériver des modèles de planification traçables.

La documentation publiée de la Naval Maritime Ontology est accessible sur [GitHub Pages](https://echauvea.github.io/lotusim-scenario-generator/).

## Référentiels et responsabilités

- La **Naval Maritime Ontology** est la source normative des concepts, types, capacités, équipements et relations structurelles.
- Le **Mission Catalog** est la source normative des missions et de leurs objectifs.
- Le **Task Catalog** est la source normative des tâches. Les sémantiques sont portées par chaque signature typée ; les sémantiques communes sont centralisées dans les Semantic Families.
- La **LSG Domain Engineering Method (DEM)** fixe les règles de conception et le métamodèle du Task Catalog.
- Le **State Model v0.3** est le vocabulaire dynamique dérivé des trois référentiels métier. Sa source YAML est normative pour les états des signatures enrichies.
- Le **domaine et les problèmes HDDL** seront dérivés du State Model. Ils ne sont pas encore présents dans ce dépôt.

## Chaîne de dérivation

```text
Naval Maritime Ontology ─┐
Mission Catalog ─────────┼─> State Model ─> HDDL Domain / Problems
Task Catalog ────────────┘
```

L’ontologie fournit les concepts et relations structurelles, le Mission Catalog les préconditions et objectifs, et le Task Catalog les lectures, effets et conditions des tâches.

## Arborescence

```text
.
├── .github/workflows/           Génération et publication automatiques
├── README.md
├── references/
│   ├── ontology/                Source TTL normative
│   ├── mission-catalog/         Mission Catalog
│   ├── task-catalog/            Task Catalog courant synchronisé
│   └── state-model/             State Model YAML normatif
├── site/                         Fichiers maintenus du site publié
├── specification/
│   ├── INDEX.md                 Index documentaire officiel
│   ├── architecture/            Architecture de référence de LSG
│   ├── dem/                     Versions courantes de la méthode DEM
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

Le workflow [`.github/workflows/referential-integrity.yml`](.github/workflows/referential-integrity.yml) exécute automatiquement le validateur à chaque pull request concernée et après fusion dans `main`. Il contrôle notamment les identifiants, la traçabilité missions–tâches, l’affectation des Semantic Families, les références ontologiques, ainsi que les états, types et bindings des signatures enrichies.

Exécution locale :

```powershell
python -m pip install -r tools/validation/requirements.txt
python -m unittest discover -s tools/validation/tests -v
python tools/validation/validate_referentials.py
```

Une validation réussie affiche les effectifs contrôlés. En cas d’erreur, le code du contrôle, le document concerné et l’incohérence sont indiqués ; dans GitHub, ces erreurs apparaissent aussi comme annotations de la pull request.

## Statut

Les référentiels sont encore à des niveaux de maturité différents : l’architecture est une proposition à valider, l’ontologie, les catalogues et le State Model v0.3 sont des brouillons de travail, et DEM-1/DEM-2 sont des spécifications méthodologiques en brouillon. Le Task Catalog v0.10.0 est la version courante : ses 24 signatures enrichies utilisent les identifiants stables du State Model selon DEM-1/DEM-2 v0.6. Les 55 autres signatures restent à traiter progressivement.

La liste exhaustive, les versions, le statut et le caractère normatif ou informatif de chaque document figurent dans [specification/INDEX.md](specification/INDEX.md).
