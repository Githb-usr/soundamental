# apps/content/app_blog/utils.py

from collections import defaultdict
from django.db.models import Count, Q
from .models import Article, CategorieArticle

def build_archive_dict():
    """
    Renvoie un dict {année: [mois1, mois2, ...]} trié.
    Ignore les articles sans date de publication.
    """
    archives = defaultdict(set)

    # Filtrage explicite sur les dates non nulles
    dates = (
        Article.objects.published()
        .filter(date_publication__isnull=False)
        .values_list("date_publication", flat=True)
    )

    for dt in dates:
        archives[dt.year].add(dt.month)

    return {
        year: sorted(months)
        for year, months in sorted(archives.items(), reverse=True)
    }

def get_categories_with_articles():
    """
    Renvoie les catégories qui sont reliées à au moins un article publié
    (en catégorie principale ou secondaire).
    Ajoute les nombres d’articles pour chaque type de lien.
    """
    return (
        CategorieArticle.objects.annotate(
            nb_principale=Count(
                'articles_avec_cette_categorie_principale',
                filter=Q(articles_avec_cette_categorie_principale__est_publie=True),
                distinct=True
            ),
            nb_secondaire=Count(
                'articles_avec_cette_categorie_secondaire',
                filter=Q(articles_avec_cette_categorie_secondaire__est_publie=True),
                distinct=True
            ),
        ).filter(
            Q(nb_principale__gt=0) | Q(nb_secondaire__gt=0)
        ).order_by("nom")  # Tri alphabétique sur le champ "nom"
    )
