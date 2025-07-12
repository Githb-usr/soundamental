# Plan de code – app_main

## 🎯 Objectif de l’app
Gérer les pages statiques et dynamiques, les fichiers téléchargeables, les tags transversaux et les paramètres globaux de l'application.

---

## 🧩 Modèles principaux

### `AppMainSettings`
- Stocke des paramètres globaux configurables en base (avec cache automatique).
- Clé `name` avec `choices`, valeur `value` (int).

### `StaticPageMeta`
- Page statique avec contenu TinyMCE, catégorie, publication, tags.
- Slug généré automatiquement à partir du titre.
- Historique géré via `StaticPageHistory` (10 dernières modifs).

### `StaticPageHistory`
- Archive des modifications de `StaticPageMeta` (date + utilisateur).

### `DynamicPagePattern`
- Gabarits d’URL dynamiques par catégorie avec format d’affichage (`{name}`).
- Sert à générer dynamiquement les noms affichés.

### `DynamicPageInfo`
- Associe un nom technique (`page_name`) à un nom affiché (`display_name`).
- Utilise `DynamicPagePattern` pour nommer automatiquement.

### `DynamicPageTag`
- Lie un `Tag` à une page dynamique (`page_name`, `display_name` facultatif).

### `DownloadableFile`
- Gère un fichier téléchargeable + image associée.
- Incrémentation automatique du compteur de téléchargements.
- Méthode `register_download()` crée une entrée de log.

### `DownloadLog`
- Enregistre chaque téléchargement avec date.

### `Tag`
- Tag global (pages statiques, dynamiques, articles...).
- Slug automatique.
- Niveau d’accès (`access_level`) : public / inscrit / modérateur / admin.

### `TagPageMeta`
- Lie un `Tag` à d'autres tags connexes (ManyToMany).

---

## 🧠 Signaux
- `post_save` sur `AppMainSettings` pour mettre à jour le cache, sauf si `DISABLE_SIGNALS` est actif (utile en test).

---

## 👁️‍🗨️ Vues principales

### Pages statiques
- `static_page_view(slug)` : affiche une page statique publiée.
- `edit_page(slug)` : formulaire d’édition (TinyMCE) – accès restreint.
- `aide_detail(slug)` : gère l’affichage de la FAQ.

### Pages dynamiques
- `dynamic_page_view(page_name)` : gère toutes les pages dynamiques, redirige si nécessaire vers une page statique ou spéciale (`index`, `telechargements`, etc.).

### Téléchargements
- `telechargements_view()` : liste paginée avec tri.
- `download_file(file_id)` : déclenche le téléchargement + log.

### Tags
- `tag_page_view(slug)` : affiche tous les éléments liés à un tag, triés et paginés en 3 colonnes avec filtres par type.
- `get_visible_tags(user)` : filtre les tags selon les droits.

### Contact
- `contact_view()` : formulaire de contact (catégorie + reCAPTCHA).
- `confirmation_contact()` : page de confirmation après envoi.

---

## 📝 Formulaires

- `StaticPageForm` : édition d'une page statique (`content` via TinyMCE).
- `DownloadableFileForm` : upload de fichiers (formats contrôlés).
- `ContactForm` :
  - Champs : nom, email, structure, sujet, message, catégorie.
  - Protection : champ honeypot + reCAPTCHA.
  - Envoie deux emails (admin + confirmation utilisateur).

---

## 🔗 URLs (`urls.py`)
- Page d’accueil : redirige vers `static_page_accueil`
- `edit/<slug>/` : édition d’une page
- `contact/`, `contact/confirmation-envoi-message/`
- `telechargements/`, `download/<int:id>/`
- `tag/<slug>/`
- `aide/<slug>/` et `aide/`
- Pages statiques explicites (via `STATIC_PAGES`)
- Pages dynamiques : `<str:page_name>/`

---

## ⚙️ Utilitaires
- `paginate()` : gère la pagination avec fallback.
- `check_request_delay()` : anti-spam par délai entre requêtes (utilisé pour le formulaire de contact).


---

## 🖼️ Templates HTML utilisés

### `base.html`
- 📁 `templates/`
- Structure principale du site : header, footer, layout, scripts, blocs extensibles.

### `dynamic_page.html`
- 📁 `templates/app_main/`
- Utilisé par `dynamic_page_view`.
- Inclut soit `telechargements.html`, soit `tag_page.html` selon le nom de la page dynamique.

### `edit_page.html`
- 📁 `templates/app_main/`
- Utilisé par `edit_page`.
- Formulaire pour éditer une page statique avec TinyMCE.

### `telechargements.html`
- 📁 `templates/app_main/`
- Utilisé dans `telechargements_view`, via `dynamic_page.html`.
- Affiche la liste des fichiers téléchargeables, avec options de tri.

### `static_page.html`
- 📁 `templates/pages/`
- Utilisé par `static_page_view` et `aide_detail`.
- Affiche une page statique enrichie (TinyMCE, image, tags, JSON-LD).

### `tag_page.html`
- 📁 `templates/pages/`
- Utilisé par `tag_page_view`.
- Affiche les objets liés à un tag, triés par type et répartis sur 3 colonnes avec pagination.

### `contact.html`
- 📁 `templates/pages/`
- Utilisé par `contact_view`.
- Formulaire de contact avec protection anti-spam, preview du message si déjà envoyé.

### `confirmation_contact.html`
- 📁 `templates/pages/`
- Utilisé par `confirmation_contact`.
- Affiche la confirmation du message avec récapitulatif des champs saisis.

### `error_404.html`
- 📁 `templates/pages/`
- Affiché via `dynamic_page_view` ou configuration globale.
- Design "track not found" original, structure MP3 player stylisée.

### `error_500.html`
- 📁 `templates/pages/`
- Affiché en cas d’erreur serveur.
- Look rétro "terminal", message de panne système.

---


## 📌 À compléter / TODO
- Ajouter tests unitaires.
- Ajouter gestion d’image + suppression dans admin.
- Voir si gestion des rôles avancée est nécessaire ici ou dans une app dédiée.

---

## Points à améliorer (bonnes pratiques Python/Django)
- Tests complets :
  Intégrer des tests pour les vues, les permissions, les erreurs 404, etc.
- Permissions/accès :
  Prévoir une gestion des rôles plus fine dans les vues (admin, modérateurs, visiteurs…).
- Logging :
  Remplacer les print() par le module logging pour une meilleure gestion en production.
- Internationalisation (i18n) :
  Ajouter {% trans %} ou gettext() sur les chaînes visibles du site (formulaires, erreurs, titres...).
