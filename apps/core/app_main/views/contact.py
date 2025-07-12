from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.core.app_main.forms.contact import ContactForm
from apps.core.utils import check_request_delay

# ======================================
# 📂 VUES POUR LE FORMULAIRE DE CONTACT
# ======================================

def handle_contact_submission(request, form):
    """Gère l'envoi du formulaire et l'enregistrement des données en session."""
    # Vérification reCAPTCHA automatique grâce à Django
    form.send_email()
    request.session["last_contact_time"] = now().timestamp() # Sauvegarde l'heure d'envoi
    # Stocke les données du message dans la session pour les afficher sur la confirmation
    request.session["contact_message"] = {
        "nom": form.cleaned_data["nom"],
        "email": form.cleaned_data["email"],
        "structure": form.cleaned_data["structure"],
        "sujet": form.cleaned_data["sujet"],
        "message": form.cleaned_data["message"],
    }
    return redirect("app_main:confirmation_contact") # Redirection vers la page de confirmation

def contact_view(request):
    """
    Vue pour afficher le formulaire de contact et gérer l'envoi des messages.
    """
    form = ContactForm(request.POST or None)
    base_context = {
        "form": form,
        "page_title": "Contact",
    }

    # Empêche le renvoi immédiat d’un nouveau message (anti-spam)
    delay_info = check_request_delay(request, session_key="last_contact_time")
    if delay_info:
        return render(request, "pages/contact.html", {**base_context, **delay_info})

    if form.is_bound and form.is_valid():
        return handle_contact_submission(request, form)

    return render(request, "pages/contact.html", base_context)

def confirmation_contact(request):
    """
    Affiche la page de confirmation après l'envoi du formulaire de contact.
    """
    message_data = request.session.pop("contact_message", None)  # Récupère et supprime après affichage

    return render(request, "pages/confirmation_contact.html", {"message_data": message_data})
