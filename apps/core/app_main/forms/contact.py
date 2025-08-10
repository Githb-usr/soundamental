from django import forms
from django.forms import Textarea
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import bleach

# =========================
# 📂 FORMULAIRE DE CONTACT
# =========================

# Balises et attributs autorisés pour le message de contact
ALLOWED_TAGS = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'a']
ALLOWED_ATTRS = {'a': ['href']}  # on n'autorise QUE l'URL
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

class ContactForm(forms.Form):
    """
    Formulaire de contact avec choix de catégorie, validation et protection anti-spam.
    """
    CATEGORIES = [
        ("general_site", "Une question sur le site"),
        ("general_forum", "Une question sur le forum"),
        ("technique_site", "Un problème technique sur le site"),
        ("technique_forum", "Un problème technique sur le forum"),
        ("partenariat", "Une proposition de partenariat"),
        ("autre", "Une autre thématique"),
    ]

    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Votre nom'}),
        required=True
    ) 

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Votre email'}),
        required=True
    )
    
    structure = forms.CharField(
        max_length=150,
        required=False,  # 🔹 Champ optionnel
        widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Votre structure (optionnel)'})
    )
    
    categorie = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-select rounded-0'}),
        required=True
    )  # Choix de catégorie

    sujet = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Sujet de votre message'}),
        required=True
    )
    
    message = forms.CharField(
        widget=Textarea(attrs={
            "class": "form-control richtext-contact",
            "style": "min-height: 250px;",
            "placeholder": "Votre message"
        }),
        required=True
    )

    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )  # Champ caché pour piéger les bots
    
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())  # Ajout du reCAPTCHA

    def clean_honeypot(self):
        """Bloque les spams qui remplissent ce champ invisible."""
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError("Spam détecté !")
        return self.cleaned_data['honeypot']
    
    def clean_message(self):
        """
        Nettoie le HTML saisi : on garde une mise en forme minimale (gras/italique/souligné,
        listes, liens) et on supprime tout le reste (styles inline, scripts, iframes, etc.).
        """
        raw = self.cleaned_data.get("message", "")

        # Sanitize strict avec whitelist (constantes définies en haut de fichier)
        safe_html = bleach.clean(
            raw,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True  # supprime les balises interdites au lieu de les échapper
        )

        # Normalisation légère pour éviter les espaces/balises parasites
        safe_html = " ".join(safe_html.split())

        return safe_html

    def send_email(self):
        """ Envoie l'email après validation du formulaire et une copie au visiteur avec format HTML """
        
        context = {
            "nom": self.cleaned_data["nom"],
            "email": self.cleaned_data["email"],
            "categorie": dict(self.CATEGORIES).get(self.cleaned_data["categorie"], "Non spécifiée"),
            "structure": self.cleaned_data["structure"] or "Non renseignée",
            "sujet": self.cleaned_data["sujet"],
            "message": self.cleaned_data["message"]
        }

        # Génération du contenu HTML et texte brut
        html_message = render_to_string("emails/contact_notification.html", context)
        plain_message = strip_tags(html_message)

        # Définition des destinataires administrateurs
        admin_emails = [email for _, email in settings.ADMINS]

        try:
            # Envoi à l'administrateur
            email_admin = EmailMultiAlternatives(
                subject=f"[Soundamental] Nouveau message de {context['nom']} via le formulaire de contact",
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_emails,
            )
            email_admin.attach_alternative(html_message, "text/html")
            email_admin.send()

            # Envoi de la confirmation au visiteur
            html_message_user = render_to_string("emails/contact_confirmation.html", context)
            plain_message_user = strip_tags(html_message_user)

            email_user = EmailMultiAlternatives(
                subject="[Soundamental] Confirmation de votre message",
                body=plain_message_user,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[context["email"]],
            )
            email_user.attach_alternative(html_message_user, "text/html")
            email_user.send()

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi des emails : {e}")  # Debug simple (à remplacer par un logger)
