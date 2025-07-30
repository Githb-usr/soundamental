from django.urls import path
from django.shortcuts import redirect
from django.conf import settings

from apps.core.app_main.views import static_pages
from apps.core.app_main.views.static_pages import static_page_view, edit_page
from apps.core.app_main.views.dynamic_pages import dynamic_page_view
from apps.core.app_main.views.downloads import telechargements_view, download_file
from apps.core.app_main.views.home import home_view
from apps.core.app_main.views.tags import tag_page_view
from apps.core.app_main.views.contact import contact_view, confirmation_contact

app_name = "app_main"

urlpatterns = [
    # Page d'accueil
    path("", home_view, name="home"),
    
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
    
    # Pages statiques d'aide individuelles
    path("aide/", static_pages.aide_detail, {"slug": "aide"}, name="aide_root"),
    path("aide/<slug:slug>/", static_pages.aide_detail, name="aide_detail"),
    
    # Pages statiques (accès par tout slug correspondant à une page publiée en BDD)
    # Route universelle : capture tout slug pour afficher une page statique si elle existe (sinon 404)
    path("<slug:slug>/", static_page_view, name="static_page"),
     
    # Gestion des pages dynamiques (elles ne doivent PAS entrer en conflit avec les pages statiques)
    path("<str:page_name>/", dynamic_page_view, name="dynamic_page"),  # 🔹 Toujours utile pour les autres pages dynamiques
]
  