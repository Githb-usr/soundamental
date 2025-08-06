// blog_categories_sidebar.js
// Ce script gère l'affichage des catégories supplémentaires dans la sidebar du blog.
// Par défaut, seules les 10 premières catégories sont visibles.
// Au clic sur le bouton "Afficher toutes les catégories", on affiche l'ensemble des catégories (enlevant display:none).
// Le bouton change de texte pour permettre de masquer de nouveau les catégories supplémentaires.
// Fonctionne sans dépendance externe.

document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('toggle-categories-btn');
    if (!btn) return;

    var extraCats = document.querySelectorAll('.extra-cat');
    var expanded = false;

    btn.addEventListener('click', function () {
        expanded = !expanded;
        extraCats.forEach(function (el) {
            el.style.display = expanded ? 'list-item' : 'none';
        });
        btn.textContent = expanded ? 'Masquer les catégories' : 'Afficher toutes les catégories';
    });
});
