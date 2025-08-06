# apps/content/app_blog/views/category.py
from django.views.generic import ListView
from django.db.models import Q, Count
from django.db.models.functions import ExtractYear
from django.utils.timezone import now
from ..models import Article, CategorieArticle
from ..utils import build_archive_dict, get_categories_with_articles


class ArticleCategorieView(ListView):
    model = Article
    template_name = "app_blog/article_list.html"  # on réutilise le même template
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        self.categorie = CategorieArticle.objects.get(slug=self.kwargs["slug"])
        qs = (
            Article.objects.published()
            .filter(
                Q(categorie_principale=self.categorie) |
                Q(categories_secondaires=self.categorie)
            )
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
            .order_by("-date_publication")
            .distinct()
        )
        annee = self.kwargs.get("annee")
        if annee:
            qs = qs.filter(date_publication__year=annee)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archives"] = build_archive_dict()
        # On compte les articles publiés dans chaque catégorie (principale ou secondaire)
        context["categories"] = get_categories_with_articles()
        context["categorie_active"] = self.categorie
        context["annee_actuelle"] = now().year
        
        if hasattr(self, 'categorie') and 'annee' in self.kwargs:
            annee = int(self.kwargs["annee"])
            context["annee"] = annee
            # Liste des années où il y a des articles pour cette catégorie
            annees_existantes = (
                Article.objects.published()
                .filter(
                    Q(categorie_principale=self.categorie) | Q(categories_secondaires=self.categorie)
                )
                .annotate(annee=ExtractYear("date_publication"))
                .values_list("annee", flat=True)
                .distinct()
            )
            annees_valides = sorted(set(annees_existantes))
            if annee in annees_valides:
                idx = annees_valides.index(annee)
                if idx > 0:
                    context["annee_prec"] = annees_valides[idx - 1]
                if idx < len(annees_valides) - 1:
                    context["annee_suiv"] = annees_valides[idx + 1]

        return context
