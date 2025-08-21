# apps/core/app_search/services.py

from django.db.models import Q

def search_blog_block(query: str):
    """
    Bloc 'Blog' extrait depuis la vue originale.

    Retourne: (results_blog, total_blog)
    """
    results_blog = []
    total_blog = 0
    if not query:
        return results_blog, total_blog

    try:
        # Import local pour éviter les imports croisés au démarrage
        from apps.content.app_blog.models import Article  # noqa

        # Recherche multi-champs (insensible à la casse) sur contenu publié
        filtre = (
            Q(titre__icontains=query) |
            Q(resume__icontains=query) |
            Q(contenu__icontains=query)
        )
        qs = (
            Article.objects
            .filter(est_publie=True)
            .filter(filtre)
            .order_by("-date_publication")[:20]  # limite d'affichage initiale
        )

        results_blog = list(qs)
        total_blog = len(results_blog)

    except Exception:
        # Aucune remontée d'erreur en prod : on préfère ne rien afficher que planter
        results_blog = []
        total_blog = 0

    return results_blog, total_blog


def search_pages_block(query: str):
    """
    Bloc 'Pages statiques' extrait depuis la vue originale.

    Retourne: (results_pages, total_pages)
    """
    results_pages, total_pages = [], 0
    if not query:
        return results_pages, total_pages

    try:
        from apps.core.app_main.models.static_pages import StaticPageMeta  # import local
        filtre_pages = Q(title__icontains=query) | Q(content__icontains=query)
        qs_pages = (StaticPageMeta.objects
                    .filter(published=True)           # uniquement publiées
                    .filter(filtre_pages)
                    .order_by("title")[:20])          # tri simple ; on paginera plus tard
        results_pages = list(qs_pages)
        total_pages = len(results_pages)
    except Exception:
        results_pages, total_pages = [], 0

    return results_pages, total_pages


def search_index_block(query: str, index_category_codes: set | None,
                       _first_letter, _active_subletters_for, _sub_letter_alpha):
    """
    Bloc 'Index (entrées + alias)' extrait depuis la vue originale.

    Retourne: (results_index, total_index)
    """
    results_index, total_index = [], 0
    if not query:
        return results_index, total_index

    try:
        from apps.core.app_index.models.index_entry import IndexEntry
        from apps.core.app_index.models.aliases_index import IndexAlias

        # a) Matchs sur noms principaux
        qs_entries = (
            IndexEntry.objects
            .select_related("category")
            .filter(name__icontains=query)
        )
        if index_category_codes:
            qs_entries = qs_entries.filter(category__code__in=index_category_codes)
        qs_entries = qs_entries.order_by("name")[:100]

        by_id: dict[int, dict] = {}

        for e in qs_entries:
            letter = _first_letter(e.name)
            # Pas de sous-lettres pour chiffres ni '@'
            sub_letter = None
            if "A" <= letter <= "Z":
                active = _active_subletters_for(e.category)
                if letter in active:
                    sub_letter = _sub_letter_alpha(e.name)

            by_id[e.id] = {
                "id": e.id,
                "name": e.name,
                "category_code": getattr(e.category, "code", None),
                "category_name": getattr(e.category, "name", None),
                "letter": letter,
                "sub_letter": sub_letter,   # None si non applicable
                "matched_aliases": [],
            }

        # b) Matchs sur alias → remonter l’entrée principale
        qs_alias = (
            IndexAlias.objects
            .select_related("entry", "entry__category")
            .filter(alias__icontains=query)
        )
        if index_category_codes:
            qs_alias = qs_alias.filter(entry__category__code__in=index_category_codes)
        qs_alias = qs_alias.order_by("alias")[:200]

        for al in qs_alias:
            e = al.entry
            if not e:
                continue
            item = by_id.get(e.id)
            if not item:
                # Crée l’entrée si elle n’existe pas encore dans le map
                letter = _first_letter(e.name)
                sub_letter = None
                if "A" <= letter <= "Z":
                    active = _active_subletters_for(e.category)
                    if letter in active:
                        sub_letter = _sub_letter_alpha(e.name)

                item = {
                    "id": e.id,
                    "name": e.name,
                    "category_code": getattr(e.category, "code", None),
                    "category_name": getattr(e.category, "name", None),
                    "letter": letter,
                    "sub_letter": sub_letter,
                    "matched_aliases": [],
                }
                by_id[e.id] = item

            alias_text = (al.alias or "").strip()
            if alias_text and alias_text not in item["matched_aliases"]:
                item["matched_aliases"].append(alias_text)

        # c) Liste finale (1 ligne par entrée principale)
        results_index = list(by_id.values())
        results_index.sort(key=lambda d: (d["name"].lower(), d["category_name"] or ""))

        if len(results_index) > 20:
            results_index = results_index[:20]
        total_index = len(results_index)

    except Exception:
        results_index, total_index = [], 0

    return results_index, total_index


