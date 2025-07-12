import os
import hashlib
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify


@login_required
@require_http_methods(["GET", "POST"])
def upload_image_form_view(request, section):
    """
    Vue générique pour uploader une image dans une section donnée.
    Exemple : /medias/site/upload/, /medias/pressages/upload/, etc.
    L’utilisateur choisit un sous-dossier réel dans media/<section>/...
    """
    # Chemin du dossier de la section
    base_dir = Path(settings.MEDIA_ROOT) / section
    if not base_dir.exists() or not base_dir.is_dir():
        return HttpResponseBadRequest(f"Section inconnue ou dossier introuvable : {section}")

    # Liste des sous-dossiers disponibles (1er niveau uniquement)
    sous_dossiers = sorted([
        p.name for p in base_dir.iterdir() if p.is_dir()
    ])

    if request.method == "POST":
        image = request.FILES.get("image")
        subfolder = request.POST.get("subfolder", "").strip()

        if not image or not subfolder:
            return HttpResponseBadRequest("Fichier ou dossier manquant.")

        subfolder_safe = slugify(subfolder)
        target_dir = base_dir / subfolder_safe
        os.makedirs(target_dir, exist_ok=True)

        # Sécurité : pas de nom de fichier non nettoyé
        name, ext = os.path.splitext(image.name)
        filename = f"{slugify(name)}{ext.lower()}"
        file_path = target_dir / filename
        rel_url = f"{settings.MEDIA_URL}{section}/{subfolder_safe}/{filename}"

        # Détection de doublon (par hash)
        content_hash = hashlib.md5(image.read()).hexdigest()
        image.seek(0)
        if file_path.exists():
            with open(file_path, "rb") as f:
                existing_hash = hashlib.md5(f.read()).hexdigest()
            if existing_hash == content_hash:
                return JsonResponse({"location": rel_url})
            # nom déjà pris mais contenu différent
            i = 2
            while True:
                alt_filename = f"{slugify(name)}-{i}{ext.lower()}"
                alt_path = target_dir / alt_filename
                if not alt_path.exists():
                    file_path = alt_path
                    rel_url = f"{settings.MEDIA_URL}{section}/{subfolder_safe}/{alt_filename}"
                    break
                i += 1

        # Écriture réelle
        with open(file_path, "wb+") as dest:
            for chunk in image.chunks():
                dest.write(chunk)

        return JsonResponse({"location": rel_url})

    # Si GET → affiche le formulaire
    return render(request, "app_medias/upload_form.html", {
        "section": section,
        "sous_dossiers": sous_dossiers,
    })
