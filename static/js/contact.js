document.addEventListener("DOMContentLoaded", function () {
    // Compte à rebours
    let countdownElement = document.getElementById("timer");
    let errorContainer = document.getElementById("error-container");

    if (countdownElement) {
        let timeLeft = parseInt(countdownElement.innerText, 10);

        let countdownInterval = setInterval(function () {
            if (timeLeft > 1) {
                timeLeft--;
                countdownElement.innerText = timeLeft; // 🔹 Met à jour dynamiquement le compte à rebours
            } else {
                clearInterval(countdownInterval);
                if (errorContainer) {
                    errorContainer.style.display = "none"; // 🔹 Cache le message d'erreur une fois fini
                }
                let sendButton = document.querySelector("button[type='submit']");
                if (sendButton) {
                    sendButton.disabled = false;  // 🔹 Réactive le bouton "Envoyer"
                }
            }
        }, 1000);
    }

    // Bouton Effacer
    let resetButton = document.getElementById("reset-btn");
    let contactForm = document.getElementById("contact-form");

    if (resetButton && contactForm) {
        resetButton.addEventListener("click", function () {
            console.log("DEBUG: Bouton Effacer cliqué !");
            contactForm.reset();

            if (window.editors && window.editors["id_message"]) {
                window.editors["id_message"].setData("");
            }
        });
    }
});
