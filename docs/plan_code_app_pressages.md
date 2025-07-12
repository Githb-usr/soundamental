# Plan de code – app_pressages

## Modèles principaux

### 1. Pressage
- titre_principal
- titre_secondaire
- mention_edition
- annee_sortie
- nb_titres_affiches
- formats (ManyToMany)
- supports (ManyToMany)
- contenants (ManyToMany)
- particularites (ManyToMany)
- types_distribution (ManyToMany)
- zones_distribution (ManyToMany)
- zone_fabrication (FK)
- distributeurs (ManyToMany vers Label)
- labels (ManyToMany vers Label)
- references (ManyToMany)
- codes_barres (ManyToMany)
- slug
- created_at / updated_at

### 2. PressageArtiste
- pressage (FK)
- artiste (FK)
- type_role (présente / principal / feat / autre…)
- role_affiche (ex : "vs.", "introducing")
- ordre_affichage

### 3. Track
- pressage (FK)
- numero (ex : A1, B2)
- titre_affiche
- version_affiche
- duree
- ordre_affichage
- titre_repertoire (FK vers app_repertoire)
- est_cachee (boolean)
- nb_titres_caches (entier)

### 4. NoteTechnique
- pressage (OneToOne)
- note (texte ou TinyMCE)
- code_prix
- code_matrice
- societes_gestion (ManyToMany)
- images_associees (ManyToMany)
- ordre_affichage

## Modèles secondaires (listes)

- Format
- Support
- Contenant
- Particularite
- TypeDistribution
- ZoneDistribution
- ZoneFabrication
- ReferencePressage
- CodeBarre
- SocieteGestion
- ImagePressage

## Relations externes
- Artiste → app_artistes
- Label → app_labels
- TitreVersionRepertoire → app_repertoire


## Modèles secondaires – Listes prédéfinies

### Format
- nom
- description (optionnel)

### Support
- nom
- type_media (optionnel)

### Contenant
- nom
- materiau (optionnel)

### Particularite
- nom
- code / alias (optionnel)

### TypeDistribution
- nom
- commentaire (optionnel)

### ZoneDistribution
- nom
- code_pays (optionnel)

### ZoneFabrication
- nom
- code (optionnel)

### ReferencePressage
- texte

### CodeBarre
- valeur
- type (optionnel : sticker, verso…)

### SocieteGestion
- nom
- code (optionnel)

### ImagePressage
- fichier
- legende
- credit
- ordre_affichage
