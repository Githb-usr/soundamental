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
        fields = ["title", "description", "file", "image", "download_count"]

        # ✅ Activation de TinyMCE sur le champ "description"
        widgets = {
            "description": Textarea(attrs={
                "class": "form-control richtext",
                "style": "min-height: 300px;"
            })
        }
