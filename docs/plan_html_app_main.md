# Plan HTML – app_main

Conventions de nommage et d’organisation

- Tous les templates sont classés dans un dossier templates/, avec sous-dossiers par app si besoin (app_main/, pages/, etc.).

- Les includes sont dans templates/includes/, accessibles à tout le site.

- Les templates suivent une structure modulaire autour de base.html, qui définit l’ossature commune :

    - header.html et footer.html sont inclus automatiquement.

    - Le bloc <main> contient :

        - page_header : en-tête optionnelle (titre dynamique, grille de lettres…)

        - content : cœur du contenu de la page

        - extra_js : zone pour JS spécifique par page

- Le nom des fichiers reflète leur usage :

    - static_page.html pour les pages éditables

    - dynamic_page.html pour les pages à contenu dynamique

    - edit_page.html, contact.html, confirmation_contact.html, etc. pour les vues spécialisées

- Les fichiers d’includes ont des noms explicites et réutilisables : page_title.html, pagination.html, tags.html, etc.


## Templates principaux

### `base.html`
- Structure de base du site
- Inclut :
  - `includes/header.html`
  - `includes/footer.html`
  - Bloc principal `main` avec :
    - `page_header` (facultatif)
    - `content` (contenu principal)
    - `extra_js` (scripts additionnels)

### `edit_page.html`
- Édition d’une page statique via TinyMCE

### `dynamic_page.html`
- Vue dynamique qui inclut :
  - `tag_page.html` si tag
  - `telechargements.html` si page de téléchargements
  - `includes/tags.html` à la fin

### `telechargements.html`
- Liste de fichiers téléchargeables avec options de tri
- Utilise :
  - `includes/page_title.html`
  - `includes/tags.html`

## Dossier `templates/pages/`

### `static_page.html`
- Affiche une page statique (avec image, titre, contenu)
- Gestion spéciale pour `aide`
- Inclut `includes/tags.html` si tags

### `tag_page.html`
- Affiche les contenus liés à un tag :
  - Tri par type (site, blog, etc.)
  - 3 colonnes d’éléments
  - Filtres + pagination + tags associés

### `contact.html`
- Formulaire de contact avec reCAPTCHA, champs et erreurs
- Affiche le résumé du message en cas de validation

### `confirmation_contact.html`
- Affiche un message de confirmation post-envoi

### `error_404.html`, `error_500.html`
- Pages d’erreur personnalisées avec style propre


## Includes (`includes/`)

### `header.html`
- Logo du site
- Inclut `menu.html`

### `menu.html`
- Menu principal (News, Index, Forum, Aide, Téléchargements, Liens, Contact)
- Dropdowns pour index et forum

### `footer.html`
- Navigation secondaire avec 4 colonnes :
  - Navigation, Soundamental, Ressources, Support
  - Lien RSS + copyright

### `tags.html`
- Affiche les tags associés à une page

### `pagination.html`
- Composant de pagination personnalisée

### `page_title.html`
- Affiche un `<h1>` avec `page_title` si défini, sinon `page.title`
