document.addEventListener('DOMContentLoaded', function () {
    const accordions = document.querySelectorAll('.index-accordion details');

    // 1) Un seul accordéon ouvert à la fois
    accordions.forEach((acc) => {
        acc.addEventListener('toggle', function () {
            if (this.open) {
                accordions.forEach((other) => {
                    if (other !== this) {
                        other.open = false;
                    }
                });
            }
        });
    });

    // 2) Fermer tous les accordéons si clic en dehors
    document.addEventListener('click', function (event) {
        const clickedInsideAccordion = event.target.closest('.index-accordion details');
        if (!clickedInsideAccordion) {
            accordions.forEach((acc) => {
                acc.open = false;
            });
        }
    });
});
