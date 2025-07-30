from django import forms
from django.forms import Textarea
from apps.core.app_main.models.downloads import DownloadableFile

# =====================================
# 📂 FORMULAIRE POUR UPLOAD DE FICHIER
# =====================================

class DownloadableFileForm(forms.ModelForm):
    """
    Formulaire pour l'upload de fichiers téléchargeables.
    """
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        help_text="Formats acceptés : CSV, DOCX, JPG, MP3, PDF, PNG, XLSX, ZIP"
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        help_text="Formats acceptés : GIF, JPG, PNG"
    )

    class Meta:
        model = DownloadableFile
        fields = ["title", "subtitle", "description", "file", "image", "download_count"]

        # Activation de TinyMCE sur le champ "description"
        widgets = {
            "description": Textarea(attrs={
                "class": "form-control richtext",
                "style": "min-height: 300px;"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        subtitle = cleaned_data.get("subtitle")

        if title:
            qs = DownloadableFile.objects.filter(title=title, subtitle=subtitle)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Un fichier avec ce titre et ce sous-titre existe déjà."
                )

        return cleaned_data