def enrich_index_links_block(results_index):
    """
    Blocs d'enrichissement 'get_links' extraits depuis la vue originale (fusionnés).
    Conserve les commentaires d'origine.
    """
    if not results_index:
        return results_index

    # --- Récupérer les 5 liens "natifs" des entrées d'index, sans les recréer ---
    # Objectif : pour chaque item de results_index, attacher l'objet IndexEntry existant
    #            + ses liens tels que fournis par la mécanique de l'index (get_links).
    #            On NE CHANGE PAS la logique d'affichage, on se contente d'exposer ces données.

    # Récupération des IDs présents dans la liste des résultats "index"
    index_ids = [it.get("id") for it in results_index or [] if it.get("id")]

    if index_ids:
        # Chargement en masse des entrées pour éviter le N+1
        # On prend la catégorie si nécessaire à d’autres endroits
        from apps.core.app_index.models import IndexEntry  # import local pour rester fidèle
        entries = (
            IndexEntry.objects
            .select_related("category")
            .only("id", "name", "category")  # prudence : on ne charge pas tout
            .filter(id__in=index_ids)
        )
        entries_by_id = {e.id: e for e in entries}

        # On enrichit CHAQUE item déjà construit, sans toucher au reste
        for item in results_index:
            eid = item.get("id")
            entry_obj = entries_by_id.get(eid)
            if not entry_obj:
                # Entrée introuvable : on laisse passer, sans casser l'affichage
                item["entry_obj"] = None
                item["links"] = []
                continue

            # On rattache l'objet (si besoin du nom, catégorie, etc.)
            item["entry_obj"] = entry_obj

            # Très important : on NE recrée pas les 5 liens.
            # On réutilise la logique existante (ordre/tagging dépendants de la catégorie).
            # get_links doit déjà renvoyer la structure attendue par l’index (URL/None + étiquette/court code).
            try:
                links_pack = getattr(entry_obj, "get_links", None)
                # Selon ton implémentation, get_links peut être une @property, une cached_property, ou une méthode.
                if callable(links_pack):
                    links_pack = links_pack()
            except Exception:
                links_pack = None

            # Normalise : liste de 5 éléments (URL ou None + label si fourni par ton modèle)
            # Si ton get_links renvoie déjà la bonne structure, on la passe telle quelle.
            item["links"] = list(links_pack or [])

    # ========= Injecter les liens "natifs" de l'index dans results_index =========
    # Objectif : pour chaque item e de results_index, attacher :
    # - e["entry_obj"] : l'objet IndexEntry existant
    # - e["links"]     : la liste des 5 liens telle que déjà définie par l'index (bio/disco/vidéo/…/forum)
    # On NE recrée rien dans la vue : on réutilise get_links de l'IndexEntry.

    try:
        # Adapte si ton modèle est exposé différemment
        from apps.core.app_index.models.index_entry import IndexEntry
    except ModuleNotFoundError:
        from apps.core.app_index.models import IndexEntry

    index_ids = [item.get("id") for item in (results_index or []) if item.get("id")]
    if index_ids:
        # Charge en une requête, récupère la catégorie si utile ailleurs
        entries = (
            IndexEntry.objects
            .select_related("category")
            .only("id", "name", "category")   # on reste léger
            .filter(id__in=index_ids)
        )
        by_id = {obj.id: obj for obj in entries}

        for item in results_index:
            obj = by_id.get(item.get("id"))
            item["entry_obj"] = obj  # pourra servir au template si besoin
            if not obj:
                item["links"] = []
                continue

            # get_links peut être une propriété, cached_property ou méthode
            links = getattr(obj, "get_links", None)
            if callable(links):
                try:
                    links = links()   # si c’est une méthode
                except Exception:
                    links = None

            # Normalise : liste (5 éléments attendus) ou vide
            item["links"] = list(links or [])

    return results_index
