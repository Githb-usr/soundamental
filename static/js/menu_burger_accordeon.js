document.addEventListener('DOMContentLoaded', function() {
    let lastIsMobile = null;

    function isMobileMenu() {
        return window.innerWidth <= 991;
    }

    function deactivateBootstrapDropdowns() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function(link) {
            link.removeAttribute('data-bs-toggle');
            link.removeAttribute('aria-expanded');
            link.classList.remove('dropdown-toggle');
        });
    }

    function activateBootstrapDropdowns() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function(link) {
            link.setAttribute('data-bs-toggle', 'dropdown');
            link.setAttribute('aria-expanded', 'false');
            link.classList.add('dropdown-toggle');
        });
        // Supprime la classe "open" éventuelle
        document.querySelectorAll('.site-menu .nav-item.dropdown').forEach(function(item){
            item.classList.remove('open');
        });
    }

    // Nettoie tous les anciens listeners sur les liens de dropdown mobile
    function removeMobileListeners() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function(link) {
            link.replaceWith(link.cloneNode(true));
        });
    }

    // Active l'accordéon mobile (une seule fois)
    function activateAccordionBurgerMenu() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function(parentLink) {
            parentLink.addEventListener('click', function(e) {
                e.preventDefault();
                var parentItem = this.parentElement;
                // Ferme les autres
                document.querySelectorAll('.site-menu .nav-item.dropdown').forEach(function(item){
                    if(item!==parentItem){item.classList.remove('open');}
                });
                parentItem.classList.toggle('open');
            });
        });
    }

    function refreshMenuBehavior() {
        const isMobile = isMobileMenu();
        if (isMobile === lastIsMobile) return; // évite les re-exécutions inutiles
        lastIsMobile = isMobile;

        removeMobileListeners();
        if (isMobile) {
            deactivateBootstrapDropdowns();
            activateAccordionBurgerMenu();
        } else {
            activateBootstrapDropdowns();
        }
    }

    // Initialisation
    refreshMenuBehavior();

    // Mise à jour sur redimensionnement de la fenêtre
    window.addEventListener('resize', refreshMenuBehavior);
});
