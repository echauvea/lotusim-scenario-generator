# LSG — LOTUSim Scenario Generator

Ce dépôt est le référentiel officiel de spécification et de méthode d’ingénierie de domaine de **LSG — LOTUSim Scenario Generator**. Il rassemble l’architecture, les référentiels métier, l’ontologie navale maritime et les règles permettant de dériver des modèles de planification traçables.

La documentation publiée de la Naval Maritime Ontology est accessible sur [GitHub Pages](https://echauvea.github.io/lotusim-scenario-generator/).

## Référentiels et responsabilités

- La **Naval Maritime Ontology** est la source normative des concepts, types, capacités, équipements et relations structurelles.
- Le **Mission Catalog** est la source normative des missions et de leurs objectifs.
- Le **Task Catalog** est la source normative des tâches. Les sémantiques sont portées par chaque signature typée ; les sémantiques communes sont centralisées dans les Semantic Families.
- La **LSG Domain Engineering Method (DEM)** fixe les règles de conception et le métamodèle du Task Catalog.
- Le **State Model** est un artefact dérivé. Il n’est pas encore présent dans ce dépôt.
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
├── README.md
├── references/
│   ├── ontology/                Source TTL normative
│   ├── mission-catalog/         Mission Catalog
│   └── task-catalog/            Task Catalog courant synchronisé
├── specification/
│   ├── INDEX.md                 Index documentaire officiel
│   ├── architecture/            Architecture de référence de LSG
│   ├── dem/                     Versions courantes de la méthode DEM
│   └── archive/dem/             Versions DEM obsolètes ou fusionnées
├── work-in-progress/            Expérimentations non normatives
└── docs/                        Site WIDOCO généré et publié par GitHub Pages
```

Le dossier `docs/` est réservé aux fichiers générés par WIDOCO. Les sources documentaires maintenues manuellement se trouvent dans `references/` et `specification/`.

## Documentation de l’ontologie avec WIDOCO

La documentation est générée avec WIDOCO 1.4.25 à partir de :

```text
references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl
```

Commande de référence :

```powershell
java -jar <chemin-vers-widoco.jar> `
  -ontFile references/ontology/LOTUSim_Naval_Maritime_Ontology_v2.0-draft.ttl `
  -outFolder docs `
  -rewriteAll -webVowl -lang en-fr
```

Les scripts personnels `generer_doc.bat` et `ouvrir_doc.bat` restent volontairement ignorés par Git. Leur variable `ONT_FILE` doit pointer vers la source TTL ci-dessus. Après génération, `docs/index.html` redirige vers la documentation anglaise et `docs/.nojekyll` permet la publication directe par GitHub Pages.

## Statut

Les référentiels sont encore à des niveaux de maturité différents : l’architecture est une proposition à valider, l’ontologie et les catalogues sont des brouillons de travail, et DEM-1/DEM-2 sont des spécifications méthodologiques en brouillon. Le pilote sémantique v0.6.0 reste expérimental et ne remplace pas le Task Catalog courant.

La liste exhaustive, les versions, le statut et le caractère normatif ou informatif de chaque document figurent dans [specification/INDEX.md](specification/INDEX.md).
