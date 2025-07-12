## 📁 plan_html_app_index.md

Ce document décrit la structure HTML des templates utilisés dans l'app **`app_index`** du projet Soundamental.

---

### 🗂️ Template : `templates/app_index/index.html`

#### 🔗 Hérite de :
- `base.html`

#### 📦 Blocs utilisés :
- `{% block main_class %}` : applique les classes CSS `main-index no-top-padding`
- `{% block page_header %}` : affiche le titre et les lettres de navigation (grille principale A-Z + 0-9 + @)
- `{% block content %}` : contenu principal avec grille des sous-lettres, tableau des résultats et pagination

#### 🔤 Variables attendues dans le contexte :
- `category` → pour filtrer l’index (ex : artistes, labels…)
- `letter` → lettre sélectionnée
- `sub_letter` → sous-lettre sélectionnée (ex: Aa, Ab...)
- `show_sub_buttons` → booléen pour afficher les sous-lettres
- `index_data` → liste paginée des entrées, chaque item contient :
  - `entry.name`
  - `entry.category`
  - `entry.category_url`
  - `entry.links` → liste de dictionnaires `{ link, label }`
- `page_obj`, `paginator` → pagination

#### 🧩 Includes utilisés :
- `includes/pagination.html` (2 fois)

#### 🧠 Particularités :
- Gestion intelligente des lettres et sous-lettres avec redirections automatiques
- Affichage des types de liens disponibles pour chaque entrée (BIO, DIS, etc.)
- Affichage conditionnel du lien vers la catégorie quand `category` est absente (index général)
- Design responsive basé sur une grille CSS (`grid-4x10`, `index-table`, etc.)

---

👉 Le fichier `index.html` constitue **l'unique template HTML spécifique à l'app `app_index`** à ce jour. Les autres composants (grille, pagination, layout) sont partagés avec le reste du site via les `includes/` et `base.html`.
