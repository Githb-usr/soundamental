from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.core.app_main.models.static_pages import StaticPageMeta
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.forms.static_pages import PublicPageEditForm
from apps.core.app_main.views.tags import get_visible_tags
import logging
logger = logging.getLogger("django")

# =================================
# 📂 VUES POUR LES PAGES STATIQUES
# =================================

def static_page_view(request, slug):
    """
    Vue pour afficher une page statique enregistrée en BDD.
    Vérifie aussi si la page est publiée.
    """
    # Récupérer la page statique depuis la base
    page = get_object_or_404(StaticPageMeta, slug=slug, published=True)
    
    # 🔒 Si la page est de catégorie "aide", on n'autorise pas l'accès direct "/<slug>/"
    # → Redirection 301 vers "/aide/<slug>/" (et "/aide/" pour la racine)
    if page.category == "aide":
        if page.slug == "aide":
            return redirect("app_main:aide_root", permanent=True)
        return redirect("app_main:aide_detail", slug=page.slug, permanent=True)

    # Récupérer uniquement les tags associés à cette page ET visibles pour l'utilisateur
    tags = list(Tag.objects.filter(static_pages=page).filter(id__in=get_visible_tags(request.user)))
    
    message_data = None  # Stockage des infos du message envoyé

    # Vérifier si on est sur la page de confirmation et afficher le message envoyé
    if slug == "confirmation-envoi-message":
        message_data = request.session.pop("contact_message", None)  # Récupère et supprime après affichage

    return render(request, "pages/static_page.html", {
        "page": page,
        "message_data": message_data,
        "tags": tags
    })

@login_required
def edit_page(request, slug):
    """
    Permet de modifier une page statique via TinyMCE-7.
    ⚠️ Exception : la page 'aide' (accueil de Aide / FAQ) n’est pas éditable via l’interface,
    car son contenu est géré directement dans le template 'static_page.html'.
    Le bouton d’édition est masqué dans le template quand slug == 'aide'.
    """
    page = get_object_or_404(StaticPageMeta, slug=slug)
    
    # Vérifie si l'utilisateur est admin ou a un rôle d'éditeur
    if not request.user.is_superuser and not request.user.has_perm("app_main.change_staticpagemeta"):
        return redirect("app_main:static_page", slug=slug)  # Redirige vers la page si pas autorisé

    if request.method == "POST":
        form = PublicPageEditForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect("app_main:static_page", slug=page.slug)  # Retourne à la page après édition
    else:
        form = PublicPageEditForm(instance=page)

    return render(request, "app_main/edit_page.html", {"form": form, "page": page})

#########################
## Pages de Aide / FAQ ##
#########################
# ⚠️ Particularité de la page statique "aide"
#
# La page d'accueil de l'aide (slug = "aide") est une exception :
# - Elle doit exister en base dans StaticPageMeta (titre, slug, publication).
# - Mais son contenu HTML n'est pas tiré du champ "content" : il est défini en dur dans le template via un include.
# - Cela permet d'afficher dynamiquement des liens vers les sous-pages d’aide, en détectant leur présence via "pages_by_slug".
# - Le champ "content" est donc ignoré à l'affichage, mais il doit contenir un minimum de texte pour passer les validations admin.

# 🔹 Vue : page individuelle d'une rubrique d'aide
# Affiche le contenu de la page statique correspondant au slug demandé
def aide_detail(request, slug):
    # ⚠️ On limite explicitement aux pages de catégorie "aide"
    page = get_object_or_404(StaticPageMeta, slug=slug, published=True, category="aide")

    # S'il s'agit de la page d'accueil de l'aide, on fournit aussi les autres pages d'aide
    pages_by_slug = None
    if slug == "aide":
        # ⚠️ On ne liste que les sous-pages d'aide
        autres_pages = (StaticPageMeta.objects
                        .filter(published=True, category="aide")
                        .exclude(slug="aide"))
        pages_by_slug = {p.slug: p for p in autres_pages}

    return render(request, "pages/static_page.html", {
        "page": page,
        "pages_by_slug": pages_by_slug,
    })
