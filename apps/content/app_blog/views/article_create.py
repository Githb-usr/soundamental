from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.timezone import now

from ..models import Article
from ..forms.article_form import ArticleForm


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue de création d’un article de blog via un formulaire en ligne.
    Accessible uniquement aux utilisateurs connectés appartenant au groupe "Contributeurs"
    ou ayant le statut staff.
    """
    model = Article  # Modèle utilisé pour créer un objet
    form_class = ArticleForm  # Formulaire personnalisé (exclut certains champs)
    template_name = "app_blog/article_form.html"  # Template HTML à utiliser
    success_url = reverse_lazy("app_blog:liste_articles")  # Redirection après succès (à adapter selon tes URLs)

    def test_func(self):
        """
        Fonction utilisée par UserPassesTestMixin pour vérifier les droits d'accès.
        L'utilisateur doit être staff OU membre du groupe "Contributeurs".
        """
        return self.request.user.is_staff or self.request.user.groups.filter(name="Contributeurs").exists()
    
    def form_valid(self, form):
        form.instance.auteur = self.request.user
        form.instance.est_publie = True
        if not form.instance.date_publication:
            form.instance.date_publication = now()
        if not form.instance.slug:
            form.instance.slug = Article.generate_slug(form.instance)
        return super().form_valid(form)
