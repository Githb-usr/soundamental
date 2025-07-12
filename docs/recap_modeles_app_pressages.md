# Récapitulatif des modèles principaux – app_pressages

## Modèle `Pressage`

| Champ | Type | Commentaire |
|-------|------|-------------|
| titre_principal | CharField | Titre principal du disque |
| titre_secondaire | CharField (optionnel) | Titre complémentaire |
| mention_edition | CharField (optionnel) | Ex : Édition limitée, Remixes, etc. |
| annee_sortie | PositiveSmallIntegerField | Année de sortie |
| nb_titres_affiches | SmallIntegerField | Nombre de titres listés |
| formats | ManyToManyField vers Format | Plusieurs formats possibles |
| supports | ManyToManyField vers Support | CD, vinyle, etc. |
| contenants | ManyToManyField vers Contenant | Boîtier, digipack, etc. |
| particularites | ManyToManyField vers Particularite | Promo, édition spéciale, etc. |
| types_distribution | ManyToManyField vers TypeDistribution | Commerce, promo, etc. |
| zones_distribution | ManyToManyField vers ZoneDistribution | Zone de sortie |
| zone_fabrication | ForeignKey vers ZoneFabrication | Pays ou zone |
| distributeurs | ManyToManyField vers Label | Labels agissant comme distributeurs |
| labels | ManyToManyField vers Label | Labels éditeurs |
| references | ManyToManyField vers ReferencePressage | Un ou plusieurs codes ref. |
| codes_barres | ManyToManyField vers CodeBarre | Code barre support ou sticker |
| slug | SlugField | Pour l’URL du pressage |
| created_at / updated_at | DateTimeField | Suivi de création / modification |

---

## Modèle `PressageArtiste`

| Champ | Type | Commentaire |
|-------|------|-------------|
| pressage | ForeignKey vers Pressage | Lien vers le pressage |
| artiste | ForeignKey vers Artiste | Artiste concerné |
| type_role | CharField (choix) | principal, feat, présente, etc. |
| role_affiche | CharField (optionnel) | Mention exacte affichée sur pochette |
| ordre_affichage | IntegerField (optionnel) | Tri d’affichage des artistes |

---

## Modèle `Track`

| Champ | Type | Commentaire |
|-------|------|-------------|
| pressage | ForeignKey vers Pressage | Lien vers la fiche |
| numero | CharField | Ex. : "A1", "2", "B3", etc. |
| titre_affiche | CharField | Titre tel qu’imprimé |
| version_affiche | CharField (optionnel) | Ex. : Remix, Edit… |
| duree | DurationField (optionnel) | Durée réelle |
| ordre_affichage | PositiveSmallIntegerField | Pour trier les pistes |
| titre_repertoire | ForeignKey vers TitreVersionRepertoire | Lien vers le répertoire |
| est_cachee | BooleanField | Piste non listée (ni sur disque ni sur pochette) |
| nb_titres_caches | PositiveSmallIntegerField | Nombre de titres cachés dans cette piste |

---

## Modèle `NoteTechnique`

| Champ | Type | Commentaire |
|-------|------|-------------|
| pressage | OneToOneField vers Pressage | Lien vers le pressage |
| note | TextField ou RichTextField (TinyMCE) | Notes libres, remarques techniques |
| code_prix | CharField (optionnel) | Code prix sur sticker ou pochette |
| code_matrice | CharField (optionnel) | Code gravé ou imprimé |
| societes_gestion | ManyToManyField vers SocieteGestion | SACEM, BIEM, etc. |
| images_associees | ManyToManyField vers ImagePressage | Images de pressages liés |
| ordre_affichage | IntegerField (optionnel) | Tri des images associées |
