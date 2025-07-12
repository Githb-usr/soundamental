# apps/content/app_blog/views/category.py
from django.views.generic import ListView
from django.db.models import Q, Count
from django.utils.timezone import now

from ..models import Article, CategorieArticle
from ..utils import build_archive_dict


class ArticleCategorieView(ListView):
    model = Article
    template_name = "app_blog/article_list.html"  # on réutilise le même template
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        self.categorie = CategorieArticle.objects.get(pk=self.kwargs["pk"])
        return (
            Article.objects.published()
            .filter(
                Q(categorie_principale=self.categorie) |
                Q(categories_secondaires=self.categorie)
            )
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
            .order_by("-date_publication")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archives"] = build_archive_dict()
        context["categories"] = (
            CategorieArticle.objects.annotate(
                nb_principale=Count("articles_avec_cette_categorie_principale", distinct=True),
                nb_secondaire=Count("articles_avec_cette_categorie_secondaire", distinct=True),
            )
        )
        context["categorie_active"] = self.categorie
        context["annee_actuelle"] = now().year
        
        return context