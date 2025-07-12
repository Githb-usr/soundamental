from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from django.utils.text import slugify

from ..models import Article
from ..forms.widgets import TagSelect2TagWidget
from apps.core.app_main.models.tags import Tag


class ArticleForm(forms.ModelForm):
    """
    Formulaire de création/édition d’un article en ligne pour les contributeurs.
    Certaines options (ex: catégories secondaires) peuvent être limitées côté vue.
    """
    class Meta:
        model = Article
        fields = [
            "titre",
            "resume",
            "contenu",
            "image",
            "categorie_principale",
            "categories_secondaires",
            "tags",
        ]
        widgets = {
            "contenu": Textarea(attrs={
                "class": "form-control richtext",
                "style": "min-height: 400px;",
            }),
            "resume": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "tags": TagSelect2TagWidget(
                attrs={
                    "data-placeholder": "Rechercher ou créer un tag…",
                    "style": "width: 100%",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        titre = cleaned_data.get("titre")

        if titre:
            slug = slugify(titre)[:100]
            if Article.objects.filter(slug=slug).exists():
                raise ValidationError({
                    "titre": "Un article avec un titre similaire existe déjà. Veuillez en choisir un autre."
                })

        return cleaned_data
