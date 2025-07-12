from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from apps.core.app_main.models.downloads import DownloadableFile
from apps.core.app_main.models.dynamic_pages import DynamicPageTag
from apps.core.app_main.models.tags import Tag

# =================================
# 📂 VUES POUR LES TÉLÉCHARGEMENTS
# =================================

def telechargements_view(request):
    """
    Affiche la liste des fichiers téléchargeables avec options de tri.
    """
    files = DownloadableFile.objects.all()
    
    # Récupérer les tags associés à la **page Téléchargements**
    page_tags = Tag.objects.filter(
        id__in=DynamicPageTag.objects.filter(page_name="telechargements").values_list("tag", flat=True)
    )
    
    # Récupérer le critère de tri depuis l'URL
    sort_by = request.GET.get("sort", "uploaded_at")  # Valeur par défaut : date d'ajout

    # Dictionnaire des options de tri pour éviter les répétitions
    sort_options = {
        "uploaded_at": "-uploaded_at",    # Du plus récent au plus ancien
        "-uploaded_at": "uploaded_at",    # Du plus ancien au plus récent
        "title": "title",                 # Tri alphabétique A-Z
        "-title": "-title",               # Tri alphabétique Z-A
        "download_count": "download_count",  # Tri par nombre de téléchargements croissant
        "-download_count": "-download_count", # Tri par nombre de téléchargements décroissant
    }

    # 🔹 Si le critère de tri est dans notre dictionnaire, on applique `order_by()`
    if sort_by in sort_options:
        files = files.order_by(sort_options[sort_by])

    # 🔹 Cas particulier : tri par taille (get_file_size() est une méthode, donc tri manuel avec `sorted()`)
    elif sort_by in ["file_size", "-file_size"]:
        files = sorted(files, key=lambda f: f.get_file_size(), reverse=(sort_by == "-file_size"))


    return render(request, "app_main/telechargements.html", {
        "files": files,
        "current_sort": sort_by,
        "tags": page_tags  # 🔹 On passe les tags de la page au template
    })

def download_file(request, file_id):
    """
    Vue qui gère le téléchargement et enregistre l'événement.
    """
    file_obj = get_object_or_404(DownloadableFile, id=file_id)

    # Enregistre le téléchargement
    file_obj.register_download()

    return FileResponse(file_obj.file.open("rb"), as_attachment=True, filename=file_obj.file.name)
