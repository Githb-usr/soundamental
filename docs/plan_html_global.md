# Plan HTML global du site Soundamental

## 1. Templates de base (communs à toutes les apps)

### `base.html`
- Structure de base de toutes les pages
- Blocs principaux :
  - `head` (personnalisable)
  - `title` (par défaut : Soundamental)
  - `main` (avec `page_header`, `content`, `extra_js`)
  - `form.media` (pour TinyMCE)
- Inclut :
  - `includes/header.html`
  - `includes/footer.html`

### `header.html`
- Structure du haut de page
- Contient :
  - Logo cliquable vers l’accueil
  - Inclusion de `menu.html`

### `menu.html`
- Barre de navigation principale
- Contenu :
  - Liens vers News, Index (dropdown), Forum (dropdown), Aide, Téléchargements, Liens, Contact

### `footer.html`
- Pied de page en 4 colonnes :
  - Navigation (Accueil, News, Index...)
  - Soundamental (Pages informatives)
  - Ressources (Liens + RSS)
  - Support (FAQ + Contact)


## 2. Includes génériques

### `tags.html`
- Affiche les tags associés à la page

### `pagination.html`
- Pagination personnalisée avec ellipses

### `page_title.html`
- Affiche un titre de page en `<h1>`
- Utilise `page_title` si défini, sinon `page.title`


## 3. Templates par app

### ▶ **`app_main`**  ✔
- Voir fichier dédié : `Plan Html App Main`

### ▶ **`app_index`**  ✔
- Voir fichier dédié : `Plan Html App Index`

### ▶ **`app_blog`**  ❌ (pas encore inclus)
- À rédiger une fois l’app finalisée

### ▶ Autres apps (futures)
- Aucun template recensé pour l’instant


## 4. Templates d'erreur

### `error_404.html`
- Affichage personnalisé : lecteur MP3 + message "Track Not Found"

### `error_500.html`
- Style "console DOS" avec message technique et humour visuel


## 5. Templates spécifiques email (pas encore inclus)
- Templates HTML pour l’envoi de mails via le formulaire de contact
- à documenter plus tard si besoin


## ✨ Propositions futures
- Ajouter un fichier `README.md` dans `templates/` pour répertorier les conventions
- Regrouper tous les includes dans un sous-dossier `includes/` (déjà en place)
- Harmoniser les noms de classes CSS si besoin


## Points à améliorer (bonnes pratiques HTML)

### Accessibilité (a11y)
- Ajouter aria-label, aria-expanded, role="navigation", etc. pour le menu, les dropdowns, les icônes seules.

### SEO et titres
- Ajouter des <h2>, <h3> dans les sections internes (footer, contact, aide, etc.).
- Compléter systématiquement le bloc {% block title %}.

### JS modulaire (future-proof)
- Prévoir un JS par composant/page (éviter surcharge de base.html).
- Ajouter des conventions data-* au besoin.

### Cache de templates (optionnel)
- Possibilité d’utiliser {% cache %} sur certains blocs très consultés (tags, index).

### Fallback d’image
- Ajouter un placeholder si page.image est absent (ou via CSS/class).

