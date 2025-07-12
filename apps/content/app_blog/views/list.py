# apps/content/app_blog/views/list.py
from datetime import datetime
from django.utils.timezone import now
from django.views.generic import ListView
from django.db.models import Count

from ..models import Article, CategorieArticle
from ..utils import build_archive_dict


class ArticleListView(ListView):
    model = Article
    template_name = "app_blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        return (
            Article.objects.published()
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
            .order_by("-date_publication")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archives"] = build_archive_dict()
        context["annee_actuelle"] = now().year
        # Ajoute au contexte la liste des catégories disponibles,
        # avec pour chacune le nombre d’articles associés :
        # - comme catégorie principale
        # - comme catégorie secondaire
        # Le total est calculé dans le template.
        context["categories"] = (
            CategorieArticle.objects.annotate(
                nb_principale=Count("articles_avec_cette_categorie_principale", distinct=True),
                nb_secondaire=Count("articles_avec_cette_categorie_secondaire", distinct=True),
            )
        )

        return context