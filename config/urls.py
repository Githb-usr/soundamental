from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import render
from apps.core.app_index import urls as app_index_urls
from django.http import HttpRequest
from config.handlers import custom_error_500

def trigger_error(request: HttpRequest):
    1 / 0

# handler400 = "config.handlers.custom_error_400"
# handler403 = "config.handlers.custom_error_403"
handler404 = "config.handlers.custom_error_404"
handler500 = "config.handlers.custom_error_500"

urlpatterns = [
    path("error-500/", custom_error_500),  # TEMP pour test visuel
    path("test-error-500/", trigger_error),
    path('admin/', admin.site.urls), # Active l'admin Django
    path("select2/", include("django_select2.urls")),  # ⬅ requis pour le JS/AJAX, recherche dans les formulaires en ligne
    
    # L’index général et les index thématiques
    path("index/", include(app_index_urls, namespace="app_index")),
    
    # Le blog (news)
    path('news/', include('apps.content.app_blog.urls', namespace='app_blog')),
    
    # Route vers la vue d'upload d'image centralisée (utilisée par TinyMCE)
    path("medias/", include("apps.core.app_medias.urls", namespace="app_medias")),
    
    # Connexion et déconnexion
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Toutes les autres routes dynamiques (accueil, pages, contact, etc.)
    path("", include("apps.core.app_main.urls", namespace="app_main")),
]

# Permet à Django de servir les fichiers uploadés en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Ajout conditionnel de Debug Toolbar
    try:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    except ImportError:
        pass  # Si debug_toolbar n'est pas installé, on ignore l'erreur

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
