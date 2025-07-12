# 🗂️ App Index – Soundamental

Cette app Django gère l’**index général** et les **index thématiques** (artistes, labels, compilations, lexique) du projet Soundamental.

## 🔧 Fonctionnalités principales

- Affichage dynamique d’un index trié par lettre et sous-lettre.
- Filtrage par catégorie (ex : uniquement les artistes).
- Lien vers des pages internes (biographie, discographie, etc.) si elles existent.
- Lien vers le forum si un topic est référencé.
- Import/export des entrées via l’admin (fichier Excel).
- Activation des sous-lettres configurable par catégorie.

## 🧩 Structure des modèles

### `IndexEntry`
Représente une entrée de l’index (artiste, compilation, label, etc.).

- `name` : nom de l’entrée.
- `category` : catégorie (`artiste`, `label`, etc.).
- `id_forum` : identifiant de topic sur le forum.
- `get_links` : liste les liens disponibles pour cette entrée.
- `get_forum_url` : génère l’URL complète du forum.

### `PageExistence`
Stocke les pages réellement existantes (par type et nom) pour éviter de générer des liens invalides.

- `category` : type d'entrée (`artiste`, `label`, etc.)
- `name` : nom associé.
- `page_type` : type de page (biographie, discographie...).

### `IndexSettings`
Paramètres d’affichage (notamment les sous-lettres) selon la catégorie.

- `category` : `index` (général) ou une catégorie précise.
- `apply_to_all` : active les sous-lettres pour toutes les lettres/chiffres.
- `letters_with_sub_buttons` : lettres personnalisées activant des sous-pages.

---

## 🔄 Signaux

- Création d'une `IndexEntry` si une nouvelle `PageExistence` est ajoutée.
- Suppression de la `IndexEntry` si la dernière page associée est supprimée.

---

## 🧠 Logique de vues

### `index_or_category_view()`
- Gère :
  - L’index général : `/index/A/`, `/index/B/Ba/`, etc.
  - Les index thématiques : `/category/artistes/A/Az/`
- Applique le filtre selon la lettre, la sous-lettre, et la catégorie.
- Charge dynamiquement les liens disponibles via `get_links`.

---

## 📄 Template : `index.html`

- Gère l'affichage des lettres, sous-lettres, catégorie.
- Grille de 5 liens maximum par entrée.
- Table responsive avec pagination intégrée.
- Utilisation des variables :
  - `letter`, `sub_letter`, `category`, `index_data`, `show_sub_buttons`.

---

## 🛠️ Admin

- `IndexEntryAdmin` :
  - Import/export via `django-import-export`.
  - Colonne personnalisée `liens_existant` pour visualiser les liens actifs.
- `PageExistenceAdmin` :
  - Gestion manuelle si besoin.
- `IndexSettingsAdmin` :
  - Activation des sous-lettres personnalisée ou globale.

---

## 📁 Fichiers

- `models.py` : modèles principaux de l’index.
- `views.py` : logique de filtrage, redirection, rendu.
- `urls.py` : routes de l’index général et thématique.
- `admin.py` : intégration avancée dans l’admin.
- `signals/index.py` : signaux pour mise à jour auto des entrées.
- `templates/app_index/index.html` : rendu HTML de l’index.
- `tests/` : tests à ajouter.

---

## 🧪 TODO : Tests

Il reste à ajouter les tests automatiques pour :

- Le modèle `IndexEntry`.
- Le modèle `PageExistence`.
- La vue `index_or_category_view()`.
- La génération des liens (`get_links`).

---

## 💬 Remarques

- L’app est pensée pour être **extensible** (plus de 5 liens à terme).
- Toutes les URLs générées sont **conditionnelles** : elles apparaissent seulement si la page existe (`PageExistence`) ou si `id_forum` est renseigné.
- L'import Excel dans l'admin est conçu pour faciliter le démarrage du projet.

---

## Points à améliorer (bonnes pratiques Python/Django)
- Tests automatiques : Aucun test n’est encore défini pour app_index. Il faudrait :
  - tester la génération de l’index (vues index_or_category_view)
  - tester les URLs avec lettres/sous-lettres
  - tester les cas où une page n’existe pas
- Permissions d’accès : Toutes les vues sont publiques. Prévoir :
  - une restriction à l’admin pour certaines fonctions ?
  - un accès conditionnel à certains types d’entrées ou catégories ?
- Internationalisation (i18n) : Les chaînes visibles dans le HTML ne sont pas encore traduisibles (gettext, {% trans %}, etc.).
- Logging (optionnel) : Quelques print() ou vérifications (dans l’admin notamment) pourraient être remplacés par logging.
