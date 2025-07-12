# apps/content/app_blog/utils.py

from collections import defaultdict
from .models import Article

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
