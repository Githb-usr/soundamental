# apps/core/app_search/views.py
# V1 : Blog + Pages statiques + Index (entrées & alias)
# - Blog : titre, résumé, contenu (publiés)
# - Index : 1 ligne par entrée principale ; si match par alias, affiche l’entrée principale + mention de l’alias.
# - Pages statiques : titre + contenu (publiées)

from django.shortcuts import render
from django.db.models import Q  # Permet les recherches multi-champs
from unidecode import unidecode
from django.db.models import Prefetch
from apps.core.app_index.models import IndexEntry  # modèle qui expose get_links
from .services import (
    search_blog_block,
    search_pages_block,
    search_index_block,
    enrich_index_links_block,
)
from .utils_index import (
    INDEX_SUBFILTERS,
    _codes_for_index_type,
    _first_letter,
    _sub_letter_alpha,
    _active_subletters_for,
)

# Petit cache mémoire pour éviter de requêter IndexSettings à chaque entrée
_SUB_CFG_CACHE: dict[int | str, set[str]] = {}

def search_view(request):
    """
    Page de recherche :
      - Paramètres GET : q (requête), scope (tout/index/blog/pages)
      - V1 : on renvoie des résultats Blog si 'q' est fournie et si scope est 'tout' ou 'blog'.
    """
    # 1) Lecture propre des paramètres
    query = (request.GET.get("q") or "").strip()
    scope = (request.GET.get("scope") or "tout").strip().lower()
    if scope not in {"tout", "index", "blog", "pages"}:
        scope = "tout"  # sécurisation
        
    # Sous-filtre spécifique à la portée "index"
    index_type = (request.GET.get("index_type") or "tout").strip().lower()
    if index_type not in {"tout", "artistes", "compilations", "labels"}:
        index_type = "tout"
    index_category_codes = _codes_for_index_type(index_type)  # set(...) ou None

    results_blog = []
    total_blog = 0

    # 2) Blog : actif si l'utilisateur a saisi une requête ET si la portée l'autorise
    results_blog, total_blog = [], 0
    if query and scope in {"tout", "blog"}:
        results_blog, total_blog = search_blog_block(query)

    # 3) PAGES STATIQUES
    results_pages, total_pages = [], 0
    if query and scope in {"tout", "pages"}:
        results_pages, total_pages = search_pages_block(query)

    # 4) INDEX (entrées + alias)
    results_index, total_index = [], 0
    if query and scope in {"tout", "index"}:
        results_index, total_index = search_index_block(
            query=query,
            index_category_codes=index_category_codes,
            _first_letter=_first_letter,
            _active_subletters_for=_active_subletters_for,
            _sub_letter_alpha=_sub_letter_alpha,
        )
         
    # ========= Récupérer les 5 liens "natifs" des entrées d'index, sans les recréer =========
    # Objectif : pour chaque item de results_index, attacher l'objet IndexEntry existant
    #            + ses liens tels que fournis par la mécanique de l'index (get_links).
    #            On NE CHANGE PAS la logique d'affichage, on se contente d'exposer ces données.

    # ========= Injecter les liens "natifs" de l'index dans results_index =========
    # Objectif : pour chaque item e de results_index, attacher :
    # - e["entry_obj"] : l'objet IndexEntry existant
    # - e["links"]     : la liste des 5 liens telle que déjà définie par l'index (bio/disco/vidéo/…/forum)
    # On NE recrée rien dans la vue : on réutilise get_links de l'IndexEntry.

    results_index = enrich_index_links_block(results_index)

    # 5) Contexte
    context = {
        "query": query,
        "active_filter": scope,
        "filters": ["tout", "index", "blog", "pages"],

        "results_blog": results_blog,
        "total_blog": total_blog,

        "results_pages": results_pages,
        "total_pages": total_pages,

        "results_index": results_index,
        "total_index": total_index,
        
        # === sous-filtre 'index' exposé à l'UI ===
        "index_type": index_type,                   # valeur active ('tout' par défaut)
        "index_subfilters": ["tout", "artistes", "compilations", "labels"],  # pour l'UI
    }
    
    return render(request, "app_search/search.html", context)
