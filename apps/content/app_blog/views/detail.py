# apps/content/app_blog/views/detail.py
from django.views.generic import DetailView
from django.utils import timezone
from django.db.models import Count, F, Q
from ..models import Article, CategorieArticle
from ..utils import build_archive_dict, get_categories_with_articles

class ArticleDetailView(DetailView):
    model = Article
    template_name = "app_blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Incrémente le compteur de vues et la date de dernière vue
        Article.objects.filter(pk=obj.pk).update(
            views=F('views') + 1,
            last_viewed=timezone.now()
        )
        return obj

    def get_queryset(self):
        return (
            Article.objects.published()
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        # Article suivant (le plus ancien après l'actuel)
        context['article_suivant'] = (
            Article.objects
            .published()
            .filter(date_publication__gt=article.date_publication)
            .order_by('date_publication')
            .first()
        )
        # Article précédent (le plus récent avant l'actuel)
        context['article_precedent'] = (
            Article.objects
            .published()
            .filter(date_publication__lt=article.date_publication)
            .order_by('-date_publication')
            .first()
        )
        
        # Liste des derniers articles
        context['recent_articles'] = (
            Article.objects.published()
            .order_by('-date_publication')[:5]  # 5 derniers articles
        )

        # Liste des catégories avec le nombre d’articles associés, et uniquement celles non vides
        context["categories"] = get_categories_with_articles()

        # Archives
        context["archives"] = build_archive_dict()

        return context
