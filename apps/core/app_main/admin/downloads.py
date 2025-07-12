from django.contrib import admin
from apps.core.app_main.models.downloads import DownloadableFile, DownloadLog
from apps.core.app_main.forms import DownloadableFileForm

# ===================================
# 📂 AJOUT DE FICHIERS A TELECHARGER
# ===================================

@admin.register(DownloadableFile)
class DownloadableFileAdmin(admin.ModelAdmin):
    form = DownloadableFileForm  # 🔹 On force l'utilisation du formulaire personnalisé
    list_display = ("title", "download_count", "uploaded_at")
    search_fields = ("title",)
    readonly_fields = ("uploaded_at",)
    list_filter = ("uploaded_at",)  # 🔹 Ajoute un filtre par date d'upload
    ordering = ("-download_count",)  # 🔹 Affiche les fichiers les plus téléchargés en premier


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ("file", "downloaded_at")
    search_fields = ("file__title",)
    readonly_fields = ("file", "downloaded_at")
    list_filter = ("downloaded_at",)  # 🔹 Ajoute un filtre par date de téléchargement
    list_per_page = 50  # 🔹 Réduit le nombre d'entrées par page pour alléger l'affichage
