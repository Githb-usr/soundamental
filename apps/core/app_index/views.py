from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from apps.core.utils import paginate
from apps.core.app_index.models import IndexEntry, IndexSettings, PageExistence

# =======================
# # 📂 VUES POUR L'INDEX
# =======================

def get_index_settings(category):
    """
    Récupère les paramètres d'affichage pour une catégorie donnée (ou l'index général).
    """
    try:
        return IndexSettings.objects.get(category=category if category else "index")
    except IndexSettings.DoesNotExist:
        return None  # Aucune configuration trouvée

def filter_index_entries(category, letter, sub_letter):
    """
    Filtre les entrées de l'index en fonction de la catégorie, lettre et sous-lettre.
    """
    index_entries = IndexEntry.objects.only("id", "name", "category", "id_forum").order_by("name")

    # Filtrage par catégorie
    if category:
        category_singular = settings.CATEGORY_MAPPING.get(category.lower(), category.lower())
        index_entries = index_entries.filter(category=category_singular)

    # Filtrage par lettre
    if letter == "@":
        index_entries = index_entries.filter(name__regex=r"^[^A-Za-z0-9]")  # Caractères spéciaux
    else:
        index_entries = index_entries.filter(name__istartswith=letter)

    # Filtrage par sous-lettre
    sub_letter = sub_letter or ""
    if sub_letter == letter:
        index_entries = index_entries.filter(
            Q(name__istartswith=sub_letter + " ") |  
            Q(name__istartswith=sub_letter + ".") |  
            Q(name__istartswith=sub_letter + "-") |  
            Q(name__istartswith=sub_letter + "'")  
        )
    else:
        index_entries = index_entries.filter(name__istartswith=sub_letter)

    return index_entries

def generate_index_data(index_entries):
    """
    Génère les données d'affichage pour l'index à partir des entrées filtrées.
    Utilise directement la propriété `get_links` de chaque entrée.
    """
    index_data = []

    for entry in index_entries:
        template = settings.INDEX_LINK_TEMPLATES.get(entry.category.lower(), [None] * 5)
        links = entry.get_links  # 🔹 Utilise la méthode centralisée

        index_data.append({
            "entry": entry,
            "category_url": settings.CATEGORY_MAPPING.get(entry.category.lower(), entry.category.lower()),
            "links": [
                {"link": l, "label": settings.INDEX_LINK_CODES.get(k, "-")} if k else {"link": None, "label": "-"}
                for l, k in zip(links, template)
            ]
        })

    return index_data

from django.shortcuts import redirect

def normalize_letters(category, letter, sub_letter, active_letters, show_sub_buttons):
    """
    Normalise la lettre et la sous-lettre et gère les redirections si nécessaire.
    """
    letter = letter or ""  # Assure que letter est toujours une chaîne

    # Vérifier si la lettre doit activer les sous-boutons
    if letter and letter.upper() not in active_letters:
        show_sub_buttons = False

    # Redirection si aucune lettre spécifiée
    if not letter:
        return redirect('app_index:category_index_letter', category=category, letter='A') if category else \
               redirect('app_index:index_letter', letter='A')

    # Redirection si les sous-lettres sont activées
    if not sub_letter:
        if show_sub_buttons:
            return redirect('app_index:category_index_sub_letter', category=category, letter=letter, sub_letter=letter) if category else \
                   redirect('app_index:index_sub_letter', letter=letter, sub_letter=letter)
        else:
            sub_letter = ""  # Afficher tout le contenu sans redirection

    return letter, sub_letter, show_sub_buttons

def index_or_category_view(request, category=None, letter=None, sub_letter=None):
    """
    Affiche l'index général ou filtré par catégorie (artistes, labels, compilations, lexique)
    avec gestion des lettres et sous-lettres.
    """
    # Vérifie si `category` est absente et la récupère depuis l'URL
    category = (category or request.resolver_match.kwargs.get("category") or "").strip()
 
    # Récupérer la configuration de l'index (ou par catégorie)
    index_settings = get_index_settings(category)

    # Déterminer si les sous-boutons doivent être affichés
    show_sub_buttons = index_settings.apply_to_all or bool(index_settings.get_active_letters()) if index_settings else False
    #active_letters = index_settings.get_active_letters() or []
    active_letters = index_settings.get_active_letters() or [] if index_settings else []

    # Normalise les lettres et gère les éventuelles redirections si nécessaires
    result = normalize_letters(category, letter, sub_letter, active_letters, show_sub_buttons)

    # Si la fonction retourne une redirection (ex: vers 'A' par défaut), on la suit immédiatement
    if isinstance(result, HttpResponseRedirect):
        return result

    # sinon, on récupère les valeurs normalisées
    letter, sub_letter, show_sub_buttons = result

    # Récupère les entrées de l'index filtrées par catégorie, lettre et sous-lettre
    index_entries = filter_index_entries(category, letter, sub_letter)

    # Construction des données pour le template
    index_data = generate_index_data(index_entries)

    # 🔹 Sélection du bon template
    template_name = "app_index/index.html"
    
    # PAGINATION
    page_obj, paginator = paginate(index_data, request)

    return render(request, template_name, {
        "index_data": page_obj,
        "letter": letter,
        "sub_letter": sub_letter,
        "category": category,
        "paginator": paginator,
        "page_obj": page_obj,
        "show_sub_buttons": show_sub_buttons  # Maintenant, l'affichage est géré depuis l'admin
    })

def page_exists(category, name, page_type):
    """
    Vérifie si une page existe en tenant compte de la catégorie et du type de page.
    """
    exists = PageExistence.objects.filter(
        category=category, name=name, page_type=f"{category}_{page_type}"
    ).exists()

    return exists
