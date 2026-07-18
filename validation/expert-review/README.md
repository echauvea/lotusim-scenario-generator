# Revue experte des référentiels — dispositif

> **Statut :** prototype (campagne pilote Escort)
> **Périmètre :** validation métier du Method Catalog par des experts opérationnels.

## Principe

Le validateur automatique (`tools/validation/validate_referentials.py`) garantit la cohérence
formelle des référentiels. Ce dispositif couvre ce que la machine ne peut pas juger : la **vérité
opérationnelle** des décisions doctrinales (applicabilité, décomposition, synchronisations,
conduite sur incident, critères de succès, discriminants entre méthodes alternatives).

La couverture est **structurelle** : `tools/validation/generate_expert_review.py` dérive un item
de vérification de chaque champ doctrinal de chaque méthode du catalogue. Un item sans formulation
française fait échouer la génération — rien ne peut être oublié. Les items identiques d'une méthode
à l'autre sont posés une seule fois (`covered_by` dans la matrice).

Les experts ne voient jamais de YAML : chaque item est traduit en affirmation opérationnelle
concrète (Vrai / Faux / Ça dépend), en mise en situation (« le choix du commandant ») ou en défi
(« chasse aux manques »). **« Ça dépend » + commentaire est la réponse la plus utile** : c'est là
qu'apparaissent les conditions manquantes.

## Flux (frugal : peu d'experts, asynchrone)

1. **Générer** : `python tools/validation/generate_expert_review.py --wording validation/expert-review/wording_<campagne>.yaml`
   → matrice `items_<campagne>.yaml` + questionnaire `questionnaire_<campagne>.html`.
2. **Distribuer** : envoyer le fichier HTML aux experts. Il est autonome et hors-ligne
   (aucune donnée ne quitte le poste) ; ~20 minutes par expert, en parallèle ou en différé.
3. **Collecter** : chaque expert exporte un fichier `reponses_<campagne>_<nom>.json` et le renvoie ;
   les fichiers sont déposés dans `validation/expert-review/responses/`.
4. **Adjuger** : un item passe à `validé` (statut dans la matrice) après accord d'au moins un
   expert ; toute réponse « Ça dépend », divergente entre experts ou contraire à la position du
   catalogue passe l'item en `contesté`. Seuls les items contestés justifient un échange synchrone.
5. **Corriger** : chaque correction du Method Catalog issue d'un item contesté référence l'item
   (`VQ-…`) dans sa PR ; l'item repasse en `pending` et sera reposé à la campagne suivante.

« Tout vérifié » = 100 % des items de la matrice au statut `validé`.

## Fichiers

- `wording_<campagne>.yaml` — formulations françaises rédigées à la main, reliées aux items par
  leur identifiant ; contient aussi la position actuelle du catalogue (`expected`, jamais montrée
  aux experts) et les mises en situation de niveau catalogue.
- `items_<campagne>.yaml` — matrice de couverture générée : ne pas éditer à la main, sauf le champ
  `status` lors de l'adjudication.
- `questionnaire_<campagne>.html` — formulaire autonome généré, à distribuer tel quel.
- `responses/` — réponses collectées (JSON), une par expert et par campagne.

## Extensions prévues

- Script d'agrégation des réponses (tableau des écarts réponse/`expected`, désaccords entre
  experts, mise à jour des statuts de la matrice).
- Réutilisation du même dispositif pour la revue métier des missions candidates MC-034 à MC-066.
