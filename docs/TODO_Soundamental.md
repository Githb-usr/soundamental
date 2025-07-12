
## TODO – Projet Soundamental (à jour)

### Tests unitaires à créer (prioritaire)
- [ ] Tous les modèles principaux : `StaticPageMeta`, `Article`, `Tag`, etc.
- [ ] Vues principales (création, affichage, upload, navigation)
- [ ] Upload : détection de doublons, rendu JSON correct (vérification par dossier uniquement)
- [ ] Index : rendu des pages thématiques, des lettres, tri
- [ ] Blog : affichage par catégorie, navigation article précédent/suivant, archives
- [ ] Filtres custom : `add_class`, `add_data_attr`

### Responsivité du site

---

## Par application

### ✨ app_main (pages statiques / dynamiques)
- [ ] Harmoniser TinyMCE (fait pour `StaticPageForm` ✅ avec `data-section="site"`, `data-subfolder="contenu"`)
- [ ] Vérifier les autres formulaires admin (pages dynamiques si créées)
- [ ] Ajouter tests si des vues spécifiques sont ajoutées
- [ ] Contrôler et valider le rendu HTML (notamment sur mobile)
- [ ] (plus tard) Valider ou désactiver les liens internes dans les contenus enrichis  ???

### 🔍 app_index (index thématiques)
- [ ] Corriger ou améliorer le rendu principal (colonnes, espacement, styles) ???
- [ ] Gérer le cas des liens inactifs (forum uniquement ?) ???
- [ ] Tester la logique de génération par lettre, tri par slug ???

### 🏛️ app_medias (upload / insertion)
- [ ] Tests : `upload_image_form_view`, `media_images_insert_view`, JSON
- [ ] Vérifier le comportement du fallback vers dossier `autres`
- [ ] Valider la bonne insertion via `uploadImageGeneric` + `data-section`/`data-subfolder`
- [ ] (facultatif) Affichage d'un message visuel post-upload dans la popup avant fermeture
- [ ] (facultatif) Tri alphabétique et indentation des sous-dossiers
- [ ] (plus tard) permettre navigation dans des bibliothèques autres que `site` (ex : `pressages`, `artistes`, etc.)

### 📖 app_blog (articles / news)
- [ ] Corriger navigation entre articles (liens précédent / suivant visibles)
- [ ] Revoir présentation des archives (mois/année) + ergonomie
- [ ] Revoir styles CSS des articles (images, badges, marges)
- [ ] Harmoniser config TinyMCE dans le formulaire `ArticleAdminForm` :
  - ✅ `class=richtext`
  - ✅ `data-section=blog`, `data-subfolder=contenu`
- [ ] Ajouter les attributs dynamiquement si usage hors admin (via `add_data_attr`)
- [ ] Ajouter tests : catégories principales/secondaires, navigation, slug, tag, insertion image

---

### 📁 JS / INIT TinyMCE (général)
- [ ] Renommage et clarification des fichiers :
  - `tinymce_rich_init.js` → pour contenu admin et avancé (blog, statiques)
  - `tinymce_basic_init.js` → pour usage allégé, modéré (formulaires simples)
  - `tinymce_contact_init.js` → pour visiteurs (aucun accès fichier, image simple)
- [ ] Vérifier que tous les textarea enrichis hors admin ont bien :
  - `class="richtext"`
  - `data-section="..."`
  - `data-subfolder="..."`
- [ ] Documenter ces règles dans `CONVENTIONS.md`
