from django.shortcuts import render, redirect
from apps.core.app_main.models.dynamic_pages import DynamicPageInfo
from apps.core.app_main.models.static_pages import StaticPageMeta
from apps.core.app_main.views.tags import get_visible_tags
from apps.core.app_index.views import index_or_category_view
from apps.core.app_main.views.static_pages import static_page_view
from django.conf import settings
from django.http import Http404

# ==================================
# 📂 VUES POUR LES PAGES DYNAMIQUES
# ==================================

def dynamic_page_view(request, page_name):
    """
    Vue pour afficher une page dynamique, sauf si elle existe en tant que page statique.
    Exemple : 'telechargements' affichera la liste des fichiers téléchargeables.
    """
    # 🔒 Ne pas traiter certaines routes système
    if page_name in ["400", "403", "404", "500", "test-error-500", "error-500"]:
        raise Http404("Route réservée au système")
    
    # 🚨 Vérifier si la page existe en tant que page statique
    STATIC_PAGES = settings.STATIC_PAGES  # On récupère la liste des pages statiques
    if page_name in STATIC_PAGES:
        return static_page_view(request, slug=page_name)

    # 🚨 Vérifier si la page existe dans la base de données des pages dynamiques
    if not DynamicPageInfo.objects.filter(page_name=page_name).exists():
        return render(request, "pages/errors/error_404.html", status=404)
    
    if page_name == "index":
        return index_or_category_view(request)  # 🔹 Appelle la vue index_view directement
    
    # Vérifier si la page existe en tant que page statique
    if StaticPageMeta.objects.filter(slug=page_name, published=True).exists():
        return static_page_view(request, slug=page_name)  # Redirige vers la vue statique

    # Vérifier si une info de page dynamique existe
    page_info = DynamicPageInfo.objects.filter(page_name=page_name).first()
    
    # if not page_info:
    #     raise Http404("Page non trouvée")
    
    context = {"page_name": page_name}
    
    # Récupérer les tags associés à cette page dynamique
    # tags = get_visible_tags(request.user).filter(dynamicpagetag__page_name=page_name)
    tags = get_visible_tags(request.user).filter(dynamic_pages__page_name=page_name)
    context["tags"] = tags
    
    # Vérifier si un `display_name` est défini pour cette page dynamique
    page_info = DynamicPageInfo.objects.filter(page_name=page_name).first()
    display_name = page_info.display_name if page_info else page_name.replace("-", " ").title() # Génère un nom si absent
    context["display_name"] = display_name  # Ajout au contexte
    
    return render(request, "app_main/dynamic_page.html", context)
