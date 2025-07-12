import pytest
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.messages import get_messages
from unittest.mock import patch
from apps.core.app_main.models.static_pages import StaticPageMeta
from apps.core.app_main.forms.contact import ContactForm


@pytest.mark.django_db
def test_contact_view_get(client):
    """Test de l'affichage de la page de contact en mode GET"""
    # Création d'une page statique pour "contact"
    StaticPageMeta.objects.create(title="Contact", slug="contact", content="Page de contact")

    response = client.get(reverse("app_main:contact"))
    
    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], ContactForm)
    assert "page_title" in response.context
    assert "Contact" in response.content.decode()


import pytest
from unittest.mock import patch
from django.urls import reverse
from apps.core.app_main.forms.contact import ContactForm

import pytest
from unittest.mock import patch
from django.urls import reverse
from apps.core.app_main.forms.contact import ContactForm

@pytest.mark.django_db
@patch("apps.core.app_main.forms.contact.ContactForm.send_email")  # Mock l'envoi d'email
@patch("apps.core.app_main.forms.contact.ReCaptchaField.clean")  # Mock le reCAPTCHA pour éviter l'erreur
def test_contact_view_post_valid(mock_recaptcha, mock_send_email, client):
    """Test de soumission valide du formulaire de contact"""
    mock_recaptcha.return_value = True  # Bypass la validation du reCAPTCHA

    form_data = {
        "nom": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "structure": "Test Corp",
        "categorie": "general_site",
        "sujet": "Problème sur le site",
        "message": "Bonjour, j'ai un souci...",
    }

    response = client.post(reverse("app_main:contact"), data=form_data, follow=True)

    # ✅ Vérifier si la redirection a bien eu lieu
    assert response.redirect_chain, "❌ Pas de redirection détectée !"
    assert response.redirect_chain[-1][0] == reverse("app_main:confirmation_contact"), "❌ Mauvaise redirection"

    # ✅ Vérifier que l'email a bien été envoyé
    assert mock_send_email.called, "❌ L'email n'a pas été envoyé"

@pytest.mark.django_db
@patch("apps.core.app_main.forms.contact.ReCaptchaField.clean")  # Mock le reCAPTCHA pour éviter l'erreur
def test_contact_view_post_invalid(mock_recaptcha, client):
    """Test de soumission invalide du formulaire (champs vides)"""
    mock_recaptcha.return_value = True  # Bypass la validation du reCAPTCHA

    form_data = {
        "nom": "",
        "email": "",
        "structure": "",
        "categorie": "",
        "sujet": "",
        "message": "",
    }

    response = client.post(reverse("app_main:contact"), data=form_data, follow=True)

    # ✅ Vérifier que la clé "form" est bien présente
    assert "form" in response.context, "❌ Le contexte ne contient pas `form`"

    # ✅ Vérifier que le formulaire a bien été lié à la requête
    form = response.context["form"]
    assert isinstance(form, ContactForm), f"❌ `form` n'est pas un `ContactForm`, trouvé : {type(form)}"
    assert form.is_bound, "❌ Le formulaire n'a pas été lié (is_bound=False), il n'a pas reçu les données POST"

    # ✅ Vérifier que le formulaire contient bien des erreurs
    assert form.errors, "❌ Le formulaire aurait dû contenir des erreurs"



@pytest.mark.django_db
def test_contact_view_delay(client):
    """Test de la protection contre le spam (délai entre deux envois)"""
    session = client.session
    session["last_contact_time"] = now().timestamp()
    session.save()

    response = client.post(reverse("app_main:contact"), follow=True)
    
    messages = list(get_messages(response.wsgi_request))
    assert any("Vous devez attendre encore" in str(m) for m in messages)  # Vérifie la présence du message d'erreur


@pytest.mark.django_db
def test_confirmation_contact(client):
    """Test de la page de confirmation après envoi du formulaire"""
    session = client.session
    session["contact_message"] = {
        "nom": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "sujet": "Test",
        "message": "Ceci est un message de test.",
    }
    session.save()

    response = client.get(reverse("app_main:confirmation_contact"))
    
    assert response.status_code == 200
    assert "Jean Dupont" in response.content.decode()  # Vérifie l'affichage des données du message
