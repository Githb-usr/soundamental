# apps/content/app_blog/views/archive.py
from collections import defaultdict
from django.views.generic import ListView
from django.db.models.functions import ExtractYear, TruncMonth
from django.db.models import Count, Q

from ..models import Article, CategorieArticle
from ..utils import build_archive_dict


class ArticleArchiveView(ListView):
    model = Article
    template_name = "app_blog/article_archive.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        annee = int(self.kwargs['annee'])
        mois = self.kwargs.get('mois')
        qs = (
            Article.objects.published()
            .select_related("auteur", "categorie_principale")
            .prefetch_related("tags", "categories_secondaires")
        )

        if mois:
            qs = qs.filter(
                date_publication__year=annee,
                date_publication__month=int(mois)
            )
        else:
            qs = qs.filter(date_publication__year=annee)

        return qs.order_by('-date_publication')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        annee = int(self.kwargs["annee"])
        mois = self.kwargs.get("mois")
        context["annee"] = annee
        context["mois"] = mois

        # --- calcul des mois valides (année+mois) ---
        mois_valides = (
            Article.objects
            .published()
            .annotate(mois_dt=TruncMonth("date_publication"))
            .values_list("mois_dt", flat=True)
            .distinct()
        )
        mois_valides_set = {(dt.year, dt.month) for dt in mois_valides}

        # --- navigation ANNÉES et LISTE DES MOIS DISPONIBLES ---
        if not mois:
            # mois disponibles pour l'année
            mois_dispo = [
                m for (y, m) in mois_valides_set if y == annee
            ]
            context["mois_disponibles"] = sorted(mois_dispo)

            # années valides
            annees_existantes = (
                Article.objects
                .published()
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

        # --- navigation mois précédent / mois suivant (intelligent) ---
        if mois:
            m = int(mois)
            # précédent
            p = (annee - 1, 12) if m == 1 else (annee, m - 1)
            if p in mois_valides_set:
                context["mois_prec"] = p
            # suivant
            s = (annee + 1, 1) if m == 12 else (annee, m + 1)
            if s in mois_valides_set:
                context["mois_suiv"] = s
                
        # Liste des derniers articles
        context['recent_articles'] = (
            Article.objects.published()
            .order_by('-date_publication')[:5]  # 5 derniers articles
        )
        context["categories"] = (
            CategorieArticle.objects.annotate(
                nb_principale=Count("articles_avec_cette_categorie_principale", distinct=True),
                nb_secondaire=Count("articles_avec_cette_categorie_secondaire", distinct=True),
            )
        )
        context["archives"] = build_archive_dict()

        return context
