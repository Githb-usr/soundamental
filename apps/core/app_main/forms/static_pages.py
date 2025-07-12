from django import forms
from django.forms import Textarea
from apps.core.app_main.models.static_pages import StaticPageMeta

class StaticPageForm(forms.ModelForm):
    """
    Formulaire permettant d'éditer le contenu d'une page statique.
    Utilise TinyMCE-7.7.1 comme éditeur de texte.
    """
    content = forms.CharField(
        label="Contenu de la page",
        widget=Textarea(attrs={
            "class": "form-control richtext",
            "style": "min-height: 400px;",
            "data-section": "site",         # utilisé pour déterminer le chemin d’upload
            "data-subfolder": "contenu",    # sous-dossier cible dans media/site/
        }),
        help_text="Vous pouvez utiliser la mise en forme avancée grâce à l'éditeur TinyMCE."
    )

    class Meta:
        model = StaticPageMeta  # Associe le formulaire au modèle des pages statiques
        fields = "__all__"  

    class Media:
        js = [
            "/static/js/tinymce/tinymce.min.js",
            "/static/js/tinymce_rich_init.js",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.slug == "aide":
            self.fields["tags"].disabled = True
            self.fields["tags"].help_text = (
                '<span style="color: red;">⚠️ Les tags ne sont pas utilisés pour les pages d’aide.</span>'
            )


class PublicPageEditForm(forms.ModelForm):
    """
    Formulaire simplifié pour l'édition publique : seul le contenu est modifiable.
    """
    class Meta:
        model = StaticPageMeta
        fields = ["content"]  # Uniquement le champ éditable publiquement
        widgets = {
            "content": Textarea(attrs={
                "class": "form-control richtext",
                "style": "min-height: 400px;",
                "data-section": "site",
                "data-subfolder": "contenu"
            }),
        }
