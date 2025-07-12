import os
import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.core.files.uploadedfile import UploadedFile


@csrf_exempt  # TinyMCE peut mal transmettre le CSRF : on vérifie manuellement
@require_POST
@login_required
def upload_image_site(request):
    """
    Upload d’image pour TinyMCE vers media/site/<SOUS_DOSSIER>/.
    Le sous-dossier est transmis par le champ 'subfolder'.
    Détection de doublon par nom + contenu.
    """
    # Vérification CSRF minimale
    if not request.META.get("HTTP_X_CSRFTOKEN"):
        return HttpResponseForbidden("CSRF token manquant.")

    image: UploadedFile = request.FILES.get("image")
    if not image:
        return HttpResponseBadRequest("Aucun fichier envoyé.")

    # Sous-dossier choisi (ex : 'illustrations', 'logos'...)
    subfolder = slugify(request.POST.get("subfolder", "").strip()) or "autres"

    base_dir = os.path.join(settings.MEDIA_ROOT, "site", subfolder)
    base_url = f"{settings.MEDIA_URL.rstrip('/')}/site/{subfolder}"

    os.makedirs(base_dir, exist_ok=True)

    # Hash du fichier pour éviter les doublons
    content_hash = hashlib.md5(image.read()).hexdigest()
    image.seek(0)

    name, ext = os.path.splitext(image.name)
    filename = f"{slugify(name)}{ext.lower()}"
    file_path = os.path.join(base_dir, filename)
    url_path = f"{base_url}/{filename}"

    # Si fichier existe déjà
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            existing_hash = hashlib.md5(f.read()).hexdigest()
        if existing_hash == content_hash:
            return JsonResponse({"location": url_path})  # doublon → on renvoie le lien

        # Nom alternatif en cas de même nom mais contenu différent
        i = 2
        while True:
            alt_filename = f"{slugify(name)}-{i}{ext.lower()}"
            alt_path = os.path.join(base_dir, alt_filename)
            if not os.path.exists(alt_path):
                file_path = alt_path
                url_path = f"{base_url}/{alt_filename}"
                break
            i += 1

    # Sauvegarde
    with open(file_path, "wb+") as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return JsonResponse({"location": url_path})
