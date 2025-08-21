// Ouverture/fermeture du popover de recherche dans la navbar
// - Clic sur la loupe : toggle
// - Focus automatique sur l'input à l'ouverture
// - Echap ou clic hors du popover : fermeture

(function () {
  var btn    = document.getElementById('nav-search-toggle');
  var pop    = document.getElementById('nav-search-popover');
  if (!btn || !pop) return;

  var input  = pop.querySelector('input[name="q"]');

  function openPop() {
    pop.classList.add('is-open');
    btn.setAttribute('aria-expanded', 'true');
    if (input) {
      // focus après paint pour éviter les scrolls intempestifs
      setTimeout(function(){ input.focus(); }, 0);
    }
  }

  function closePop() {
    pop.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
  }

  function togglePop() {
    if (pop.classList.contains('is-open')) closePop();
    else openPop();
  }

  btn.addEventListener('click', function (e) {
    e.preventDefault();
    togglePop();
  });

  // Ferme au clic hors du popover
  document.addEventListener('click', function (e) {
    if (!pop.classList.contains('is-open')) return;
    var toggleClicked = btn.contains(e.target);
    var insidePop     = pop.contains(e.target);
    if (!toggleClicked && !insidePop) closePop();
  });

  // Ferme à l'Echap
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pop.classList.contains('is-open')) {
      closePop();
      btn.focus();
    }
  });

  // À la soumission, on laisse la navigation vers la page de recherche
  // (aucune fermeture nécessaire : la page change)
})();
