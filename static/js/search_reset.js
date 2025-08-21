// Réinitialisation du formulaire de recherche sans toucher aux résultats
// ---------------------------------------------------------------
// - Remet le champ q vide et la portée sur "tout" sans soumission.
// - Ne déclenche aucun rechargement : les résultats affichés restent visibles.

document.addEventListener('DOMContentLoaded', function () {
  const form  = document.getElementById('search-form');
  if (!form) return;

  const input = form.querySelector('input[name="q"]');
  const scope = form.querySelector('select[name="scope"]');
  const btn   = document.getElementById('reset-form-btn');

  if (btn) {
    btn.addEventListener('click', function () {
      if (input) input.value = '';
      if (scope) scope.value = 'tout'; // valeur par défaut attendue côté vue
      if (input) input.focus();
    });
  }
});
