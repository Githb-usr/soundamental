# CONVENTIONS.md

## Conventions de développement pour Soundamental

---

### 1. Structure des templates
- Tous les fichiers HTML sont dans `templates/`.
- Sous-dossiers par app si besoin : `app_main/`, `pages/`, etc.
- Fichiers réutilisables dans `includes/`.
- Un layout principal `base.html` structure tout le site.

### 2. Nommage des fichiers templates
- `static_page.html` : page statique gérée via l’admin
- `dynamic_page.html` : générée dynamiquement (ex : téléchargements)
- `edit_page.html`, `contact.html`, `confirmation_contact.html` : pages fonctionnelles
- Les includes suivent la forme : `page_title.html`, `pagination.html`, `tags.html`, etc.

### 3. Structure de `base.html`
- Blocs principaux utilisés :
  - `head` : balises <meta>, opengraph, etc.
  - `title` : titre de l’onglet navigateur
  - `main_class` : pour les classes CSS adaptatives
  - `page_header` : affichage facultatif (titre, grille...)
  - `content` : contenu principal
  - `extra_js` : scripts JS optionnels par page

### 4. CSS / JS
- Fichier CSS principal : `custom.css`
- Aucun style global non ciblé (pas de `h1 {}` global)
- JS appelé via bloc `extra_js`, chargé en fin de page avec `defer`

### 5. Accessibilité & SEO
- Un seul `<h1>` par page, utilisé via `page_title.html`
- Attributs `alt` toujours définis pour les images
- Balises `meta` avec description + opengraph + JSON-LD si nécessaire

### 6. Pagination & Tags
- Pagination personnalisée avec `pagination.html`
- Tags affichés via `tags.html`, adaptés aux droits utilisateur

### 7. Includes
- Tous les blocs réutilisables doivent être isolés dans `includes/`
- Les noms doivent être explicites : `header.html`, `footer.html`, `menu.html`

### 8. Convention de rôles (template)
- Les vues passent toutes les variables nécessaires explicitement
- Aucun comportement implicite ou dépendance cachée dans les templates

### 9. Images
Conventions d’utilisation des attributs alt et title pour les balises <img>

alt : obligatoire, sauf cas décoratif
Cas d’image	                                       Attribut alt à utiliser
Image informative (logo, visuel, illustration)	   alt="Logo du label XYZ"
Image décorative (ornement, icône sans rôle)	     alt="" (vide, sans espace)
Image utilisée comme lien	                         alt="Voir la fiche label XYZ"

🎯 Le alt doit être court, descriptif, et sans doublon inutile.
⛔ Ne jamais écrire "image de", sauf si c’est pertinent (ex. : alt="Image manquante").
-----------------------------

title : optionnel
Cas d’usage	                             Utiliser title ?
Besoin d’une infobulle complémentaire	   ✅ Oui, ex : title="Ancien logo (1998-2004)"
Redondant avec alt	                     ❌ Non
Accessibilité ou navigation mobile	     ❌ Non recommandé (non fiable)

⚠️ Ne pas compter sur title pour l’accessibilité.
Il s’affiche au survol souris, mais pas sur mobile ou clavier.


🔐 Règle : correspondance catégorie / sous-dossier pour TinyMCE
Le champ categorie_principale d’un article de blog est utilisé pour déterminer automatiquement le dossier cible d’upload d’image dans l’éditeur TinyMCE.
⚠️ Par convention, la value HTML de chaque catégorie (ex: news_site, news_artistes) doit correspondre exactement au nom d’un sous-dossier dans media/blog/.
Exemple :
- categorie_principale = "news_labels" → images stockées dans media/blog/news_labels/
- Si aucune catégorie n’est sélectionnée → fallback : media/blog/illustrations/

---

> Ce fichier est à maintenir à jour à chaque évolution des templates, includes, ou conventions de style.
