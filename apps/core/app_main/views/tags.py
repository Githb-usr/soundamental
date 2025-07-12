from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from apps.core.app_main.models.dynamic_pages import DynamicPageTag
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.models.tag_meta import TagPageMeta

# ========================
# # 📂 VUES POUR LES TAGS
# ========================

# Correspondance type → classe CSS (badge)
BADGE_CLASSES = {
    "site": "badge-type-site",
    "page": "badge-type-page",
    "blog": "badge-type-blog",
    "pressage": "badge-type-pressage",
    "tag": "badge-type-page",
    # tu pourras en ajouter d'autres ici plus tard
}

# Nombre max d’éléments par colonne sur une page tag
MAX_TAGS_PER_COLUMN = 20

def collect_tagged_items(tag):
    """
    Rassemble tous les objets associés au tag avec leur type et leur badge.
    """
    items = []

    for page in tag.static_pages.all():
        items.append({"type": "site", "object": page, "badge_class": BADGE_CLASSES["site"]})

    for dyn in DynamicPageTag.objects.filter(tag=tag).select_related("page_info"):
        items.append({"type": "page", "object": dyn, "badge_class": BADGE_CLASSES["page"]})

    for article in tag.articles.filter(est_publie=True).order_by('-date_publication'):
        items.append({"type": "blog", "object": article, "badge_class": BADGE_CLASSES["blog"]})
        
    # Pages de tags associées (TagPageMeta → related_tags)
    for meta in TagPageMeta.objects.filter(related_tags=tag).select_related("tag"):
        items.append({
            "type": "tag",
            "object": meta.tag,  # Le tag correspondant à la page
            "badge_class": BADGE_CLASSES["tag"]
            # "badge_class": BADGE_CLASSES.get("tag", "badge-type-page"),  # Couleur par défaut
        })

    return items

def sort_items(items):
    """
    Trie les items selon le nom visible (titre, display_name ou titre d'article).
    """
    return sorted(
        items,
        key=lambda i: getattr(i["object"], "title", None) or
                      getattr(i["object"], "page_info", None) and i["object"].page_info.display_name or
                      getattr(i["object"], "titre", "")
    )

def paginate_and_split(items, request, per_page=60, num_columns=3, max_per_column=20):
    """
    Paginer les items et les répartit dans des colonnes équilibrées.
    """
    paginator = Paginator(items, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    columns = [[] for _ in range(num_columns)]
    for i, item in enumerate(page_obj.object_list):
        col_index = min(i // max_per_column, num_columns - 1)
        columns[col_index].append(item)

    return page_obj, columns


def tag_page_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    try:
        tag_meta = TagPageMeta.objects.get(tag=tag)
        related_tags = tag_meta.related_tags.all()
    except TagPageMeta.DoesNotExist:
        related_tags = []
    all_items = sort_items(collect_tagged_items(tag))

    selected_type = request.GET.get("type")
    filtered_items = [i for i in all_items if i["type"] == selected_type] if selected_type else all_items

    types_present = set(i["type"] for i in all_items)  # Tous les types existants (même si filtré)
    page_obj, (column1, column2, column3) = paginate_and_split(filtered_items, request, max_per_column=MAX_TAGS_PER_COLUMN)

    context = {
        "tag": tag,
        "page_name": f"tag-{tag_slug}",
        "page_obj": page_obj,
        "column1": column1,
        "column2": column2,
        "column3": column3,
        "total_items": len(filtered_items),
        "selected_type": selected_type,
        "badge_classes": BADGE_CLASSES,
        "types_present": types_present,
        "related_tags": related_tags,
    }

    return render(request, "pages/tag_page.html", context)

def get_visible_tags(user):
    """
    Récupère les tags visibles selon le rôle de l'utilisateur.
    """
    if user.is_superuser:
        return Tag.objects.all().order_by("name")  # Admin voit tout
    elif user.is_authenticated:
        return Tag.objects.exclude(access_level=Tag.ACCESS_LEVELS["admin"]).order_by("name")  # Utilisateur normal ne voit pas les tags admin
    else:
        return Tag.objects.filter(access_level=Tag.ACCESS_LEVELS["public"]).order_by("name")   # Visiteur ne voit que les tags publics
