document.addEventListener('DOMContentLoaded', function () {
    let lastIsMobile = null;

    function isMobileMenu() {
        return window.innerWidth <= 991;
    }

    function deactivateBootstrapDropdowns() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function (link) {
            link.removeAttribute('data-bs-toggle');
            link.removeAttribute('aria-expanded');
            link.classList.remove('dropdown-toggle');
        });
    }

    function activateBootstrapDropdowns() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function (link) {
            link.setAttribute('data-bs-toggle', 'dropdown');
            link.setAttribute('aria-expanded', 'false');
            link.classList.add('dropdown-toggle');
        });
        document.querySelectorAll('.site-menu .nav-item.dropdown').forEach(function (item) {
            item.classList.remove('open');
        });
    }

    function removeMobileListeners() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function (link) {
            link.replaceWith(link.cloneNode(true));
        });
    }

    function activateAccordionBurgerMenu() {
        document.querySelectorAll('.site-menu .nav-item.dropdown > .nav-link').forEach(function (parentLink) {
            parentLink.addEventListener('click', function (e) {
                e.preventDefault();
                var parentItem = this.parentElement;
                document.querySelectorAll('.site-menu .nav-item.dropdown').forEach(function (item) {
                    if (item !== parentItem) {
                        item.classList.remove('open');
                    }
                });
                parentItem.classList.toggle('open');
            });
        });
    }

    function refreshMenuBehavior() {
        const isMobile = isMobileMenu();
        if (isMobile === lastIsMobile) return;
        lastIsMobile = isMobile;

        removeMobileListeners();
        if (isMobile) {
            deactivateBootstrapDropdowns();
            activateAccordionBurgerMenu();
        } else {
            activateBootstrapDropdowns();
        }
    }

    refreshMenuBehavior();
    window.addEventListener('resize', refreshMenuBehavior);

    const burger = document.getElementById("burgerIcon");
    const navList = document.getElementById("mainNavList");

    if (burger && navList) {
        burger.addEventListener("click", function () {
            navList.classList.toggle("open");
            navList.style.display = navList.classList.contains("open") ? "block" : "";
        });

        document.addEventListener("click", function (event) {
            const isOpen = navList.classList.contains("open");
            const clickedInsideMenu = navList.contains(event.target);
            const clickedBurger = burger.contains(event.target);

            if (isOpen && !clickedInsideMenu && !clickedBurger) {
                navList.classList.remove("open");
                navList.style.display = "";
            }
        }, true); // capture
    }
});
