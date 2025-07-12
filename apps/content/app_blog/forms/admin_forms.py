# apps/content/app_blog/forms.py

from django import forms
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.forms import Textarea

from ..models import Article, CategorieArticle


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "contenu": Textarea(attrs={
                "class": "form-control richtext",
                "style": "min-height: 400px;",
                "data-section": "blog",
                "data-subfolder": "contenu",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "contenu" in self.fields:
            self.fields["contenu"].help_text = "Contenu principal avec mise en forme TinyMCE."

    def clean_categories_secondaires(self):
        secondaries = self.cleaned_data.get("categories_secondaires")
        if secondaries and len(secondaries) > 4:
            raise forms.ValidationError(
                "Vous ne pouvez sélectionner que 4 catégories secondaires maximum."
            )
        return secondaries
