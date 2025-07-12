import os
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from urllib.parse import unquote


@login_required
def browse_images(request):
    """
    Vue pour parcourir toutes les images situées sous /media/
    Exclut le dossier downloads/data/ (non images).
    """
    base_dir = os.path.abspath(settings.MEDIA_ROOT)
    base_url = settings.MEDIA_URL.rstrip("/")

    # Chemin demandé par l'utilisateur
    rel_path = unquote(request.GET.get("path", "")).strip("/")
    abs_path = os.path.abspath(os.path.join(base_dir, rel_path))

    # 🔒 Sécurité : interdit de sortir de MEDIA_ROOT
    if not abs_path.startswith(base_dir):
        raise Http404("Chemin interdit.")

    # 🔒 Interdit d'accéder à downloads/data/
    if os.path.normpath(rel_path).startswith("downloads/data"):
        raise Http404("Ce dossier n’est pas accessible.")

    if not os.path.isdir(abs_path):
        raise Http404("Dossier introuvable.")

    # Liste des sous-dossiers visibles (hors "downloads/data")
    subdirs = sorted([
        d for d in os.listdir(abs_path)
        if os.path.isdir(os.path.join(abs_path, d))
        and not (rel_path == "downloads" and d == "data")
    ])

    # Liste des fichiers image autorisés
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
    files = sorted([
        f for f in os.listdir(abs_path)
        if os.path.isfile(os.path.join(abs_path, f)) and os.path.splitext(f)[1].lower() in image_extensions
    ])

    current_url = f"{base_url}/{rel_path}".rstrip("/")

    return render(request, "medias/browse_images.html", {
        "current_path": rel_path,
        "current_url": current_url,
        "subdirs": subdirs,
        "files": files,
    })
