# apps/content/app_blog/views/detail.py
from django.views.generic import DetailView
from django.db.models import Count, Q

from ..models import Article, CategorieArticle

class ArticleDetailView(DetailView):
    model = Article
    template_name = "app_blog/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return (
            Article.objects.published()
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        context['article_suivant'] = (
            Article.objects
            .published().filter(date_publication__gt=article.date_publication)
            .order_by('date_publication')
            .first()
        )

        context['article_precedent'] = (
            Article.objects
            .published().filter(date_publication__gt=article.date_publication)
            .order_by('-date_publication')
            .first()
        )

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