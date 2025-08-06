# apps/content/app_blog/views/list.py
from datetime import datetime
from django.utils.timezone import now
from django.views.generic import ListView
from django.db.models import Q, Count

from ..models import Article, CategorieArticle
from ..utils import build_archive_dict, get_categories_with_articles


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
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Liste des derniers articles
        context['recent_articles'] = (
            Article.objects.published()
            .order_by('-date_publication')[:5]  # 5 derniers articles
        )
        
        # Ajoute au contexte la liste des catégories disponibles
        context["categories"] = get_categories_with_articles()
        
        context["archives"] = build_archive_dict()
        context["annee_actuelle"] = now().year
        
        return context
