from django.urls import path
from django.shortcuts import redirect
from django.conf import settings

from apps.core.app_main.views import static_pages
from apps.core.app_main.views.static_pages import static_page_view, edit_page
from apps.core.app_main.views.dynamic_pages import dynamic_page_view
from apps.core.app_main.views.downloads import telechargements_view, download_file
from apps.core.app_main.views.tags import tag_page_view
from apps.core.app_main.views.contact import contact_view, confirmation_contact

STATIC_PAGES = getattr(settings, "STATIC_PAGES", [])  # Récupérer STATIC_PAGES avec une valeur par défaut
DYNAMIC_RESERVED_NAMES = getattr(settings, "DYNAMIC_RESERVED_NAMES")  # Liste des pages dynamiques réservées

# 🔹 Vérifier s'il y a un conflit entre STATIC_PAGES et les pages dynamiques réservées
conflicts = set(STATIC_PAGES) & set(DYNAMIC_RESERVED_NAMES)
if conflicts:
    raise ValueError(f"🚨 Conflit entre pages statiques et dynamiques : {conflicts}")

app_name = "app_main"

urlpatterns = [
    path("", lambda request: redirect("app_main:static_page_accueil"), name="home"),
    
    # Téléchargements
    path("download/<int:file_id>/", download_file, name="download_file"),
    path("telechargements/", telechargements_view, name="telechargements"),  # 🔹 Route directe pour la page des téléchargements
    
    # Édition des pages en ligne
    path("edit/<slug:slug>/", edit_page, name="edit_page"),  # Doit être placé AVANT <slug:slug>
    
    # Contact
    path("contact/", contact_view, name="contact"),  # Route pour la page contact
    path("contact/confirmation-envoi-message/", confirmation_contact, name="confirmation_contact"),
    
    # Page d'un tag
    path("tag/<slug:tag_slug>/", tag_page_view, name="tag_page"),
    
    # Gestion des pages statiques définies explicitement (PRIORITÉ SUR LES DYNAMIQUES)
    *[path(f"{page}/", static_page_view, {"slug": page}, name=f"static_page_{page}") for page in STATIC_PAGES],

    # Pages statiques d'aide individuelles
    path("aide/", static_pages.aide_detail, {"slug": "aide"}, name="aide_root"),
    path("aide/<slug:slug>/", static_pages.aide_detail, name="aide_detail"),
    
    # Gestion des pages dynamiques (elles ne doivent PAS entrer en conflit avec les pages statiques)
    path("<str:page_name>/", dynamic_page_view, name="dynamic_page"),  # 🔹 Toujours utile pour les autres pages dynamiques
]
  